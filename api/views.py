from django.shortcuts import render
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import timedelta
from rest_framework.decorators import api_view , permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate
from rest_framework import status
from .models import *
from .serializers import *
import time
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination

# Genarate Token Function
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    access_token_lifetime = timedelta(days=1)
    access_token_expires_at = timezone.now() + access_token_lifetime
    return {
        'refresh_token': str(refresh),
        'access_token': str(refresh.access_token),
        'access_token_expires_at': access_token_expires_at.timestamp(),  # Include the expiration timestamp in the response
    }


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    if request.method == 'POST':
        name = request.data.get('name')
        email = request.data.get('email')
        password = request.data.get('password')
        confirm_password = request.data.get("confirm_password")

        if password!= confirm_password:
            return Response({'error': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)

        User.objects.create_user(
            name=name,
            email=email, 
            password=password,)

        return Response({'success': 'User registered successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Only POST requests are allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    if request.method == 'POST':
        email = request.data.get('email')
        password = request.data.get('password')

        if email is None or password is None:
            return Response({'error': 'Email and password are reqwuired'}, status=status.HTTP_400_BAD_REQUEST)

        # Authenticate user using obtained username and provided password
        user = authenticate(request, email=email, password=password)

        if user is not None:
            token = get_tokens_for_user(user)
            token_data = {
                "user": user.id,
                "access_token": token['access_token'],
                "refresh_token": token['refresh_token']
            }
            token_serializer = TokenSerializer(data=token_data)
            
            if token_serializer.is_valid():
                token_serializer.save()  
                return Response({
                    "success": True,
                    'message': 'Login successful',
                    "token": token,
                },status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response({'error': 'Only POST requests are allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_search(request):
    query = request.query_params.get('name', '')
    paginator = PageNumberPagination()
    paginator.page_size = 4
    users = User.objects.filter(Q(email__iexact=query) | Q(name__icontains=query))
    result_page = paginator.paginate_queryset(users, request)
    serializer = UserSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

rate_limit = {}

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_friend_request(request):
    to_user_id = request.data.get('to_user_id')
    if not to_user_id:
        return Response({'error': 'to_user_id is required'}, status=status.HTTP_400_BAD_REQUEST)

    if time.time() - rate_limit.get(request.user.id, 0) < 20:
        return Response({'error': 'Too many friend requests. Please wait a moment.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

    rate_limit[request.user.id] = time.time()

    to_user = User.objects.get(id=to_user_id)
    if FriendRequest.objects.filter(from_user=request.user, to_user=to_user).exists():
        return Response({'error': 'Friend request already sent'}, status=status.HTTP_400_BAD_REQUEST)

    friend_request = FriendRequest(from_user=request.user, to_user=to_user)
    friend_request.save()
    return Response(FriendRequestSerializer(friend_request).data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def respond_friend_request(request):
    request_id = request.data.get('request_id')
    action = request.data.get('action')
    friend_request = FriendRequest.objects.get(id=request_id)

    if friend_request.to_user != request.user:
        return Response({'error': 'Not authorized'}, status=status.HTTP_403_FORBIDDEN)

    if action == 'accept':
        friend_request.status = 'accepted'
    elif action == 'reject':
        friend_request.status = 'rejected'
    else:
        return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

    friend_request.save()
    return Response(FriendRequestSerializer(friend_request).data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_friends(request):
    friends = User.objects.filter(
        Q(sent_requests__to_user=request.user, sent_requests__status='accepted') |
        Q(received_requests__from_user=request.user, received_requests__status='accepted')
    ).distinct()
    serializer = UserSerializer(friends, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_pending_requests(request):
    pending_requests = FriendRequest.objects.filter(to_user=request.user, status='pending')
    serializer = FriendRequestSerializer(pending_requests, many=True)
    return Response(serializer.data)
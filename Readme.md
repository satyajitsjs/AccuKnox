```markdown
# Social Network API

## Installation Steps

1. Clone the repository:
   ```bash
   git clone <repo_url>
   cd socialnetwork
   ```

2. Build and run the Docker containers:
   ```bash
   docker-compose up --build
   ```

## API Endpoints

- `POST /api/signup/`
- `POST /api/login/`
- `GET /api/search/?query=`
- `POST /api/friend-request/`
- `PUT /api/friend-request/respond/`
- `GET /api/friends/`
- `GET /api/pending-requests/`

## Postman Collection
```
Import the `postman` folder in Postman to test the endpoints.
```


### Postman Collection

Create a Postman collection with the following endpoints and export it as `postman_collection.json`:

- `POST /api/signup/`
- `POST /api/login/`
- `GET /api/search/?query=`
- `POST /api/friend-request/`
- `PUT /api/friend-request/respond/`
- `GET /api/friends/`
- `GET /api/pending-requests/`
# Chat App

A modern chat application featuring:

- **Django** main backend (REST API, WebSocket(dev testing purposes), PostgreSQL, Redis,Elasticsearch)
- **FastAPI** main chat microservice (ScyllaDB)
- **Docker Compose** for local development
- Real-time chat with WebSockets
- Scalable architecture for future extensions

## Project Structure

```
.
├── chat_service/           # FastAPI microservice (ScyllaDB)
│   └── app/
├── docker/                 # Dockerfiles & requirements
│   ├── chat_service/
│   └── projectile/
├── projectile/             # Django project
│   ├── base/
│   ├── chat/
│   ├── core/
│   ├── elastic/
│   ├── member/
│   ├── message/
│   ├── permission/
│   ├── projectile_settings/
│   └── server/
├── templates/              # HTML templates
├── .env                    # Environment variables
├── docker-compose.yml
├── Makefile
└── ...
```

## Getting Started

### Prerequisites

- [Docker]
- [Docker Compose]
- [Make can help :)]

### Setup

1. **Clone the repository:**
    ```sh
    git clone https://github.com/RiashadHassan/chat-app.git
    cd chat-app
    ```

2. **Configure environment variables:**
    - Copy `.env-example` to `.env` and fill in any secrets or credentials.

3. **Build and start all services:**
    ```sh
    ./setup_docker.sh
    docker compose up --build
    ```

4. **Access the app:**
    - Django API & Web: [http://localhost:8000](http://localhost:8000)
    - FastAPI service: [http://localhost:9000](http://localhost:9000)

### Startup Commands

- Run Django management commands:
    ```sh
    make migrate
    make create_fake_data
    ```

### Services

- **web**: Django backend (REST, WebSocket, PostgreSQL, Redis, Elasticsearch)
- **chat_service**: FastAPI microservice (ScyllaDB)
- **db**: PostgreSQL database
- **redis**: Redis cache
- **elasticsearch**: Elasticsearch engine
- **scylla**: ScyllaDB (Cassandra-compatible)
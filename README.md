# Ciceron

## Installation (DEV, Non-Docker)
```bash
apt-get update
apt-get install python3 python3-pip
pip3 install -r requirements.dev.txt
```

## Installation and run (DOCKER)
```bash
docker-compose up -d
```

## Tests
```bash
docker-compose up -d
docker-compose exec -e APP_URL=0.0.0.0:8080 app sh -c "pytest tests/routes"
```

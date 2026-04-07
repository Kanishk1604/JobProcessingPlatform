rebuild containers: 
docker compose -f infra/docker/docker-compose.yml down
docker compose -f infra/docker/docker-compose.yml up --build
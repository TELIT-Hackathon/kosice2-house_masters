docker container rm database-graphql-engine-1
docker container rm database-postgres-1
docker volume rm database_db_data
docker build -t init-gql ./init-gql
docker build -t web-backend ./web
docker compose up --remove-orphans
echo "Running at http://localhost:8080/console/api/api-explorer"

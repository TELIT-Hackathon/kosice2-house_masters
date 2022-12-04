FROM alpine
WORKDIR /database
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk --no-cache add curl
RUN apk add --no-cache python3 py3-pip
COPY create.sql create.sql
COPY init.py init.py
COPY requirements.txt requirements.txt
COPY hasura_metadata.json hasura_metadata.json
RUN pip install -r requirements.txt
EXPOSE 8080
COPY . .
CMD python3 init.py
# CMD curl -i -H "Accept: application/json" -H "X-Hasura-Admin-Secret:$HASURA_GRAPHQL_ADMIN_SECRET" -H "Content-Type:application/json" -X POST --data '{"type": "run_sql","args": {"source": "default","sql": "$(cat create.sql)"}}' $HASURA_SERVICE_NAME:8080/v2/query

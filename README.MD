# Test work for jibrel.network

### Service for get currencies,
### get last rate and get average volumes for last ten records

## 1. run app

`docker-compose up --build -d`

## 2. apply migrations 
`docker exec jibrel_service_1 /jibrel/manage.py migrate`

## 3. run tests
`docker exec jibrel_service_1 /jibrel/manage.py test`

## 4. create user
`docker exec -ti jibrel_service_1 /jibrel/manage.py createsuperuser`

## 5. insert initial data
`docker exec jibrel_service_1 /jibrel/manage.py insert_data`

## 6. restart
`docker-compose restart`

# 7. ??PROFIT??

# User Management Service

## API Specification

### /register
```shell
curl --location --request POST 'http://127.0.0.1:5000/register' \
--header 'Content-Type: application/json' \
--data-raw '{"username":"newuser", "password":"newpassword123"}'
```

### /login
```shell
curl --location --request POST 'http://127.0.0.1:5000/login' \
--header 'Content-Type: application/json' \
--data-raw '{"username":"newuser", "password":"newpassword123"}'
```
# MVS DID service
MVS service for exchanger to store registration of DID.

## RESTfull APIs
### add did
http method: `POST`:
```
http://hostname:port/mvs/api/v1/did/{exchanger}/{customer}/{did}/{address}
```
Excample:
Request:
```
curl -i -X POST 'http://127.0.0.1:5000/mvs/api/v1/did' -H "Content-Type: application/json" -d '{"exchanger": "rightbtc", "customer": "kesalin", "did": "kesalin", "address": "MTrW3QK8mjmTYSozdkLa7k9hyCExUBWYwP"}'
```
Response:
```json
{
  "error": 0,
  "result": "{\"did\": \"kesalin\", \"customer\": \"kesalin\", \"address\": \"MTqgx7CHA8y1TUF1re5NLyT4mzKvCxWTyi\", \"exchanger\": \"rightbtc\"}"
}
```
### get did
http method: `GET`:
```
http://hostname:port/mvs/api/v1/did/{exchanger}/{customer}
```
Excample:
Request:
```
curl -i -X GET 'http://127.0.0.1:5000/mvs/api/v1/did/rightbtc/kesalin'
```
Response:
```json
{
  "code": 0,
  "result": "{\"did\": \"kesalin\", \"customer\": \"kesalin\", \"address\": \"MTqgx7CHA8y1TUF1re5NLyT4mzKvCxWTyi\", \"exchanger\": \"rightbtc\"}"
}
```

### delete did
http method: `DELETE`:
```
http://hostname:port/mvs/api/v1/did/{exchanger}/{customer}
```
Excample:
Request:
```
curl -i -X DELETE 'http://127.0.0.1:5000/mvs/api/v1/did/rightbtc/kesalin'
```
Response:
```json
{
  "code": 0,
  "result": "{\"did\": \"kesalin\", \"customer\": \"kesalin\", \"address\": \"MTqgx7CHA8y1TUF1re5NLyT4mzKvCxWTyi\", \"exchanger\": \"rightbtc\"}"
}
```

## Response Codes
> 0 : success
> 1 : invalid parameter
> 2 : not found
> 3 : already exist

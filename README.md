# MVS DID service
MVS service for exchanger to store registration of DID.

## Build Image And Run Container
### Build Image
```bash
docker build -t didservice -f Dockerfile .
```
### Run Container
```bash
docker run --name=didservice -p 5000:5000 didservice
```

## RESTfull APIs
### add did
http method: `POST` with parameters {exchanger, customer, did, address}
```
http://hostname:port/mvs/api/v1/did
```
Excample:  
Request:
```
curl -i -X POST 'http://127.0.0.1:5000/mvs/api/v1/did' -H "Content-Type: application/json" -d '{"exchanger": "rightbtc", "customer": "kesalin", "did": "kesalin", "address": "MTrW3QK8mjmTYSozdkLa7k9hyCExUBWYwP"}'
```
Response:
```json
{
  "code": 0,
  "result": {
    "address": "MTrW3QK8mjmTYSozdkLa7k9hyCExUBWYwP",
    "customer": "kesalin",
    "did": "kesalin",
    "exchanger": "rightbtc"
  }
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
  "result": {
    "address": "MTrW3QK8mjmTYSozdkLa7k9hyCExUBWYwP",
    "customer": "kesalin",
    "did": "kesalin",
    "exchanger": "rightbtc"
  }
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
  "result": {
    "address": "MTrW3QK8mjmTYSozdkLa7k9hyCExUBWYwP",
    "customer": "kesalin",
    "did": "kesalin",
    "exchanger": "rightbtc"
  }
}
```

## Response Codes
> 0 : success  
> 1 : invalid parameter  
> 2 : not found  
> 3 : already exist  

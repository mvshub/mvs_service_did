# MVS DID service
MVS service for exchanger to store registation of DID.

## RESTfull APIs
### adddid
adddid:
```
http://127.0.0.1:5000/adddid/{exchanger}/{customer}/{did}/{address}
```
Excample:
Request:
```
http://127.0.0.1:5000/adddid/rightbtc/kesalin/kesalin/MTqgx7CHA8y1TUF1re5NLyT4mzKvCxWTyi
```
Response:
```json
{
  "error": 0,
  "result": "{\"did\": \"kesalin\", \"customer\": \"kesalin\", \"address\": \"MTqgx7CHA8y1TUF1re5NLyT4mzKvCxWTyi\", \"exchanger\": \"rightbtc\"}"
}
```
### get did
getdid:
```
http://127.0.0.1:5000/getdid/{exchanger}/{customer}
```
Excample:
Request:
```
http://127.0.0.1:5000/getdid/rightbtc/kesalin
```
Response:
```json
{
  "code": 0,
  "result": "{\"did\": \"kesalin\", \"customer\": \"kesalin\", \"address\": \"MTqgx7CHA8y1TUF1re5NLyT4mzKvCxWTyi\", \"exchanger\": \"rightbtc\"}"
}
```

### delete did
deletedid:
```
http://127.0.0.1:5000/deletedid/{exchanger}/{customer}
```
Excample:
Request:
```
http://127.0.0.1:5000/deletedid/rightbtc/kesalin
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

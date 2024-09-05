## Installation

use command "pip install -r req.txt"

## signup

```
curl --location 'http://127.0.0.1:8000/insidedb/signup/' \
--form 'username="Enter your Name"' \
--form 'password="Enter your password"' \
--form 'email="Enter your email"'

```
## test token
```

curl --location 'http://127.0.0.1:8000/insidedb/test_token' \
--header 'Authorization: Token <"enter your token'>'
```

### login
```
curl --location 'http://127.0.0.1:8000/insidedb/login/' \
--form 'username="enter usernam"' \
--form 'password="enter password"'
```
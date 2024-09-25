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

### Pagination
'''
curl --location 'http://127.0.0.1:8000/insidedb/list/?limit=10&offset=10%0A'
'''

### search
'''
curl --location 'http://127.0.0.1:8000/insidedb/search?TECH=2G%2C%203G&STANDARD_SET=null&PATENT_OWNER=null&IPRD_REFERENCE=null&PATENT_NUM=null&STANDARD=null&Sub_Tech=null&DATE_FROM=&DATE_TO='
'''

### single search with primary key
'''
curl --location 'http://127.0.0.1:8000/insidedb/1'
'''

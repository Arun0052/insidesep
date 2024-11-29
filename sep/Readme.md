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
http://127.0.0.1:8000/insidedb/list/?limit=10&offset=0
curl --location 'http://127.0.0.1:8000/insidedb/list/?limit=10&offset=10%0A'
'''

### search
'''
#http://127.0.0.1:8000/insidedb/search?TECH[]=2G, 3G&TECH[]=2G
#http://127.0.0.1:8000/insidedb/search?PATENT_OWNER&PATENT_NUM&STANDARD&Sub_Tech&limit=10&offset=10
curl --location --globoff 'http://127.0.0.1:8000/insidedb/search?TECH=["2G, 3G", "2G"]&STANDARD_SET=["ETSI"]&PATENT_OWNER=null&IPRD_REFERENCE=null&PATENT_NUM=null&STANDARD=null&Sub_Tech=null&DATE_FROM=&DATE_TO='
'''

### user_limit
'''
curl --location 'http://127.0.0.1:8000/insidedb/user_limit' \
--header 'Authorization: Token 3c6d42af0290098089029a33ed6e594acf04bf54'
'''
### reset limit
'''
curl --location 'http://127.0.0.1:8000/insidedb/reset-userlimit/' \
--header 'Authorization: Token 3c6d42af0290098089029a33ed6e594acf04bf54' \
--form 'action="reset"'
'''


### single search with primary key
'''
curl --location 'http://127.0.0.1:8000/insidedb/1'
'''
### attribute_search
'''
http://127.0.0.1:8000/insidedb/search_by_attribute/?attribute_name=PATENT_OWNER
'''

### auto complete
'''
http://127.0.0.1:8000/insidedb/patents-autocomplete/?q=AU
'''

### unique for dropdown
'''
http://127.0.0.1:8000/insidedb/unique_data
'''
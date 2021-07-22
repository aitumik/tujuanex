# Tujuanex
Tujuanex is a flask api for dating
>  Tujuanex api an inspiration from a tv show the **tujueanex** 


## Installation
Git clone the project from my repository

```bash
git clone https://github.com/aitumik/tujuanex-api.git
```
Then change to the directory where you cloned the repo

```bash
cd tujuanex-api
```

You will have to create a virtual environment for your packages however it is optional
To create a *virtual* environment 
```bash
python3 -m venv <name-of-virtualenv>
```

Install the packages in the `requirements.txt` using `pip`

```bash
pip3 install -r requirements.txt
```

Finally start the server by:

```bash
python3 manage.py runserver
```

### Registering a user
To register a user post to this endpoint <code>api/v1/auth/register</code> with
the below structure
```javascript
{
    "username": "aitumik",
    "password": "testing",
    "email": "aitumik@tujuanex.com",
    "phone": "+2547099707792"
}
```

### Logging in and getting and access token
To login post to this endpoint <code>api/v1/auth/login</code> with the below
structure
```javascript
{
    "username":"aitumik",
    "password":"testing"
}
```

### Performing your first requests
To make api calls to the app you can use any tool of your choice or language but for our case we will use curl
```bash
curl http://localhost:5000/api/v1/<endpoint>
```

### Creating posts
```bash
curl http://localhost:5000/api/v1/posts/create -H '{"Authorization: Bearer "token"}' -d '{"name": "Hello There"}'
```

## Contributing
Pull requests are welcome. For major changes please open an issue first 
to discuss what you want to change

## License
[MIT](https://choosealicense.com/licenses/mit/)

## Forking?



import os



BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_NAME = "Template"

SECURITY_KEY = "ZHBCJHCJEDSJNKFDJDNKDJNKLD"

DEBUG = True

BACKEND_CORS_ORIGINS = [
    "localhost",
    "127.0.0.1:8000",
    "*"
]


CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Cache-Control',
    'X-Requested-With',    
]

CORS_ALLOW_METHODS = [
    'GET',
    'POST',
    'PUT',
    'DELETE',
    'PATCH',
    'OPTIONS'
]


# MONGODB_NAME = 'omegle'

# MONGODB_URL='mongodb+srv://mydbuserlol:wxa5Fjvr2XyrUfAh@cluster0-jodr9.mongodb.net/omegle?retryWrites=true&w=majority'

MAX_POOL_SIZE=10

MIN_POOL_SIZE=1

JWT_TOKEN_PREFIX = 'TOKEN'

ACCESS_TOKEN_EXPIRY = 60

ALGORITHM = 'HS512'
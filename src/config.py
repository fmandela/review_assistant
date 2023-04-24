import os 

class BaseConfig(object):
    # CACHE_TYPE = os.environ['CACHE_TYPE']
    # CACHE_REDIS_HOST = os.environ['CACHE_REDIS_HOST']
    # CACHE_REDIS_PORT = os.environ['CACHE_REDIS_PORT']
    # CACHE_REDIS_DB = os.environ['CACHE_REDIS_DB']
    # CACHE_REDIS_URL = os.environ['CACHE_REDIS_URL']
    # CACHE_DEFAULT_TIMEOUT = os.environ['CACHE_DEFAULT_TIMEOUT']
    ENV= os.environ['ENV']
    MONGO_URL = os.getenv('MONGO_URL', '')
    MONGO_DB = os.getenv('MONGO_DB', 'test')
    PORT= os.getenv('PORT', 8080)
    SECRET_KEY= os.getenv('SECRET_KEY', 'SECRET_KEY')
    PUBLIC_KEY= os.getenv('PUBLICK_KEY', 'PUBLICKEYIN')
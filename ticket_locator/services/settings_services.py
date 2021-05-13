import environ


environ.Env.read_env()

env = environ.Env(
    DEBUG=(bool, False)
)

TK_API_KEY = env('TK_API_KEY')
TK_SECRET_KEY = env('TK_SECRET_KEY')

TRANSAVIA_API_KEY = env('TRANSAVIA_API_KEY')
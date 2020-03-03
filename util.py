import oauth2 as oauth
import config

def get_authenticated_client():
    consumer = oauth.Consumer(config.APP_KEY, config.APP_SEC)
    token = oauth.Token(config.OAUTH_TOKEN, config.OAUTH_TOKEN_SECRET)
    client = oauth.Client(consumer, token)
    return client

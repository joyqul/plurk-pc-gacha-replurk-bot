import oauth2 as oauth
import urllib.parse as urlparse


OAUTH_REQUEST_TOKEN = 'https://www.plurk.com/OAuth/request_token'
OAUTH_ACCESS_TOKEN = 'https://www.plurk.com/OAuth/access_token'


def get_request_token(app_key, app_secret):
    consumer = oauth.Consumer(app_key, app_secret)
    client = oauth.Client(consumer)
    response = client.request(OAUTH_REQUEST_TOKEN, method='GET')
    return urlparse.parse_qs(response[1])


def get_access_token(app_key, app_secret, oauth_token, oauth_token_secret, oauth_verifier):
    consumer = oauth.Consumer(app_key, app_secret)
    token = oauth.Token(oauth_token, oauth_token_secret)
    token.set_verifier(oauth_verifier)
    client = oauth.Client(consumer, token)
    response = client.request(OAUTH_ACCESS_TOKEN, method='GET')
    return urlparse.parse_qs(response[1])


if __name__ == '__main__':
    import appraisal_secret as config
    fetched_oauth = get_request_token(config.APP_KEY, config.APP_SEC)
    oauth_token = fetched_oauth[b'oauth_token'][0].decode("utf-8")
    oauth_token_secret = fetched_oauth[b'oauth_token_secret'][0].decode("utf-8")
    print(oauth_token, oauth_token_secret)
    print("https://www.plurk.com/OAuth/authorize?oauth_token="+oauth_token)
    verifier = input("Enter verifier:")
    print(get_access_token(config.APP_KEY, config.APP_SEC, oauth_token, oauth_token_secret, verifier))

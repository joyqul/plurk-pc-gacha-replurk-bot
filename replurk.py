import oauth2 as oauth
import urllib.parse as urlparse
import json
import config

ANONYMOUS_ID = 99999

def search_pc_gatcha():
    consumer = oauth.Consumer(config.APP_KEY, config.APP_SEC)
    token = oauth.Token(config.OAUTH_TOKEN, config.OAUTH_TOKEN_SECRET)
    client = oauth.Client(consumer, token)
    url = 'https://www.plurk.com/APP/PlurkSearch/search?query=噗幣轉蛋'
    response = client.request(url, method='GET')
    return json.loads(response[1].decode("utf-8"))


def valid_to_replurk(post):
    if post['user_id']!=ANONYMOUS_ID: return False
    if post['content'].find("#噗幣轉蛋")<0: return False
    return True


def find_candidate_posts():
    plurk_posts = search_pc_gatcha()
    candidates = plurk_posts['plurks']
    for candidate in candidates:
        if not valid_to_replurk(candidate): continue
        #print(candidate)
        if candidate['replurked']: break

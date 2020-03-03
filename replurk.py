import oauth2 as oauth
import urllib.parse as urlparse
import json
import config, util

ANONYMOUS_ID = 99999

def search_pc_gatcha():
    client = util.get_authenticated_client()
    url = 'https://www.plurk.com/APP/PlurkSearch/search?query=噗幣轉蛋'
    response = client.request(url, method='GET')
    return json.loads(response[1].decode("utf-8"))


def valid_to_replurk(post):
    if post['user_id']!=ANONYMOUS_ID: return False
    if post['content'].find("#噗幣轉蛋")<0: return False
    return True


def replurk_post(ids):
    client = util.get_authenticated_client()
    ids = json.dumps(ids)
    url = 'https://www.plurk.com/APP/Timeline/replurk?ids='+ids
    response = client.request(url, method='GET')


def find_candidate_posts():
    plurk_posts = search_pc_gatcha()
    candidates = plurk_posts['plurks']
    plurk_ids = []
    for candidate in candidates:
        if not valid_to_replurk(candidate): continue
        plurk_ids.append(candidate['plurk_id'])
        if candidate['replurked']: break
    replurk_post(plurk_ids)


if __name__ == '__main__':
    find_candidate_posts()

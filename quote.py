import json, datetime, urllib
import util, replurk


def valid_to_replurk(post, config):
    if post['user_id']!=replurk.ANONYMOUS_ID: return False

    found_must_have_tag = False
    for tag in config.MUST_HAVE_AT_LEAST_ONE:
        if post['content'].find(tag)>=0:
            found_must_have_tag = True
            break
    if not found_must_have_tag: return False
    return True


def get_candidates_posts(config, secret):
    posted_time_limit = datetime.datetime.utcnow()-datetime.timedelta(minutes=config.INTERVAL_MINUTES)

    posts = replurk.search_plurk(config, secret)
    candidates = []
    for post in posts:
        if not replurk.valid_to_replurk(post, config): continue
        posted_time = datetime.datetime.strptime(post['posted'], '%a, %d %b %Y %H:%M:%S %Z')
        if posted_time<posted_time_limit: continue
        candidates.append(post)
    return candidates


def base36encode(number):
    if not isinstance(number, (int)):
        raise TypeError('number must be an integer')
    if number < 0:
        raise ValueError('number must be positive')

    alphabet, base36 = ['0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', '']

    while number:
        number, i = divmod(number, 36)
        base36 = alphabet[i] + base36

    return (base36 or alphabet[0]).lower()


def quote_post(post, secret):
    client = util.get_authenticated_client(secret)
    url = 'https://www.plurk.com/APP/Timeline/plurkAdd?'
    plurk_url_id = base36encode(post['plurk_id'])
    full_plurk_url = 'https://www.plurk.com/p/'+plurk_url_id

    content = 'plurk_id: '+plurk_url_id+'\n'
    if post['publish_to_followers']:
        content += '**可能為親友粉絲限定**'
    else:
        content += '**偷偷說公開河道 only**'
    content += '\n' + full_plurk_url
    params = urllib.parse.urlencode({'content': content, 'qualifier': 'says'})
    url = url+params
    response = client.request(url, method='GET')

    
def quote_pc_gatch_plurk():
    import ura_pc_gacha_config as config, ura_pc_gacha_secret as secret
    posts = get_candidates_posts(config, secret)
    posts.reverse()
    for post in posts:
        quote_post(post, secret)
        

if __name__ == '__main__':
    quote_pc_gatch_plurk()

import json
import util

ANONYMOUS_ID = 99999

def search_plurk(config, secret):
    client = util.get_authenticated_client(secret)
    plurks = []
    keywords = config.SEARCH_KEYWORDS
    for keyword in keywords:
        url = 'https://www.plurk.com/APP/PlurkSearch/search?query='+keyword
        response = client.request(url, method='GET')
        found_posts = json.loads(response[1].decode("utf-8"))
        plurks += found_posts['plurks']
    return plurks


def valid_to_replurk(post, config):
    if post['user_id']!=ANONYMOUS_ID: return False
    if post['publish_to_followers']: return False

    found_must_have_tag = False
    for tag in config.MUST_HAVE_AT_LEAST_ONE:
        if post['content'].find(tag)>=0:
            found_must_have_tag = True
            break
    if not found_must_have_tag: return False

    for skip_tag in config.SKIP_TAGS:
        if post['content'].find(skip_tag)>0: return False
    return True


def replurk_post(ids, secret):
    client = util.get_authenticated_client(secret)
    ids = json.dumps(ids)
    url = 'https://www.plurk.com/APP/Timeline/replurk?ids='+ids
    response = client.request(url, method='GET')


def search_and_replurk_posts(config, secret):
    candidates = search_plurk(config, secret)
    plurk_ids = []
    for candidate in candidates:
        if not valid_to_replurk(candidate, config): continue
        if candidate['replurked']: break
        plurk_ids.append(candidate['plurk_id'])

    replurk_post(plurk_ids, secret)
    return plurk_ids


def replurk_pc_gatch_posts():
    import pc_gacha_config, pc_gacha_secret
    search_and_replurk_posts(pc_gacha_config, pc_gacha_secret)


def replurk_appraisal_posts():
    import appraisal_config, appraisal_secret
    search_and_replurk_posts(appraisal_config, appraisal_secret)


if __name__ == '__main__':
    replurk_pc_gatch_posts()
    replurk_appraisal_posts()

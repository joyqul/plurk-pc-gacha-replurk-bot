import json, urllib
import util


ANONYMOUS_ID = 99999
ROOT_URL = 'https://www.plurk.com'

class ReplurkBot():
    def __init__(self, config, secret):
        self.ANONYMOUS_ID = 99999
        self.config = config
        self.secret = secret
        self.client = util.get_authenticated_client(secret)
        try:
            self.replurk_normal_post = config.replurk_normal_post
        except:
            self.replurk_normal_post = False


    def search_plurk(self):
        plurks = []
        keywords = self.config.SEARCH_KEYWORDS
        for keyword in keywords:
            url = "%s/APP/PlurkSearch/search?query=%s" %(ROOT_URL, keyword)
            response = self.client.request(url, method='GET')
            found_posts = json.loads(response[1].decode("utf-8"))
            plurks += found_posts['plurks']
        return plurks


    def contain_tag(post, tags):
        for tag in tags:
            if post['content'].lower().find(tag)>=0:
                return True
        return False


    def contain_must_have_tag(self, post):
        return ReplurkBot.contain_tag(post, self.config.MUST_HAVE_AT_LEAST_ONE)


    def contain_must_replurk_tag(self, post):
        return ReplurkBot.contain_tag(post, self.config.MUST_REPLURK_TAGS)


    def contain_skip_tag(self, post):
        return ReplurkBot.contain_tag(post, self.config.SKIP_TAGS)


    def valid_to_replurk(self, post):
        if not self.replurk_normal_post and post['user_id']!=ANONYMOUS_ID: return False
        if self.contain_must_replurk_tag(post): return True
        if not self.contain_must_have_tag(post): return False
        if self.contain_skip_tag(post): return False
        return True


    def replurk_post(self, ids):
        ids = json.dumps(ids)
        url = '%s/APP/Timeline/replurk?ids=%s' %(ROOT_URL, ids)
        response = self.client.request(url, method='GET')
        return response


    def search_and_replurk_posts(self, auto_comment_content=None):
        candidates = self.search_plurk()
        plurk_ids = []
        for candidate in candidates:
            if candidate['replurked']: continue
            if not self.valid_to_replurk(candidate): continue
            plurk_id = candidate['plurk_id']
            plurk_ids.append(plurk_id)
            if auto_comment_content:
                self.add_response(plurk_id, auto_comment_content)
        return self.replurk_post(plurk_ids)

    def add_response(self, plurk_id, content):
        url = '%s/APP/Responses/responseAdd?' %(ROOT_URL)
        params = urllib.parse.urlencode({'plurk_id': plurk_id, 'content': content, 'qualifier': 'says'})
        url = url+params
        response = self.client.request(url, method='GET')
        return response

    def like_post(self, ids):
        ids = json.dumps(ids)
        url = '%s/APP/Timeline/favoritePlurks?ids=%s' %(ROOT_URL, ids)
        response = self.client.request(url, method='GET')
        return response

    def search_and_like_posts(self):
        candidates = self.search_plurk()
        plurk_ids = []
        for candidate in candidates:
            if not self.valid_to_replurk(candidate): continue
            if candidate['favorite']: continue
            plurk_id = candidate['plurk_id']
            plurk_ids.append(plurk_id)
        return self.like_post(plurk_ids)


def replurk_pc_gatch_posts():
    import pc_gacha_config, pc_gacha_secret
    bot = ReplurkBot(pc_gacha_config, pc_gacha_secret)
    bot.search_and_replurk_posts()


def like_pc_gatch_posts():
    import pc_gacha_config, pc_gacha_secret
    bot = ReplurkBot(pc_gacha_config, pc_gacha_secret)
    bot.search_and_like_posts()


def replurk_appraisal_posts():
    import appraisal_config, appraisal_secret
    bot = ReplurkBot(appraisal_config, appraisal_secret)
    bot.search_and_replurk_posts()


def replurk_avalon_group_posts():
    import avalon_group_config, avalon_group_secret
    bot = ReplurkBot(avalon_group_config, avalon_group_secret)
    bot.search_and_replurk_posts()

def replurk_commission_posts():
    import commission_config, commission_secret
    bot = ReplurkBot(commission_config, commission_secret)
    bot.search_and_replurk_posts()

if __name__ == '__main__':
    replurk_commission_posts()

import json, datetime, urllib
import util, replurk


class QuoteBot(replurk.ReplurkBot):
    def valid_to_replurk(self, post):
        if post['user_id']!=replurk.ANONYMOUS_ID: return False
        if not self.contain_must_have_tag(post): return False
        return True


    def get_candidates_posts(self):
        timedelta = datetime.timedelta(minutes=self.config.INTERVAL_MINUTES)
        posted_time_limit = datetime.datetime.utcnow()-timedelta
        posts = self.search_plurk()
        candidates = []
        for post in posts:
            if not self.valid_to_replurk(post): continue
            posted_time = datetime.datetime.strptime(post['posted'], '%a, %d %b %Y %H:%M:%S %Z')
            if posted_time_limit>=posted_time>=posted_time_limit-timedelta:
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


    def quote_post(self, post):
        url = 'https://www.plurk.com/APP/Timeline/plurkAdd?'
        plurk_url_id = QuoteBot.base36encode(post['plurk_id'])
        full_plurk_url = 'https://www.plurk.com/p/'+plurk_url_id

        content = ''
        if post['publish_to_followers']:
            content += '**可能為親友粉絲限定**'
        else:
            content += '**偷偷說公開河道 only**'
        content +='\n'+post['content_raw']
        content += '\n'+full_plurk_url
        params = urllib.parse.urlencode({'content': content, 'qualifier': 'says'})
        url = url+params
        response = self.client.request(url, method='GET')


    def search_and_quote_posts(self):
        posts = self.get_candidates_posts()
        posts.reverse()
        for post in posts:
            self.quote_post(post)

def quote_pc_gatch_plurk():
    import ura_pc_gacha_config as config, ura_pc_gacha_secret as secret
    bot = QuoteBot(config, secret)
    bot.search_and_quote_posts()


if __name__ == '__main__':
    quote_pc_gatch_plurk()

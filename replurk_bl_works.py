import replurk


class ReplurkBlWroksBot(replurk.ReplurkBot):
    def contain_must_replurk_tag(self, post):
        return ReplurkBlWroksBot.contain_tag(post, self.config.MUST_REPLURK_TAGS)
        

    def valid_to_replurk(self, post):
        if post['user_id']==replurk.ANONYMOUS_ID: return False
        if not self.contain_must_have_tag(post): return False
        if self.contain_skip_tag(post): return False
        if self.contain_must_replurk_tag(post): return True
        if post['replurkers_count']>0: return True
        return False


def replurk_bl_works():
    import bl_works_config, bl_works_secret
    bot = ReplurkBlWroksBot(bl_works_config, bl_works_secret)
    bot.search_and_replurk_posts()


if __name__ == '__main__':
    replurk_bl_works()

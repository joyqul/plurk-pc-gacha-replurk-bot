import replurk


class ReplurkBlWroksBot(replurk.ReplurkBot):
    def is_possible_creater_user(self, post):
        none_creater_user_ids = [
            5087621, #卡布店小二
        ]
        return post['user_id'] not in none_creater_user_ids


    def valid_to_replurk(self, post):
        if not self.is_possible_creater_user(post): return False
        if self.contain_must_replurk_tag(post): return True
        if post['user_id']==replurk.ANONYMOUS_ID: return False
        if not self.contain_must_have_tag(post): return False
        if self.contain_skip_tag(post): return False
        if post['replurkers_count']>0: return True
        return False


def replurk_bl_works():
    import bl_works_config, bl_works_secret
    bot = ReplurkBlWroksBot(bl_works_config, bl_works_secret)
    bot.search_and_replurk_posts()


if __name__ == '__main__':
    replurk_bl_works()

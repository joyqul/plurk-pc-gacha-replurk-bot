import replurk, quote, ura_pc_gacha_config
import replurk_bl_works
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=10)
def timed_job():
    pass
    ## temporary closed
    #replurk.replurk_pc_gatch_posts()


@sched.scheduled_job('interval', minutes=ura_pc_gacha_config.INTERVAL_MINUTES)
def timed_job():
    quote.quote_pc_gatch_plurk()


@sched.scheduled_job('interval', minutes=30)
def timed_job():
    replurk.replurk_appraisal_posts()


@sched.scheduled_job('interval', hours=1)
def timed_job():
    replurk_bl_works.replurk_bl_works()
    

sched.start()

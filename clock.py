import replurk
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=10)
def timed_job():
    replurk.replurk_pc_gatch_posts()

sched.start()

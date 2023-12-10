from apscheduler.schedulers.background import BackgroundScheduler
from credits.services import pay_all_credits

        
def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(pay_all_credits, 'interval', minutes=1)
    scheduler.start()
    
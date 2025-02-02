import datetime
from uniulm_mensaparser import format_meals, get_unformatted_plan, Canteen, SimpleAdapter2
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


class MensaParser:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.refresh_plan, CronTrigger.from_crontab("0 9 * * *"), jitter=600)  # at 9 am
        self.scheduler.start()

        self._plan = None
        self._fs_et_plan = None
        self._last_updated = None
        self._canteens = {Canteen.UL_UNI_Sued, Canteen.UL_UNI_West}

    def refresh_plan(self):
        update = datetime.datetime.now()
        update = update.replace(microsecond=0)
        self._last_updated = update.isoformat()

        unformatted = get_unformatted_plan(self._canteens)

        self._plan = format_meals(unformatted, SimpleAdapter2)
        self._plan["last_updated"] = self._last_updated

    def get_plan(self):
        if self._plan is None:
            print("plan is none, so parsing mensa plan")
            self.refresh_plan()
        return self._plan


mensa_parser = MensaParser()


def get_mensa_parser() -> MensaParser:
    return mensa_parser

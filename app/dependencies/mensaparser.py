import datetime
from uniulm_mensaparser import format_meals, get_unformatted_plan, Canteen, SimpleAdapter2
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


class MensaParser:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.refresh_plan, CronTrigger.from_crontab("0 9 * * *"), jitter=600)  # at 9 am
        self.scheduler.start()

        self._last_updated = None
        self._canteens = {Canteen.UL_UNI_Sued, Canteen.UL_UNI_West}

        self._plan_de = None
        self._plan_en = None

    def refresh_plan(self):
        update = datetime.datetime.now()
        update = update.replace(microsecond=0)
        self._last_updated = update.isoformat()

        unformatted_de = get_unformatted_plan(self._canteens, "de")
        unformatted_en = get_unformatted_plan(self._canteens, "en")

        self._plan_de = format_meals(unformatted_de, SimpleAdapter2)
        self._plan_en = format_meals(unformatted_en, SimpleAdapter2)
        self._plan_de["last_updated"] = self._last_updated
        self._plan_en["last_updated"] = self._last_updated

    def get_plan_de(self):
        if self._plan_de is None:
            self.refresh_plan()
        return self._plan_de

    def get_plan_en(self):
        if self._plan_en is None:
            self.refresh_plan()
        return self._plan_en

    def get_plan(self, language: str):
        if language == "en":
            return self.get_plan_en()
        else:
            return self.get_plan_de()


mensa_parser = MensaParser()


def get_mensa_parser() -> MensaParser:
    return mensa_parser

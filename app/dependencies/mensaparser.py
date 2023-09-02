import datetime
from uniulm_mensaparser import get_plan, Canteen, SimpleAdapter2, FsEtAdapter
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


class MensaParser:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.refresh_plan, CronTrigger.from_crontab("0 9 * * *"), jitter=600)  # at 9 am
        self.scheduler.start()

        self._plan = None
        self._fs_et_plan = None
        self._last_updated = None
        self._canteens = {Canteen.UL_UNI_Sued, Canteen.UL_UNI_West, Canteen.UL_UNI_Nord}

    def refresh_plan(self):
        update = datetime.datetime.now()
        update = update.replace(microsecond=0)
        self._last_updated = update.isoformat()
        self._plan = get_plan(canteens=self._canteens, adapter_class=SimpleAdapter2)
        self._plan["last_updated"] = self._last_updated
        self._fs_et_plan = get_plan(canteens=self._canteens, adapter_class=FsEtAdapter)
        self._fs_et_plan["last_updated"] = self._last_updated

    def get_plan(self):
        if self._plan is None:
            self.refresh_plan()
        return self._plan

    def get_fs_plan(self):
        if self._fs_et_plan is None:
            self.refresh_plan()
        return self._fs_et_plan


def get_mensa_parser() -> MensaParser:
    return MensaParser()

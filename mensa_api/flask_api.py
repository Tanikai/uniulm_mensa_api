import datetime
import flask
from flask import Flask, redirect, url_for, make_response, Response, json
from flask_cors import CORS
from mensa_parser import parser, adapter
from mensa_parser.speiseplan_website_parser import Canteens
from datetime import date, timedelta
from flask_matomo import Matomo
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


def make_json_response(resp: dict) -> Response:
    json_text = json.dumps(resp, ensure_ascii=False, sort_keys=False).encode('utf8')
    response = make_response(json_text)
    response.headers['Content-length'] = len(json_text)
    response.headers['Content-Type'] = "application/json; charset=utf-8"
    return response


class MensaApi(Flask):
    plan = None
    fs_et_plan = None
    last_updated = None
    canteens = {Canteens.UL_UNI_Sued, Canteens.UL_UNI_West}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(self.refresh_plan, CronTrigger.from_crontab("0 9 * * *"), jitter=600)  # at 9 am
        self.scheduler.start()
        self.refresh_plan()

    def refresh_plan(self):
        update = datetime.datetime.now()
        update = update.replace(microsecond=0)
        print(update, "plan refreshed")
        self.last_updated = update.isoformat()
        self.plan = parser.get_plans_for_canteens(self.canteens, adapter.SimpleAdapter)
        self.plan["last_updated"] = self.last_updated
        self.fs_et_plan = parser.get_plans_for_canteens(self.canteens, adapter.FsEtAdapter)
        self.fs_et_plan["last_updated"] = self.last_updated

    def get_plan(self):
        if self.plan is None:
            self.refresh_plan()
        return self.plan

    def get_fs_plan(self):
        if self.fs_et_plan is None:
            self.refresh_plan()
        return self.fs_et_plan


def create_app(config: dict):
    app = MensaApi(__name__)
    CORS(app)

    if config["Matomo"]["enabled"]:
        matomo = Matomo(app,
                        matomo_url=config["Matomo"]["url"],
                        id_site=config["Matomo"]["site_id"],
                        token_auth=config["Matomo"]["token_auth"],
                        )
    else:
        # noop-matomo
        matomo = Matomo(app=None, matomo_url="placeholder", id_site=-1)

    limiter = Limiter(app, key_func=get_remote_address)

    @app.route("/")
    @matomo.ignore()
    def index():
        return redirect("https://github.com/Tanikai/uniulm_mensa_api", 302)

    @app.route("/api/v1/canteens/<mensa_id>/days/<mensa_date>/meals",
               methods=["GET"])
    @limiter.limit("30/minute")
    def return_mensaplan(mensa_id, mensa_date):
        formatted = app.get_plan()
        try:
            day_plan = formatted[mensa_id][mensa_date]
            return make_json_response(day_plan)
        except KeyError:
            return f"Could not find plan for {mensa_id} on date {mensa_date}", 404

    @limiter.limit("30/minute")
    @app.route("/api/v1/canteens/<mensa_id>", methods=["GET"])
    def return_next_plan(mensa_id):
        formatted = app.get_plan()

        day = date.today()
        found = False
        mensa = None
        try:
            mensa = formatted[mensa_id]
        except KeyError:
            return f"Could not find mensa {mensa_id}"

        day_plan = []
        date_key = ""
        while not found:
            date_key = day.strftime("%Y-%m-%d")
            if date_key not in mensa:
                day = day + timedelta(days=1)
                continue

            day_plan = mensa[date_key]
            if len(day_plan) > 0:
                found = True
            else:
                day = day + timedelta(days=1)

        return redirect(url_for("return_mensaplan", mensa_id=mensa_id,
                                mensa_date=date_key))

    @limiter.limit("30/minute")
    @app.route("/api/v1/canteens/<mensa_id>/all", methods=["GET"])
    def return_all(mensa_id):
        formatted = app.get_plan()
        # ggf. hier noch nen adapter
        return make_json_response(formatted)

    @limiter.limit("30/minute")
    @app.route("/api/v1/mensaplan.json")
    def return_fs_et():
        return make_json_response(app.get_fs_plan())

    @app.errorhandler(429)
    def ratelimit_handler(e):
        return flask.Response("ratelimited", 429)

    return app

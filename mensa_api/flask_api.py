from flask import Flask, jsonify, redirect, url_for
from mensa_parser import parser, adapter
from mensa_parser.speiseplan_website_parser import Canteens
from cachetools import cached, TTLCache
from datetime import date, timedelta
from flask_matomo import Matomo


# cache parsed plan for 1 hour
@cached(cache=TTLCache(maxsize=4, ttl=3600))
def get_cached_plan():
    print("parse plan...")
    canteens = {Canteens.UL_UNI_Sued, Canteens.UL_UNI_West}
    formatted = parser.get_plans_for_canteens(canteens, adapter.SimpleAdapter)
    return formatted


def create_app(config: dict):
    app = Flask(__name__)

    if config["Matomo"]["enabled"]:
        matomo = Matomo(app,
                        matomo_url=config["Matomo"]["url"],
                        id_site=config["Matomo"]["site_id"],
                        token_auth=config["Matomo"]["token_auth"],
                        )
    else:
        # noop-matomo
        matomo = Matomo(app=None, matomo_url="placeholder", id_site=-1)

    @app.route("/")
    @matomo.ignore()
    def index():
        return redirect("https://github.com/Tanikai/uniulm_mensa_api", 302)

    @app.route("/api/v1/canteens/<mensa_id>/days/<mensa_date>/meals",
               methods=["GET"])
    def return_mensaplan(mensa_id, mensa_date):
        formatted = get_cached_plan()
        try:
            day_plan = formatted[mensa_id][mensa_date]
            return jsonify(day_plan)
        except KeyError:
            return f"Could not find plan for {mensa_id} on date {mensa_date}", 404

    @app.route("/api/v1/canteens/<mensa_id>", methods=["GET"])
    def return_next_plan(mensa_id):
        formatted = get_cached_plan()

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

    return app

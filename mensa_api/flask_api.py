import flask
from flask import Flask, jsonify, redirect, url_for, make_response, Response, json
from flask_cors import CORS
from mensa_parser import parser, adapter
from mensa_parser.speiseplan_website_parser import Canteens
from cachetools import cached, TTLCache
from datetime import date, timedelta
from flask_matomo import Matomo
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import gzip


# cache parsed plan for 1 hour
@cached(cache=TTLCache(maxsize=4, ttl=3600))
def get_cached_plan():
    print("parse plan...")
    canteens = {Canteens.UL_UNI_Sued, Canteens.UL_UNI_West}
    formatted = parser.get_plans_for_canteens(canteens, adapter.SimpleAdapter)
    return formatted

def make_compressed_response(resp: dict) -> Response:
    json_text = json.dumps(resp, ensure_ascii=False)
    content = gzip.compress(json_text.encode('utf8'), 5)
    response = make_response(content)
    response.headers['Content-length'] = len(content)
    response.headers['Content-Encoding'] = 'gzip'
    response.headers['Content-Type'] = "application/json; charset=utf-8"
    return response


def create_app(config: dict):
    app = Flask(__name__)
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
        formatted = get_cached_plan()
        try:
            day_plan = formatted[mensa_id][mensa_date]
            return make_compressed_response(day_plan)
        except KeyError:
            return f"Could not find plan for {mensa_id} on date {mensa_date}", 404

    @limiter.limit("30/minute")
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

    @limiter.limit("30/minute")
    @app.route("/api/v1/canteens/<mensa_id>/all", methods=["GET"])
    def return_all(mensa_id):
        formatted = get_cached_plan()
        # ggf. hier noch nen adapter
        return make_compressed_response(formatted)

    @app.errorhandler(429)
    def ratelimit_handler(e):
        return flask.Response("ratelimited", 429)

    return app

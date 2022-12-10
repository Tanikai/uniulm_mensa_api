import configparser
from mensa_api import flask_api
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


def parse_config():
    # TODO: allow for other config paths
    config_path = "config.ini"

    cparser = configparser.ConfigParser()
    cparser.read(config_path)

    c = {
        "Matomo": {
            "enabled": False
        }
    }

    if "Matomo" in cparser.sections():
        c["Matomo"] = {
             "enabled": bool(cparser["Matomo"]["enabled"]),
             "url": cparser["Matomo"]["url"],
             "site_id": int(cparser["Matomo"]["site_id"]),
             "token_auth": cparser["Matomo"]["token_auth"],
        }

    return c


config = parse_config()
application = flask_api.create_app(config)
scheduler = BackgroundScheduler()

if __name__ == "__main__":
    app = flask_api.create_app(config)
    app.refresh_plan()

    scheduler.add_job(app.refresh_plan, CronTrigger.from_crontab("0 9 * * *"), jitter=600)  # at 9 am
    scheduler.start()

    app.run()


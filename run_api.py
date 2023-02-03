import configparser
from mensa_api import flask_api
from flask_compress import Compress


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
compress = Compress()

if __name__ == "__main__":
    app = flask_api.create_app(config)
    compress.init_app(app)
    app.run()


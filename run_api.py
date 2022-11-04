import configparser
import sys
from mensa_api import flask_api


def parse_config():
    config_path = "config.ini"
    if len(sys.argv) > 1:
        config_path = sys.argv[1]

    config = configparser.ConfigParser()
    config.read(config_path)

    if "Matomo" not in config.sections():
        return

    matomo_config = {
        "url": config["matomo"]["url"],
        "site_id": config["matomo"]["site_id"],
        "token_auth": config["matomo"]["token_auth"],
    }


application = flask_api.create_app()

if __name__ == "__main__":
    parse_config()
    app = flask_api.create_app()
    app.run()


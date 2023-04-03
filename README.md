# Uni Ulm Mensa Plan REST API

This project contains a REST API that provides data from the
[Tanikai/uniulm_mensaparser](https://github.com/Tanikai/uniulm_mensaparser)
module.

The parsed data can be accessed here:
[uulm.anter.dev/api/v1/canteens/ul_uni_sued](https://uulm.anter.dev/api/v1/canteens/ul_uni_sued)

## Getting Started

These instructions will give you a copy of the project up and running on
your local machine for development and testing purposes. See deployment
for notes on deploying the project on a live system.

### Prerequisites

This project is tested and deployed with Python 3.9+. It might work with lower
versions, but without guarantee.

### Installing

Firstly, clone this repository and install the required Python modules:

```sh
git clone https://github.com/Tanikai/uniulm_mensa_api.git
cd uniulm_mensa_api
pip install -r requirements.txt
```

After that, you can run the REST API with:

```sh
python run_api.py
```

## Deployment

When you want to deploy the application, you will need a WSGI server. For
example, you can use the [waitress](https://github.com/Pylons/waitress) module:

```sh
python -m waitress --port 8080 run_api:application
```

## API Documentation

The following canteens at Ulm University are currently supported:

- Mensa Süd (id: **ul_uni_sued**)
- Mensa West (id: **ul_uni_west**)

Support for Mensa Nord (Bistro) is planned.

| Path                                                        | Description                                                                                      |
|-------------------------------------------------------------|--------------------------------------------------------------------------------------------------|
| `BASE_URL/api/v1/canteens/CANTEEN_ID/`                      | Get the next daily plan for the specified canteen (days where the canteen is closed are skipped) |
| `BASE_URL/api/v1/canteens/CANTEEN_ID/days/YYYY-MM-DD/meals` | Get the canteen plan for a specific day                                                          |
| `BASE_URL/api/v1/canteens/CANTEEN_ID/all`                   | Get all plans for the specified canteen                                                          |
| `BASE_URL/api/v1/mensaplan.json`                            | Data in [FS-ET format](https://mensaplan.fs-et.de/data/mensaplan.json) (work in progess)         |


## Analytics

To track the API usage in a GDPR-friendly way, a Python integration
for [Matomo](https://matomo.org/) is integrated into the project. It is only
enabled when a `config.ini` file is placed in the root directory (same directory
as `run_api.py`). If you want to connect the API to your Matomo instance, set
the following properties:

```ini
[Matomo]
enabled = True 
; The URL to your Matomo instance
url = YOUR_MATOMO_URL
; Your Matomo site_id for the API (e.g. 5)
site_id = YOUR_MATOMO_SITE_ID 
; Visitor might be behind a proxy. To change the IP address of the 
; POST Request, an auth token is required. You can get it in Matomo
; under Settings > Personal > Security > Auth tokens.
token_auth = YOUR_API_TOKEN
```

## Built With

- [flask](https://flask.palletsprojects.com/) for the REST API
- Fork of [flask-matomo](https://flask-matomo.readthedocs.io/en/latest/) for tracking
  - Fork repository: [github.com/Tanikai/flask-matomo](https://github.com/Tanikai/flask-matomo)

## Authors

- **Kai Anter** - [GitHub](https://github.com/Tanikai) - [Mastodon](https://hachyderm.io/@tanikai)

## License

This project is licensed under the GNU General Public License Version 3 - see
the [LICENSE](LICENSE) file for details

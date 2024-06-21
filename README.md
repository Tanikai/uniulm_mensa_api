# Uni Ulm Mensa Plan REST API

This project contains a REST API that provides data from the
[Tanikai/uniulm_mensaparser](https://github.com/Tanikai/uniulm_mensaparser)
module.

The parsed data can be accessed here:
[uulm.anter.dev/api/v1/canteens/all](https://uulm.anter.dev/api/v1/canteens/all)

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
uvicorn app.main:app --reload
```

## Deployment

When you want to deploy the application, you will need a WSGI server. For
example, you can use the [waitress](https://github.com/Pylons/waitress) module:

```sh
uvicorn app.main:app --reload
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

To track the API usage in a GDPR-friendly way, a Middleware
for [Matomo](https://matomo.org/) is integrated into the project. Alternatively,
you can use [Umami](https://umami.is/). Both are disabled by default.

To enable analytics, set the respective `_ENABLED` variable to `True` and pass
the required configuration values:

```sh
# Matomo
MATOMO_ENABLED=True
MATOMO_URL=YOUR_MATOMO_URL
MATOMO_SITE_ID=YOUR_MATOMO_SITE_ID

# Umami
UMAMI_ENABLED=True
UMAMI_URL=YOUR_UMAMI_URL
UMAMI_SITE_ID=YOUR_UMAMI_SITE_ID
```

## Authors

- **Kai Anter** - [GitHub](https://github.com/Tanikai) - [Mastodon](https://hachyderm.io/@tanikai)

## License

This project is licensed under the GNU General Public License Version 3 - see
the [LICENSE](LICENSE) file for details

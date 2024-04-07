## Requirements

- docker
- docker-compose
- python3
- pip3

## Presentation

### Data import

- dag_datalake_sirene : https://github.com/etalab/annuaire-entreprises-search-infra/tree/112a26da9aab5dabd2760fa839eebd8a086b5657
- added files:
  - ./import.py
  - ./dag_datalake_sirene/import_data.py
- changed files: many files under ./dag_datalake_sirene to remove private Etalab data (RNE, INSEE, Bilans financiers, Marché inclusion, etc.)

### API

- aio : https://github.com/etalab/annuaire-entreprises-search-api/tree/2fc2b16664da4b21262e5092bedd9b1ee817ad29/aio
- changed files: removed the APM part in aio proxy.

## Installation

### MacOS prerequisites

To make work the request SSL downloads:

```bash
ln -s /etc/ssl/* /Library/Frameworks/Python.framework/Versions/Current/etc/openssl/
```

### Start databases

This elasticsearch db will store all the enterprise data in a persistent local storage (./.esdata).

```bash
mkdir ./.esdata
# chown the ./.esdata, make sure that docker will be able to write in it.

# Feel free to:
# - Adjust the 8g RAM heap size (docker-compose.yml)
# - Choose a specific location for your elastic data (needs at least 70GB)
docker compose up -d elasticsearch
```

Start redis:

```bash
docker compose up -d redis
```

### Import data:

- Source data import (downloads + sqlite indexation):
  - (8 CPU + 16GB RAM, 70GB high-speed disk for sqlite data): About 4h
- Elastic indexation: (16 CPU + 32GB RAM, 70GB high-speed disk):
  - (16 CPU + 32GB RAM, 70GB high-speed disk for elastic data): About 7h

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt

cp .env.sample .env
nano .env # Choose the DATA_DIR for import data

#python3 import.py # Executes both import and elastic indexation \/
nohup python import.py > output.log 2>&1 &
```

## Usage

`aio` proxy hosts the python search API:

```bash
docker compose up -d http-proxy
```

Then you can fetch the API: `http://localhost:4500/search?q=Carrefour+chalon+sur+saone`

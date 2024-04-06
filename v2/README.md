## Presentation 

### Data import
* dag_datalake_sirene : https://github.com/etalab/annuaire-entreprises-search-infra/tree/112a26da9aab5dabd2760fa839eebd8a086b5657
* added files:
    * ./import.py
    * ./dag_datalake_sirene/import_data.py
* changed files: many files under ./dag_datalake_sirene to remove private Etalab data (RNE, INSEE, Bilans financiers, Marché inclusion, etc.)

### API

* aio : https://github.com/etalab/annuaire-entreprises-search-api/tree/2fc2b16664da4b21262e5092bedd9b1ee817ad29/aio

## Installation

### MacOS prerequisites

To make work the request SSL downloads:

```bash
ln -s /etc/ssl/* /Library/Frameworks/Python.framework/Versions/Current/etc/openssl/
```

### Import data:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip3 install -r requirements.txt
python3 import.py
```

## Usage


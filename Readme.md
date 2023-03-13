
This project simplifies the import and deployment of the https://github.com/etalab/annuaire-entreprises-site database and API.

No kibana, no APM, no live-deploying (green / blue), no worflows.

Just a one-shot deployment of the search API of french enterprises.

For now, it's not possible to import the `dirigeant` data from the INPI SFTP.

# Requirements 

- docker
- docker-compose 
- python3


# Install the importer

```
pip3 install -r requirements.txt
``` 

# Import data 

## Start the ELK environement

This elasticsearch db will store all the enterprise data in a persistent local storage (./esdata)

``` 
docker compose up -d elasticsearch 
```

## Import the data in the ELK index

Be warned that about 25GB of temporary files will be generated in ./tmp

```
python3 import.py > import.log 2>&1 &
```

It takes few hours.

# Start the API

AIO API gonna host the python search API

```
docker compose up -d
```

http://localhost:4500/search?q=Carrefour+chalon+sur+saone
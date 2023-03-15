
This project simplifies the import and deployment of the https://github.com/etalab/annuaire-entreprises-site database and API.

No kibana, no APM, no live-deploying (green / blue), no worflows.

Just a simple importation and deployment of the search API of french enterprises.

For now, it's not possible to import the `dirigeant` data from the `inpi.db` filled from the INPI SFTP data :
- https://data.inpi.fr/content/editorial/Serveur_ftp_entreprises
- https://github.com/etalab/dag_inpi_data
- https://data.inpi.fr
- https://github.com/etalab/rncs_worker_api_entreprise
- https://www.inpi.fr/sites/default/files/formulaire%20de%20cr%C3%A9ation%20de%20compte_V15_remplissable.pdf

# Requirements 

- docker
- docker-compose 
- python3
- pip3


# Install the importer

```
pip3 install -r requirements.txt
``` 

# Import data 

## Start the ELK environement

This elasticsearch db will store all the enterprise data in a persistent local storage (./.esdata).

```
mkdir ./.esdata
# chown the ./.esdata, make sure that docker will be able to write in it.

# Feel free to adjust the 8g RAM heap size (docker-compose.yml)
docker compose up -d elasticsearch 
```

## Import the data in the ELK index

Be warned that about 25GB of temporary files will be generated in ./tmp and that the Elasticsearch db is 35GB in ./.esdata

```
python3 import.py > import.log 2>&1 &
```

It takes up to 6 to 24 hours depending your server performance.

# Start the API

AIO API gonna host the python search API

```
docker compose up -d
```

http://localhost:4500/search?q=Carrefour+chalon+sur+saone

# Annuaire des Entreprises - [Infrastructure de recherche]

Ce site est disponible en ligne : [L’Annuaire des Entreprises](https://annuaire-entreprises.data.gouv.fr)

Ce repository décrit le workflow qui récupère, traite et indexe les données publiques d'entreprises.

Ce code s'exécute dans une infrastructure Airflow basée sur cette stack 👉 https://github.com/etalab/data-engineering-stack.

## Architecture du service 🏗

Ce repository fait partie d'un ensemble de services qui constituent l'[Annuaire des Entreprises](https://annuaire-entreprises.data.gouv.fr) :

| Description | Accès |
|-|-|
|Le site Web | [par ici 👉](https://github.com/etalab/annuaire-entreprises-site) |
|L’API du Moteur de recherche | [par ici 👉](https://github.com/etalab/annuaire-entreprises-search-api) |
|L‘API de redondance de Sirene | [par ici 👉](https://github.com/etalab/annuaire-entreprises-sirene-api) |
|Le traitement permettant la génération de données à ingérer dans le moteur de recherche | [par ici 👉](https://github.com/etalab/annuaire-entreprises-search-infra) |

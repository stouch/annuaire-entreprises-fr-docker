import logging
logger = logging.getLogger(__name__)

import pandas as pd


def preprocess_etablissements_data(departement):
    url = (
        f"https://files.data.gouv.fr/geo-sirene/last/dep/geo_siret"
        f"_{departement}.csv.gz"
    )
    logging.info(f"Dep file url: {url}")
    df_dep = pd.read_csv(
        url,
        compression="gzip",
        dtype=str,
        usecols=[
            "siren",
            "siret",
            "dateCreationEtablissement",
            "trancheEffectifsEtablissement",
            "activitePrincipaleRegistreMetiersEtablissement",
            "etablissementSiege",
            "numeroVoieEtablissement",
            "libelleVoieEtablissement",
            "codePostalEtablissement",
            "libelleCommuneEtablissement",
            "libelleCedexEtablissement",
            "typeVoieEtablissement",
            "codeCommuneEtablissement",
            "codeCedexEtablissement",
            "complementAdresseEtablissement",
            "distributionSpecialeEtablissement",
            "complementAdresse2Etablissement",
            "indiceRepetition2Etablissement",
            "libelleCedex2Etablissement",
            "codeCedex2Etablissement",
            "numeroVoie2Etablissement",
            "typeVoie2Etablissement",
            "libelleVoie2Etablissement",
            "codeCommune2Etablissement",
            "libelleCommune2Etablissement",
            "distributionSpeciale2Etablissement",
            "dateDebut",
            "etatAdministratifEtablissement",
            "enseigne1Etablissement",
            "enseigne1Etablissement",
            "enseigne2Etablissement",
            "enseigne3Etablissement",
            "denominationUsuelleEtablissement",
            "activitePrincipaleEtablissement",
            "geo_adresse",
            "geo_id",
            "longitude",
            "latitude",
            "indiceRepetitionEtablissement",
            "libelleCommuneEtrangerEtablissement",
            "codePaysEtrangerEtablissement",
            "libellePaysEtrangerEtablissement",
            "libelleCommuneEtranger2Etablissement",
            "codePaysEtranger2Etablissement",
            "libellePaysEtranger2Etablissement",
        ],
    )
    df_dep = df_dep.rename(
        columns={
            "dateCreationEtablissement": "date_creation",
            "trancheEffectifsEtablissement": "tranche_effectif_salarie",
            "activitePrincipaleRegistreMetiersEtablissement": "activite_principale"
            "_registre_metier",
            "etablissementSiege": "est_siege",
            "numeroVoieEtablissement": "numero_voie",
            "typeVoieEtablissement": "type_voie",
            "libelleVoieEtablissement": "libelle_voie",
            "codePostalEtablissement": "code_postal",
            "libelleCedexEtablissement": "libelle_cedex",
            "libelleCommuneEtablissement": "libelle_commune",
            "codeCommuneEtablissement": "commune",
            "complementAdresseEtablissement": "complement_adresse",
            "complementAdresse2Etablissement": "complement_adresse_2",
            "numeroVoie2Etablissement": "numero_voie_2",
            "indiceRepetition2Etablissement": "indice_repetition_2",
            "typeVoie2Etablissement": "type_voie_2",
            "libelleVoie2Etablissement": "libelle_voie_2",
            "codeCommune2Etablissement": "commune_2",
            "libelleCommune2Etablissement": "libelle_commune_2",
            "codeCedex2Etablissement": "cedex_2",
            "libelleCedex2Etablissement": "libelle_cedex_2",
            "codeCedexEtablissement": "cedex",
            "dateDebut": "date_debut_activite",
            "distributionSpecialeEtablissement": "distribution_speciale",
            "distributionSpeciale2Etablissement": "distribution_speciale_2",
            "etatAdministratifEtablissement": "etat_administratif_etablissement",
            "enseigne1Etablissement": "enseigne_1",
            "enseigne2Etablissement": "enseigne_2",
            "enseigne3Etablissement": "enseigne_3",
            "activitePrincipaleEtablissement": "activite_principale",
            "indiceRepetitionEtablissement": "indice_repetition",
            "denominationUsuelleEtablissement": "nom_commercial",
            "libelleCommuneEtrangerEtablissement": "libelle_commune_etranger",
            "codePaysEtrangerEtablissement": "code_pays_etranger",
            "libellePaysEtrangerEtablissement": "libelle_pays_etranger",
            "libelleCommuneEtranger2Etablissement": "libelle_commune_etranger_2",
            "codePaysEtranger2Etablissement": "code_pays_etranger_2",
            "libellePaysEtranger2Etablissement": "libelle_pays_etranger_2",
        }
    )
    return df_dep

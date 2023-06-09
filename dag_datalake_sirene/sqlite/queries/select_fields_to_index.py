select_fields_to_index_query = """SELECT
            ul.activite_principale_unite_legale as activite_principale_unite_legale,
            ul.categorie_entreprise as categorie_entreprise,
            ul.date_creation_unite_legale as date_creation_unite_legale,
            ul.date_mise_a_jour_unite_legale as date_mise_a_jour_unite_legale,
            ul.denomination_usuelle_1 as denomination_usuelle_1_unite_legale,
            ul.denomination_usuelle_2 as denomination_usuelle_2_unite_legale,
            ul.denomination_usuelle_3 as denomination_usuelle_3_unite_legale,
            ul.economie_sociale_solidaire_unite_legale as
            economie_sociale_solidaire_unite_legale,
            ul.etat_administratif_unite_legale as etat_administratif_unite_legale,
            ul.identifiant_association_unite_legale as
            identifiant_association_unite_legale,
            ul.nature_juridique_unite_legale as nature_juridique_unite_legale,
            ul.nom as nom,
            ul.nom_raison_sociale as nom_raison_sociale,
            ul.nom_usage as nom_usage,
            ul.prenom as prenom,
            ul.sigle as sigle,
            ul.siren,
            st.siret as siret_siege,
            ul.tranche_effectif_salarie_unite_legale as
            tranche_effectif_salarie_unite_legale,
            (SELECT count FROM count_etab ce WHERE ce.siren = st.siren) as
            nombre_etablissements,
            (SELECT count FROM count_etab_ouvert ceo WHERE ceo.siren = st.siren) as
            nombre_etablissements_ouverts,
            (SELECT json_group_array(
                json_object(
                    'siren', siren,
                    'nom_patronymique', nom_patronymique,
                    'nom_usage', nom_usage,
                    'prenoms', prenoms,
                    'date_naissance', datenaissance,
                    'ville_naissance', villenaissance,
                    'pays_naissance', paysnaissance,
                    'qualite', qualite
                    )
                ) FROM
                (
                    SELECT siren, nom_patronymique, nom_usage, prenoms,
                    datenaissance, villenaissance, paysnaissance, qualite
                    FROM dirigeant_pp
                    WHERE siren = st.siren
                )
            ) as dirigeants_pp,
            (SELECT json_group_array(
                    json_object(
                        'siren', siren,
                        'siren_pm', siren_pm,
                        'denomination', denomination,
                        'sigle', sigle,
                        'qualite', qualite
                        )
                    ) FROM
                    (
                        SELECT siren, siren_pm, denomination, sigle, qualite
                        FROM dirigeant_pm
                        WHERE siren = st.siren
                    )
                ) as dirigeants_pm,
            (SELECT json_group_array(
                    json_object(
                        'activite_principale',activite_principale,
                        'activite_principale_registre_metier',
                        activite_principale_registre_metier,
                        'cedex',cedex,
                        'cedex_2',cedex_2,
                        'code_pays_etranger',code_pays_etranger,
                        'code_pays_etranger_2',code_pays_etranger_2,
                        'code_postal',code_postal,
                        'commune',commune,
                        'commune_2',commune_2,
                        'complement_adresse',complement_adresse,
                        'complement_adresse_2',complement_adresse_2,
                        'date_creation',date_creation,
                        'date_debut_activite',date_debut_activite,
                        'distribution_speciale',distribution_speciale,
                        'distribution_speciale_2',distribution_speciale_2,
                        'enseigne_1',enseigne_1,
                        'enseigne_2',enseigne_2,
                        'enseigne_3',enseigne_3,
                        'est_siege',est_siege,
                        'etat_administratif',etat_administratif_etablissement,
                        'geo_adresse',geo_adresse,
                        'geo_id',geo_id,
                        'indice_repetition',indice_repetition,
                        'indice_repetition_2',indice_repetition_2,
                        'latitude',latitude,
                        'libelle_cedex',libelle_cedex,
                        'libelle_cedex_2',libelle_cedex_2,
                        'libelle_commune',libelle_commune,
                        'libelle_commune_2',libelle_commune_2,
                        'libelle_commune_etranger',libelle_commune_etranger,
                        'libelle_commune_etranger_2',libelle_commune_etranger_2,
                        'libelle_pays_etranger',libelle_pays_etranger,
                        'libelle_pays_etranger_2',libelle_pays_etranger_2,
                        'libelle_voie',libelle_voie,
                        'libelle_voie_2',libelle_voie_2,
                        'liste_finess', liste_finess,
                        'liste_idcc', liste_idcc,
                        'liste_rge', liste_rge,
                        'liste_uai', liste_uai,
                        'longitude',longitude,
                        'nom_commercial',nom_commercial,
                        'numero_voie',numero_voie,
                        'numero_voie_2',numero_voie_2,
                        'siren', siren,
                        'siret', siret,
                        'tranche_effectif_salarie',tranche_effectif_salarie,
                        'type_voie',type_voie,
                        'type_voie_2',type_voie_2
                        )
                    ) FROM
                    (
                        SELECT
                        s.activite_principale as activite_principale,
                        s.activite_principale_registre_metier as
                        activite_principale_registre_metier,
                        s.cedex as cedex,
                        s.cedex_2 as cedex_2,
                        s.code_pays_etranger as code_pays_etranger,
                        s.code_pays_etranger_2 as code_pays_etranger_2,
                        s.code_postal as code_postal,
                        s.commune as commune,
                        s.commune_2 as commune_2,
                        s.complement_adresse as complement_adresse,
                        s.complement_adresse_2 as complement_adresse_2,
                        s.date_creation as date_creation,
                        s.date_debut_activite as date_debut_activite,
                        s.distribution_speciale as distribution_speciale,
                        s.distribution_speciale_2 as distribution_speciale_2,
                        s.enseigne_1 as enseigne_1,
                        s.enseigne_2 as enseigne_2,
                        s.enseigne_3 as enseigne_3,
                        s.est_siege as est_siege,
                        s.etat_administratif_etablissement as
                        etat_administratif_etablissement,
                        s.geo_adresse as geo_adresse,
                        s.geo_id as geo_id,
                        s.indice_repetition as indice_repetition,
                        s.indice_repetition_2 as indice_repetition_2,
                        s.latitude as latitude,
                        s.libelle_cedex as libelle_cedex,
                        s.libelle_cedex_2 as libelle_cedex_2,
                        s.libelle_commune as libelle_commune,
                        s.libelle_commune_2 as libelle_commune_2,
                        s.libelle_commune_etranger as libelle_commune_etranger,
                        s.libelle_commune_etranger_2 as libelle_commune_etranger_2,
                        s.libelle_pays_etranger as libelle_pays_etranger,
                        s.libelle_pays_etranger_2 as libelle_pays_etranger_2,
                        s.libelle_voie as libelle_voie,
                        s.libelle_voie_2 as libelle_voie_2,
                        (SELECT liste_finess FROM finess WHERE siret = s.siret) as
                        liste_finess,
                        (SELECT liste_idcc FROM convention_collective WHERE siret =
                        s.siret) as liste_idcc,
                        (SELECT liste_rge FROM rge WHERE siret = s.siret) as liste_rge,
                        (SELECT liste_uai FROM uai WHERE siret = s.siret) as liste_uai,
                        s.longitude as longitude,
                        s.nom_commercial as nom_commercial,
                        s.numero_voie as numero_voie,
                        s.numero_voie_2 as numero_voie_2,
                        s.siren as siren,
                        s.siret as siret,
                        s.tranche_effectif_salarie as tranche_effectif_salarie,
                        s.type_voie as type_voie,
                        s.type_voie_2 as type_voie_2
                        FROM siret s
                        WHERE s.siren = ul.siren
                    )
                ) as etablissements,
            (SELECT json_object(
                        'activite_principale',activite_principale,
                        'activite_principale_registre_metier',
                        activite_principale_registre_metier,
                        'cedex',cedex,
                        'cedex_2',cedex_2,
                        'code_pays_etranger',code_pays_etranger,
                        'code_pays_etranger_2',code_pays_etranger_2,
                        'code_postal',code_postal,
                        'commune',commune,
                        'commune_2',commune_2,
                        'complement_adresse',complement_adresse,
                        'complement_adresse_2',complement_adresse_2,
                        'date_creation',date_creation,
                        'date_debut_activite',date_debut_activite,
                        'distribution_speciale',distribution_speciale,
                        'distribution_speciale_2',distribution_speciale_2,
                        'enseigne_1',enseigne_1,
                        'enseigne_2',enseigne_2,
                        'enseigne_3',enseigne_3,
                        'est_siege',est_siege,
                        'etat_administratif',etat_administratif_etablissement,
                        'geo_adresse',geo_adresse,
                        'geo_id',geo_id,
                        'indice_repetition',indice_repetition,
                        'indice_repetition_2',indice_repetition_2,
                        'latitude',latitude,
                        'libelle_cedex',libelle_cedex,
                        'libelle_cedex_2',libelle_cedex_2,
                        'libelle_commune',libelle_commune,
                        'libelle_commune_2',libelle_commune_2,
                        'libelle_commune_etranger',libelle_commune_etranger,
                        'libelle_commune_etranger_2',libelle_commune_etranger_2,
                        'libelle_pays_etranger',libelle_pays_etranger,
                        'libelle_pays_etranger_2',libelle_pays_etranger_2,
                        'libelle_voie',libelle_voie,
                        'libelle_voie_2',libelle_voie_2,
                        'liste_finess', liste_finess,
                        'liste_idcc', liste_idcc,
                        'liste_rge', liste_rge,
                        'liste_uai', liste_uai,
                        'longitude',longitude,
                        'nom_commercial',nom_commercial,
                        'numero_voie',numero_voie,
                        'numero_voie_2',numero_voie_2,
                        'siren', siren,
                        'siret', siret,
                        'tranche_effectif_salarie',tranche_effectif_salarie,
                        'type_voie',type_voie,
                        'type_voie_2',type_voie_2
                        )
                    FROM
                    (
                        SELECT
                        s.activite_principale as activite_principale,
                        s.activite_principale_registre_metier as
                        activite_principale_registre_metier,
                        s.cedex as cedex,
                        s.cedex_2 as cedex_2,
                        s.code_pays_etranger as code_pays_etranger,
                        s.code_pays_etranger_2 as code_pays_etranger_2,
                        s.code_postal as code_postal,
                        s.commune as commune,
                        s.commune_2 as commune_2,
                        s.complement_adresse as complement_adresse,
                        s.complement_adresse_2 as complement_adresse_2,
                        s.date_creation as date_creation,
                        s.date_debut_activite as date_debut_activite,
                        s.distribution_speciale as distribution_speciale,
                        s.distribution_speciale_2 as distribution_speciale_2,
                        s.enseigne_1 as enseigne_1,
                        s.enseigne_2 as enseigne_2,
                        s.enseigne_3 as enseigne_3,
                        s.est_siege as est_siege,
                        s.etat_administratif_etablissement as
                        etat_administratif_etablissement,
                        s.geo_adresse as geo_adresse,
                        s.geo_id as geo_id,
                        s.indice_repetition as indice_repetition,
                        s.indice_repetition_2 as indice_repetition_2,
                        s.latitude as latitude,
                        s.libelle_cedex as libelle_cedex,
                        s.libelle_cedex_2 as libelle_cedex_2,
                        s.libelle_commune as libelle_commune,
                        s.libelle_commune_2 as libelle_commune_2,
                        s.libelle_commune_etranger as libelle_commune_etranger,
                        s.libelle_commune_etranger_2 as libelle_commune_etranger_2,
                        s.libelle_pays_etranger as libelle_pays_etranger,
                        s.libelle_pays_etranger_2 as libelle_pays_etranger_2,
                        s.libelle_voie as libelle_voie,
                        s.libelle_voie_2 as libelle_voie_2,
                        (SELECT liste_finess FROM finess WHERE siret = s.siret) as
                        liste_finess,
                        (SELECT liste_idcc FROM convention_collective WHERE siret =
                        s.siret) as liste_idcc,
                        (SELECT liste_rge FROM rge WHERE siret = s.siret) as liste_rge,
                        (SELECT liste_uai FROM uai WHERE siret = s.siret) as liste_uai,
                        s.longitude as longitude,
                        s.nom_commercial as nom_commercial,
                        s.numero_voie as numero_voie,
                        s.numero_voie_2 as numero_voie_2,
                        s.siren as siren,
                        s.siret as siret,
                        s.tranche_effectif_salarie as tranche_effectif_salarie,
                        s.type_voie as type_voie,
                        s.type_voie_2 as type_voie_2
                        FROM siretsiege as s
                        WHERE s.siren = st.siren
                    )
                ) as siege,
            (SELECT est_entrepreneur_spectacle FROM spectacle WHERE siren = ul.siren) as
             est_entrepreneur_spectacle,
            (SELECT colter_code_insee FROM colter WHERE siren = ul.siren) as
            colter_code_insee,
            (SELECT colter_code FROM colter WHERE siren = ul.siren) as colter_code,
            (SELECT colter_niveau FROM colter WHERE siren = ul.siren) as colter_niveau,
            (SELECT json_group_array(
                json_object(
                    'siren', siren,
                    'nom', nom,
                    'prenom', prenom,
                    'date_naissance', date_naissance,
                    'sexe', sexe,
                    'fonction', fonction
                    )
                ) FROM
                (
                    SELECT siren, nom, prenom, date_naissance,
                    sexe, fonction
                    FROM elus
                    WHERE siren = ul.siren
                )
            ) as colter_elus
            FROM
                siretsiege st
            LEFT JOIN
                unite_legale ul
            ON
                ul.siren = st.siren;"""

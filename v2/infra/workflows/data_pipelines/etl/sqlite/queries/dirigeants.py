create_table_dirigeant_pp_query = """
        CREATE TABLE IF NOT EXISTS dirigeants_pp
        (
            siren,
            date_mise_a_jour,
            date_de_naissance,
            role,
            nom,
            nom_usage,
            prenoms,
            nationalite,
            role_description
        )
    """

create_table_dirigeant_pm_query = """
        CREATE TABLE IF NOT EXISTS dirigeants_pm
        (
            siren,
            date_mise_a_jour,
            denomination,
            siren_dirigeant,
            role,
            forme_juridique,
            role_description
        )
    """


def get_chunk_dirig_pm_from_db_query(chunk_size, iterator):
    query = f"""
        SELECT DISTINCT siren, date_mise_a_jour, denomination,
        siren_dirigeant, role, forme_juridique
        FROM dirigeants_pm
        WHERE siren IN
        (
            SELECT DISTINCT siren
            FROM dirigeants_pm
            WHERE siren != ''
            LIMIT {chunk_size}
            OFFSET {int(iterator * chunk_size)})
        """
    return query


def get_chunk_dirig_pp_from_db_query(chunk_size, iterator):
    query = f"""
        SELECT DISTINCT siren, date_mise_a_jour, date_de_naissance, role,
        nom, nom_usage, prenoms, nationalite
        FROM dirigeants_pp
        WHERE siren IN
            (
            SELECT DISTINCT siren
            FROM dirigeants_pp
            WHERE siren != ''
            LIMIT {chunk_size}
            OFFSET {int(iterator * chunk_size)})
        """
    return query

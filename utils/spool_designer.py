# ==========================================================
# S435 DIMENSION DATABASE
# ==========================================================

S435_LENGTH = {

    "DN25": 200,

    "DN50": 230,

    "DN65": 230,

    "DN80": 250,

    "DN100": 300,

    "DN125": 350,

    "DN150": 400,

    "DN200": 500,

    "DN250": 600,

    "DN300": 700

}

# ==========================================================
# REDUCER / EXPANDER STANDARD LENGTH
# ==========================================================

REDUCER_LENGTH = 150

EXPANDER_LENGTH = 150


# ==========================================================
# DESIGN SPOOL
# ==========================================================

def design_spool(

    existing_dn,

    recommended_dn,

    upstream,

    downstream

):

    meter_length = S435_LENGTH.get(
        recommended_dn,
        250
    )

    total = (

        REDUCER_LENGTH

        + upstream

        + meter_length

        + downstream

        + EXPANDER_LENGTH

    )

    return {

        "existing_dn": existing_dn,

        "recommended_dn": recommended_dn,

        "reducer_length": REDUCER_LENGTH,

        "meter_length": meter_length,

        "expander_length": EXPANDER_LENGTH,

        "upstream": upstream,

        "downstream": downstream,

        "total_length": total

    }

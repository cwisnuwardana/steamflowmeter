from utils.pipe_lookup import get_pipe_data

# ==========================================================
# S435 FACE TO FACE DIMENSION (Dimension A - Datasheet)
# ==========================================================

S435_LENGTH = {

    "DN25": 100,      # Estimated (datasheet starts from DN40)
    "DN40": 100,
    "DN50": 110,
    "DN65": 110,
    "DN80": 110,
    "DN100": 120,
    "DN125": 133,
    "DN150": 160,
    "DN200": 185,
    "DN250": 210,
    "DN300": 240

}

# ==========================================================
# REDUCER / EXPANDER ESTIMATION
# ==========================================================

REDUCER_LENGTH = 152
EXPANDER_LENGTH = 152
# Preliminary estimation based on ASME B16.9 butt-weld fittings.
# Dynamic reducer/expander lookup will be implemented in future revision.

# ==========================================================
# DESIGN SPOOL
# ==========================================================

def design_spool(

    existing_dn,
    recommended_dn,
    upstream,
    downstream,
    schedule

):

    # --------------------------------------------
    # Existing Straight Pipe (Nominal DN)
    # --------------------------------------------

    existing_dn_mm = int(
        existing_dn.replace("DN", "")
    )

    existing_5D = existing_dn_mm * 5

    # --------------------------------------------
    # Meter Length
    # --------------------------------------------

    meter_length = S435_LENGTH.get(
        recommended_dn,
        110
    )

    # --------------------------------------------
    # Fabrication Length
    # --------------------------------------------

    fabrication_length = (

        REDUCER_LENGTH
        + upstream
        + meter_length
        + downstream
        + EXPANDER_LENGTH

    )

    # --------------------------------------------
    # Installation Envelope
    # --------------------------------------------

    installation_envelope = (

        existing_5D
        + fabrication_length
        + existing_5D

    )

    return #{

        #"existing_dn": existing_dn,
        #"recommended_dn": recommended_dn,
        #"existing_5D": round(existing_5D),
        #"reducer_length": REDUCER_LENGTH,
        #"meter_length": meter_length,
        #"expander_length": EXPANDER_LENGTH,
        #"upstream": round(upstream),
        #"downstream": round(downstream),
        #"fabrication_length": round(fabrication_length),
        #"installation_envelope": round(installation_envelope)
    #}

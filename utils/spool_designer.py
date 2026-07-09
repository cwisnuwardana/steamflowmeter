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

    return {

        "existing_dn": existing_dn,

        "recommended_dn": recommended_dn,

        "existing_5D": round(existing_5D),

        "reducer_length": REDUCER_LENGTH,

        "meter_length": meter_length,

        "expander_length": EXPANDER_LENGTH,

        "upstream": round(upstream),

        "downstream": round(downstream),

        "fabrication_length": round(fabrication_length),

        "installation_envelope": round(installation_envelope)

    }

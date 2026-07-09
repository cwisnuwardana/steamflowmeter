from utils.spool_designer import design_spool
from utils.hydraulic_assessment import hydraulic_assessment
from utils.pipe_lookup import get_pipe_data
from utils.installation_rules import installation_rules


def evaluate_pipe(

    result,
    existing_dn,
    selected_dn,
    pressure,
    schedule,
    disturbance

):

    # =====================================
    # PIPE OPTIMIZATION RESULT
    # =====================================

    optimization = result["pipe_optimization"]

    best = optimization.iloc[0]

    selected = optimization[
        optimization["DN"] == selected_dn
    ].iloc[0]

    # =====================================
    # PIPE DATA
    # =====================================

    pipe = get_pipe_data(
        selected["DN"],
        schedule
    )

    pipe_id = pipe["id"]

    # =====================================
    # NOMINAL PIPE DIAMETER (mm)
    # =====================================
    
    selected_dn_mm = int(
        selected["DN"].replace("DN", "")
    )
    
    existing_dn_mm = int(
        existing_dn.replace("DN", "")
    )
    
    # =====================================
    # EFFECTIVE DISTURBANCE
    # =====================================
    
    # Existing pipe unchanged
    if selected["DN"] == existing_dn:
    
        effective_disturbance = disturbance
    
    # Pipe reduction required
    else:
    
        effective_disturbance = "Reducer"
    
    rule = installation_rules[effective_disturbance]
    
    upstream_D = rule["upstream"]
    
    downstream_D = rule["downstream"]
    
    print("Existing Disturbance :", disturbance)
    print("Effective Disturbance:", effective_disturbance)
    print(rule)

    # =====================================
    # DESIGN SPOOL
    # =====================================

    spool = design_spool(

        existing_dn,

        selected["DN"],

        required_upstream,

        required_downstream,

        schedule

    )

    # =====================================
    # HYDRAULIC
    # =====================================

    hydraulic = hydraulic_assessment(

        operating_pressure_bar=pressure,

        pressure_drop_bar_per_m=selected["Pressure Drop (bar/m)"],

        spool_length_mm=spool["fabrication_length"]

    )

    # =====================================
    # VELOCITY STATUS
    # =====================================

    velocity = selected["Velocity (m/s)"]

    if 10 <= velocity <= 35:

        velocity_note = "ideal"

    elif 5 <= velocity < 10:

        velocity_note = "acceptable"

    elif 35 < velocity <= 45:

        velocity_note = "slightly high"

    else:

        velocity_note = "outside the recommended range"

    # =====================================
    # RETURN
    # =====================================

    return {
    
        "best": best,
    
        "selected": selected,
    
        "spool": spool,
    
        "hydraulic": hydraulic,
    
        "velocity_note": velocity_note,
    
        "effective_disturbance": effective_disturbance
    
    }

from utils.spool_designer import design_spool
from utils.hydraulic_assessment import hydraulic_assessment
from utils.pipe_lookup import get_pipe_data

def evaluate_pipe(

    result,

    existing_dn,

    selected_dn,

    pressure,

    schedule

):

    optimization = result["pipe_optimization"]

    best = optimization.iloc[0]
    
    selected = optimization[
        optimization["DN"] == selected_dn
    ].iloc[0]

    pipe = get_pipe_data(

        selected["DN"],
    
        schedule
    
    )

    required_upstream = pipe["id"] * 20
    
    required_downstream = pipe["id"] * 5
    
    spool = design_spool(
    
        existing_dn,
    
        selected["DN"],
    
        required_upstream,
    
        required_downstream
    
    )

    hydraulic = hydraulic_assessment(

        operating_pressure_bar=pressure,

        pressure_drop_bar_per_m=selected["Pressure Drop (bar/m)"],

        spool_length_mm=spool["total_length"]

    )

    velocity = selected["Velocity (m/s)"]

    if 10 <= velocity <= 35:
        velocity_note = "ideal"

    elif 5 <= velocity < 10:
        velocity_note = "acceptable"

    elif 35 < velocity <= 45:
        velocity_note = "slightly high"

    else:
        velocity_note = "outside the recommended range"

    return {
        
        "best": best,
        
        "selected": selected,

        "spool": spool,

        "hydraulic": hydraulic,

        "velocity_note": velocity_note

    }

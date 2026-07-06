from utils.pipe_lookup import get_pipe_data
from utils.flow_lookup import get_flow_range
from utils.steam_lookup import get_steam_property
from utils.recommendation import get_recommendation
from utils.meter_selector import recommend_meter
from utils.engineering_score import calculate_engineering_score
from utils.velocity_calculator import calculate_velocity
from utils.pipe_optimizer import optimize_pipe

import pandas as pd

# ==========================================================
# LOAD INSTALLATION RULE
# ==========================================================

installation_rules = {

    "Straight Pipe": {
        "upstream": 10,
        "downstream": 5
    },

    "Flange": {
        "upstream": 10,
        "downstream": 5
    },

    "Reducer": {
        "upstream": 15,
        "downstream": 5
    },

    "90° Elbow": {
        "upstream": 20,
        "downstream": 5
    },

    "2 × 90° Elbow": {
        "upstream": 30,
        "downstream": 5
    },

    "Valve": {
        "upstream": 35,
        "downstream": 5
    },

    "Two Elbows on Different Plane": {
        "upstream": 40,
        "downstream": 5
    }

}

# ==========================================================
# ANALYZE INSTALLATION
# ==========================================================

def analyze_installation(

    customer_steam,

    pressure,

    temperature,

    dn,

    schedule,

    actual_flow,

    disturbance,

    available_upstream,

    available_downstream

):

    # ==========================================
    # PIPE DATA
    # ==========================================

    pipe = get_pipe_data(
        dn,
        schedule
    )

    pipe_id = pipe["id"]

    # ==========================================
    # FLOW RANGE
    # ==========================================

    print("========================")
    print("Pressure :", pressure)
    print("DN :", dn)
    
    flow = get_flow_range(
        pressure,
        dn
    )
    
    if flow is None:
        raise ValueError(
            f"Flow lookup failed. Pressure={pressure}, DN={dn}"
        )     
    # ==========================================
    # STEAM PROPERTY
    # ==========================================

    steam = get_steam_property(
        pressure
    )

    # ==========================================
    # STEAM VERIFICATION
    # ==========================================

    boiling = steam["boiling_point"]

    if temperature > boiling:

        calculated_steam = "Superheated"

    else:

        calculated_steam = "Saturated"

    # ==========================================
    # INSTALLATION RULE
    # ==========================================

    rule = installation_rules[disturbance]
    
    upstream_D = rule["upstream"]
    
    downstream_D = rule["downstream"]

    required_upstream = upstream_D * pipe_id

    required_downstream = downstream_D * pipe_id

    installation_status = (
        "PASS"
        if
        available_upstream >= required_upstream
        and
        available_downstream >= required_downstream
        else
        "FAIL"
    )

    # ==========================================
    # FLOW STATUS
    # ==========================================

    if actual_flow < flow["min_flow"]:

        flow_status = "LOW"

    elif actual_flow > flow["max_flow"]:

        flow_status = "HIGH"

    else:

        flow_status = "NORMAL"

    # ==========================================
    # METER RECOMMENDATION
    # ==========================================
    
    meter = recommend_meter(
        pressure,
        actual_flow
    )

    # ==========================================
    # PIPE OPTIMIZATION
    # ==========================================
    
    pipe_optimization = optimize_pipe(
    
        pressure,
    
        actual_flow,
    
        schedule
    
    )
    
    # ==========================================
    # RECOMMENDATION
    # ==========================================

    recommendation = get_recommendation(

        customer_steam,

        calculated_steam,

        installation_status,

        actual_flow,

        flow["min_flow"],

        flow["max_flow"]

    )

    # ==========================================
    # ENGINEERING SCORE
    # ==========================================
    
    #engineering_score = calculate_engineering_score(
    
    #    customer_steam,
    
    #    calculated_steam,
    
    #    installation_status,
    
    #    flow_status
    
    #)
    
    # ==========================================
    # RETURN
    # ==========================================

    return {
    
        "pipe": pipe,
    
        "steam": steam,
    
        "flow": flow,
    
        "meter": meter,

        "engineering_score": engineering_score,
    
        "flow_status": flow_status,
    
        "customer_steam": customer_steam,
    
        "calculated_steam": calculated_steam,
    
        "installation_status": installation_status,
    
        "required_upstream": round(required_upstream,1),
    
        "required_downstream": round(required_downstream,1),
    
        "recommendation": recommendation,

        "pipe_optimization": pipe_optimization
    
    }

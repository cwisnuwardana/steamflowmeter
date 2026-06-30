from utils.pipe_lookup import get_pipe_data
from utils.flow_lookup import get_flow_range
from utils.steam_lookup import get_steam_property
from utils.recommendation import get_recommendation

import pandas as pd

# ==========================================================
# LOAD INSTALLATION RULE
# ==========================================================

installation_rules = {

    "Tee": {
        "upstream": 15,
        "downstream": 5
    },

    "90° Elbow": {
        "upstream": 20,
        "downstream": 5
    },

    "2 × 90° Elbow": {
        "upstream": 35,
        "downstream": 5
    },

    "Reducer": {
        "upstream": 20,
        "downstream": 5
    },

    "Flange": {
        "upstream": 10,
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

    flow = get_flow_range(
        pressure,
        dn
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

    row = rule_db[
        rule_db["Disturbance"] == disturbance
    ]

    row = row.iloc[0]

    upstream_D = float(
        row["Upstream_D"]
    )

    downstream_D = float(
        row["Downstream_D"]
    )

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
    # RETURN
    # ==========================================

    return {

        "pipe": pipe,

        "steam": steam,

        "flow": flow,

        "flow_status": flow_status,

        "customer_steam": customer_steam,

        "calculated_steam": calculated_steam,

        "installation_status": installation_status,

        "required_upstream": round(required_upstream,1),

        "required_downstream": round(required_downstream,1),

        "recommendation": recommendation

    }

import pandas as pd

from utils.pipe_lookup import get_pipe_data
from utils.flow_lookup import get_flow_range
from utils.steam_lookup import get_steam_property
from utils.velocity_calculator import calculate_velocity
from utils.reynolds import calculate_reynolds


# ==========================================================
# PIPE OPTIMIZATION
# ==========================================================

AVAILABLE_DN = [

    "DN25",
    "DN50",
    "DN65",
    "DN80",
    "DN100",
    "DN125",
    "DN150",
    "DN200",
    "DN250",
    "DN300"

]


def optimize_pipe(

    pressure,
    actual_flow,
    schedule

):

    steam = get_steam_property(pressure)

    density = steam["density"]

    viscosity = steam["viscosity"]

    result = []

    for dn in AVAILABLE_DN:

        try:

            pipe = get_pipe_data(
                dn,
                schedule
            )

            flow = get_flow_range(
                pressure,
                dn
            )

            velocity = calculate_velocity(

                actual_flow,

                density,

                pipe["id"]

            )

            reynolds = calculate_reynolds(

                density,

                velocity["velocity"],

                pipe["id"],

                viscosity

            )

            # =====================================
            # Flow Status
            # =====================================

            if actual_flow < flow["min_flow"]:

                flow_status = "Below Range"

                score = 0

            elif actual_flow > flow["max_flow"]:

                flow_status = "Above Range"

                score = 20

            else:

                flow_status = "Within Range"

                score = 60

            # =====================================
            # Velocity Score
            # =====================================

            v = velocity["velocity"]

            if 10 <= v <= 35:

                score += 30

            elif 5 <= v < 10:

                score += 20

            elif 35 < v <= 45:

                score += 15

            else:

                score += 5

            # =====================================
            # Reynolds Score
            # =====================================

            if reynolds["flow_regime"] == "Turbulent":

                score += 10

            result.append({

                "DN": dn,

                "Velocity (m/s)": round(
                    velocity["velocity"], 2
                ),

                "Reynolds": int(
                    reynolds["reynolds"]
                ),

                "Flow Status": flow_status,

                "Engineering Score": score

            })

        except Exception as e:

            raise e

    df = pd.DataFrame(result)

    df = df.sort_values(

        by="Engineering Score",

        ascending=False

    )

    return df

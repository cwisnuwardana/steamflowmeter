import pandas as pd

from utils.pipe_lookup import get_pipe_data
from utils.flow_lookup import get_flow_range
from utils.steam_lookup import get_steam_property
from utils.velocity_calculator import calculate_velocity
from utils.reynolds import calculate_reynolds
from utils.pressure_drop import calculate_pressure_drop


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

            #print("========================")
            #print("DN          :", dn)
            #print("Flow        :", actual_flow)
            #print("Density     :", density)
            #print("Pipe ID     :", pipe["id"])
            #print(type(actual_flow))
            #print(actual_flow)

            #new revision
            
            
            
            velocity = calculate_velocity(

                actual_flow,

                density,

                pipe["id"]

            )
            
            print("Velocity    :", velocity["velocity"])
            
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

                score = 40

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

            # =====================================
            # Pressure Drop
            # =====================================
            
            pressure_drop = calculate_pressure_drop(
            
                density,
            
                velocity["velocity"],
            
                pipe["id"],
            
                1.0,              # 1 meter spool
            
                reynolds["reynolds"]
            
            )

            # =====================================
            # Pressure Drop Score
            # =====================================
            
            dp = pressure_drop["pressure_drop_bar"]
            
            if dp < 0.02:
            
                score += 20
            
            elif dp < 0.05:
            
                score += 15
            
            elif dp < 0.10:
            
                score += 10
            
            else:
            
                score += 0
            
            # =====================================
            # RESULT
            # =====================================

            result.append({
            
                "DN": dn,
            
                "Density (kg/m³)": round(
                    density, 3
                ),
            
                "Pipe ID (mm)": round(
                    pipe["id"], 2
                ),
            
                "Actual Flow (t/h)": actual_flow,
            
                "Velocity (m/s)": round(
                    velocity["velocity"], 2
                ),
            
                "Reynolds": int(
                    reynolds["reynolds"]
                ),

                "Pressure Drop (bar/m)": round(
                    pressure_drop["pressure_drop_bar"],
                    7,
                
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

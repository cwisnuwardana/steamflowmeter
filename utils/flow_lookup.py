import pandas as pd

# ==========================================
# LOAD DATABASE
# ==========================================

flow_db = pd.read_excel(
    "data/S435_Flow_Range_Database.xlsx"
)


# ==========================================
# GET FLOW RANGE
# ==========================================

def get_flow_range(
    pressure,
    dn
):

flow_db["Pressure_MPa"] = flow_db["Pressure_MPa"].round(2)

pressure = round(float(pressure),2)

row = flow_db[
    (flow_db["Pressure_MPa"] == pressure)
    &
    (flow_db["DN"] == dn)
]

    if row.empty:
        return None

    row = row.iloc[0]

    return {

        "min_flow": float(row["Min_tph"]),

        "max_flow": float(row["Max_tph"])

    }

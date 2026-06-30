import pandas as pd

# ======================================================
# LOAD FLOW DATABASE
# ======================================================

flow_db = pd.read_excel(
    "data/S435_Flow_Range_Database.xlsx"
)

# Pastikan tipe data benar
flow_db["Pressure_MPa"] = flow_db["Pressure_MPa"].astype(float)
flow_db["DN"] = flow_db["DN"].astype(str)

# ======================================================
# GET FLOW RANGE
# ======================================================

def get_flow_range(pressure, dn):

    pressure = round(float(pressure), 1)

    row = flow_db[
        (flow_db["Pressure_MPa"].round(1) == pressure)
        &
        (flow_db["DN"].str.strip() == dn.strip())
    ]

    if row.empty:

        print("Flow Lookup Failed")
        print("Pressure :", pressure)
        print("DN :", dn)

        return None

    row = row.iloc[0]

    return {

        "min_flow": float(row["Min_tph"]),

        "max_flow": float(row["Max_tph"])

    }

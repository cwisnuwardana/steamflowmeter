import pandas as pd

# ======================================================
# LOAD FLOW DATABASE
# ======================================================

flow_db = pd.read_excel(
    "data/S435_Flow_Range_Database.xlsx"
)

flow_db.columns = flow_db.columns.str.strip()

flow_db["Pressure_MPa"] = pd.to_numeric(
    flow_db["Pressure_MPa"],
    errors="coerce"
)

flow_db["Min_tph"] = pd.to_numeric(
    flow_db["Min_tph"],
    errors="coerce"
)

flow_db["Max_tph"] = pd.to_numeric(
    flow_db["Max_tph"],
    errors="coerce"
)

flow_db["DN"] = (
    flow_db["DN"]
    .astype(str)
    .str.strip()
    .str.upper()
)

# ======================================================
# METER SELECTOR
# ======================================================

def recommend_meter(

    pressure,

    actual_flow

):

    pressure = round(float(pressure), 1)

    db = flow_db[
        abs(
            flow_db["Pressure_MPa"] - pressure
        ) < 0.001
    ].copy()

    if db.empty:

        return None

    # Urutkan dari meter terkecil

    db = db.sort_values(
        by="Min_tph"
    )

    # Cari meter yang memenuhi

    for _, row in db.iterrows():

        if (

            actual_flow >= row["Min_tph"]

            and

            actual_flow <= row["Max_tph"]

        ):

            return {

                "recommended_dn": row["DN"],

                "min_flow": float(row["Min_tph"]),

                "max_flow": float(row["Max_tph"])

            }

    return None

import pandas as pd

# ======================================================
# LOAD DATABASE
# ======================================================

flow_db = pd.read_excel("data/S435_Flow_Range_Database.xlsx")

# Rapikan Header
flow_db.columns = flow_db.columns.str.strip()

# Rapikan Data
flow_db["Pressure_MPa"] = pd.to_numeric(
    flow_db["Pressure_MPa"],
    errors="coerce"
)

flow_db["DN"] = (
    flow_db["DN"]
    .astype(str)
    .str.strip()
    .str.upper()
)

# ======================================================
# FLOW LOOKUP
# ======================================================

def get_flow_range(pressure, dn):

    pressure = round(float(pressure), 1)

    dn = str(dn).strip().upper()

    # Debug
    print("------------------------------------")
    print("INPUT PRESSURE :", pressure)
    print("INPUT DN       :", dn)

    # Filter Pressure
    db = flow_db.copy()

    db = db[
        abs(db["Pressure_MPa"] - pressure) < 0.001
    ]

    print("Row after Pressure Filter :", len(db))

    # Filter DN
    db = db[
        db["DN"] == dn
    ]

    print("Row after DN Filter :", len(db))

    if db.empty:

        print(flow_db)

        raise ValueError(
            "Flow Database Lookup Failed"
        )

    row = db.iloc[0]

    return {

        "min_flow": float(row["Min_tph"]),

        "max_flow": float(row["Max_tph"])

    }

import pandas as pd

# ======================================================
# LOAD FLOW DATABASE
# ======================================================

flow_db = pd.read_excel(
    "data/S435_Flow_Range_Database.xlsx"
)

# ======================================================
# CLEAN DATABASE
# ======================================================

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
# GET FLOW RANGE
# ======================================================

def get_flow_range(
    pressure,
    dn
):

    pressure = float(pressure)

    dn = str(dn).strip().upper()

    # ==========================================
    # Cari pressure terdekat
    # ==========================================

    nearest_pressure = min(
        flow_db["Pressure_MPa"].dropna().unique(),
        key=lambda x: abs(x - pressure)
    )

    # ==========================================
    # Filter
    # ==========================================

    row = flow_db[
        (flow_db["Pressure_MPa"] == nearest_pressure)
        &
        (flow_db["DN"] == dn)
    ]

    if row.empty:

        return None

    row = row.iloc[0]

    return {

        "pressure_used": nearest_pressure,

        "dn": dn,

        "min_flow": float(row["Min_tph"]),

        "max_flow": float(row["Max_tph"])

    }

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
# METER COMPARISON
# ======================================================

def compare_meters(
    pressure,
    actual_flow
):

    pressure = float(pressure)

    actual_flow = float(actual_flow)

    # ==========================================
    # Nearest Pressure
    # ==========================================

    nearest_pressure = min(
        flow_db["Pressure_MPa"].dropna().unique(),
        key=lambda x: abs(x-pressure)
    )

    db = flow_db[
        flow_db["Pressure_MPa"] == nearest_pressure
    ].copy()

    db = db.sort_values(
        by="Min_tph"
    )

    result = []

    for _, row in db.iterrows():

        if actual_flow < row["Min_tph"]:

            status = "🔴 Too Large"

        elif actual_flow > row["Max_tph"]:

            status = "🟠 Too Small"

        else:

            status = "🟢 Recommended"

        utilization = round(
            actual_flow / row["Max_tph"] * 100,
            1
        )

        result.append({

            "Meter": row["DN"],

            "Min Flow (t/h)": row["Min_tph"],

            "Max Flow (t/h)": row["Max_tph"],

            "Actual Flow (t/h)": actual_flow,

            "Utilization (%)": utilization,

            "Status": status

        })

    return pd.DataFrame(result)

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
# METER COMPARISON
# ======================================================

def compare_meters(pressure, actual_flow):

    pressure = float(pressure)
    actual_flow = float(actual_flow)

    # Cari pressure terdekat
    nearest_pressure = min(
        flow_db["Pressure_MPa"].dropna().unique(),
        key=lambda x: abs(x - pressure)
    )

    db = flow_db[
        flow_db["Pressure_MPa"] == nearest_pressure
    ].copy()

    db = db.sort_values(
        by="Min_tph"
    )

    result = []

    for _, row in db.iterrows():

        utilization = round(
            actual_flow / row["Max_tph"] * 100,
            1
        )

        if actual_flow < row["Min_tph"]:

            status = "🔴 Oversized"
            note = "Actual flow below minimum measurable range."

        elif utilization < 20:

            status = "🟡 Acceptable"
            note = "Measurement possible but low utilization."

        elif utilization < 80:

            status = "🟢 Recommended"
            note = "Good measuring range."

        else:

            status = "🟠 Near Maximum"
            note = "Close to maximum measuring range."

        result.append({

            "Meter": row["DN"],

            "Min Flow (t/h)": round(row["Min_tph"], 2),

            "Max Flow (t/h)": round(row["Max_tph"], 2),

            "Actual Flow (t/h)": round(actual_flow, 2),

            "Utilization (%)": utilization,

            "Status": status,

            "Engineering Note": note

        })

    return pd.DataFrame(result)

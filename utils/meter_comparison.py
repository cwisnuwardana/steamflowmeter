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

    nearest_pressure = min(
        flow_db["Pressure_MPa"].dropna().unique(),
        key=lambda x: abs(x - pressure)
    )

    db = flow_db[
        flow_db["Pressure_MPa"] == nearest_pressure
    ].copy()

    db = db.sort_values(by="Min_tph")

    result = []

    for _, row in db.iterrows():

        utilization = round(
            actual_flow / row["Max_tph"] * 100,
            1
        )

        if actual_flow < row["Min_tph"]:

            status = "🔴 Oversized"
            note = "Actual flow is below the minimum measurable flow."

        elif actual_flow <= row["Max_tph"]:

            if utilization >= 60:

                status = "🟢 Best Choice"
                note = "Excellent measuring range."

            elif utilization >= 30:

                status = "🟢 Recommended"
                note = "Good measuring range."

            else:

                status = "🟢 Recommended"
                note = "Flow is inside measuring range. Low utilization but acceptable."

        else:

            status = "🟠 Undersized"
            note = "Actual flow exceeds maximum measurable flow."

        result.append({

            "Meter": row["DN"],

            "Min Flow (t/h)": round(row["Min_tph"], 3),

            "Max Flow (t/h)": round(row["Max_tph"], 3),

            "Actual Flow (t/h)": round(actual_flow, 3),

            "Utilization (%)": utilization,

            "Status": status,

            "Engineering Note": note

        })

    return pd.DataFrame(result)

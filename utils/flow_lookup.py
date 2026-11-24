import pandas as pd

# ======================================================
# LOAD FLOW DATABASE
# ======================================================

flow_db = pd.read_excel("data/S435_Flow_Range_Database.xlsx", sheet_name="Flow_Range")

required_columns = {"Pressure_MPa", "DN", "Min_tph", "Max_tph"}
missing_columns = required_columns - set(flow_db.columns)
if missing_columns:
    raise ValueError(
        "S435 flow database is missing required columns: "
        + ", ".join(sorted(missing_columns))
    )

flow_db.columns = flow_db.columns.str.strip()
for column in ["Pressure_MPa", "Min_tph", "Max_tph"]:
    flow_db[column] = pd.to_numeric(flow_db[column], errors="coerce")

flow_db["DN"] = flow_db["DN"].astype(str).str.strip().str.upper()
flow_db = flow_db.dropna(subset=["Pressure_MPa", "DN", "Min_tph", "Max_tph"])

if flow_db.empty:
    raise ValueError("S435 flow database contains no valid flow-range records.")

# ======================================================
# GET FLOW RANGE
# ======================================================

def get_flow_range(pressure, dn):
    pressure = float(pressure)
    dn = str(dn).strip().upper()

    available_pressures = sorted(flow_db["Pressure_MPa"].unique())
    if not available_pressures:
        raise ValueError("No pressure values are available in the S435 flow database.")

    nearest_pressure = min(available_pressures, key=lambda x: abs(x - pressure))

    # Do not silently use a distant pressure row.
    if abs(nearest_pressure - pressure) > 0.051:
        raise ValueError(
            f"Pressure {pressure:.2f} MPa is outside the flow database coverage "
            f"({min(available_pressures):.2f}–{max(available_pressures):.2f} MPa)."
        )

    row = flow_db[
        (flow_db["Pressure_MPa"].sub(nearest_pressure).abs() < 1e-6)
        & (flow_db["DN"] == dn)
    ]

    if row.empty:
        available_dn = sorted(
            flow_db.loc[
                flow_db["Pressure_MPa"].sub(nearest_pressure).abs() < 1e-6, "DN"
            ].unique()
        )
        raise ValueError(
            f"No flow-range record for {dn} at {nearest_pressure:.2f} MPa. "
            f"Available DN: {', '.join(available_dn) or 'none'}."
        )

    row = row.iloc[0]
    return {
        "pressure_used": float(nearest_pressure),
        "dn": dn,
        "min_flow": float(row["Min_tph"]),
        "max_flow": float(row["Max_tph"]),
    }

import pandas as pd

flow_db = pd.read_excel("data/S435_Flow_Range_Database.xlsx")

# Rapikan data
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

def get_flow_range(pressure, dn):

    pressure = round(float(pressure), 1)
    dn = str(dn).strip().upper()

    # Toleransi floating point
    row = flow_db[
        (abs(flow_db["Pressure_MPa"] - pressure) < 0.0001)
        &
        (flow_db["DN"] == dn)
    ]

    if row.empty:

        raise ValueError(
            f"""
Flow lookup failed

Pressure Input : {pressure}

DN Input : {dn}

Available Pressure :
{flow_db['Pressure_MPa'].unique()}

Available DN :
{flow_db['DN'].unique()}
"""
        )

    row = row.iloc[0]

    return {

        "min_flow": float(row["Min_tph"]),

        "max_flow": float(row["Max_tph"])

    }

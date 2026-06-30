import pandas as pd

# ==========================================
# LOAD DATABASE
# ==========================================

steam_db = pd.read_excel(
    "data/steam_table.xlsx"
)


# ==========================================
# GET STEAM PROPERTY
# ==========================================

def get_steam_property(
    pressure,
    temperature
):

    row = steam_db[
        (steam_db["Pressure"] == pressure)
        &
        (steam_db["Temperature"] == temperature)
    ]

    if row.empty:
        return None

    row = row.iloc[0]

    return {

        "density": row["Density"],

        "specific_volume": row["Specific Volume"],

        "enthalpy": row["Enthalpy"],

        "entropy": row["Entropy"]

    }

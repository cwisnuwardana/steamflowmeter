import pandas as pd

# =====================================
# LOAD DATABASE
# =====================================

steam_db = pd.read_excel(
    "data/steam_table.xlsx"
)


# =====================================
# GET STEAM PROPERTY
# =====================================

def get_steam_property(pressure):

    row = steam_db[
        steam_db["Absolute Pressure"] == pressure
    ]

    if row.empty:
        return None

    row = row.iloc[0]

    return {

        "boiling_point":
            float(row["Boiling Point"]),

        "specific_volume":
            float(row["Specific Volume (steam)"]),

        "density":
            float(row["Density (steam)"]),

        "enthalpy":
            float(row["Specific Enthalpy of Steam"]),

        "latent_heat":
            float(row["Latent heat of Vaporization"]),

        "specific_heat":
            float(row["Specific Heat"])

    }

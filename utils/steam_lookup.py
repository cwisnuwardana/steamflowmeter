import pandas as pd

# ==========================================================
# LOAD STEAM TABLE
# ==========================================================

steam_db = pd.read_excel(
    "data/steam_table.xlsx",
    skiprows=4,
    header=None
)

steam_db.columns = [

    "Pressure",

    "Boiling_Point",

    "Specific_Volume",

    "Density",

    "Liquid_Enthalpy_kJ",

    "Liquid_Enthalpy_kcal",

    "Steam_Enthalpy_kJ",

    "Steam_Enthalpy_kcal",

    "Latent_Heat_kJ",

    "Latent_Heat_kcal",

    "Specific_Heat",

    "Dynamic_Viscosity_Pa_s"

]


# ==========================================================
# GET STEAM PROPERTY
# ==========================================================

def get_steam_property(pressure):

    row = steam_db[
        steam_db["Pressure"] == pressure
    ]

    if row.empty:
        return None

    row = row.iloc[0]

    return {
    
        "boiling_point": float(row["Boiling_Point"]),
    
        "specific_volume": float(row["Specific_Volume"]),
    
        "density": float(row["Density"]),
    
        "enthalpy": float(row["Steam_Enthalpy_kJ"]),
    
        "latent_heat": float(row["Latent_Heat_kJ"]),
    
        "specific_heat": float(row["Specific_Heat"]),
    
        "viscosity": float(row["Dynamic_Viscosity_Pa_s"])
    
    }

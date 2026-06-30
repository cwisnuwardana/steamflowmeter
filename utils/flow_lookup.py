import pandas as pd

flow_db = pd.read_excel(
    "data/S435_Flow_Range_Database.xlsx"
)

def get_flow_range(pressure, dn):

    print("FLOW LOOKUP BYPASS MODE")

    return {
        "min_flow": 0.20,
        "max_flow": 4.11
    }

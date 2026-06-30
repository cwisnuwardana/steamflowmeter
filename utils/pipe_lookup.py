import pandas as pd

# ============================================
# LOAD PIPE DATABASE
# ============================================

pipe_db = pd.read_excel("data/pipe_database.xlsx")


# ============================================
# GET PIPE DATA
# ============================================

def get_pipe_data(dn, schedule):

    row = pipe_db[
        (pipe_db["DN"] == dn)
    ]

    if row.empty:
        return None

    row = row.iloc[0]

    od = float(row["OD"])

    thickness = float(row[schedule])

    pipe_id = od - (2 * thickness)

    return {

        "DN": dn,

        "OD": od,

        "Thickness": thickness,

        "ID": round(pipe_id,2)

    }

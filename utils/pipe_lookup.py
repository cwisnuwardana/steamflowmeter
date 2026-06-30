import pandas as pd

# ===================================================
# LOAD PIPE DATABASE
# ===================================================

pipe_db = pd.read_excel(
    "data/pipe_database.xlsx"
)


# ===================================================
# GET PIPE DATA
# ===================================================

def get_pipe_data(
    dn,
    schedule
):

    # -----------------------------------------

    dn_number = int(
        dn.replace(
            "DN",
            ""
        )
    )

    # -----------------------------------------

    row = pipe_db[
        pipe_db["DN"] == dn_number
    ]

    if row.empty:
        return None

    row = row.iloc[0]

    od = float(
        row["OD"]
    )

    thickness = row[schedule]

    if pd.isna(thickness):

        return None

    thickness = float(
        thickness
    )

    pipe_id = od - (2 * thickness)

    return {

        "dn": dn,

        "od": round(
            od,
            2
        ),

        "thickness": round(
            thickness,
            2
        ),

        "id": round(
            pipe_id,
            2
        )

    }

# ==========================================================
# HYDRAULIC ASSESSMENT
# SUTO S435 Engineering Assistant
# ==========================================================

def hydraulic_assessment(

    operating_pressure_bar,
    pressure_drop_bar_per_m,
    spool_length_mm

):

    # ==========================================
    # mm → m
    # ==========================================

    spool_length_m = spool_length_mm / 1000

    # ==========================================
    # TOTAL PRESSURE DROP
    # ==========================================

    total_pressure_drop = (
        pressure_drop_bar_per_m
        * spool_length_m
    )

    # ==========================================
    # PRESSURE LOSS RATIO
    # ==========================================

    if operating_pressure_bar > 0:

        loss_ratio = (
            total_pressure_drop
            / operating_pressure_bar
        ) * 100

    else:

        loss_ratio = 0

    # ==========================================
    # HYDRAULIC STATUS
    # ==========================================

    if loss_ratio < 0.5:

        status = "Negligible"

    elif loss_ratio < 2:

        status = "Acceptable"

    elif loss_ratio < 5:

        status = "Consider Review"

    else:

        status = "Not Recommended"

    # ==========================================
    # ENGINEERING COMMENT
    # ==========================================

    if status == "Negligible":

        comment = (
            "Estimated pressure loss is negligible and "
            "will not significantly affect the steam distribution system."
        )

    elif status == "Acceptable":

        comment = (
            "Pressure loss is acceptable for normal steam service."
        )

    elif status == "Consider Review":

        comment = (
            "Pressure loss is moderate. Hydraulic review is recommended."
        )

    else:

        comment = (
            "Pressure loss is considered high. "
            "Pipe sizing should be re-evaluated."
        )

    # ==========================================
    # RETURN
    # ==========================================

    return {

        "pressure_drop_per_meter": pressure_drop_bar_per_m,

        "spool_length_m": spool_length_m,

        "total_pressure_drop": total_pressure_drop,

        "loss_ratio": loss_ratio,

        "status": status,

        "comment": comment

    }

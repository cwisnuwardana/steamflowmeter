import math

# ==========================================================
# PRESSURE DROP (Darcy-Weisbach)
# ==========================================================

def calculate_pressure_drop(

    density,
    velocity,
    diameter_mm,
    length_m,
    reynolds

):

    # ==========================================
    # mm → m
    # ==========================================

    diameter = diameter_mm / 1000

    # ==========================================
    # Friction Factor
    # ==========================================

    if reynolds < 2300:

        # Laminar
        friction_factor = 64 / reynolds

    else:

        # Blasius Correlation
        friction_factor = 0.3164 / (reynolds ** 0.25)

    # ==========================================
    # Darcy-Weisbach
    # ==========================================

    pressure_drop_pa = (

        friction_factor

        * (length_m / diameter)

        * (density * velocity**2 / 2)

    )

    pressure_drop_kpa = pressure_drop_pa / 1000

    pressure_drop_bar = pressure_drop_pa / 100000

    return {

        "friction_factor": round(friction_factor, 5),

        "pressure_drop_pa": round(
            pressure_drop_pa, 2
        ),

        "pressure_drop_kpa": round(
            pressure_drop_kpa, 3
        ),

        "pressure_drop_bar": round(
            pressure_drop_bar, 5
        )

    }

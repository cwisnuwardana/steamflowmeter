# ==========================================================
# REYNOLDS NUMBER CALCULATOR
# SUTO S435 Engineering Assistant
# ==========================================================

def calculate_reynolds(

    density,
    velocity,
    pipe_id_mm,
    viscosity

):

    # Pipe ID
    diameter = pipe_id_mm / 1000

    # Reynolds Number
    reynolds = (
        density
        * velocity
        * diameter
        / viscosity
    )

    # Flow Regime
    if reynolds < 2300:

        regime = "Laminar"

    elif reynolds < 4000:

        regime = "Transition"

    else:

        regime = "Turbulent"

    return {

        "reynolds": round(reynolds, 0),

        "flow_regime": regime

    }

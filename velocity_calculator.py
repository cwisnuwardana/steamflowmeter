import math

# ==========================================
# STEAM VELOCITY
# ==========================================

def calculate_velocity(

    flow_tph,

    density,

    pipe_id_mm

):

    # ton/h → kg/s
    mass_flow = flow_tph * 1000 / 3600

    # mm → m
    diameter = pipe_id_mm / 1000

    area = math.pi * diameter**2 / 4

    velocity = mass_flow / (density * area)

    return {

        "velocity": round(velocity, 2),

        "area": round(area, 6),

        "mass_flow": round(mass_flow, 4)

    }

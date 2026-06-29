from data.pipe_database import pipe_data
from data.installation_rules import installation_rules


def analyze_installation(
    dn,
    disturbance,
    upstream,
    downstream,
    steam_condition
):

    pipe = pipe_data[dn]

    pipe_id = pipe["id"]

    rule = installation_rules[disturbance]

    required_up = pipe_id * rule["upstream"]
    required_down = pipe_id * rule["downstream"]

    status = (
        "PASS"
        if upstream >= required_up and downstream >= required_down
        else "FAIL"
    )

    recommendation = (
        "Installation complies with SUTO recommendation."
        if status == "PASS"
        else f"Increase upstream straight pipe to at least {required_up:.0f} mm."
    )

    return {

        "steam_state":
            "Superheated"
            if steam_condition == "Superheated Steam"
            else "Saturated",

        "status": status,

        "required_up": required_up,

        "required_down": required_down,

        "recommendation": recommendation,

        "image": rule["image"]
    }

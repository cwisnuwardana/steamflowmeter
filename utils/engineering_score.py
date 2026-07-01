# ======================================================
# ENGINEERING SCORE
# ======================================================

def calculate_engineering_score(

    customer_steam,

    calculated_steam,

    installation_status,

    flow_status

):

    score = 0

    detail = {}

    # ==========================================
    # Steam Verification (30)
    # ==========================================

    if customer_steam == calculated_steam:

        steam_score = 30

    else:

        steam_score = 10

    score += steam_score

    detail["Steam"] = steam_score

    # ==========================================
    # Installation (30)
    # ==========================================

    if installation_status == "PASS":

        install_score = 30

    else:

        install_score = 0

    score += install_score

    detail["Installation"] = install_score

    # ==========================================
    # Flow Range (40)
    # ==========================================

    if flow_status == "NORMAL":

        flow_score = 40

    elif flow_status == "LOW":

        flow_score = 15

    else:

        flow_score = 10

    score += flow_score

    detail["Flow"] = flow_score

    # ==========================================
    # Overall Status
    # ==========================================

    if score >= 90:

        status = "🟢 Excellent"

    elif score >= 75:

        status = "🟢 Good"

    elif score >= 60:

        status = "🟡 Fair"

    else:

        status = "🔴 Needs Improvement"

    return {

        "score": score,

        "status": status,

        "detail": detail

    }

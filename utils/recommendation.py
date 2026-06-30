# ==========================================================
# S435 ENGINEERING RECOMMENDATION ENGINE
# ==========================================================

def get_recommendation(
    customer_steam,
    calculated_steam,
    installation_status,
    actual_flow,
    min_flow,
    max_flow
):

    recommendations = []

    warnings = []

    overall = "PASS"

    severity = "LOW"

    # ======================================================
    # STEAM VERIFICATION
    # ======================================================

    if customer_steam != calculated_steam:

        warnings.append(
            "Customer steam condition does not match engineering calculation."
        )

        recommendations.append(
            "Verify steam condition using pressure and temperature measurement."
        )

        overall = "REVIEW"

        severity = "MEDIUM"

    # ======================================================
    # FLOW RANGE VERIFICATION
    # ======================================================

    if actual_flow < min_flow:

        warnings.append(
            "Operating flow is below minimum measuring range."
        )

        recommendations.append(
            "Current operating flow is below the minimum measurable flow."
        )

        recommendations.append(
            "Consider reducing spool diameter or selecting a smaller flowmeter."
        )

        recommendations.append(
            "If low flow only occurs during start-up, verify normal operating flow before resizing."
        )

        overall = "NOT RECOMMENDED"

        severity = "HIGH"

    elif actual_flow > max_flow:

        warnings.append(
            "Operating flow exceeds maximum measuring range."
        )

        recommendations.append(
            "Consider selecting a larger flowmeter size."
        )

        overall = "NOT RECOMMENDED"

        severity = "HIGH"

    # ======================================================
    # INSTALLATION CHECK
    # ======================================================

    if installation_status == "FAIL":

        warnings.append(
            "Straight pipe requirement is not fulfilled."
        )

        recommendations.append(
            "Increase upstream and downstream straight pipe length according to SUTO installation guideline."
        )

        if severity != "HIGH":
            severity = "MEDIUM"

        if overall == "PASS":
            overall = "REVIEW"

    # ======================================================
    # ALL PASS
    # ======================================================

    if len(recommendations) == 0:

        recommendations.append(
            "Installation complies with SUTO Engineering Guideline."
        )

        recommendations.append(
            "Current operating condition is within the recommended measuring range."
        )

    # ======================================================
    # RETURN
    # ======================================================

    return {

        "overall": overall,

        "severity": severity,

        "warnings": warnings,

        "recommendations": recommendations

    }

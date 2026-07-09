import streamlit as st
from PIL import Image
from utils.meter_comparison import compare_meters
from utils.installation_note import notes
from utils.spool_designer import design_spool
from utils.svg_spool import generate_svg_spool
from utils.spool_designer import design_spool
from utils.hydraulic_assessment import hydraulic_assessment
from utils.evaluation_engine import evaluate_pipe
from my_footer import *
from modules.progress import *
import os

from utils.analyzer import analyze_installation

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="SUTO S435 Engineering Assistant",
    page_icon="💨",
    layout="wide"
)

# ==========================================================
# ASSET
# ==========================================================

LOGO = "assets/suto_logo.png"
PRODUCT = "assets/S435.png"

# ==========================================================
# HEADER
# ==========================================================

col1, col2 = st.columns([1,5])

with col1:

    if os.path.exists(LOGO):
        st.image(LOGO, width=170)

with col2:

    st.title("S435 Steam Flowmeter Engineering Assistant")

    st.caption(
        "Engineering Verification • Installation Assessment • Flow Range Evaluation"
    )

st.divider()

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("Engineering Input")

company = st.sidebar.text_input(
    "Company",
    placeholder="PT Suto iTec Indonesia"
)

project = st.sidebar.text_input(
    "Steam Monitoring",
    placeholder="Steam Flowmeter Installation"
)

engineer = st.sidebar.text_input(
    "Engineer",
    placeholder="Cahyadi"
)

st.sidebar.divider()

st.sidebar.subheader("Customer Operating Data")

steam_condition = st.sidebar.radio(

    "Steam Condition (Customer Statement)",

    [
        "Saturated",
        "Superheated"
    ]

)

pressure = st.sidebar.number_input(

    "Pressure (MPa)",

    min_value=0.02,

    max_value=1.60,

    value=0.60,

    step=0.10

)

temperature = st.sidebar.number_input(

    "Temperature (°C)",

    min_value=0.0,

    value=147.0,

    step=1.0

)

dn = st.sidebar.selectbox(

    "Pipe Size",

    [
        "DN25",
        "DN40",
        "DN50",
        "DN65",
        "DN80",
        "DN100",
        "DN125",
        "DN150",
        "DN200",
        "DN250",
        "DN300"
    ]

)

schedule = st.sidebar.selectbox(

    "Pipe Schedule",

    [
        "SCH10",
        "SCH20",
        "SCH40",
        "SCH60",
        "SCH80",
        "SCH100",
        "SCH120",
        "SCH140",
        "SCH160"
    ]

)

actual_flow = st.sidebar.number_input(

    "Actual Steam Flow (t/h)",

    min_value=0.00,

    value=0.1,

    step=0.01

)

disturbance = st.sidebar.selectbox(

    "Nearest Upstream Disturbance",

    [
        "Straight Pipe",

        "Flange",

        "Reducer",

        "90° Elbow",

        "2 × 90° Elbow",

        "Valve",

        "Two Elbows on Different Plane"
    ]

)

upstream = st.sidebar.number_input(

    "Available Upstream Length (mm)",

    value=2500

)

downstream = st.sidebar.number_input(

    "Available Downstream Length (mm)",

    value=1000

)

st.sidebar.divider()

generate = st.sidebar.button(

    "🚀 Generate Engineering Analysis",

    use_container_width=True

)

# ==========================================================
# PRODUCT IMAGE
# ==========================================================

if os.path.exists(PRODUCT):

    st.image(PRODUCT, width=260)

# ==========================================================
# RESULT
# ==========================================================

if "result" not in st.session_state:
    st.session_state.result = None

if "comparison" not in st.session_state:
    st.session_state.comparison = None

if generate:

    st.session_state.result = analyze_installation(

        customer_steam=steam_condition,

        pressure=pressure,

        temperature=temperature,

        dn=dn,

        schedule=schedule,

        actual_flow=actual_flow,

        disturbance=disturbance,

        available_upstream=upstream,

        available_downstream=downstream

    )
    st.session_state.comparison = compare_meters(

        pressure,

        actual_flow

    )

result = st.session_state.result
comparison = st.session_state.comparison

# ==========================================================
# INSTALLATION IMAGE MAP
# ==========================================================

image_map = {

    "Straight Pipe": "assets/pipe_installation/straight.png",

    "Flange": "assets/pipe_installation/flange.png",

    "Reducer": "assets/pipe_installation/reducer.png",

    "90° Elbow": "assets/pipe_installation/elbow90.png",

    "2 × 90° Elbow": "assets/pipe_installation/elbow90x2.png",

    "Valve": "assets/pipe_installation/valve.png",

    "Two Elbows on Different Plane": "assets/pipe_installation/two_plane.png"

}

# ==========================================================
# TAB
# ==========================================================

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(

    [
        "📊 Summary",
        "📐 Pipe",
        "🔥 Steam",
        "📈 Flow",
        "📏 Installation",
        "⚙ Pipe Optimization",
        "💡 Recommendation",
        "📚 Methodology",
        "📊 Meter Comparison"
    ]

)
# ==========================================================
# TAB Summary
# ==========================================================
with tab1:

    st.header("Engineering Summary")

    if result is None:

        st.info("Click **Generate Engineering Analysis**")

    else:

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Customer Statement",
                result["customer_steam"]
            )

            st.metric(
                "Calculated Steam",
                result["calculated_steam"]
            )

        with col2:

            st.metric(
                "Installation",
                result["installation_status"]
            )

            st.metric(
                "Flow Status",
                result["flow_status"]
            )

        with col3:

            st.metric(
                "Min Flow",
                f'{result["flow"]["min_flow"]:.2f} t/h'
            )

            st.metric(
                "Max Flow",
                f'{result["flow"]["max_flow"]:.2f} t/h'
            )

        st.success(result["recommendation"])

with tab2:

    st.header("📐 Pipe Information")

    if result:

        pipe = result["pipe"]

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Pipe Size", pipe["dn"])

        with col2:
            st.metric("Outside Diameter", f'{pipe["od"]:.2f} mm')

        with col3:
            st.metric("Wall Thickness", f'{pipe["thickness"]:.2f} mm')

        with col4:
            st.metric("Inside Diameter", f'{pipe["id"]:.2f} mm')

with tab3:

    st.header("🔥 Steam Property")

    if result:

        steam = result["steam"]

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Boiling Point",
                f'{steam["boiling_point"]:.2f} °C'
            )

            st.metric(
                "Density",
                f'{steam["density"]:.3f} kg/m³'
            )

        with col2:

            st.metric(
                "Specific Volume",
                f'{steam["specific_volume"]:.3f} m³/kg'
            )

            st.metric(
                "Specific Heat",
                f'{steam["specific_heat"]:.3f} kJ/kg·K'
            )

        with col3:

            st.metric(
                "Steam Enthalpy",
                f'{steam["enthalpy"]:.1f} kJ/kg'
            )

            st.metric(
                "Latent Heat",
                f'{steam["latent_heat"]:.1f} kJ/kg'
            )

    else:

        st.info(
            "Click **Generate Engineering Analysis**"
        )

with tab4:

    st.header("📈 Flow Range")

    if result:

        flow = result["flow"]

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Pressure Used",
                f'{flow["pressure_used"]:.2f} MPa'
            )

        with col2:

            st.metric(
                "Minimum Flow",
                f'{flow["min_flow"]:.3f} t/h'
            )

        with col3:

            st.metric(
                "Maximum Flow",
                f'{flow["max_flow"]:.3f} t/h'
            )

    else:

        st.info(
            "Click **Generate Engineering Analysis**"
        )
        
with tab5:

    st.header("📏 Installation Assessment")

    if result:

        # ==========================================
        # Reference Installation Drawing
        # ==========================================

        image_path = image_map.get(disturbance)

        if image_path and os.path.exists(image_path):

            st.image(
                image_path,
                caption=f"Reference Installation - {disturbance}",
                use_container_width=True
            )

        st.divider()

        # ==========================================
        # Installation Requirement
        # ==========================================

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Required Upstream",
                f'{result["required_upstream"]:.0f} mm'
            )

            st.metric(
                "Available Upstream",
                f"{upstream:.0f} mm"
            )

        with col2:

            st.metric(
                "Required Downstream",
                f'{result["required_downstream"]:.0f} mm'
            )

            st.metric(
                "Available Downstream",
                f"{downstream:.0f} mm"
            )

        st.divider()

        # ==========================================
        # Installation Status
        # ==========================================

        if result["installation_status"] == "PASS":

            st.success(
                "✅ Installation complies with the SUTO installation recommendation."
            )

        else:

            st.error(
                "❌ Installation does NOT comply with the minimum straight pipe requirement."
            )

        st.divider()

        # ==========================================
        # Engineering Guidance
        # ==========================================

        st.subheader(
            notes[disturbance]["title"]
        )

        st.info(
            notes[disturbance]["note"]
        )

    else:

        st.info(
            "Click **Generate Engineering Analysis**"
        )

with tab6:

    st.header("⚙ Pipe Optimization")

    if result:

        optimization = result["pipe_optimization"]

        selected_dn = st.radio(
            "🛠 Engineering Evaluation",
            optimization["DN"].tolist(),
            horizontal=True,
            key="selected_dn"
        )
                
        # ===============================
        # BEST PIPE
        # ===============================

        #best = optimization.iloc[0]
        
        #selected = optimization[
        #    optimization["DN"] == selected_dn
        #].iloc[0]

        #best = optimization.iloc[0]

        #selected = best
        
        #col1, col2, col3, col4, col5 = st.columns(5)

        #with col1:
        #    st.metric("🏆 Recommended", best["DN"])
        
        #with col2:
        #    st.metric("🔧 Evaluated", selected["DN"])
        
        #with col3:
        #    st.metric("Score", selected["Engineering Score"])
        
        #with col4:
        #    st.metric("Velocity", f'{selected["Velocity (m/s)"]:.2f} m/s')
        
        #with col5:
        #    st.metric("Flow Status", selected["Flow Status"])
        # ==========================================
        # ENGINEERING INTERPRETATION
        # ==========================================
        
        #velocity = selected["Velocity (m/s)"]
        
        #if 10 <= velocity <= 35:
        #    velocity_note = "ideal"
        
        #elif 5 <= velocity < 10:
        #    velocity_note = "acceptable"
        
        #elif 35 < velocity <= 45:
        #    velocity_note = "slightly high"
        
        #else:
        #    velocity_note = "outside the recommended range"

        # ===============================
        # ENGINEERING EVALUATION Rev 7/7
        # ===============================
        
        evaluation = evaluate_pipe(
        
            result,
        
            dn,
        
            selected_dn,
        
            pressure,

            schedule,

            disturbance
        
        )
        
        best = evaluation["best"]
        
        selected = evaluation["selected"]
        
        spool = evaluation["spool"]
        
        hydraulic = evaluation["hydraulic"]
        
        velocity_note = evaluation["velocity_note"]
        
        
        # ===============================
        # METRICS
        # ===============================
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        with col1:
            st.metric("🏆 Recommended", best["DN"])
        
        with col2:
            st.metric("🔧 Evaluated", selected["DN"])
        
        with col3:
            st.metric("Score", selected["Engineering Score"])
        
        with col4:
            st.metric(
                "Velocity",
                f'{selected["Velocity (m/s)"]:.2f} m/s'
            )
        
        with col5:
            st.metric(
                "Flow Status",
                selected["Flow Status"]
            )
        
        conclusion = f"""
        ### ✅ Engineering Evaluation

        **Software Recommendation : {best["DN"]}**

        **Current Engineering Evaluation : {selected["DN"]}**
        
        The selected pipe size **{selected["DN"]}** has been evaluated for the current operating condition.
        
        • Steam velocity = **{selected["Velocity (m/s)"]:.2f} m/s**, classified as **{velocity_note}**, which falls within the recommended operating velocity range (10–35 m/s) for vortex flow measurement.
        
        • Reynolds number = **{selected["Reynolds"]:,}**, indicating fully turbulent flow and ensuring stable vortex shedding.
        
        • Engineering Score = **{selected["Engineering Score"]}/100**.
        
        • Based on the hydraulic and flow analysis, **{selected["DN"]}** is considered technically suitable for evaluation under the current operating condition.
        """
        
        st.success(conclusion)
        
        st.subheader("📐 Installation Layout")
        
        # ======================================
        # GET SPOOL DATA
        # ======================================
        
        #spool = design_spool(
        
        #    dn,                    # Existing pipe
        
        #    selected["DN"],        # Pipe yang sedang dievaluasi
        
        #    result["required_upstream"],
        
        #    result["required_downstream"]
        
        #)

        #hydraulic = hydraulic_assessment(

        #    operating_pressure_bar=pressure,
        
        #    pressure_drop_bar_per_m=selected["Pressure Drop (bar/m)"],
        
        #    spool_length_mm=spool["fabrication_length"]
        
        #)
        
        # ======================================
        # DRAW SVG
        # ======================================
        print(spool)
        svg = generate_svg_spool(spool)
        
        st.components.v1.html(
            svg,
            height=380,
            scrolling=False
        )
        
        # ======================================
        # SHOW DIMENSIONS
        # ======================================
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:

            st.metric(
                "Inlet Straight Pipe",
                f'{spool["existing_5D"]:.0f} mm'
            )
        
            st.metric(
                "Reducer",
                f'{spool["reducer_length"]:.0f} mm'
            )        
        with col2:

            st.metric(
                "Reducer → S435",
                f'{spool["upstream"]:.0f} mm'
            )
        
            st.metric(
                "S435",
                f'{spool["meter_length"]:.0f} mm'
            )
        
        with col3:

            st.metric(
                "S435 → Expander",
                f'{spool["downstream"]:.0f} mm'
            )
        
            st.metric(
                "Expander",
                f'{spool["expander_length"]:.0f} mm'
            )

        with col4:

            st.metric(
                "Outlet Straight Pipe",
                f'{spool["existing_5D"]:.0f} mm'
            )
        
            st.metric(
                "Installation Envelope",
                f'{spool["installation_envelope"]:.0f} mm'
            )
            
        # ======================================
        # Hydraulic Assessment
        # ======================================
        
        st.subheader("💧 Hydraulic Assessment")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "Pressure Drop Rate",
                f'{hydraulic["pressure_drop_per_meter"]:.6f} bar/m'
            )
        
        with col2:
            st.metric(
                "Estimated Total Pressure Drop",
                f'{hydraulic["total_pressure_drop"]:.4f} bar'
            )
        
        with col3:
            st.metric(
                "Pressure Loss Ratio",
                f'{hydraulic["loss_ratio"]:.2f} %'
            )
        
        with col4:

            st.metric(
                "Operating Pressure",
                f'{hydraulic["operating_pressure"]:.2f} bar'
            )
        st.caption(

            "Installation envelope includes the recommended inlet/outlet straight pipe sections (5D), metering spool, and transition fittings."

        )
        
        if hydraulic["status"] == "Negligible":
        
            st.success(
                f'**Hydraulic Status:** {hydraulic["status"]}\n\n'
                f'{hydraulic["comment"]}'
            )
        
        elif hydraulic["status"] == "Acceptable":
        
            st.info(
                f'**Hydraulic Status:** {hydraulic["status"]}\n\n'
                f'{hydraulic["comment"]}'
            )
        
        elif hydraulic["status"] == "Consider Review":
        
            st.warning(
                f'**Hydraulic Status:** {hydraulic["status"]}\n\n'
                f'{hydraulic["comment"]}'
            )
        
        else:
        
            st.error(
                f'**Hydraulic Status:** {hydraulic["status"]}\n\n'
                f'{hydraulic["comment"]}'
            )
        
        # ===============================
        # RANKING TABLE
        # ===============================

        st.dataframe(
            optimization,
            use_container_width=True,
            hide_index=True
        )

        st.success(
        f"""
        ### Hydraulic Engineering Assessment
        
        The proposed **{selected['DN']}** metering spool has an estimated pressure
        drop of **{hydraulic["total_pressure_drop"]:.4f} bar**
        over a fabricated spool length of
        **{spool["fabrication_length"]/1000:.2f} m**.
        
        This represents only
        **{hydraulic["loss_ratio"]:.2f}%**
        of the operating pressure
        (**{hydraulic["operating_pressure"]:.2f} bar**).
        
        Therefore, the hydraulic impact of the proposed metering spool is considered negligible 
        and is not expected to significantly affect the existing steam distribution system.
        The hydraulic assessment is based on the fabricated metering spool length only and 
        does not include the recommended existing straight pipe sections used for installation purposes."""
        )
    
    else:

        st.info("Click Generate Engineering Analysis")

with tab7:

    st.header("Engineering Recommendation")

    if result:

        rec = result["recommendation"]

        st.subheader(
            rec["overall"]
        )
        
        st.metric(
            "Severity",
            rec["severity"]
        )
        
        st.divider()
        
        st.subheader("Warnings")
        
        for w in rec["warnings"]:
        
            st.warning(w)
        
        st.subheader("Engineering Recommendations")
        
        for r in rec["recommendations"]:
        
            st.success(r)
    else:

        st.info(
            "Click **Generate Engineering Analysis**"
        )
    
with tab8:

    st.header("Engineering Methodology")

    st.markdown("""

### Methodology

1. Verify customer steam statement.
2. Compare operating temperature with saturation temperature.
3. Calculate pipe internal diameter.
4. Determine required straight pipe length.
5. Verify installation (PASS / FAIL).
6. Compare operating flow with SUTO S435 flow range.
7. Generate engineering recommendation.
""")

with tab9:

    st.header("S435 Meter Selection")

    if comparison is not None:

        st.info(f"""

        **Operating Pressure :** {pressure:.2f} MPa
        
        **Actual Steam Flow :** {actual_flow:.2f} t/h
        
        The table below compares all available S435 meter sizes based on the current operating condition.
        
        """)

        st.dataframe(

            comparison,

            use_container_width=True,

            hide_index=True

        )

        # ==========================================
        # BEST RECOMMENDED METER
        # ==========================================

        recommended = comparison[
            comparison["Status"] == "🟢 Recommended"
        ]

        if not recommended.empty:

            best = recommended.iloc[0]

            st.success(f"""
### ✅ Best Recommended Meter

**Meter :**
{best['Meter']}

**Flow Range :**
{best['Min Flow (t/h)']} – {best['Max Flow (t/h)']} t/h

**Engineering Note :**
{best['Engineering Note']}
""")

        else:

            st.error("""
⚠ No suitable S435 meter found.

Please review operating pressure or steam flow.
""")

    else:

        st.info(
            "Click Generate Engineering Analysis"
        )

show_progress()
show_my_footer()

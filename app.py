import streamlit as st
from PIL import Image
from utils.meter_comparison import compare_meters
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
    placeholder="PT ABC Indonesia"
)

project = st.sidebar.text_input(
    "Project",
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

    value=0.90,

    step=0.10

)

temperature = st.sidebar.number_input(

    "Temperature (°C)",

    min_value=0.0,

    value=170.0,

    step=1.0

)

dn = st.sidebar.selectbox(

    "Pipe Size",

    [
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

    value=1.00,

    step=0.01

)

disturbance = st.sidebar.selectbox(

    "Nearest Upstream Disturbance",

    [
        "Tee",
        "90° Elbow",
        "2 × 90° Elbow",
        "Reducer",
        "Flange",
        "Two Elbows on Different Plane"
    ]

)

upstream = st.sidebar.number_input(

    "Available Upstream Length (mm)",

    value=1000

)

downstream = st.sidebar.number_input(

    "Available Downstream Length (mm)",

    value=500

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

result = None

if generate:

    result = analyze_installation(

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
    comparison = compare_meters(

        pressure,

        actual_flow

    )
# ==========================================================
# TAB
# ==========================================================

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(

    [

        "📊 Summary",

        "📐 Pipe",

        "🔥 Steam",

        "📈 Flow",

        "📏 Installation",

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

    st.header("Pipe Information")
    
    if result:
    
        st.write(result["pipe"])

with tab3:

    st.header("Steam Property")

    if result:

        st.write(result["steam"])

with tab4:

    st.header("Flow Range")

    if result:

        st.write(result["flow"])

with tab5:

    st.header("Installation")

    if result:

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Required Upstream",
                f'{result["required_upstream"]:.0f} mm'
            )

        with col2:
            st.metric(
                "Required Downstream",
                f'{result["required_downstream"]:.0f} mm'
            )

        with col3:
            st.metric(
                "Status",
                result["installation_status"]
            )

with tab6:

    st.header("Engineering Recommendation")

    if result:

        st.success(result["recommendation"])

with tab7:

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

with tab8:

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
        
        **Meter :** {best['Meter']}
        
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

import streamlit as st
from PIL import Image
import os

# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="SUTO S435 Steam Flowmeter",
    page_icon="💨",
    layout="wide"
)

# =====================================================
# LOAD IMAGES
# =====================================================
logo_path = "assets/suto_logo.png"
product_path = "assets/S435.png"

# =====================================================
# HEADER
# =====================================================
col1, col2 = st.columns([1, 5])

with col1:
    if os.path.exists(logo_path):
        st.image(logo_path, width=120)

with col2:
    st.title("S435 Steam Flowmeter Installation Assistant")
    st.caption("Engineering Installation Verification Tool")

st.divider()

# =====================================================
# SIDEBAR
# =====================================================
st.sidebar.header("Input Parameters")

company = st.sidebar.text_input(
    "Company Name",
    placeholder="PT. ABC Indonesia"
)

steam_condition = st.sidebar.radio(
    "Steam Condition",
    [
        "Saturated Steam",
        "Superheated Steam"
    ]
)

pressure = st.sidebar.number_input(
    "Pressure (bar)",
    min_value=0.0,
    value=7.0,
    step=0.5
)

temperature = st.sidebar.number_input(
    "Temperature (°C)",
    min_value=0.0,
    value=170.0,
    step=1.0
)

dn = st.sidebar.selectbox(
    "Pipe DN",
    [
        "DN15","DN20","DN25","DN32","DN40","DN50",
        "DN65","DN80","DN100","DN125","DN150",
        "DN200","DN250","DN300"
    ]
)

disturbance = st.sidebar.selectbox(
    "Nearest Upstream Disturbance",
    [
        "Tee",
        "90° Elbow",
        "2 × 90° Elbow",
        "Flange",
        "Reducer",
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

generate = st.sidebar.button(
    "Generate Analysis",
    use_container_width=True
)

# =====================================================
# PRODUCT IMAGE
# =====================================================
if os.path.exists(product_path):
    st.image(product_path, width=260)

# =====================================================
# TABS
# =====================================================
tab1, tab2, tab3 = st.tabs(
    [
        "📊 Analysis",
        "📘 Methodology",
        "📚 Reference"
    ]
)

# =====================================================
# TAB 1
# =====================================================
with tab1:

    st.subheader("Steam Installation Analysis")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Steam State",
            "-"
        )

    with col2:
        st.metric(
            "Installation",
            "-"
        )

    with col3:
        st.metric(
            "Required Upstream",
            "-"
        )

    with col4:
        st.metric(
            "Required Downstream",
            "-"
        )

    st.divider()

    st.info(
        "Click **Generate Analysis** to start calculation."
    )

    st.subheader("Installation Illustration")

    st.empty()

    st.subheader("Flow Range")

    st.empty()

# =====================================================
# TAB 2
# =====================================================
with tab2:

    st.subheader("Methodology")

    st.markdown("""
1. Input steam operating condition.

2. Select pipe size.

3. Select nearest upstream disturbance.

4. Determine required straight pipe.

5. Compare actual installation.

6. Validate PASS / FAIL.

7. Display applicable flow range.
""")

# =====================================================
# TAB 3
# =====================================================
with tab3:

    st.subheader("Reference")

    st.markdown("""
- SUTO S435 User Manual

- Steam Table

- Installation Best Practice

- Internal Engineering Guideline
""")

# =====================================================
# FOOTER
# =====================================================
st.divider()

st.caption(
    "© SUTO ITEC Indonesia | Steam Flowmeter Installation Assistant Ver 1.0 created by Cahyadi Wisnu Wardana, MM"
)

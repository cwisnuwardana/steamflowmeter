# ==========================================================
# SVG SPOOL GENERATOR V3
# SUTO S435 Engineering Assistant
# ==========================================================

def generate_svg_spool(spool):

    upstream = spool["upstream"]
    downstream = spool["downstream"]

    reducer = spool["reducer_length"]
    meter = spool["meter_length"]
    expander = spool["expander_length"]

    existing = spool["existing_dn"]
    recommended = spool["recommended_dn"]

    existing_5D = spool["existing_5D"]

    fabrication = spool["fabrication_length"]

    envelope = spool["installation_envelope"]

    svg = f"""
<svg
width="100%"
height="430"
viewBox="0 0 1200 430"
xmlns="http://www.w3.org/2000/svg">

<style>

text {{
    font-family: Arial;
}}

.title {{
    font-size:22px;
    font-weight:bold;
}}

.label {{
    font-size:16px;
}}

.small {{
    font-size:14px;
}}

.dimension {{
    font-size:15px;
    fill:#0A58CA;
}}

</style>

<!-- ================================================= -->
<!-- TITLE -->
<!-- ================================================= -->

<text x="30" y="35" class="title">
SUTO S435 Metering Spool Layout
</text>

<text x="1010" y="35" class="label">
Steam →
</text>

<!-- ================================================= -->
<!-- EXISTING PIPE -->
<!-- ================================================= -->

<line
x1="50"
y1="170"
x2="180"
y2="170"
stroke="black"
stroke-width="8"/>

<!-- REDUCER -->

<polygon
points="
180,150
250,160
250,180
180,190"
fill="#D9D9D9"
stroke="black"/>

<!-- REDUCED PIPE -->

<line
x1="250"
y1="170"
x2="430"
y2="170"
stroke="black"
stroke-width="5"/>

<!-- ================================================= -->
<!-- S435 -->
<!-- ================================================= -->

<rect
x="430"
y="135"
width="180"
height="70"
fill="#FFD600"
stroke="black"
stroke-width="2"/>

<text
x="490"
y="165"
font-size="20"
font-weight="bold">
SUTO
</text>

<text
x="485"
y="188"
font-size="18">
S435
</text>

<!-- REDUCED PIPE -->

<line
x1="610"
y1="170"
x2="790"
y2="170"
stroke="black"
stroke-width="5"/>

<!-- ================================================= -->
<!-- EXPANDER -->
<!-- ================================================= -->

<polygon
points="
790,160
860,150
860,190
790,180"
fill="#D9D9D9"
stroke="black"/>

<!-- EXISTING PIPE -->

<line
x1="860"
y1="170"
x2="1050"
y2="170"
stroke="black"
stroke-width="8"/>

<!-- ================================================= -->
<!-- PIPE LABEL -->
<!-- ================================================= -->

<text x="80" y="145" class="label">
{existing}
</text>

<text x="320" y="145" class="label">
{recommended}
</text>

<text x="655" y="145" class="label">
{recommended}
</text>

<text x="930" y="145" class="label">
{existing}
</text>

<!-- ================================================= -->
<!-- COMPONENT -->
<!-- ================================================= -->

<text x="185" y="220" class="small">
Reducer
</text>

<text x="790" y="220" class="small">
Expander
</text>

<!-- ================================================= -->
<!-- UPSTREAM -->
<!-- ================================================= -->

<line
x1="250"
y1="270"
x2="430"
y2="270"
stroke="#0A58CA"
stroke-width="2"/>

<polygon
points="250,270 258,266 258,274"
fill="#0A58CA"/>

<polygon
points="430,270 422,266 422,274"
fill="#0A58CA"/>

<text
x="285"
y="255"
class="dimension">

← {upstream:.0f} mm →

</text>

<!-- ================================================= -->
<!-- METER -->
<!-- ================================================= -->

<line
x1="430"
y1="315"
x2="610"
y2="315"
stroke="green"
stroke-width="2"/>

<polygon
points="430,315 438,311 438,319"
fill="green"/>

<polygon
points="610,315 602,311 602,319"
fill="green"/>

<text
x="470"
y="300"
fill="green">

← {meter} mm →

</text>

<!-- ================================================= -->
<!-- DOWNSTREAM -->
<!-- ================================================= -->

<line
x1="610"
y1="270"
x2="790"
y2="270"
stroke="#0A58CA"
stroke-width="2"/>

<polygon
points="610,270 618,266 618,274"
fill="#0A58CA"/>

<polygon
points="790,270 782,266 782,274"
fill="#0A58CA"/>

<text
x="640"
y="255"
class="dimension">

← {downstream:.0f} mm →

</text>

<!-- ================================================= -->
<!-- SUMMARY -->
<!-- ================================================= -->

<line
x1="30"
y1="350"
x2="1100"
y2="350"
stroke="#CCCCCC"/>

<text
x="30"
y="380"
font-size="18"
font-weight="bold">

Recommended Installation Envelope :
{envelope:.0f} mm

</text>

<text
x="30"
y="405"
font-size="14">

Inlet Straight :
{existing_5D:.0f} mm

|

Reducer :
{reducer} mm

|

Fabrication :
{fabrication:.0f} mm

|

Meter :
{meter} mm

|

Expander :
{expander} mm

|

Outlet Straight :
{existing_5D:.0f} mm

</text>

</svg>
"""

    return svg

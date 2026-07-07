# ==========================================================
# SVG SPOOL GENERATOR V2
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

    total = spool["total_length"]

    # ==========================================================
    # SCALE CALCULATION
    # ==========================================================
    
    LEFT = 60
    RIGHT = 1060
    
    DRAW_WIDTH = RIGHT - LEFT
    
    scale = DRAW_WIDTH / total
    
    x0 = LEFT
    
    x1 = x0 + reducer * scale
    
    x2 = x1 + upstream * scale
    
    x3 = x2 + meter * scale
    
    x4 = x3 + downstream * scale
    
    x5 = x4 + expander * scale
    
    svg = f"""
<svg width="1200" height="420"
xmlns="http://www.w3.org/2000/svg">

<style>

text {{
    font-family:Arial;
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


<!-- ===================================================== -->
<!-- TITLE -->
<!-- ===================================================== -->

<text x="30" y="35" class="title">
SUTO S435 Metering Spool Layout
</text>

<text x="980" y="35" class="label">
Steam Flow →
</text>


<!-- ===================================================== -->
<!-- EXISTING PIPE -->
<!-- ===================================================== -->

<line x1="20"
      y1="170"
      x2="{x0:.1f}"
      y2="170"
      stroke="black"
      stroke-width="8"/>


<!-- REDUCER -->

<polygon
points="
{x0:.1f},150
{x1:.1f},160
{x1:.1f},180
{x0:.1f},190"
fill="#D9D9D9"
stroke="black"/>


<!-- REDUCED PIPE -->

<line x1="250"
      y1="170"
      x2="430"
      y2="170"
      stroke="black"
      stroke-width="5"/>


<!-- METER -->

<rect
x="430"
y="135"
width="180"
height="70"
fill="#FFD600"
stroke="black"
stroke-width="2"/>

<text
x="{x2 + meter*scale/2 - 20:.1f}"
y="165"
font-size="20"
font-weight="bold">
SUTO
</text>

<text
x="{x2 + meter*scale/2 - 18:.1f}"
y="188"
font-size="18">
S435
</text>


<!-- REDUCED PIPE -->

<line x1="610"
      y1="170"
      x2="790"
      y2="170"
      stroke="black"
      stroke-width="5"/>


<!-- EXPANDER -->

<polygon
points="
{x4:.1f},160
{x5:.1f},150
{x5:.1f},190
{x4:.1f},180"
fill="#D9D9D9"
stroke="black"/>


<!-- EXISTING PIPE -->

<line
x1="{x5:.1f}"
y1="170"
x2="1180"
y2="170"
stroke="black"
stroke-width="8"/>


<!-- ===================================================== -->
<!-- PIPE LABELS -->
<!-- ===================================================== -->

<text x="75" y="145" class="label">
{existing}
</text>

<text x="325" y="145" class="label">
{recommended}
</text>

<text x="655" y="145" class="label">
{recommended}
</text>

<text x="930" y="145" class="label">
{existing}
</text>


<!-- ===================================================== -->
<!-- COMPONENT LABEL -->
<!-- ===================================================== -->

<text x="185" y="220" class="small">
Reducer
</text>

<text x="485" y="220" class="small">
S435
</text>

<text x="790" y="220" class="small">
Expander
</text>


<!-- ===================================================== -->
<!-- UPSTREAM DIMENSION -->
<!-- ===================================================== -->

<line
x1="{x1:.1f}"
y1="170"
x2="{x2:.1f}"
y2="170"
stroke="black"
stroke-width="5"/>

<polygon points="250,270 258,266 258,274"
fill="#0A58CA"/>

<polygon points="430,270 422,266 422,274"
fill="#0A58CA"/>

<text
x="285"
y="255"
class="dimension">

← {upstream:.0f} mm →

</text>


<!-- ===================================================== -->
<!-- METER -->
<!-- ===================================================== -->

<rect
x="{x2:.1f}"
y="135"
width="{meter*scale:.1f}"
height="70"
fill="#FFD600"
stroke="black"
stroke-width="2"/>

<polygon points="430,315 438,311 438,319"
fill="green"/>

<polygon points="610,315 602,311 602,319"
fill="green"/>

<text
x="470"
y="300"
fill="green">

← {meter} mm →

</text>


<!-- ===================================================== -->
<!-- DOWNSTREAM -->
<!-- ===================================================== -->

<line
x1="{x3:.1f}"
x2="{x4:.1f}"
x2="790"
y2="270"
stroke="#0A58CA"
stroke-width="2"/>

<polygon points="610,270 618,266 618,274"
fill="#0A58CA"/>

<polygon points="790,270 782,266 782,274"
fill="#0A58CA"/>

<text
x="640"
y="255"
class="dimension">

← {downstream:.0f} mm →

</text>


<!-- ===================================================== -->
<!-- SUMMARY -->
<!-- ===================================================== -->

<line
x1="30"
y1="350"
x2="1100"
y2="350"
stroke="#CCCCCC"/>

<text
x="30"
y="385"
font-size="18"
font-weight="bold">

Overall Spool Length : {total:.0f} mm

</text>

<text
x="500"
y="385"
font-size="16">

Reducer : {reducer} mm
|
Meter : {meter} mm
|
Expander : {expander} mm

</text>

</svg>
"""

    return svg

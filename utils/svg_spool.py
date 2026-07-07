# ==========================================================
# SVG SPOOL GENERATOR
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

    svg = f"""
<svg width="1100" height="320"
xmlns="http://www.w3.org/2000/svg">

<style>

text {{
font-family:Arial;
}}

</style>

<!-- Flow Direction -->

<text x="40" y="25" font-size="18">
Steam Flow →
</text>

<!-- Main Pipe -->

<line x1="50"
      y1="150"
      x2="1050"
      y2="150"
      stroke="black"
      stroke-width="6"/>

<!-- Reducer -->

<polygon
points="180,140 230,120 230,180 180,160"
fill="lightgray"
stroke="black"/>

<!-- Meter -->

<rect
x="430"
y="115"
width="170"
height="70"
fill="#FFD600"
stroke="black"
stroke-width="2"/>

<text
x="465"
y="155"
font-size="20"
font-weight="bold">
S435
</text>

<!-- Expander -->

<polygon
points="760,120 810,140 810,160 760,180"
fill="lightgray"
stroke="black"/>

<!-- Labels -->

<text x="55" y="120">
{existing}
</text>

<text x="920" y="120">
{existing}
</text>

<text x="465" y="210">
{recommended}
</text>

<!-- Upstream -->

<line
x1="230"
y1="250"
x2="430"
y2="250"
stroke="blue"/>

<text
x="285"
y="240"
fill="blue">

Upstream

{upstream:.0f} mm

</text>

<!-- Meter -->

<line
x1="430"
y1="280"
x2="600"
y2="280"
stroke="green"/>

<text
x="470"
y="300"
fill="green">

S435

{meter} mm

</text>

<!-- Downstream -->

<line
x1="600"
y1="250"
x2="760"
y2="250"
stroke="blue"/>

<text
x="630"
y="240"
fill="blue">

Downstream

{downstream:.0f} mm

</text>

<!-- Total -->

<text
x="40"
y="310"
font-size="18"
font-weight="bold">

Estimated Total Spool Length :
{total:.0f} mm

</text>

</svg>

"""

    return svg

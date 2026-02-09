import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import matplotlib.patheffects as pe
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# ──────────────────────────────────────────────────────────────
# DATA
# ──────────────────────────────────────────────────────────────
# Values estimated from the original NYT chart bar heights,
# cross-referenced with public reporting:
#   - Bloomberg: WNBA revenue ~$102M in 2019
#   - Forbes/Sportico: ~$200M projected for 2023
#   - NBA players receive ~50% of Basketball Related Income
#   - WNBA players receive ~7-10% of league revenue
# Sources: Bloomberg, Forbes, Sportico, Rodney Fort's Sports Business Data

data = pd.DataFrame({
    "Year": [2019, 2020, 2021, 2022, 2023, 2024, 2025],
    "WNBA Revenue": [95, 120, 142, 170, 193, 220, 295],
    "50% Share (NBA-equivalent)": [45, 57, 68, 82, 93, 105, 143],
    "Actual Player Salary": [12, 12, 17, 18, 18, 18, 18],
})

# ──────────────────────────────────────────────────────────────
# STATIC MATPLOTLIB RECREATION
# ──────────────────────────────────────────────────────────────

def create_static_chart():
    """Create a near-exact matplotlib replica of the NYT WNBA revenue chart."""

    fig, ax = plt.subplots(figsize=(10, 7.5))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    years = data["Year"].values
    revenue = data["WNBA Revenue"].values
    share_50 = data["50% Share (NBA-equivalent)"].values
    actual = data["Actual Player Salary"].values

    x = np.arange(len(years))

    # Bar widths — gray widest, blue medium, dark blue narrow
    w_gray = 0.55
    w_blue = 0.40
    w_dark = 0.20

    # Colors matched from the original chart
    color_gray = "#d4d4d4"
    color_blue = "#9cb4d8"
    color_dark = "#4a6fa5"

    # Draw bars — gray behind, blue in front, dark blue at front
    # All bars are left-aligned (same left edge)
    offset = -0.15
    bars_gray = ax.bar(x + offset + w_gray / 2, revenue, width=w_gray,
                       color=color_gray, zorder=1, edgecolor="none")
    bars_blue = ax.bar(x + offset + w_blue / 2, share_50, width=w_blue,
                       color=color_blue, zorder=2, edgecolor="none")
    bars_dark = ax.bar(x + offset + w_dark / 2, actual, width=w_dark,
                       color=color_dark, zorder=3, edgecolor="none")

    # ── Y-axis styling ──
    ax.set_ylim(0, 320)
    yticks = [50, 100, 150, 200, 250, 300]
    ax.set_yticks(yticks)

    # Custom y-tick labels like the original: "50 mil.", "100 mil.", etc.
    # The top one says "$300 million"
    ylabels = []
    for v in yticks:
        if v == 300:
            ylabels.append("")  # We'll place "$300 million" as text
        else:
            ylabels.append(f"${v} mil." if v == 50 else f"{v} mil.")
    # Actually looking at the original more carefully:
    # "$300 million" is at the top, then "250 mil.", "200 mil.", etc.
    ylabels = []
    for v in yticks:
        if v == 300:
            ylabels.append("")
        elif v == 50:
            ylabels.append("50 mil.")
        else:
            ylabels.append(f"{v} mil.")
    ax.set_yticklabels(ylabels, fontsize=11, color="#555555",
                       fontfamily="Georgia")

    # Add underlines to y-tick labels (horizontal lines at each tick)
    for v in yticks:
        ax.axhline(y=v, color="#cccccc", linewidth=0.5, zorder=0,
                   xmin=0.0, xmax=0.04)

    # "$300 million" text at top
    ax.text(-0.8, 305, "$300 million", fontsize=11, color="#555555",
            fontfamily="Georgia", ha="left", va="bottom")

    # Light horizontal grid lines
    for v in yticks:
        ax.axhline(y=v, color="#e8e8e8", linewidth=0.4, zorder=0)

    # ── X-axis styling ──
    ax.set_xticks(x)
    ax.set_xticklabels(years, fontsize=12, color="#333333",
                       fontfamily="Georgia")

    # ── Remove spines ──
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_visible(False)
    ax.spines["bottom"].set_color("#999999")
    ax.spines["bottom"].set_linewidth(0.5)

    # Remove y-axis tick marks
    ax.tick_params(axis="y", length=0, pad=8)
    ax.tick_params(axis="x", length=0, pad=8)

    # ── Title ──
    ax.text(-0.8, 330, "ANNUAL REVENUE", fontsize=14, fontweight="bold",
            color="#333333", fontfamily="Georgia", ha="left",
            transform=ax.transData)

    # ── Annotations with curved arrows ──
    # Annotation 1: "How much money the W.N.B.A. makes" → gray bars (top right)
    ax.annotate(
        "",
        xy=(5.3, 230),          # arrow tip (points to 2024 gray bar top area)
        xytext=(5.3, 290),      # arrow start
        arrowprops=dict(
            arrowstyle="->,head_length=0.4,head_width=0.25",
            connectionstyle="arc3,rad=-0.3",
            color="#333333",
            lw=1.2,
        ),
    )
    # Text for annotation 1 (with underline for the key phrase)
    ax.text(3.0, 300, "How much money the W.N.B.A. makes",
            fontsize=10.5, color="#333333", fontfamily="Georgia",
            ha="left", va="bottom",
            style="italic")
    # Underline beneath "How much money the W.N.B.A. makes"
    ax.plot([3.0, 6.35], [297, 297], color="#333333", linewidth=0.7,
            transform=ax.transData)

    # Annotation 2: "Money the players would share,\nif they were paid like N.B.A. players"
    ax.annotate(
        "",
        xy=(1.5, 75),           # arrow tip (points to ~2020 blue bar)
        xytext=(2.8, 195),      # arrow start
        arrowprops=dict(
            arrowstyle="->,head_length=0.4,head_width=0.25",
            connectionstyle="arc3,rad=0.4",
            color="#333333",
            lw=1.2,
        ),
    )
    ax.text(1.2, 197, "Money the players would share,",
            fontsize=10.5, color="#333333", fontfamily="Georgia",
            ha="left", va="bottom")
    ax.text(1.2, 183, "if they were paid like N.B.A. players",
            fontsize=10.5, color="#333333", fontfamily="Georgia",
            ha="left", va="bottom",
            style="italic")
    # Underline
    ax.plot([1.2, 5.25], [194, 194], color="#333333", linewidth=0.7)
    ax.plot([1.2, 5.5], [180, 180], color="#333333", linewidth=0.7)

    # Annotation 3: "Money that W.N.B.A.\nplayers actually make" → dark blue bars
    ax.annotate(
        "",
        xy=(0.0, 20),           # arrow tip (points to 2019 dark bar)
        xytext=(0.5, 100),      # arrow start
        arrowprops=dict(
            arrowstyle="->,head_length=0.4,head_width=0.25",
            connectionstyle="arc3,rad=0.3",
            color="#b37540",
            lw=1.2,
        ),
    )
    ax.text(-0.3, 115, "Money that W.N.B.A.",
            fontsize=10.5, color="#b37540", fontfamily="Georgia",
            ha="left", va="bottom")
    ax.text(-0.3, 101, "players actually make",
            fontsize=10.5, color="#b37540", fontfamily="Georgia",
            ha="left", va="bottom")
    # Underline
    ax.plot([-0.3, 2.1], [112, 112], color="#b37540", linewidth=0.7)
    ax.plot([-0.3, 2.15], [98, 98], color="#b37540", linewidth=0.7)

    # ── Source footer ──
    fig.text(0.08, 0.02,
             "Sources: Bloomberg, Forbes, Sportico, Rodney Fort's Sports Business Data",
             fontsize=9, color="#888888", fontfamily="Georgia", ha="left")

    plt.tight_layout(rect=[0.05, 0.05, 0.98, 0.95])
    return fig


# ──────────────────────────────────────────────────────────────
# INTERACTIVE PLOTLY CHART
# ──────────────────────────────────────────────────────────────

def create_interactive_chart(df, show_revenue=True, show_share=True,
                             show_actual=True, pct_mode=False):
    """Create an interactive Plotly bar chart."""

    fig = go.Figure()

    if pct_mode:
        # Percentage of revenue view
        if show_share:
            fig.add_trace(go.Bar(
                x=df["Year"],
                y=(df["50% Share (NBA-equivalent)"] / df["WNBA Revenue"] * 100),
                name="50% Share (NBA-equivalent)",
                marker_color="#9cb4d8",
                hovertemplate="<b>%{x}</b><br>50%% Share: %{y:.1f}%% of revenue<extra></extra>",
            ))
        if show_actual:
            fig.add_trace(go.Bar(
                x=df["Year"],
                y=(df["Actual Player Salary"] / df["WNBA Revenue"] * 100),
                name="Actual WNBA Player Salary",
                marker_color="#4a6fa5",
                hovertemplate="<b>%{x}</b><br>Actual salary: %{y:.1f}%% of revenue<extra></extra>",
            ))
        yaxis_title = "Percentage of League Revenue"
        yaxis_suffix = "%"
    else:
        # Absolute dollar view
        if show_revenue:
            fig.add_trace(go.Bar(
                x=df["Year"],
                y=df["WNBA Revenue"],
                name="WNBA Revenue",
                marker_color="#d4d4d4",
                hovertemplate="<b>%{x}</b><br>Revenue: $%{y}M<extra></extra>",
            ))
        if show_share:
            fig.add_trace(go.Bar(
                x=df["Year"],
                y=df["50% Share (NBA-equivalent)"],
                name="50% Share (NBA-equivalent)",
                marker_color="#9cb4d8",
                hovertemplate="<b>%{x}</b><br>50%% Share: $%{y}M<extra></extra>",
            ))
        if show_actual:
            fig.add_trace(go.Bar(
                x=df["Year"],
                y=df["Actual Player Salary"],
                name="Actual WNBA Player Salary",
                marker_color="#4a6fa5",
                hovertemplate="<b>%{x}</b><br>Actual salary: $%{y}M<extra></extra>",
            ))
        yaxis_title = "Millions (USD)"
        yaxis_suffix = "M"

    fig.update_layout(
        barmode="group",
        title=dict(
            text="WNBA Annual Revenue vs. Player Compensation",
            font=dict(size=18, family="Georgia, serif", color="#333333"),
        ),
        xaxis=dict(
            title="",
            tickfont=dict(size=13, family="Georgia, serif"),
            dtick=1,
        ),
        yaxis=dict(
            title=yaxis_title,
            tickfont=dict(size=12, family="Georgia, serif"),
            gridcolor="#eeeeee",
            tickprefix="$" if not pct_mode else "",
            ticksuffix=yaxis_suffix,
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0,
            font=dict(size=11, family="Georgia, serif"),
        ),
        plot_bgcolor="white",
        paper_bgcolor="white",
        margin=dict(l=60, r=30, t=80, b=60),
        hoverlabel=dict(
            bgcolor="white",
            font_size=13,
            font_family="Georgia, serif",
        ),
        annotations=[
            dict(
                text="Sources: Bloomberg, Forbes, Sportico, Rodney Fort's Sports Business Data",
                xref="paper", yref="paper",
                x=0, y=-0.15,
                showarrow=False,
                font=dict(size=10, color="#888888", family="Georgia, serif"),
            )
        ],
    )

    return fig


# ──────────────────────────────────────────────────────────────
# STREAMLIT APP
# ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="WNBA Revenue Visualization",
    page_icon="\U0001F3C0",
    layout="wide",
)

st.title("WNBA Annual Revenue: A Data Visualization Study")
st.markdown("""
**Assignment:** Replicate a published data visualization from the New York Times,
then create an interactive version using Streamlit.

**Source:** [NYT Learning Network — "What's Going On in This Graph?" (Feb 11, 2026)](https://www.nytimes.com/2026/02/05/learning/whats-going-on-in-this-graph-feb-11-2026.html)

**Data Sources:** Bloomberg, Forbes, Sportico, Rodney Fort's Sports Business Data
""")

st.divider()

# ── Section 1: Static Recreation ──
st.header("1. Static Recreation (Matplotlib)")
st.markdown("""
Below is a near-exact replica of the original NYT chart, recreated using only
Python and Matplotlib. The goal was to match the design as closely as possible:
bar layout, colors, typography, annotations, and overall aesthetic.
""")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Original Chart")
    st.image("assets/original_chart.png", use_container_width=True)

with col2:
    st.subheader("My Recreation")
    static_fig = create_static_chart()
    st.pyplot(static_fig, use_container_width=True)
    plt.close(static_fig)

st.divider()

# ── Section 2: Interactive Version ──
st.header("2. Interactive Version (Plotly)")
st.markdown("""
This interactive version adds hover tooltips with exact values,
filtering controls, and a percentage view toggle.
""")

# Sidebar controls
with st.sidebar:
    st.header("Controls")

    year_range = st.slider(
        "Year Range",
        min_value=2019,
        max_value=2025,
        value=(2019, 2025),
        step=1,
    )

    st.subheader("Show/Hide Series")
    show_revenue = st.checkbox("WNBA Revenue", value=True)
    show_share = st.checkbox("50% Share (NBA-equivalent)", value=True)
    show_actual = st.checkbox("Actual Player Salary", value=True)

    pct_mode = st.toggle("Show as % of Revenue", value=False)

    st.divider()
    st.markdown("### About This Chart")
    st.markdown("""
    The W.N.B.A. has grown quickly in recent years, with revenue increasing
    from ~$95M in 2019 to ~$295M in 2025.

    However, **WNBA players receive only ~7-10% of league revenue**,
    compared to NBA players who receive ~50%.

    The light blue bars show what WNBA players *would* earn if they
    received the same ~50% revenue share as NBA players.
    """)

# Filter data by year range
filtered = data[(data["Year"] >= year_range[0]) & (data["Year"] <= year_range[1])]

interactive_fig = create_interactive_chart(
    filtered,
    show_revenue=show_revenue,
    show_share=show_share,
    show_actual=show_actual,
    pct_mode=pct_mode,
)
st.plotly_chart(interactive_fig, use_container_width=True)

# ── Data Table ──
with st.expander("View Raw Data"):
    display_df = filtered.copy()
    display_df["Revenue Share %"] = (
        display_df["Actual Player Salary"] / display_df["WNBA Revenue"] * 100
    ).round(1)
    st.dataframe(display_df, use_container_width=True, hide_index=True)

st.divider()

# ── Section 3: Design Decisions ──
st.header("3. Design Decisions")
st.markdown("""
**Four specific elements I had to estimate or interpret:**

1. **Data values** — The original chart does not provide raw data. I reverse-engineered
   all values by measuring bar heights against the y-axis grid. I cross-referenced with
   public reporting (Bloomberg: ~$102M in 2019; Forbes: ~$200M projected for 2023) to
   validate my estimates.

2. **Typography** — The New York Times uses proprietary fonts (NYT Cheltenham for
   headlines, NYT Franklin for body text). Since these are not publicly available, I
   used Georgia (serif) as the closest system font match for the chart's aesthetic.

3. **Curved arrow annotations** — The original chart features hand-drawn-style curved
   arrows connecting text labels to specific bar groups. I used Matplotlib's
   `FancyArrowPatch` with `connectionstyle="arc3"` and tuned the `rad` parameter to
   approximate the curvature. Getting the exact bezier control points required
   significant trial and error.

4. **Bar width and overlap** — The three bar series in the original are layered
   (gray widest behind, blue medium, dark blue narrow in front) with a specific
   left-alignment. I had to estimate the exact width ratios and offsets to replicate
   this stacked-but-grouped layout.
""")

st.divider()

# ── Section 4: Reflection ──
st.header("4. Reflection")
st.markdown("""
**What made this chart hard to replicate?**

The annotations were by far the hardest element. Professional chart annotations
look effortless but require precise coordinate positioning, custom arrow styles,
and careful text layout. The curved arrows in the original chart have a natural,
almost hand-drawn quality that's difficult to achieve with Matplotlib's geometric
arrow styles.

**What limitations did I run into, and how did I bypass them?**

- **Font limitations:** NYT's proprietary fonts give their charts a distinctive look.
  I used Georgia as a fallback, which is close but not identical.
- **Annotation underlines:** The original has underlined text in annotations.
  Matplotlib doesn't natively support underlined text, so I drew thin horizontal
  lines beneath the text manually.
- **Static to interactive transition:** Matplotlib's custom annotations don't
  translate to Plotly. I had to redesign the interactive version with Plotly's
  own annotation system and lean on hover tooltips instead of static labels.

**What did this teach me about how professional charts are built?**

Professional data visualization is 20% data and 80% design. The actual data in
this chart is simple — three series across seven years. What makes it powerful is
the storytelling: the annotations guide the reader's eye, the color contrast
highlights the pay gap, and the clean layout removes all distraction. Every pixel
serves a purpose. This is the craft of data journalism.
""")

st.divider()
st.caption("Created by Miguel Artazos | Data Science Module 04 Assignment")

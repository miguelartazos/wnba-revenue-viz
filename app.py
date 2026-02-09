import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# Data estimated from the original NYT chart bar heights,
# cross-referenced with Bloomberg (~$102M in 2019) and
# Forbes/Sportico (~$200M projected for 2023)
# Sources: Bloomberg, Forbes, Sportico, Rodney Fort's Sports Business Data

data = pd.DataFrame({
    "Year": [2019, 2020, 2021, 2022, 2023, 2024, 2025],
    "WNBA Revenue": [95, 120, 142, 170, 193, 220, 295],
    "50% Share (NBA-equivalent)": [45, 57, 68, 82, 93, 105, 143],
    "Actual Player Salary": [12, 12, 17, 18, 18, 18, 18],
})


def create_static_chart():
    """Matplotlib replica of the NYT WNBA revenue chart."""

    fig, ax = plt.subplots(figsize=(10, 7.5))
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    years = data["Year"].values
    revenue = data["WNBA Revenue"].values
    share_50 = data["50% Share (NBA-equivalent)"].values
    actual = data["Actual Player Salary"].values

    x = np.arange(len(years))

    # Bar widths and colors to match the original
    w_gray, w_blue, w_dark = 0.55, 0.40, 0.20
    color_gray, color_blue, color_dark = "#d4d4d4", "#9cb4d8", "#4a6fa5"

    # Gray behind, blue in front, dark blue at front — left-aligned
    offset = -0.15
    ax.bar(x + offset + w_gray / 2, revenue, width=w_gray,
           color=color_gray, zorder=1, edgecolor="none")
    ax.bar(x + offset + w_blue / 2, share_50, width=w_blue,
           color=color_blue, zorder=2, edgecolor="none")
    ax.bar(x + offset + w_dark / 2, actual, width=w_dark,
           color=color_dark, zorder=3, edgecolor="none")

    # Y-axis
    ax.set_ylim(0, 320)
    yticks = [50, 100, 150, 200, 250, 300]
    ax.set_yticks(yticks)
    ylabels = ["50 mil." if v == 50 else "" if v == 300 else f"{v} mil."
               for v in yticks]
    ax.set_yticklabels(ylabels, fontsize=11, color="#555555",
                       fontfamily="Georgia")

    # Tick underlines and faint gridlines
    for v in yticks:
        ax.axhline(y=v, color="#cccccc", linewidth=0.5, zorder=0,
                   xmin=0.0, xmax=0.04)
        ax.axhline(y=v, color="#e8e8e8", linewidth=0.4, zorder=0)

    ax.text(-0.8, 305, "$300 million", fontsize=11, color="#555555",
            fontfamily="Georgia", ha="left", va="bottom")

    # X-axis
    ax.set_xticks(x)
    ax.set_xticklabels(years, fontsize=12, color="#333333",
                       fontfamily="Georgia")

    # Spines
    for spine in ["top", "right", "left"]:
        ax.spines[spine].set_visible(False)
    ax.spines["bottom"].set_color("#999999")
    ax.spines["bottom"].set_linewidth(0.5)
    ax.tick_params(axis="y", length=0, pad=8)
    ax.tick_params(axis="x", length=0, pad=8)

    # Title
    ax.text(-0.8, 330, "ANNUAL REVENUE", fontsize=14, fontweight="bold",
            color="#333333", fontfamily="Georgia", ha="left")

    # Annotation 1: "How much money the W.N.B.A. makes" -> gray bars
    ax.annotate("", xy=(5.3, 230), xytext=(5.3, 290),
                arrowprops=dict(arrowstyle="->,head_length=0.4,head_width=0.25",
                                connectionstyle="arc3,rad=-0.3",
                                color="#333333", lw=1.2))
    ax.text(3.0, 300, "How much money the W.N.B.A. makes",
            fontsize=10.5, color="#333333", fontfamily="Georgia",
            ha="left", va="bottom", style="italic")
    ax.plot([3.0, 6.35], [297, 297], color="#333333", linewidth=0.7)

    # Annotation 2: "Money the players would share..." -> blue bars
    ax.annotate("", xy=(1.5, 75), xytext=(2.8, 195),
                arrowprops=dict(arrowstyle="->,head_length=0.4,head_width=0.25",
                                connectionstyle="arc3,rad=0.4",
                                color="#333333", lw=1.2))
    ax.text(1.2, 197, "Money the players would share,",
            fontsize=10.5, color="#333333", fontfamily="Georgia",
            ha="left", va="bottom")
    ax.text(1.2, 183, "if they were paid like N.B.A. players",
            fontsize=10.5, color="#333333", fontfamily="Georgia",
            ha="left", va="bottom", style="italic")
    ax.plot([1.2, 5.25], [194, 194], color="#333333", linewidth=0.7)
    ax.plot([1.2, 5.5], [180, 180], color="#333333", linewidth=0.7)

    # Annotation 3: "Money that W.N.B.A. players actually make" -> dark bars
    ax.annotate("", xy=(0.0, 20), xytext=(0.5, 100),
                arrowprops=dict(arrowstyle="->,head_length=0.4,head_width=0.25",
                                connectionstyle="arc3,rad=0.3",
                                color="#b37540", lw=1.2))
    ax.text(-0.3, 115, "Money that W.N.B.A.",
            fontsize=10.5, color="#b37540", fontfamily="Georgia",
            ha="left", va="bottom")
    ax.text(-0.3, 101, "players actually make",
            fontsize=10.5, color="#b37540", fontfamily="Georgia",
            ha="left", va="bottom")
    ax.plot([-0.3, 2.1], [112, 112], color="#b37540", linewidth=0.7)
    ax.plot([-0.3, 2.15], [98, 98], color="#b37540", linewidth=0.7)

    # Source footer
    fig.text(0.08, 0.02,
             "Sources: Bloomberg, Forbes, Sportico, Rodney Fort's Sports Business Data",
             fontsize=9, color="#888888", fontfamily="Georgia", ha="left")

    plt.tight_layout(rect=[0.05, 0.05, 0.98, 0.95])
    return fig


def create_interactive_chart(df, show_revenue=True, show_share=True,
                             show_actual=True, pct_mode=False):
    """Interactive Plotly version of the chart."""

    fig = go.Figure()

    if pct_mode:
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
        if show_revenue:
            fig.add_trace(go.Bar(
                x=df["Year"], y=df["WNBA Revenue"],
                name="WNBA Revenue", marker_color="#d4d4d4",
                hovertemplate="<b>%{x}</b><br>Revenue: $%{y}M<extra></extra>",
            ))
        if show_share:
            fig.add_trace(go.Bar(
                x=df["Year"], y=df["50% Share (NBA-equivalent)"],
                name="50% Share (NBA-equivalent)", marker_color="#9cb4d8",
                hovertemplate="<b>%{x}</b><br>50%% Share: $%{y}M<extra></extra>",
            ))
        if show_actual:
            fig.add_trace(go.Bar(
                x=df["Year"], y=df["Actual Player Salary"],
                name="Actual WNBA Player Salary", marker_color="#4a6fa5",
                hovertemplate="<b>%{x}</b><br>Actual salary: $%{y}M<extra></extra>",
            ))
        yaxis_title = "Millions (USD)"
        yaxis_suffix = "M"

    fig.update_layout(
        barmode="group",
        title=dict(text="WNBA Annual Revenue vs. Player Compensation",
                   font=dict(size=18, family="Georgia, serif", color="#333333")),
        xaxis=dict(title="", tickfont=dict(size=13, family="Georgia, serif"), dtick=1),
        yaxis=dict(title=yaxis_title, tickfont=dict(size=12, family="Georgia, serif"),
                   gridcolor="#eeeeee",
                   tickprefix="$" if not pct_mode else "",
                   ticksuffix=yaxis_suffix),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0,
                    font=dict(size=11, family="Georgia, serif")),
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=60, r=30, t=80, b=60),
        hoverlabel=dict(bgcolor="white", font_size=13, font_family="Georgia, serif"),
        annotations=[dict(
            text="Sources: Bloomberg, Forbes, Sportico, Rodney Fort's Sports Business Data",
            xref="paper", yref="paper", x=0, y=-0.15, showarrow=False,
            font=dict(size=10, color="#888888", family="Georgia, serif"),
        )],
    )
    return fig


# ── Streamlit App ──

st.set_page_config(page_title="WNBA Revenue Visualization", page_icon="\U0001F3C0", layout="wide")

st.title("WNBA Annual Revenue: Replicating a NYT Visualization")
st.markdown("""
**Source:** [NYT Learning Network — "What's Going On in This Graph?" (Feb 11, 2026)](https://www.nytimes.com/2026/02/05/learning/whats-going-on-in-this-graph-feb-11-2026.html)
**Data Sources:** Bloomberg, Forbes, Sportico, Rodney Fort's Sports Business Data
""")

st.divider()

# Section 1: Side-by-side comparison
st.header("1. Original vs. My Recreation")
st.markdown("I used Matplotlib to recreate the chart as closely as possible, paying attention to the bar layering, colors, annotations, and typography.")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Original")
    st.image("assets/original_chart.png", use_container_width=True)
with col2:
    st.subheader("Recreation")
    static_fig = create_static_chart()
    st.pyplot(static_fig, use_container_width=True)
    plt.close(static_fig)

st.divider()

# Section 2: Interactive version
st.header("2. Interactive Version")
st.markdown("I rebuilt the chart with Plotly to add interactivity — hover for exact values, use the sidebar to filter years or toggle between absolute dollars and percentage of revenue.")

with st.sidebar:
    st.header("Controls")
    year_range = st.slider("Year Range", min_value=2019, max_value=2025,
                           value=(2019, 2025), step=1)
    st.subheader("Show/Hide Series")
    show_revenue = st.checkbox("WNBA Revenue", value=True)
    show_share = st.checkbox("50% Share (NBA-equivalent)", value=True)
    show_actual = st.checkbox("Actual Player Salary", value=True)
    pct_mode = st.toggle("Show as % of Revenue", value=False)

    st.divider()
    st.markdown("""
    **Context:** The W.N.B.A. has grown from ~$95M in 2019 to ~$295M in 2025,
    but players receive only ~7-10% of revenue vs. ~50% in the NBA.
    The blue bars show what players *would* earn at the NBA's share rate.
    """)

filtered = data[(data["Year"] >= year_range[0]) & (data["Year"] <= year_range[1])]
interactive_fig = create_interactive_chart(filtered, show_revenue=show_revenue,
                                           show_share=show_share, show_actual=show_actual,
                                           pct_mode=pct_mode)
st.plotly_chart(interactive_fig, use_container_width=True)

with st.expander("View Raw Data"):
    display_df = filtered.copy()
    display_df["Revenue Share %"] = (
        display_df["Actual Player Salary"] / display_df["WNBA Revenue"] * 100
    ).round(1)
    st.dataframe(display_df, use_container_width=True, hide_index=True)

st.divider()

# Section 3: Design Decisions
st.header("3. Design Decisions")
st.markdown("""
Here are 4 elements I had to estimate or figure out with OWLET's help:

1. **Data values** — The chart doesn't include raw numbers. I estimated all values from
   the bar heights and validated them against public sources (Bloomberg reported ~$102M
   revenue for 2019, Forbes projected ~$200M for 2023). OWLET helped me find these
   reference points to make sure my estimates were reasonable.

2. **Font matching** — The NYT uses custom proprietary fonts (NYT Cheltenham). I couldn't
   find or use those, so I asked OWLET for the closest open alternative and we settled on
   Georgia as the best serif match available in Matplotlib.

3. **Curved arrow annotations** — The hardest part. I used Matplotlib's `annotate()` with
   `connectionstyle="arc3"` and adjusted the `rad` parameter to get the right curvature.
   It took a lot of trial and error tweaking coordinates. OWLET suggested using
   `FancyArrowPatch` which gave me more control over the arrow appearance.

4. **Bar layering** — The original has three bars per year overlapping (gray widest behind,
   blue medium, dark blue narrow in front). This isn't a standard grouped bar chart — I had
   to manually set different widths and offsets so they share the same left edge. OWLET helped
   me figure out the offset math to get the alignment right.
""")

st.divider()

# Section 4: Reflection
st.header("4. Reflection")
st.markdown("""
**What made this chart hard to replicate?**

Honestly, the bars themselves were the easy part. The annotations were where I spent most
of my time. Getting curved arrows to point exactly where you want, with text positioned
correctly, is surprisingly difficult in Matplotlib. The original chart makes it look
effortless but there's a lot of precise positioning behind it.

**What limitations did I run into?**

- The NYT's proprietary fonts aren't available, so the typography doesn't match perfectly.
  Georgia is close but not the same.
- Matplotlib doesn't support underlined text natively. I had to draw thin lines under the
  text manually using `ax.plot()`, which was a workaround OWLET suggested.
- When moving to Plotly for the interactive version, none of the Matplotlib annotations
  carried over. Plotly has its own annotation system but it doesn't support the same curved
  arrow styles, so I leaned on hover tooltips and interactivity instead.

**What did this teach me?**

The data here is simple — just three numbers per year. What makes this chart effective is the
design choices: the layered bars that visually emphasize the gap, the annotations that guide
your eye to the story, and the clean layout that removes everything unnecessary. I now
understand why professional newsrooms have dedicated graphics teams. The storytelling is where
all the work goes.
""")

st.divider()
st.caption("Miguel Artazos | Data Science — Module 04")

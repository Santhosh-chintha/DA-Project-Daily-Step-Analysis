"""
Daily Step Analysis Dashboard
------------------------------
A beginner-friendly Streamlit dashboard to analyze daily walking activity,
track step goals, and visualize trends over time using Pandas and Matplotlib.
"""

import os
from typing import Optional, Tuple, Dict, Any
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import streamlit as st

# -----------------------------------------------------------------------------
# Configuration & Page Setup
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Daily Step Analysis Dashboard",
    page_icon="👟",
    layout="wide",
    initial_sidebar_state="expanded",
)

DEFAULT_CSV_PATH = os.path.join(os.path.dirname(__file__), "steps.csv")
DEFAULT_STEP_GOAL = 8000


# -----------------------------------------------------------------------------
# Data Loading & Validation Functions
# -----------------------------------------------------------------------------
def load_csv_data(source) -> Tuple[Optional[pd.DataFrame], Optional[str]]:
    """
    Load data from a file-like object or local file path into a pandas DataFrame.
    
    Parameters:
        source: Uploaded file object or string file path.
        
    Returns:
        Tuple of (DataFrame or None, error_message or None)
    """
    try:
        df = pd.read_csv(source)
        if df.empty:
            return None, "The uploaded CSV file is empty. Please provide a file with data."
        return df, None
    except Exception as e:
        return None, f"Could not read the CSV file: {e}"


def clean_and_validate_data(df: pd.DataFrame) -> Tuple[Optional[pd.DataFrame], Optional[str], Optional[str]]:
    """
    Validate required columns, convert types, handle missing values,
    and sort data chronologically.
    
    Parameters:
        df: Raw pandas DataFrame.
        
    Returns:
        Tuple of (Cleaned DataFrame or None, warning_message or None, error_message or None)
    """
    # Normalize column names: strip whitespace
    df = df.copy()
    df.columns = [str(col).strip() for col in df.columns]

    # Check for required columns (case-insensitive check for Date and Steps)
    col_map = {}
    for col in df.columns:
        low = col.lower()
        if low == "date":
            col_map["Date"] = col
        elif low in ["steps", "step", "step_count", "stepcount"]:
            col_map["Steps"] = col
        elif low in ["calories_burned", "calories", "calorie_burned", "cals"]:
            col_map["Calories_Burned"] = col

    if "Date" not in col_map or "Steps" not in col_map:
        return None, None, (
            "Missing required columns! Your CSV must include at least 'Date' and 'Steps' columns. "
            f"Found columns: {', '.join(df.columns)}"
        )

    # Standardize column names
    rename_dict = {col_map["Date"]: "Date", col_map["Steps"]: "Steps"}
    if "Calories_Burned" in col_map:
        rename_dict[col_map["Calories_Burned"]] = "Calories_Burned"
    df = df.rename(columns=rename_dict)

    initial_row_count = len(df)

    # Convert Date column to datetime (coerce invalid formats to NaT)
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    # Convert Steps column to numeric (coerce invalid non-numbers to NaN)
    df["Steps"] = pd.to_numeric(df["Steps"], errors="coerce")

    # If Calories_Burned is available, convert it to numeric as well
    if "Calories_Burned" in df.columns:
        df["Calories_Burned"] = pd.to_numeric(df["Calories_Burned"], errors="coerce")

    # Drop rows where Date or Steps is invalid / missing
    df = df.dropna(subset=["Date", "Steps"])

    # Discard non-sensical negative step values
    df = df[df["Steps"] >= 0]

    if df.empty:
        return None, None, "No valid data rows found after parsing dates and numeric step counts."

    # Sort chronologically and reset index
    df = df.sort_values(by="Date").reset_index(drop=True)

    # Convert Steps to integer for clean reporting
    df["Steps"] = df["Steps"].astype(int)

    # Check if any invalid rows were dropped to warn user
    dropped_rows = initial_row_count - len(df)
    warning = None
    if dropped_rows > 0:
        warning = f"Note: {dropped_rows} row(s) with invalid dates, missing values, or negative steps were ignored."

    return df, warning, None


# -----------------------------------------------------------------------------
# Metric Calculation Function
# -----------------------------------------------------------------------------
def calculate_metrics(df: pd.DataFrame, step_goal: int) -> Dict[str, Any]:
    """
    Calculate summary statistics and goal completion metrics.
    
    Parameters:
        df: Cleaned pandas DataFrame with 'Date' and 'Steps'.
        step_goal: User-specified daily step target.
        
    Returns:
        Dictionary of computed summary statistics.
    """
    total_steps = int(df["Steps"].sum())
    total_days = len(df)
    avg_steps = int(round(df["Steps"].mean())) if total_days > 0 else 0
    max_steps = int(df["Steps"].max()) if total_days > 0 else 0
    min_steps = int(df["Steps"].min()) if total_days > 0 else 0
    
    # Days where step goal was achieved
    goal_met_series = df["Steps"] >= step_goal
    days_goal_met = int(goal_met_series.sum())
    goal_percentage = (days_goal_met / total_days * 100) if total_days > 0 else 0.0

    # Best day and Lowest day dates
    max_day_row = df.loc[df["Steps"].idxmax()] if total_days > 0 else None
    min_day_row = df.loc[df["Steps"].idxmin()] if total_days > 0 else None

    return {
        "total_steps": total_steps,
        "avg_steps": avg_steps,
        "max_steps": max_steps,
        "min_steps": min_steps,
        "days_goal_met": days_goal_met,
        "total_days": total_days,
        "goal_percentage": goal_percentage,
        "best_date": max_day_row["Date"].strftime("%b %d, %Y") if max_day_row is not None else "N/A",
        "lowest_date": min_day_row["Date"].strftime("%b %d, %Y") if min_day_row is not None else "N/A",
    }


# -----------------------------------------------------------------------------
# Matplotlib Visualization Functions
# -----------------------------------------------------------------------------
def plot_daily_steps_line(df: pd.DataFrame, step_goal: int) -> plt.Figure:
    """Create a line chart showing daily steps over time with the goal threshold."""
    fig, ax = plt.subplots(figsize=(10, 4.5))

    ax.plot(
        df["Date"],
        df["Steps"],
        color="#2563EB",
        marker="o",
        linewidth=2.2,
        markersize=5,
        label="Daily Steps",
    )

    # Reference line for step goal
    ax.axhline(
        y=step_goal,
        color="#DC2626",
        linestyle="--",
        linewidth=1.8,
        label=f"Goal ({step_goal:,} steps)",
    )

    ax.set_title("Daily Steps Trend Over Time", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Date", fontsize=11, labelpad=8)
    ax.set_ylabel("Step Count", fontsize=11, labelpad=8)

    # Format x-axis dates
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    fig.autofmt_xdate(rotation=45, ha="right")

    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.grid(True, linestyle=":", alpha=0.6)
    ax.legend(loc="upper left", frameon=True)
    plt.tight_layout()
    return fig


def plot_daily_steps_bar(df: pd.DataFrame) -> plt.Figure:
    """Create a bar chart comparing daily step counts."""
    fig, ax = plt.subplots(figsize=(10, 4.5))

    # Convert date to string for readable categorical bars
    date_labels = df["Date"].dt.strftime("%b %d")
    bars = ax.bar(date_labels, df["Steps"], color="#3B82F6", edgecolor="#1D4ED8", alpha=0.85, width=0.7)

    ax.set_title("Daily Step Counts Comparison", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Date", fontsize=11, labelpad=8)
    ax.set_ylabel("Step Count", fontsize=11, labelpad=8)

    # Rotate labels
    plt.xticks(rotation=60, ha="right", fontsize=9)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.grid(axis="y", linestyle=":", alpha=0.6)

    # Mean reference line
    mean_steps = df["Steps"].mean()
    ax.axhline(
        y=mean_steps,
        color="#F59E0B",
        linestyle="-.",
        linewidth=1.6,
        label=f"Average ({int(mean_steps):,} steps)",
    )
    ax.legend(loc="upper left", frameon=True)

    plt.tight_layout()
    return fig


def plot_goal_comparison_bar(df: pd.DataFrame, step_goal: int) -> plt.Figure:
    """Create a bar chart showing steps compared with the daily goal (color-coded)."""
    fig, ax = plt.subplots(figsize=(10, 4.5))

    date_labels = df["Date"].dt.strftime("%b %d")
    met_goal = df["Steps"] >= step_goal

    # Colors: Green for goal achieved, Red/Coral for goal missed
    colors = ["#16A34A" if met else "#EF4444" for met in met_goal]
    edge_colors = ["#14532D" if met else "#991B1B" for met in met_goal]

    ax.bar(
        date_labels,
        df["Steps"],
        color=colors,
        edgecolor=edge_colors,
        alpha=0.85,
        width=0.7,
    )

    # Goal threshold line
    ax.axhline(
        y=step_goal,
        color="#1E293B",
        linestyle="--",
        linewidth=2,
        label=f"Daily Goal ({step_goal:,} steps)",
    )

    ax.set_title("Daily Steps vs. Step Goal", fontsize=14, fontweight="bold", pad=12)
    ax.set_xlabel("Date", fontsize=11, labelpad=8)
    ax.set_ylabel("Step Count", fontsize=11, labelpad=8)

    plt.xticks(rotation=60, ha="right", fontsize=9)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"{int(x):,}"))
    ax.grid(axis="y", linestyle=":", alpha=0.6)

    # Custom legend proxies for achieved vs missed
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor="#16A34A", edgecolor="#14532D", label="Goal Achieved (>= Goal)"),
        Patch(facecolor="#EF4444", edgecolor="#991B1B", label="Goal Missed (< Goal)"),
        plt.Line2D([0], [0], color="#1E293B", linestyle="--", linewidth=2, label=f"Goal: {step_goal:,}"),
    ]
    ax.legend(handles=legend_elements, loc="upper left", frameon=True)

    plt.tight_layout()
    return fig


# -----------------------------------------------------------------------------
# Main Application Flow
# -----------------------------------------------------------------------------
def main():
    # ---------------- Sidebar Controls ----------------
    st.sidebar.title("⚙️ Dashboard Settings")
    st.sidebar.markdown("Customize your step goal and data source.")

    # Goal adjustment
    step_goal = st.sidebar.number_input(
        "🎯 Daily Step Goal",
        min_value=1000,
        max_value=50000,
        value=DEFAULT_STEP_GOAL,
        step=500,
        help="Set your target number of steps per day (default: 8,000 steps).",
    )

    st.sidebar.markdown("---")
    st.sidebar.subheader("📁 Data Source")

    uploaded_file = st.sidebar.file_uploader(
        "Upload Custom CSV File",
        type=["csv"],
        help="Upload a CSV with 'Date', 'Steps', and optional 'Calories_Burned' columns.",
    )

    # Decide data source: uploaded file or sample dataset
    if uploaded_file is not None:
        raw_df, load_err = load_csv_data(uploaded_file)
        data_source_label = f"Uploaded File: `{uploaded_file.name}`"
    else:
        if os.path.exists(DEFAULT_CSV_PATH):
            raw_df, load_err = load_csv_data(DEFAULT_CSV_PATH)
            data_source_label = "Sample Dataset (`steps.csv`)"
        else:
            raw_df = None
            load_err = (
                f"Sample dataset `{DEFAULT_CSV_PATH}` was not found. "
                "Please upload a CSV file to proceed."
            )
            data_source_label = "None"

    # Sidebar info note
    st.sidebar.markdown("---")
    st.sidebar.markdown(
        """
        **Required CSV Format:**
        - `Date`: e.g. `2024-10-01`
        - `Steps`: integer step count
        - `Calories_Burned`: (optional)
        """
    )
    if os.path.exists(DEFAULT_CSV_PATH):
        with open(DEFAULT_CSV_PATH, "r", encoding="utf-8") as f:
            st.sidebar.download_button(
                label="📥 Download Sample CSV",
                data=f.read(),
                file_name="sample_steps.csv",
                mime="text/csv",
                help="Click to download the sample dataset format.",
            )

    # ---------------- Main Dashboard Header ----------------
    st.title("👟 Daily Step Analysis Dashboard")
    st.markdown(
        "Monitor your daily walking activity, track consistency, and evaluate your performance "
        "against your personal step goals."
    )
    st.caption(f"**Current Data Source:** {data_source_label}")

    # Handle loading errors
    if load_err or raw_df is None:
        st.error(f"❌ {load_err}")
        st.stop()

    # Clean and validate data
    clean_df, warning_msg, validation_err = clean_and_validate_data(raw_df)

    if validation_err or clean_df is None:
        st.error(f"❌ Data Validation Error: {validation_err}")
        st.stop()

    if warning_msg:
        st.warning(f"⚠️ {warning_msg}")

    # Calculate summary metrics
    metrics = calculate_metrics(clean_df, step_goal)

    # ---------------- KPI Metric Cards ----------------
    st.markdown("### 📌 Key Performance Indicators")
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            label="Total Steps",
            value=f"{metrics['total_steps']:,}",
            help="Total cumulative steps taken across all recorded days.",
        )
    with col2:
        st.metric(
            label="Average Daily Steps",
            value=f"{metrics['avg_steps']:,}",
            delta=f"{metrics['avg_steps'] - step_goal:+,} vs Goal",
            help="Mean number of steps recorded per day.",
        )
    with col3:
        st.metric(
            label="Highest Step Count",
            value=f"{metrics['max_steps']:,}",
            delta=metrics["best_date"],
            delta_color="off",
            help="Maximum steps recorded on a single day.",
        )
    with col4:
        st.metric(
            label="Lowest Step Count",
            value=f"{metrics['min_steps']:,}",
            delta=metrics["lowest_date"],
            delta_color="off",
            help="Minimum steps recorded on a single day.",
        )
    with col5:
        st.metric(
            label="Goal Achieved Days",
            value=f"{metrics['days_goal_met']} / {metrics['total_days']}",
            delta=f"{metrics['goal_percentage']:.1f}% success",
            help=f"Number of days where daily steps reached or exceeded {step_goal:,}.",
        )

    st.markdown("---")

    # ---------------- Visualizations Section ----------------
    st.markdown("### 📊 Activity Visualizations")

    tab1, tab2, tab3 = st.tabs([
        "📈 Daily Steps Over Time",
        "📊 Step Counts Comparison",
        "🎯 Steps vs. Daily Goal",
    ])

    with tab1:
        st.subheader("Daily Steps Over Time (Line Chart)")
        st.caption("Track how your step count progresses over the recorded time period.")
        fig1 = plot_daily_steps_line(clean_df, step_goal)
        st.pyplot(fig1, use_container_width=True)
        plt.close(fig1)

    with tab2:
        st.subheader("Daily Step Counts Comparison (Bar Chart)")
        st.caption("Compare individual day step counts alongside your overall daily average.")
        fig2 = plot_daily_steps_bar(clean_df)
        st.pyplot(fig2, use_container_width=True)
        plt.close(fig2)

    with tab3:
        st.subheader("Daily Steps Compared with Goal (Bar Chart)")
        st.caption("Visualize which days hit your target (green) versus days falling below goal (red).")
        fig3 = plot_goal_comparison_bar(clean_df, step_goal)
        st.pyplot(fig3, use_container_width=True)
        plt.close(fig3)

    st.markdown("---")

    # ---------------- Data Table Section ----------------
    st.markdown("### 📋 Daily Activity Records")

    # Prepare display dataframe
    display_df = clean_df.copy()
    display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d")
    display_df["Goal Status"] = display_df["Steps"].apply(
        lambda s: "✅ Goal Met" if s >= step_goal else "❌ Missed"
    )
    display_df["Goal Difference"] = display_df["Steps"] - step_goal

    # Reorder columns nicely
    cols_order = ["Date", "Steps", "Goal Status", "Goal Difference"]
    if "Calories_Burned" in display_df.columns:
        cols_order.append("Calories_Burned")
    display_df = display_df[cols_order]

    # Format numbers for clean presentation
    st.dataframe(
        display_df.style.format({
            "Steps": "{:,}",
            "Goal Difference": "{:+,}",
            "Calories_Burned": "{:,.0f}" if "Calories_Burned" in display_df.columns else "{}",
        }),
        use_container_width=True,
        hide_index=True,
    )

    # Optional download of cleaned table
    csv_export = display_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Download Cleaned Activity Records (CSV)",
        data=csv_export,
        file_name="daily_step_records_cleaned.csv",
        mime="text/csv",
    )


if __name__ == "__main__":
    main()

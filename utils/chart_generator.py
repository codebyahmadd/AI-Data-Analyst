import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def _get_column_series(df, column):
    """
    Safely return a selected dataframe column as a Series.

    Handles datasets that may contain duplicate column names.
    """

    if column not in df.columns:
        return pd.Series(dtype="object")

    data = df.loc[:, column]

    # If duplicate column names exist, Pandas returns a DataFrame.
    # Use the first matching column safely.
    if isinstance(data, pd.DataFrame):
        data = data.iloc[:, 0]

    return data


def _clean_column(df, column):
    """
    Return a cleaned copy of a selected column.
    Removes missing values.
    """

    data = _get_column_series(df, column)

    if data.empty:
        return pd.Series(dtype="object")

    return data.dropna()


def _apply_chart_layout(fig, title):
    """
    Apply a consistent professional layout to Plotly charts.
    """

    fig.update_layout(
        title=title,
        title_x=0.5,
        template="plotly_white",
        margin=dict(
            l=40,
            r=40,
            t=70,
            b=40
        ),
        hovermode="closest"
    )

    return fig


# =========================================================
# GET CATEGORICAL / CHART COLUMNS
# =========================================================

def get_chart_columns(df, max_unique=20):
    """
    Return columns suitable for categorical charts.

    Columns with a reasonable number of unique values
    are considered suitable for Bar and Pie charts.
    """

    suitable_columns = []

    for column in df.columns:

        data = _get_column_series(df, column)

        if data.dropna().empty:
            continue

        unique_count = data.nunique(dropna=True)

        if unique_count <= max_unique:
            suitable_columns.append(column)

    # Remove duplicate column names
    return list(dict.fromkeys(suitable_columns))


# =========================================================
# GET NUMERIC COLUMNS
# =========================================================

def get_numeric_columns(df):
    """
    Return all columns that contain usable numeric data.

    Handles numeric values stored as text and duplicate
    column names safely.
    """

    numeric_columns = []

    for column in df.columns:

        data = _get_column_series(df, column)

        if data.empty:
            continue

        converted = pd.to_numeric(
            data,
            errors="coerce"
        )

        if converted.notna().any():
            numeric_columns.append(column)

    # Remove duplicate column names
    return list(dict.fromkeys(numeric_columns))


# =========================================================
# BAR CHART
# =========================================================

def create_bar_chart(df, column):
    """
    Create a bar chart showing the top 10 values.
    """

    data = _clean_column(df, column)

    if data.empty:
        return None

    value_counts = (
        data
        .value_counts()
        .head(10)
        .reset_index()
    )

    value_counts.columns = [
        column,
        "Count"
    ]

    fig = px.bar(
        value_counts,
        x=column,
        y="Count",
        text="Count",
        title=f"Top 10 Values — {column}"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_xaxes(
        title_text=column
    )

    fig.update_yaxes(
        title_text="Count"
    )

    return _apply_chart_layout(
        fig,
        f"Top 10 Values — {column}"
    )


# =========================================================
# PIE CHART
# =========================================================

def create_pie_chart(df, column):
    """
    Create a pie chart showing the distribution
    of the top 10 categorical values.
    """

    data = _clean_column(df, column)

    if data.empty:
        return None

    value_counts = (
        data
        .value_counts()
        .head(10)
        .reset_index()
    )

    value_counts.columns = [
        column,
        "Count"
    ]

    fig = px.pie(
        value_counts,
        names=column,
        values="Count",
        title=f"Distribution — {column}",
        hole=0.35
    )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label"
    )

    return _apply_chart_layout(
        fig,
        f"Distribution — {column}"
    )


# =========================================================
# LINE CHART
# =========================================================

def create_line_chart(df, column):
    """
    Create a line chart showing the trend
    of a numeric column.
    """

    data = _get_column_series(df, column)

    if data.empty:
        return None

    data = pd.to_numeric(
        data,
        errors="coerce"
    ).dropna()

    if data.empty:
        return None

    chart_df = pd.DataFrame({
        "Index": range(1, len(data) + 1),
        column: data.to_numpy()
    })

    fig = px.line(
        chart_df,
        x="Index",
        y=column,
        markers=True,
        title=f"{column} Trend"
    )

    fig.update_xaxes(
        title_text="Record"
    )

    fig.update_yaxes(
        title_text=column
    )

    return _apply_chart_layout(
        fig,
        f"{column} Trend"
    )


# =========================================================
# HISTOGRAM
# =========================================================

def create_histogram(df, column):
    """
    Create a histogram showing the distribution
    of a numeric column.
    """

    data = _get_column_series(df, column)

    if data.empty:
        return None

    data = pd.to_numeric(
        data,
        errors="coerce"
    ).dropna()

    if data.empty:
        return None

    chart_df = pd.DataFrame({
        column: data.to_numpy()
    })

    fig = px.histogram(
        chart_df,
        x=column,
        nbins=30,
        title=f"{column} Distribution"
    )

    fig.update_xaxes(
        title_text=column
    )

    fig.update_yaxes(
        title_text="Frequency"
    )

    return _apply_chart_layout(
        fig,
        f"{column} Distribution"
    )


# =========================================================
# SCATTER PLOT
# =========================================================

def create_scatter_chart(df, x_column, y_column):
    """
    Create a scatter plot comparing two numeric columns.

    Handles:
    - Duplicate column names
    - Numeric values stored as text
    - Missing values
    - Invalid numeric values
    - Same X/Y column selection
    """

    if (
        x_column not in df.columns
        or y_column not in df.columns
    ):
        return None

    # X and Y must be different
    if x_column == y_column:
        return None

    # Safely retrieve both columns as Series
    x_data = _get_column_series(
        df,
        x_column
    )

    y_data = _get_column_series(
        df,
        y_column
    )

    if x_data.empty or y_data.empty:
        return None

    # Convert values to numeric
    x_data = pd.to_numeric(
        x_data,
        errors="coerce"
    )

    y_data = pd.to_numeric(
        y_data,
        errors="coerce"
    )

    # Build a clean dataframe using neutral internal names.
    # This avoids problems caused by duplicate source column names.
    chart_df = pd.DataFrame({
        "X": x_data.to_numpy(),
        "Y": y_data.to_numpy()
    })

    # Remove invalid/missing records
    chart_df = chart_df.dropna(
        subset=["X", "Y"]
    )

    if chart_df.empty:
        return None

    # Create scatter plot
    fig = px.scatter(
        chart_df,
        x="X",
        y="Y",
        title=f"{x_column} vs {y_column}"
    )

    fig.update_xaxes(
        title_text=x_column
    )

    fig.update_yaxes(
        title_text=y_column
    )

    return _apply_chart_layout(
        fig,
        f"{x_column} vs {y_column}"
    )


# =========================================================
# BOX PLOT
# =========================================================

def create_box_plot(df, column):
    """
    Create a box plot for a numeric column.
    """

    data = _get_column_series(
        df,
        column
    )

    if data.empty:
        return None

    data = pd.to_numeric(
        data,
        errors="coerce"
    ).dropna()

    if data.empty:
        return None

    chart_df = pd.DataFrame({
        column: data.to_numpy()
    })

    fig = px.box(
        chart_df,
        y=column,
        points="outliers",
        title=f"{column} Box Plot"
    )

    fig.update_yaxes(
        title_text=column
    )

    return _apply_chart_layout(
        fig,
        f"{column} Box Plot"
    )


# =========================================================
# CORRELATION HEATMAP
# =========================================================

def create_correlation_heatmap(df):
    """
    Create a correlation heatmap for numeric columns.
    """

    numeric_df = df.select_dtypes(
        include="number"
    )

    # At least two numeric columns are required
    if numeric_df.shape[1] < 2:
        return None

    # Remove columns containing no valid numeric values
    numeric_df = numeric_df.dropna(
        axis=1,
        how="all"
    )

    if numeric_df.shape[1] < 2:
        return None

    correlation = numeric_df.corr()

    fig = px.imshow(
        correlation,
        text_auto=".2f",
        aspect="auto",
        title="Correlation Heatmap",
        color_continuous_scale="RdBu_r",
        zmin=-1,
        zmax=1
    )

    fig.update_xaxes(
        title_text="Columns"
    )

    fig.update_yaxes(
        title_text="Columns"
    )

    return _apply_chart_layout(
        fig,
        "Correlation Heatmap"
    )
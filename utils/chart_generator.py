import plotly.express as px
import plotly.graph_objects as go


def get_chart_columns(df, max_unique=20):
    """
    Return columns suitable for categorical charts.
    """

    suitable_columns = []

    for column in df.columns:

        if df[column].nunique() <= max_unique:

            suitable_columns.append(column)

    return suitable_columns


def get_numeric_columns(df):
    """
    Return numeric columns.
    """

    return df.select_dtypes(include="number").columns.tolist()


# -----------------------------
# BAR
# -----------------------------
def create_bar_chart(df, column):

    value_counts = (
        df[column]
        .value_counts()
        .head(10)
        .reset_index()
    )

    value_counts.columns = [column, "Count"]

    fig = px.bar(
        value_counts,
        x=column,
        y="Count",
        text="Count",
        title=f"Top 10 Values - {column}"
    )

    fig.update_layout(
        template="plotly_white",
        title_x=0.5
    )

    return fig


# -----------------------------
# PIE
# -----------------------------
def create_pie_chart(df, column):

    value_counts = (
        df[column]
        .value_counts()
        .head(10)
        .reset_index()
    )

    value_counts.columns = [column, "Count"]

    fig = px.pie(
        value_counts,
        names=column,
        values="Count",
        title=f"Top 10 Values - {column}"
    )

    fig.update_layout(
        template="plotly_white",
        title_x=0.5
    )

    return fig


# -----------------------------
# LINE
# -----------------------------
def create_line_chart(df, column):

    fig = px.line(
        df,
        y=column,
        title=f"{column} Trend"
    )

    fig.update_layout(
        template="plotly_white",
        title_x=0.5
    )

    return fig


# -----------------------------
# HISTOGRAM
# -----------------------------
def create_histogram(df, column):

    fig = px.histogram(
        df,
        x=column,
        title=f"{column} Distribution"
    )

    fig.update_layout(
        template="plotly_white",
        title_x=0.5
    )

    return fig


# -----------------------------
# SCATTER
# -----------------------------
def create_scatter_chart(df, x_column, y_column):

    fig = px.scatter(
        df,
        x=x_column,
        y=y_column,
        title=f"{x_column} vs {y_column}"
    )

    fig.update_layout(
        template="plotly_white",
        title_x=0.5
    )

    return fig


# -----------------------------
# BOX
# -----------------------------
def create_box_plot(df, column):

    fig = px.box(
        df,
        y=column,
        title=f"{column} Box Plot"
    )

    fig.update_layout(
        template="plotly_white",
        title_x=0.5
    )

    return fig
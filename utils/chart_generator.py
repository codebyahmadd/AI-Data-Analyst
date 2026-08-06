import plotly.express as px


def get_chart_columns(df, max_unique=20):
    """
    Return columns suitable for Bar and Pie charts.
    Only categorical columns or columns with limited unique values are returned.
    """

    suitable_columns = []

    for column in df.columns:
        if df[column].nunique() <= max_unique:
            suitable_columns.append(column)

    return suitable_columns


def create_bar_chart(df, column):
    """
    Create a professional bar chart (Top 10 values).
    """

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
        title=f"Top 10 Values - {column}",
        text="Count"
    )

    fig.update_layout(
        template="plotly_white",
        xaxis_title=column,
        yaxis_title="Count",
        title_x=0.5
    )

    return fig


def create_pie_chart(df, column):
    """
    Create a professional pie chart (Top 10 values).
    """

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
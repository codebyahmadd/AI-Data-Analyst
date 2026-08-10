from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


def generate_pdf_report(df, insights):
    """
    Generate a professional PDF analysis report.
    """

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=20,
        spaceAfter=20,
    )

    heading_style = ParagraphStyle(
        "ReportHeading",
        parent=styles["Heading2"],
        fontSize=14,
        spaceBefore=12,
        spaceAfter=8,
    )

    body_style = ParagraphStyle(
        "ReportBody",
        parent=styles["BodyText"],
        fontSize=9,
        leading=13,
        spaceAfter=6,
    )

    story = []

    # -----------------------------
    # Report Title
    # -----------------------------
    story.append(
        Paragraph(
            "AI Data Analyst - Analysis Report",
            title_style,
        )
    )

    story.append(
        Paragraph(
            "Automatically generated analysis of the uploaded dataset.",
            body_style,
        )
    )

    story.append(Spacer(1, 10))

    # -----------------------------
    # Dataset Summary
    # -----------------------------
    story.append(
        Paragraph(
            "1. Dataset Summary",
            heading_style,
        )
    )

    missing_values = int(
        df.isnull().sum().sum()
    )

    duplicate_rows = int(
        df.duplicated().sum()
    )

    summary_data = [
        ["Metric", "Value"],
        ["Rows", f"{df.shape[0]:,}"],
        ["Columns", f"{df.shape[1]:,}"],
        ["Missing Values", f"{missing_values:,}"],
        ["Duplicate Rows", f"{duplicate_rows:,}"],
    ]

    summary_table = Table(
        summary_data,
        colWidths=[3 * inch, 2 * inch],
    )

    summary_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("PADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    story.append(summary_table)

    # -----------------------------
    # Column Information
    # -----------------------------
    story.append(
        Paragraph(
            "2. Column Information",
            heading_style,
        )
    )

    column_data = [
        ["Column", "Data Type", "Unique Values"]
    ]

    for column in df.columns:

        column_data.append(
            [
                str(column),
                str(df[column].dtype),
                f"{df[column].nunique():,}",
            ]
        )

    column_table = Table(
        column_data,
        repeatRows=1,
        colWidths=[2.7 * inch, 1.3 * inch, 1.5 * inch],
    )

    column_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("PADDING", (0, 0), (-1, -1), 5),
                ("FONTSIZE", (0, 0), (-1, -1), 8),
            ]
        )
    )

    story.append(column_table)

    # -----------------------------
    # AI Insights
    # -----------------------------
    story.append(
        Paragraph(
            "3. AI Insights",
            heading_style,
        )
    )

    for insight in insights:

        clean_insight = (
            str(insight)
            .replace("📊", "")
            .replace("✅", "")
            .replace("⚠️", "")
            .replace("🔢", "")
            .replace("📝", "")
            .replace("💡", "")
            .replace("📈", "")
        )

        story.append(
            Paragraph(
                f"• {clean_insight}",
                body_style,
            )
        )

    # -----------------------------
    # Statistical Summary
    # -----------------------------
    numeric_df = df.select_dtypes(
        include="number"
    )

    if not numeric_df.empty:

        story.append(
            Paragraph(
                "4. Statistical Summary",
                heading_style,
            )
        )

        statistics = numeric_df.describe().round(2)

        stats_data = [
            ["Statistic"] + [
                str(column)
                for column in statistics.columns
            ]
        ]

        for index, row in statistics.iterrows():

            stats_data.append(
                [str(index)] + [
                    str(value)
                    for value in row
                ]
            )

        stats_table = Table(
            stats_data,
            repeatRows=1,
        )

        stats_table.setStyle(
            TableStyle(
                [
                    (
                        "BACKGROUND",
                        (0, 0),
                        (-1, 0),
                        colors.lightgrey,
                    ),
                    (
                        "FONTNAME",
                        (0, 0),
                        (-1, 0),
                        "Helvetica-Bold",
                    ),
                    (
                        "GRID",
                        (0, 0),
                        (-1, -1),
                        0.5,
                        colors.grey,
                    ),
                    (
                        "FONTSIZE",
                        (0, 0),
                        (-1, -1),
                        7,
                    ),
                    (
                        "PADDING",
                        (0, 0),
                        (-1, -1),
                        4,
                    ),
                ]
            )
        )

        story.append(stats_table)

    # -----------------------------
    # Build PDF
    # -----------------------------
    document.build(story)

    buffer.seek(0)

    return buffer.getvalue()
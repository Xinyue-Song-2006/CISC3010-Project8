"""Render the four-page final report PDF from the measured experiment outputs."""

from __future__ import annotations

import csv
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.platypus import (
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)
from reportlab.graphics.shapes import Drawing, Rect, String, Line, Polygon


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "project8_report.pdf"


def diagram() -> Drawing:
    drawing = Drawing(480, 185)
    boxes = [
        (15, 125, 110, 35, "Edge list", colors.HexColor("#E5E7EB")),
        (185, 125, 110, 35, "Spark driver", colors.HexColor("#DBEAFE")),
        (350, 145, 110, 35, "Worker 1", colors.HexColor("#DCFCE7")),
        (350, 95, 110, 35, "Worker 2", colors.HexColor("#DCFCE7")),
        (185, 35, 110, 35, "Cached links RDD", colors.HexColor("#FEF3C7")),
        (350, 35, 110, 35, "Metrics + ranks", colors.HexColor("#FCE7F3")),
    ]
    for x, y, width, height, label, fill in boxes:
        drawing.add(Rect(x, y, width, height, rx=6, ry=6, fillColor=fill, strokeColor=colors.HexColor("#374151"), strokeWidth=1))
        drawing.add(String(x + width / 2, y + 13, label, fontName="Helvetica-Bold", fontSize=9, textAnchor="middle"))
    for x1, y1, x2, y2 in [(125, 142, 185, 142), (295, 145, 350, 162), (295, 135, 350, 112), (240, 125, 240, 70), (295, 52, 350, 52)]:
        drawing.add(Line(x1, y1, x2, y2, strokeColor=colors.HexColor("#4B5563"), strokeWidth=1.2))
        drawing.add(Polygon([x2, y2, x2 - 5, y2 + 3, x2 - 5, y2 - 3], fillColor=colors.HexColor("#4B5563"), strokeColor=colors.HexColor("#4B5563")))
    drawing.add(String(240, 92, "repeated PageRank iterations", fontName="Helvetica", fontSize=8, textAnchor="middle", fillColor=colors.HexColor("#4B5563")))
    return drawing


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#D1D5DB"))
    canvas.line(1.6 * cm, 1.25 * cm, A4[0] - 1.6 * cm, 1.25 * cm)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#6B7280"))
    canvas.drawString(1.6 * cm, 0.8 * cm, "CISC3010 Project 8 | Spark Caching and Distributed Execution")
    canvas.drawRightString(A4[0] - 1.6 * cm, 0.8 * cm, f"Page {doc.page}")
    canvas.restoreState()


def p(text: str, style: ParagraphStyle) -> Paragraph:
    return Paragraph(text, style)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()
    title = ParagraphStyle("Title", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=23, leading=28, textColor=colors.HexColor("#111827"), alignment=TA_LEFT, spaceAfter=10)
    subtitle = ParagraphStyle("Subtitle", parent=styles["Normal"], fontName="Helvetica", fontSize=12, leading=16, textColor=colors.HexColor("#4B5563"), spaceAfter=15)
    h1 = ParagraphStyle("H1", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=15, leading=19, textColor=colors.HexColor("#1D4ED8"), spaceBefore=3, spaceAfter=8)
    h2 = ParagraphStyle("H2", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=11.5, leading=15, textColor=colors.HexColor("#111827"), spaceBefore=5, spaceAfter=5)
    body = ParagraphStyle("Body", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.5, leading=13.2, textColor=colors.HexColor("#1F2937"), spaceAfter=7)
    small = ParagraphStyle("Small", parent=body, fontSize=8.2, leading=10.5, textColor=colors.HexColor("#4B5563"))
    bullet = ParagraphStyle("Bullet", parent=body, leftIndent=13, firstLineIndent=-8, bulletIndent=3, spaceAfter=4)
    callout = ParagraphStyle("Callout", parent=body, fontName="Helvetica-Bold", fontSize=11, leading=15, textColor=colors.HexColor("#1E3A8A"), backColor=colors.HexColor("#EFF6FF"), borderColor=colors.HexColor("#BFDBFE"), borderWidth=0.7, borderPadding=8, spaceBefore=4, spaceAfter=10)

    story = []
    story.append(p("Spark Caching and Distributed Execution", title))
    story.append(p("CISC3010 individual project | Project 8 | Final report baseline", subtitle))
    story.append(p("Research question", h1))
    story.append(p("When an iterative Spark application reuses the same input RDD, how much does caching change execution time, and when can cache materialization dominate the benefit?", callout))
    story.append(p("1. Architecture", h1))
    story.append(p("The application uses one Spark driver and two local worker processes in <font name='Courier'>local-cluster[2,1,1024]</font>. The driver reads a deterministic directed graph, groups outgoing neighbors into a shared <font name='Courier'>links</font> RDD, and repeats PageRank. Each iteration joins the links RDD with current ranks, emits contributions, reduces by destination node, and materializes the new rank vector.", body))
    story.append(diagram())
    story.append(Spacer(1, 6))
    story.append(p("The cached configuration persists <font name='Courier'>links</font> with <font name='Courier'>MEMORY_ONLY</font>. The uncached configuration uses the same lineage without persistence. Both configurations use two workers, one core per worker, four partitions, identical input seeds, and identical iteration counts.", body))
    story.append(p("2. Implementation and correctness", h1))
    story.append(p("The PageRank recurrence is <font name='Courier'>rank_new(v) = 0.15/N + 0.85 * sum(rank(u)/out_degree(u))</font>. A sequential reference implementation uses the same recurrence. The verifier compares every node and reports the maximum absolute error. On the six-iteration demo, both cached and uncached outputs passed with a maximum absolute error of approximately 5e-13 and checksum 1.0.", body))

    story.append(PageBreak())
    story.append(p("3. Experiment design", h1))
    story.append(p("The experiment uses three deterministic graph sizes, six iterations, four partitions, two local workers, and two repetitions per cache setting. The first <font name='Courier'>count()</font> on the shared links RDD measures initial materialization separately. The following five timings measure subsequent reuse. Raw JSON and CSV files preserve the evidence used to produce the figures.", body))
    design_data = [
        [p("Factor", h2), p("Controlled choice", h2), p("Reason", h2)],
        ["Workload", "2,000 / 10,000 / 30,000 edges", "Tests reuse as data grows"],
        ["Cache", "Off versus MEMORY_ONLY", "Isolates persistence effect"],
        ["Iterations", "6 per run", "Separates first materialization from reuse"],
        ["Resources", "2 workers, 1 core each, 4 partitions", "Same limit for both conditions"],
        ["Repetitions", "2 per condition", "Reports measurement variation"],
    ]
    table = Table(design_data, colWidths=[2.7 * cm, 6.6 * cm, 7.0 * cm], repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DBEAFE")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#1E3A8A")),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CBD5E1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTNAME", (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 1), (-1, -1), 8.5),
        ("LEADING", (0, 1), (-1, -1), 11),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    story.append(table)
    story.append(Spacer(1, 10))
    story.append(p("4. Results", h1))
    story.append(p("Times are seconds and show mean +/- standard deviation across two repetitions. The cached run pays a higher initial materialization cost, but its later iterations become relatively cheaper as the graph grows.", body))
    result_data = [
        [p("Edges", h2), p("Cache", h2), p("Materialize", h2), p("Later iter.", h2), p("Total", h2)],
        ["2,000", "Off", "5.753 +/- 0.361", "4.265 +/- 0.231", "36.397 +/- 1.968"],
        ["2,000", "On", "6.782 +/- 0.119", "4.333 +/- 0.020", "38.281 +/- 0.270"],
        ["10,000", "Off", "5.932 +/- 0.074", "4.450 +/- 0.046", "38.044 +/- 0.201"],
        ["10,000", "On", "6.772 +/- 0.059", "4.427 +/- 0.089", "38.559 +/- 0.448"],
        ["30,000", "Off", "6.238 +/- 0.263", "4.843 +/- 0.037", "40.680 +/- 0.618"],
        ["30,000", "On", "7.166 +/- 0.232", "4.585 +/- 0.263", "40.385 +/- 2.108"],
    ]
    result_table = Table(result_data, colWidths=[2.4 * cm, 2.0 * cm, 4.2 * cm, 4.0 * cm, 4.0 * cm], repeatRows=1)
    result_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DBEAFE")),
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CBD5E1")),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("FONTSIZE", (0, 1), (-1, -1), 8.3),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
        ("BACKGROUND", (1, 2), (1, 2), colors.HexColor("#EFF6FF")),
        ("BACKGROUND", (1, 4), (1, 4), colors.HexColor("#EFF6FF")),
        ("BACKGROUND", (1, 6), (1, 6), colors.HexColor("#EFF6FF")),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    story.append(result_table)
    story.append(Spacer(1, 7))
    story.append(p("The cached subsequent-iteration speedup was 0.984x on the small workload, 1.005x on the medium workload, and 1.056x on the large workload. Caching therefore helps later reuse most clearly on the largest input, but it does not guarantee lower end-to-end runtime when the materialization cost is large relative to the workload.", body))

    story.append(PageBreak())
    story.append(p("5. Visual evidence", h1))
    story.append(p("The application prints the Spark UI URL, iteration timings, partition count, storage level, and result checksum. The submitted raw CSV can be traced directly to the figures below.", body))
    for filename, caption in [("cache_speedup.png", "Figure 1. Mean time of subsequent iterations."), ("iteration_timing.png", "Figure 2. Initial materialization versus later reuse.")]:
        image_path = ROOT / "results" / filename
        story.append(Image(str(image_path), width=16.7 * cm, height=9.2 * cm))
        story.append(p(caption, small))
        story.append(Spacer(1, 4))
    story.append(p("6. Connection to the reading", h1))
    story.append(p("The project applies the RDD design idea from Zaharia et al. (2012). Persistence stores computed partitions for reuse, while lineage preserves the information needed to recompute a lost partition. This project simplifies the paper's cluster-scale fault model to two local workers and focuses on timing, cache blocks, stages, and correctness rather than throughput at scale.", body))

    story.append(PageBreak())
    story.append(p("7. Interpretation and limitations", h1))
    story.append(p("The measurements support the mechanism: the cached run pays for materialization once, then avoids recomputing the shared links lineage during later iterations. The small workload shows a slowdown because Spark startup and cache materialization dominate. The medium workload is effectively a tie. The large workload shows a 5.6% improvement in subsequent iterations and a small end-to-end improvement, with higher variation in the cached total time.", body))
    story.append(p("All workers share one laptop, so these results demonstrate distributed execution and RDD behavior rather than multi-machine cluster performance. The workload is static and uses RDDs rather than DataFrames. The optional executor-failure and skew experiments remain outside the core scope. The metadata in the JSON output explicitly records the local master, partition budget, and checksum so that these limitations are visible.", body))
    story.append(p("8. Post-presentation changes", h1))
    story.append(p("The presentation is scheduled for 26 October 2026. This report was prepared before that presentation, so the final submission must append the actual feedback and the code or documentation changes made in response. The current repository already contains the additions to the Spark example: a deterministic generator, cache toggle, separate materialization timing, sequential verifier, repeated experiment runner, raw-result retention, and figure-generation scripts.", body))
    story.append(p("9. AI-use statement", h1))
    story.append(p("AI coding assistance helped with scaffolding, debugging suggestions, documentation wording, and test planning. I validated the submitted code by running the Spark demo, checking logs and output files, comparing against the sequential reference, and inspecting the generated figures. I cite the Spark documentation and the RDD paper, and I identify custom experiment and verification code in the repository.", body))
    story.append(p("References", h1))
    story.append(p("[1] Matei Zaharia et al. “Resilient Distributed Datasets: A Fault-Tolerant Abstraction for In-Memory Cluster Computing.” NSDI, 2012.<br/>[2] Apache Spark. “RDD Programming Guide.” https://spark.apache.org/docs/latest/rdd-programming-guide.html", small))

    doc = SimpleDocTemplate(str(OUT), pagesize=A4, rightMargin=1.6 * cm, leftMargin=1.6 * cm, topMargin=1.45 * cm, bottomMargin=1.65 * cm, title="Spark Caching and Distributed Execution", author="Song Xinyue")
    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(OUT)


if __name__ == "__main__":
    main()

from pathlib import Path
import html
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Preformatted,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(__file__).with_name("presentation_script_2026-10-26.md")
OUTPUT = ROOT / "output" / "pdf" / "presentation_script_2026-10-26.pdf"


def register_fonts() -> None:
    font_dir = Path(r"C:\Windows\Fonts")
    pdfmetrics.registerFont(TTFont("NotoSansSC", str(font_dir / "NotoSansSC-Regular.ttf")))
    pdfmetrics.registerFont(TTFont("NotoSansSC-Bold", str(font_dir / "simhei.ttf")))
    pdfmetrics.registerFont(TTFont("Consolas", str(font_dir / "consola.ttf")))


def inline_markup(text: str) -> str:
    """Convert the small subset of Markdown used in the script to ReportLab markup."""
    text = html.escape(text, quote=False)
    placeholders: list[str] = []

    def save(value: str) -> str:
        placeholders.append(value)
        return f"@@PLACEHOLDER{len(placeholders) - 1}@@"

    text = re.sub(r"\*\*(.+?)\*\*", lambda m: save(f"<b>{m.group(1)}</b>"), text)
    text = re.sub(r"`([^`]+)`", lambda m: save(f"<font name='Consolas'>{m.group(1)}</font>"), text)
    for index, value in enumerate(placeholders):
        text = text.replace(f"@@PLACEHOLDER{index}@@", value)
    return text


def footer(canvas, doc) -> None:
    canvas.saveState()
    canvas.setFont("NotoSansSC", 8)
    canvas.setFillColor(colors.HexColor("#6B7280"))
    canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, f"Project 8 Presentation Script  |  {doc.page}")
    canvas.restoreState()


def build_story() -> list:
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="DocTitle",
        parent=styles["Title"],
        fontName="NotoSansSC-Bold",
        fontSize=19,
        leading=24,
        alignment=TA_CENTER,
        textColor=colors.HexColor("#102A43"),
        spaceAfter=6 * mm,
    ))
    styles.add(ParagraphStyle(
        name="H2Custom",
        parent=styles["Heading2"],
        fontName="NotoSansSC-Bold",
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#0B4F6C"),
        spaceBefore=5 * mm,
        spaceAfter=2 * mm,
        keepWithNext=True,
    ))
    styles.add(ParagraphStyle(
        name="H3Custom",
        parent=styles["Heading3"],
        fontName="NotoSansSC-Bold",
        fontSize=11.5,
        leading=15,
        textColor=colors.HexColor("#334E68"),
        spaceBefore=3 * mm,
        spaceAfter=1.5 * mm,
        keepWithNext=True,
    ))
    styles.add(ParagraphStyle(
        name="BodyCustom",
        parent=styles["BodyText"],
        fontName="NotoSansSC",
        fontSize=9.4,
        leading=13.5,
        spaceAfter=2.2 * mm,
        alignment=TA_LEFT,
    ))
    styles.add(ParagraphStyle(
        name="NoteCustom",
        parent=styles["BodyText"],
        fontName="NotoSansSC",
        fontSize=9.1,
        leading=13,
        leftIndent=5 * mm,
        rightIndent=3 * mm,
        borderColor=colors.HexColor("#B8C6D1"),
        borderWidth=0.5,
        borderPadding=4,
        backColor=colors.HexColor("#F5F8FA"),
        spaceBefore=1.5 * mm,
        spaceAfter=2.5 * mm,
    ))
    styles.add(ParagraphStyle(
        name="BulletCustom",
        parent=styles["BodyText"],
        fontName="NotoSansSC",
        fontSize=9.2,
        leading=13,
        leftIndent=6 * mm,
        firstLineIndent=-4 * mm,
        spaceAfter=1.4 * mm,
    ))
    styles.add(ParagraphStyle(
        name="CodeLabel",
        parent=styles["BodyText"],
        fontName="Consolas",
        fontSize=8.5,
        leading=11,
        leftIndent=4 * mm,
        rightIndent=4 * mm,
        borderColor=colors.HexColor("#CBD5E1"),
        borderWidth=0.5,
        borderPadding=5,
        backColor=colors.HexColor("#F1F5F9"),
        spaceBefore=1 * mm,
        spaceAfter=2.5 * mm,
    ))

    story = []
    in_code = False
    code_lines: list[str] = []
    for raw in lines:
        line = raw.rstrip()
        if line.strip().startswith("```"):
            if in_code:
                story.append(Preformatted("\n".join(code_lines), styles["CodeLabel"]))
                code_lines = []
                in_code = False
            else:
                in_code = True
            continue
        if in_code:
            code_lines.append(line)
            continue
        if not line.strip():
            story.append(Spacer(1, 1.2 * mm))
            continue
        if line.strip() == "---":
            story.append(Spacer(1, 2 * mm))
            rule = Table([[""]], colWidths=[174 * mm], rowHeights=[0.5 * mm])
            rule.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#CBD5E1"))]))
            story.append(rule)
            story.append(Spacer(1, 1.5 * mm))
            continue
        if line.startswith("# "):
            story.append(Paragraph(inline_markup(line[2:]), styles["DocTitle"]))
            continue
        if line.startswith("## "):
            story.append(Paragraph(inline_markup(line[3:]), styles["H2Custom"]))
            continue
        if line.startswith("### "):
            story.append(Paragraph(inline_markup(line[4:]), styles["H3Custom"]))
            continue
        if line.startswith("- "):
            story.append(Paragraph("• " + inline_markup(line[2:]), styles["BulletCustom"]))
            continue
        if re.match(r"^\d+\. ", line):
            story.append(Paragraph(inline_markup(line), styles["BulletCustom"]))
            continue
        if line.startswith("**[") and line.endswith("**"):
            story.append(Paragraph(inline_markup(line), styles["NoteCustom"]))
            continue
        story.append(Paragraph(inline_markup(line), styles["BodyCustom"]))
    return story


def main() -> None:
    register_fonts()
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=17 * mm,
        title="Project 8 Presentation Script",
        author="CISC3010 Project 8",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
    doc.addPageTemplates([PageTemplate(id="script", frames=[frame], onPage=footer)])
    doc.build(build_story())
    print(OUTPUT)


if __name__ == "__main__":
    main()

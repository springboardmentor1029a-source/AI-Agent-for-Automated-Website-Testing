from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
import os


def generate_pdf_report(report, output_path):
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph("<b>AI Automated Web Test Report</b>", styles["Title"]))
    story.append(Spacer(1, 0.3 * inch))

    # Summary
    story.append(Paragraph(f"<b>Run ID:</b> {report.get('id')}", styles["Normal"]))
    story.append(Paragraph(f"<b>Status:</b> {report.get('status')}", styles["Normal"]))
    story.append(Paragraph(f"<b>Duration:</b> {report.get('duration')} seconds", styles["Normal"]))
    story.append(Paragraph(f"<b>Total Steps:</b> {report.get('total_steps')}", styles["Normal"]))
    story.append(Spacer(1, 0.2 * inch))

    # Instruction & Target (IMPORTANT)
    story.append(Paragraph("<b>Test Instruction:</b>", styles["Heading2"]))
    story.append(Paragraph(report.get("instruction", ""), styles["Normal"]))
    story.append(Spacer(1, 0.1 * inch))

    story.append(Paragraph("<b>Target URL:</b>", styles["Heading2"]))
    story.append(Paragraph(report.get("target", ""), styles["Normal"]))
    story.append(Spacer(1, 0.3 * inch))

    # Steps
    for step in report.get("step_results", []):
        story.append(Paragraph(
            f"<b>Step {step['step']}:</b> {step['action']} ({step['status']})",
            styles["Heading3"]
        ))

        if step.get("detail"):
            story.append(Paragraph(step["detail"], styles["Normal"]))

        screenshot = step.get("screenshot")
        if screenshot:
            img_path = screenshot.lstrip("/")
            if os.path.exists(img_path):
                story.append(Spacer(1, 0.1 * inch))
                story.append(Image(img_path, width=6 * inch, height=3.5 * inch))
                story.append(Spacer(1, 0.2 * inch))

    doc = SimpleDocTemplate(output_path, pagesize=A4)
    doc.build(story)

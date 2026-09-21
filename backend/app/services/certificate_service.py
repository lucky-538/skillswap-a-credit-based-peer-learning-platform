import os
from datetime import datetime
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

CERT_STORAGE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "static", "certificates")
os.makedirs(CERT_STORAGE_DIR, exist_ok=True)


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_decorations()
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_decorations(self):
        width, height = landscape(letter)
        self.saveState()
        # Outer Gold/Navy Border
        self.setStrokeColor(colors.HexColor("#1E3A8A")) # Deep Navy
        self.setLineWidth(6)
        self.rect(20, 20, width - 40, height - 40)

        # Inner Thin Gold Border
        self.setStrokeColor(colors.HexColor("#D97706")) # Warm Gold
        self.setLineWidth(2)
        self.rect(28, 28, width - 56, height - 56)

        # Corner Ornaments
        self.setFillColor(colors.HexColor("#D97706"))
        self.circle(35, 35, 4, stroke=0, fill=1)
        self.circle(width - 35, 35, 4, stroke=0, fill=1)
        self.circle(35, height - 35, 4, stroke=0, fill=1)
        self.circle(width - 35, height - 35, 4, stroke=0, fill=1)
        self.restoreState()


def generate_certificate_pdf(
    certificate_id: str,
    student_name: str,
    course_title: str,
    issue_date: datetime,
    grade: str = "Distinction",
    instructor_name: str = "SkillSwap Campus Faculty"
) -> str:
    pdf_filename = f"{certificate_id}.pdf"
    file_path = os.path.join(CERT_STORAGE_DIR, pdf_filename)

    width, height = landscape(letter)
    doc = SimpleDocTemplate(
        file_path,
        pagesize=landscape(letter),
        leftMargin=50,
        rightMargin=50,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'CertTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=26,
        leading=32,
        textColor=colors.HexColor("#1E3A8A"),
        alignment=1 # Center
    )

    subtitle_style = ParagraphStyle(
        'CertSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=13,
        leading=18,
        textColor=colors.HexColor("#4B5563"),
        alignment=1
    )

    name_style = ParagraphStyle(
        'CertName',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=28,
        leading=34,
        textColor=colors.HexColor("#111827"),
        alignment=1
    )

    course_style = ParagraphStyle(
        'CertCourse',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=26,
        textColor=colors.HexColor("#2563EB"),
        alignment=1
    )

    meta_style = ParagraphStyle(
        'CertMeta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#6B7280"),
        alignment=1
    )

    story = [
        Spacer(1, 10),
        Paragraph("SKILLSWAP CAMPUS ACADEMY", title_style),
        Paragraph("DEPARTMENT OF HIGHER EDUCATION & PEER COLLABORATION", subtitle_style),
        Spacer(1, 12),
        Paragraph("— CERTIFICATE OF COMPLETION —", ParagraphStyle('SubSub', parent=subtitle_style, fontName='Helvetica-Bold', fontSize=14, textColor=colors.HexColor("#D97706"))),
        Spacer(1, 14),
        Paragraph("This is to proudly certify that", subtitle_style),
        Spacer(1, 8),
        Paragraph(student_name, name_style),
        Spacer(1, 8),
        Paragraph("has diligently studied, met all academic module criteria, passed every assessment,", subtitle_style),
        Paragraph(f"and successfully completed the certified curriculum in", subtitle_style),
        Spacer(1, 6),
        Paragraph(course_title, course_style),
        Spacer(1, 16),
    ]

    date_str = issue_date.strftime("%B %d, %Y")
    
    footer_data = [
        [
            Paragraph(f"<b>Issue Date:</b> {date_str}<br/><b>Grade:</b> {grade}", ParagraphStyle('LeftFoot', parent=meta_style, alignment=0)),
            Paragraph(f"<b>Certificate ID:</b><br/>{certificate_id}", ParagraphStyle('MidFoot', parent=meta_style, alignment=1)),
            Paragraph(f"<b>{instructor_name}</b><br/>Authorized Academic Dean", ParagraphStyle('RightFoot', parent=meta_style, alignment=2))
        ]
    ]

    t = Table(footer_data, colWidths=[2.5 * inch, 2.5 * inch, 2.5 * inch])
    t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 0),
    ]))

    story.append(t)
    story.append(Spacer(1, 10))
    story.append(Paragraph(f"Verify this credential at: <u>http://localhost:5173/verify-certificate/{certificate_id}</u>", ParagraphStyle('VerifyLink', parent=meta_style, fontSize=8, textColor=colors.HexColor("#9CA3AF"))))

    doc.build(story, canvasmaker=NumberedCanvas)
    return file_path

#!/usr/bin/env python3
"""Convert cover letter + resume DOCX to single 2-page PDF."""

import sys
import os
from fpdf import FPDF
from docx import Document
from docx.shared import Inches, Pt, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH

ONEDRIVE = "/mnt/c/Users/owner/OneDrive/ABHIMANYU-2.0"
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
MARGIN = 0.75  # inches

class AppPDF(FPDF):
    def __init__(self):
        super().__init__(orientation='P', unit='in', format='Letter')
        self.set_auto_page_break(auto=True, margin=MARGIN)
        # Add DejaVu Sans fonts
        self.add_font('DV', '', os.path.join(FONT_DIR, 'DejaVuSans.ttf'), uni=True)
        self.add_font('DV', 'B', os.path.join(FONT_DIR, 'DejaVuSans-Bold.ttf'), uni=True)
        self.set_margin(MARGIN)

    def _render_paragraph(self, p, width):
        """Render a single paragraph preserving bold/alignment/size."""
        if not p.text.strip():
            self.ln(0.08)
            return

        text = p.text
        alignment = p.alignment

        # Determine base size from runs or default
        base_size = 10
        for run in p.runs:
            if run.font.size and run.font.size > 0:
                sz = run.font.size / 12700  # EMU to pt
                if sz > 0:
                    base_size = sz
                break

        # Handle section headers (all caps, short, bold style name)
        style_name = p.style.name if p.style else ""
        is_header = ('Heading' in style_name or 'Header' in style_name)

        # Check if it looks like a section header (all caps, bold, short)
        words = text.strip().split()
        if len(words) <= 8 and text.isupper() and len(text.strip()) < 60:
            is_header = True

        # Set font
        if is_header:
            self.set_font('DV', 'B', base_size + 2)
        else:
            self.set_font('DV', '', base_size)

        # Set alignment
        if alignment == WD_ALIGN_PARAGRAPH.CENTER:
            self.set_x(MARGIN)
            self.multi_cell(width, 0.18, text, align='C')
        elif is_header and not any(c.islower() for c in text.strip()):
            self.set_x(MARGIN)
            self.multi_cell(width, 0.16, text.strip().upper(), align='L')
            # Draw underline
            y = self.get_y() - 0.02
            self.set_line_width(0.012)
            self.line(MARGIN, y, MARGIN + width, y)
            self.ln(0.04)
        else:
            # Handle bold prefixes in bullets
            self.set_x(MARGIN)
            self.multi_cell(width, 0.16, text, align='L')

        self.ln(0.02)

    def render_docx(self, docx_path):
        """Render a DOCX file to PDF pages."""
        doc = Document(docx_path)
        page_width = self.w - 2 * MARGIN

        for p in doc.paragraphs:
            self._render_paragraph(p, page_width)

def generate(company):
    date_str = "2026-06-24"
    role = "Manager_SO_Dasher_Logistics"
    folder = f"{ONEDRIVE}/{date_str}/{company}"
    lfolder = f"/home/aryan/opencode_test/ABHIMANYU-2.0/{date_str}/{company}"
    os.makedirs(folder, exist_ok=True)
    os.makedirs(lfolder, exist_ok=True)

    cover_path = os.path.join(folder, f"Cover_Letter_{company}_{role}.docx")
    resume_path = os.path.join(folder, f"Aman_Kumar_{company}_{role}.docx")

    if not os.path.exists(cover_path):
        cover_path = os.path.join(lfolder, os.path.basename(cover_path))
    if not os.path.exists(resume_path):
        resume_path = os.path.join(lfolder, os.path.basename(resume_path))

    pdf = AppPDF()

    # Page 1: Cover Letter
    pdf.add_page()
    pdf.render_docx(cover_path)

    # Page 2: Resume
    pdf.add_page()
    pdf.render_docx(resume_path)

    outpath = os.path.join(folder, f"Aman_Kumar_{company}_{role}_Application.pdf")
    try:
        pdf.output(outpath)
    except PermissionError:
        outpath = os.path.join(lfolder, os.path.basename(outpath))
        pdf.output(outpath)
    pdf.output(os.path.join(lfolder, os.path.basename(outpath)))
    print(f"PDF: {outpath}")

if __name__ == "__main__":
    company = sys.argv[1] if len(sys.argv) > 1 else "DoorDash_Canada"
    generate(company)

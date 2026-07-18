#!/usr/bin/env python3
"""Reads DOCX files (resume + cover letter) and outputs a single merged PDF."""

import sys
import os
from docx import Document
from docx.shared import Pt
from weasyprint import HTML
from pypdf import PdfWriter

ONEDRIVE = "/home/aryan/ABHIMANYU-2.0-output"
LINUX = "/home/aryan/opencode_test/ABHIMANYU-2.0"

CONFIG = {
    "Methanex": {"font": "Calibri", "size": Pt(11)},
    "Clio": "SrMgr_Integration",
    "Providence_Healthcare": {"font": "Calibri", "size": Pt(11)},
    "Indeed": {"font": "Liberation Sans", "size": Pt(10)},
    "Deloitte": {"font": "Calibri", "size": Pt(10)},
}

DATES = {
    "Indeed": "2026-06-20", "Methanex": "2026-06-21", "Deloitte": "2026-06-19",
    "Hiive": "2026-06-22", "Providence_Healthcare": "2026-06-22"
}

ROLE_STR = {
    "Methanex": "Director_Strategy", "Hiive": "Associate_Operations_Strategy",
    "Providence_Healthcare": "Director_Clinical_Operations", "Indeed": "SrMgr_Integration", "Clio": "SrMgr_Integration"
}

FONT_MAP = {"Calibri": "Calibri, sans-serif", "Liberation Sans": "Liberation Sans, sans-serif"}

def get_date(company):
    return DATES.get(company, "2026-06-22")

def html_esc(text):
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')

def docx_to_html(docx_path):
    doc = Document(docx_path)
    style = doc.styles['Normal']
    default_font = style.font.name or 'Calibri'
    default_size = style.font.size or Pt(11)
    css_font = FONT_MAP.get(default_font, f'{default_font}, sans-serif')

    html_parts = [f'''<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
@page {{ margin: 0.75in; size: letter; }}
body {{ font-family: {css_font}; font-size: {default_size.pt}pt; color: #000; line-height: 1.15; }}
h1 {{ font-size: 16pt; font-weight: bold; text-align: center; margin: 0; padding: 0; }}
.contact {{ text-align: center; font-size: 9pt; color: #505050; margin: 0 0 4pt 0; white-space: pre-wrap; }}
.section-header {{ font-size: 12pt; font-weight: bold; border-bottom: 1px solid #000; margin-top: 10pt; margin-bottom: 3pt; text-transform: uppercase; }}
.body-text {{ font-size: {default_size.pt}pt; margin: 0 0 2pt 0; white-space: pre-wrap; }}
.bullet {{ font-size: {default_size.pt}pt; margin: 0 0 1pt 0; padding-left: 25pt; text-indent: -25pt; }}
.bold {{ font-weight: bold; }}
.italic {{ font-style: italic; }}
.sig {{ font-size: {default_size.pt}pt; margin: 0; }}
.link {{ color: #0563C1; text-decoration: underline; }}
</style></head><body>
''']

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            html_parts.append('<br/>')
            continue

        alignment = para.alignment
        is_center = alignment is not None and alignment.value == 1
        runs = para.runs
        all_bold = all(r.bold for r in runs if r.text.strip())
        all_upper = text.isupper() and len(text) > 3
        is_bullet = text.startswith('•') or text.startswith('- ')

        if is_bullet:
            clean = text.lstrip('•- ')
            if ' — ' in clean:
                prefix, rest = clean.split(' — ', 1)
                html_parts.append(f'<p class="bullet"><span class="bold">{html_esc(prefix)}</span> — {html_esc(rest)}</p>')
            else:
                html_parts.append(f'<p class="bullet">{html_esc(clean)}</p>')
        elif all_bold and all_upper and len(text) > 3:
            html_parts.append(f'<p class="section-header">{html_esc(text)}</p>')
        elif is_center and len(runs) == 1 and runs[0].bold and runs[0].font.size and runs[0].font.size.pt >= 14:
            html_parts.append(f'<h1>{html_esc(text)}</h1>')
        else:
            inline_html = ''
            for run in runs:
                t = html_esc(run.text)
                if run.bold and run.italic:
                    inline_html += f'<b><i>{t}</i></b>'
                elif run.bold:
                    inline_html += f'<b>{t}</b>'
                elif run.italic:
                    inline_html += f'<i>{t}</i>'
                else:
                    inline_html += t
            if is_center:
                html_parts.append(f'<p class="contact">{inline_html}</p>')
            elif all_bold and not all_upper:
                html_parts.append(f'<p class="body-text"><b>{html_esc(text)}</b></p>')
            else:
                html_parts.append(f'<p class="body-text">{inline_html}</p>')

    html_parts.append('</body></html>')
    return '\n'.join(html_parts)

def generate(company):
    config = CONFIG.get(company, CONFIG["Methanex"])
    date_str = get_date(company)
    role_str = ROLE_STR.get(company, "Unknown")

    folder = f"{ONEDRIVE}/{date_str}/{company}"
    lfolder = f"{LINUX}/{date_str}/{company}"

    resume_docx = os.path.join(folder, f"Aman_Kumar_{company}_{role_str}.docx")
    cover_docx = os.path.join(folder, f"Cover_Letter_{company}_{role_str}.docx")
    merged_pdf_name = f"Aman_Kumar_{company}_Application.pdf"

    pdf_paths = []
    for docx_path in [resume_docx, cover_docx]:
        if not os.path.exists(docx_path):
            docx_path = os.path.join(lfolder, os.path.basename(docx_path))
        if not os.path.exists(docx_path):
            print(f"SKIP: {docx_path} not found")
            continue
        html_str = docx_to_html(docx_path)
        pdf_path = os.path.join(lfolder, f"_{os.path.basename(docx_path)}.pdf")
        HTML(string=html_str).write_pdf(pdf_path)
        pdf_paths.append(pdf_path)

    if len(pdf_paths) >= 2:
        writer = PdfWriter()
        for pdf_path in pdf_paths:
            writer.append(pdf_path)
        merged_path = os.path.join(folder, merged_pdf_name)
        try:
            writer.write(merged_path)
        except PermissionError:
            merged_path = os.path.join(lfolder, merged_pdf_name)
            writer.write(merged_path)
        writer.write(os.path.join(lfolder, merged_pdf_name))
        print(f"Merged PDF: {merged_path}")
    elif len(pdf_paths) == 1:
        print(f"Only one PDF generated, no merge needed")
    else:
        print("No PDFs generated")

    for p in pdf_paths:
        os.remove(p)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 gen_merged_pdf.py <company>")
        sys.exit(1)
    generate(sys.argv[1])

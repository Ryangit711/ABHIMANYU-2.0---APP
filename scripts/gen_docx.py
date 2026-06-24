#!/usr/bin/env python3
"""Parametric DOCX generator — reads company fit map + SHOOT package, outputs tailored DOCX."""

import sys
import os
import json
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn

ONEDRIVE = "/mnt/c/Users/owner/OneDrive/ABHIMANYU-2.0"
LINUX = "/home/aryan/opencode_test/ABHIMANYU-2.0"

NAME = "Aman Kumar"
PHONE = "+1 236-885-2285"
EMAIL = "amankumar7111@outlook.com"
LINKEDIN = "linkedin.com/in/aman1776"
LOCATION = "Vancouver, BC"

# Company-specific configs
CONFIG = {
    "Indeed": {
        "font": "Liberation Sans",
        "size": Pt(10),
        "header_size": Pt(12),
        "margins": Inches(0.75),
        "pages": 1,
        "ats_notes": "Indeed internal ATS — DOCX preferred, Liberation Sans, 0.75in margins"
    },
    "Methanex": {
        "font": "Calibri",
        "size": Pt(11),
        "header_size": Pt(13),
        "margins": Inches(0.75),
        "pages": 2,
        "ats_notes": "Methanex career portal — DOCX, Calibri 11pt, 2-page for Director level"
    },
    "Deloitte": {
        "font": "Calibri",
        "size": Pt(10),
        "header_size": Pt(12),
        "margins": Inches(0.75),
        "pages": 2,
        "ats_notes": "Deloitte Workday ATS — DOCX, Calibri 10pt"
    },
    "Hiive": {
        "font": "Calibri",
        "size": Pt(11),
        "header_size": Pt(13),
        "margins": Inches(0.75),
        "pages": 2,
        "ats_notes": "Hiive Ashby ATS — DOCX, Calibri 11pt"
    },
    "Providence_Healthcare": {
        "font": "Calibri",
        "size": Pt(11),
        "header_size": Pt(13),
        "margins": Inches(0.75),
        "pages": 2,
        "ats_notes": "Providence Oracle Cloud ATS — DOCX, Calibri 11pt"
    }
}

def set_margins(doc, margin):
    for section in doc.sections:
        section.top_margin = margin
        section.bottom_margin = margin
        section.left_margin = margin
        section.right_margin = margin

def add_contact(doc, config):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(NAME)
    run.font.name = config["font"]
    run.font.size = Pt(16)
    run.bold = True
    p2 = doc.add_paragraph()
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run2 = p2.add_run(f"{PHONE} | {EMAIL} | {LINKEDIN} | {LOCATION}")
    run2.font.name = config["font"]
    run2.font.size = Pt(9)
    run2.font.color.rgb = RGBColor(80, 80, 80)

def add_section_header(doc, text, config):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(3)
    run = p.add_run(text.upper())
    run.font.name = config["font"]
    run.font.size = config["header_size"]
    run.bold = True
    pPr = p._p.get_or_add_pPr()
    pBdr = pPr.makeelement(qn('w:pBdr'), {})
    bottom = pBdr.makeelement(qn('w:bottom'), {
        qn('w:val'): 'single', qn('w:sz'): '4',
        qn('w:space'): '1', qn('w:color'): '000000',
    })
    pBdr.append(bottom)
    pPr.append(pBdr)

def add_body(doc, text, config, bold=False, italic=False, size=None, space_after=2):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(0)
    run = p.add_run(text)
    run.font.name = config["font"]
    run.font.size = size or config["size"]
    run.bold = bold
    run.italic = italic

def add_bullet(doc, text, config, bold_prefix=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.left_indent = Inches(0.25)
    p.paragraph_format.first_line_indent = Inches(-0.25)
    if bold_prefix:
        run_b = p.add_run(f"• {bold_prefix}")
        run_b.font.name = config["font"]
        run_b.font.size = config["size"]
        run_b.bold = True
        run = p.add_run(text)
        run.font.name = config["font"]
        run.font.size = config["size"]
    else:
        run = p.add_run(f"• {text}")
        run.font.name = config["font"]
        run.font.size = config["size"]

def get_date(company):
    DATES = {
        "Indeed": "2026-06-20",
        "Methanex": "2026-06-21",
        "Deloitte": "2026-06-19",
        "Hiive": "2026-06-22",
        "Providence_Healthcare": "2026-06-22"
    }
    return DATES.get(company, "2026-06-22")

def generate(company):
    config = CONFIG.get(company, CONFIG["Methanex"])
    date_str = get_date(company)
    folder = f"{ONEDRIVE}/{date_str}/{company}"
    lfolder = f"{LINUX}/{date_str}/{company}"
    os.makedirs(folder, exist_ok=True)
    os.makedirs(lfolder, exist_ok=True)

    # --- RESUME ---
    doc = Document()
    set_margins(doc, config["margins"])
    add_contact(doc, config)

    add_section_header(doc, "Professional Summary", config)
    if company == "Methanex":
        add_body(doc,
            "Strategy and operations executive who built the strategic infrastructure for a multi-site "
            "organization from zero, scaling it from 3 to 70 employees across 32 locations and directing "
            "a $17M acquisition. Combines board-level strategic thinking with hands-on financial modelling, "
            "M&A execution, and cross-functional leadership. Equally comfortable leading an ELT strategy "
            "session, building a valuation model, or aligning diverse teams around a shared plan.", config)
    elif company == "Hiive":
        add_body(doc,
            "Operations strategist and systems builder who designed and implemented the complete operational "
            "infrastructure for a startup that grew 23x — from 3 to 70 employees across 32 locations — "
            "and directed its $17M exit. Combines a builder's instinct for scalable systems with an operator's "
            "discipline for data integrity, revenue lifecycle optimization, and cross-functional execution.", config)
    elif company == "Providence_Healthcare":
        add_body(doc,
            "Healthcare operations leader with 8 years of progressive experience directing multi-site clinical "
            "and operational infrastructure across 32 locations and 12 departments. Scaled a healthcare startup "
            "from 3 to 70 employees and $4M ARR, managed full P&L ownership, led quality improvement initiatives, "
            "and directed a $17M acquisition end-to-end. Combines strategic thinking with hands-on operational "
            "execution in complex, multi-stakeholder healthcare environments.", config)
    else:
        add_body(doc,
            "Operations executive who built multi-site operational infrastructure from scratch, "
            "scaling from 3 to 70 employees across 32 locations, then directed a $17M acquisition. "
            "Combines strategic thinking with execution.", config)

    add_section_header(doc, "Core Competencies", config)
    if company == "Methanex":
        add_body(doc,
            "Corporate Strategy & Planning  |  Financial Modelling & Valuation  |  M&A Execution & Integration  |  "
            "Board & Executive Communication  |  Cross-Functional Leadership  |  OKR & Performance Systems  |  "
            "Capital Allocation  |  Strategic Growth Initiatives", config, size=Pt(9.5))
    elif company == "Hiive":
        add_body(doc,
            "Revenue Operations  |  Operational Infrastructure Design  |  Systems Architecture & Automation  |  "
            "Bottleneck Analysis  |  Workflow Optimization  |  Data Integrity & Reporting  |  "
            "Cross-Functional Execution  |  M&A & Strategic Projects", config, size=Pt(9.5))
    elif company == "Providence_Healthcare":
        add_body(doc,
            "Multi-Site Healthcare Operations  |  Clinical Operations Leadership  |  Quality Improvement  |  "
            "Financial Management & Budgeting  |  Interdisciplinary Team Leadership  |  "
            "Change Management & Transformation  |  Regulatory Compliance  |  Strategic Planning & OKRs", config, size=Pt(9.5))
    else:
        add_body(doc,
            "M&A Integration  |  Cross-Functional Program Management  |  Operational Infrastructure  |  "
            "Strategic Planning & OKRs  |  P&L Management  |  Board Reporting  |  Multi-Site Operations", config, size=Pt(9.5))

    add_section_header(doc, "Professional Experience", config)

    # SkyflyMD
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.space_before = Pt(4)
    run = p.add_run("SkyflyMD")
    run.font.name = config["font"]
    run.font.size = config["size"]
    run.bold = True
    run2 = p.add_run("  |  Director of Operations  |  Phoenix, AZ / Vancouver, BC  |  2017 – 2025")
    run2.font.name = config["font"]
    run2.font.size = config["size"]

    if company == "Methanex":
        add_body(doc,
            "Led strategy and operations for a multi-site healthcare group. Built the strategic planning "
            "process, financial infrastructure, and operational systems from zero.", config, italic=True, size=Pt(9.5))
        add_bullet(doc,
            " — built company-wide strategic planning framework across 5 annual cycles: board-level strategy "
            "sessions, departmental OKR cascades, quarterly performance reviews with executive leadership",
            config, bold_prefix="Strategic Planning & Execution")
        add_bullet(doc,
            " — multi-scenario P&L models, capital allocation frameworks, departmental budgets across "
            "12 departments, board-ready reporting templates",
            config, bold_prefix="Financial Modelling")
        add_bullet(doc,
            " — directed end-to-end $17M acquisition: 8 due diligence workstreams, Day 1 readiness, "
            "100% key talent retention, 90-day systems consolidation",
            config, bold_prefix="M&A & Integration")
        add_bullet(doc,
            " — organizational infrastructure for 70 employees across 5 clinic groups, 32 locations — "
            "hiring frameworks, training, quality standards, cross-border coordination",
            config, bold_prefix="Organizational Leadership")
    elif company == "Hiive":
        add_body(doc,
            "Built the complete operational infrastructure for a multi-site healthcare startup from zero. "
            "Served as the primary systems architect, process designer, and cross-functional integrator "
            "across all revenue-generating and operational functions.", config, italic=True, size=Pt(9.5))
        add_bullet(doc,
            " — from zero: designed and implemented the entire operational tech stack (EHR, billing, scheduling, "
            "RCM, analytics) that scaled from 3 to 70 employees across 32 locations without adding complexity",
            config, bold_prefix="Systems Architecture & Automation")
        add_bullet(doc,
            " — identified and eliminated bottlenecks in the revenue lifecycle — automated billing workflows, "
            "replaced manual reconciliation with real-time RCM, reduced admin overhead by 40%+",
            config, bold_prefix="Revenue Operations & Optimization")
        add_bullet(doc,
            " — built KPI dashboards, board-level reporting, and data integrity systems from scratch — "
            "replaced manual spreadsheets with real-time analytics across all 32 locations",
            config, bold_prefix="Data Infrastructure & Reporting")
        add_bullet(doc,
            " — directed full-cycle $17M acquisition: 8 diligence workstreams, integration playbook, "
            "consolidated 8 systems within 90 days, retained 100% of key talent",
            config, bold_prefix="M&A & Strategic Projects")
    elif company == "Providence_Healthcare":
        add_body(doc,
            "Directed clinical and operational leadership for a multi-site healthcare organization across 32 locations. "
            "Served as the primary operational leader coordinating interdisciplinary teams, managing resources, "
            "and driving quality improvement across 12 departments and 5 clinic groups.", config, italic=True, size=Pt(9.5))
        add_bullet(doc,
            " — led clinical and operational leadership across 32 multi-site locations, coordinating interdisciplinary "
            "teams to deliver integrated, patient-centered care across 5 clinic groups and 12 departments",
            config, bold_prefix="Multi-Site Healthcare Operations")
        add_bullet(doc,
            " — managed full P&L ownership for $4M revenue healthcare organization — budget planning, variance analysis, "
            "resource allocation, capital expenditure planning across 32 locations",
            config, bold_prefix="Financial Management & Resource Allocation")
        add_bullet(doc,
            " — drove quality improvement initiatives reducing administrative overhead by 40%+ through workflow "
            "automation, standardized processes, and data-driven performance management",
            config, bold_prefix="Quality Improvement & Process Optimization")
        add_bullet(doc,
            " — directed end-to-end $17M acquisition: 8 diligence workstreams, Day 1 readiness, 90-day systems "
            "consolidation across 32 locations, 100% key talent retention",
            config, bold_prefix="Change Management & Transformation")
        add_bullet(doc,
            " — managed full operational infrastructure for a geriatrics-specialized multi-site practice — scheduling, "
            "billing (ICD coding, insurance claims), multi-facility coordination across 5+ clinic locations and "
            "multiple senior care homes serving aging populations",
            config, bold_prefix="Geriatric Practice & Senior Care Operations")
    else:
        add_body(doc,
            "Directed end-to-end operations for a multi-site healthcare group. Served as the primary "
            "bridge between executive leadership and all operational teams.", config, italic=True, size=Pt(9.5))
        add_bullet(doc,
            " — 8 concurrent due diligence workstreams, integration playbook, Day 1/100 milestones, "
            "100% key talent retention through $17M transition",
            config, bold_prefix="Full-Cycle Acquisition Execution")

    # Earlier
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.space_before = Pt(6)
    run = p.add_run("Earlier Career")
    run.font.name = config["font"]
    run.font.size = config["size"]
    run.bold = True
    add_bullet(doc, "Digital Strategy Manager (2016–2018) — led digital strategy, campaign analytics, ROI measurement", config)
    add_bullet(doc, "Client Services Representative (2014–2016) — client escalations, complex issue resolution", config)

    # Education
    add_section_header(doc, "Education", config)
    add_body(doc, "Master of Business Administration (MBA)", config, bold=True, space_after=0)
    add_body(doc, "Post-Baccalaureate Diploma in Business Management — KPU, Surrey, BC", config, size=Pt(9), space_after=0)
    add_body(doc, "Bachelor of Science, Information Technology", config, size=Pt(9), space_after=0)

    # Technical Proficiency
    add_section_header(doc, "Technical Proficiency", config)
    if company == "Methanex":
        add_body(doc,
            "Financial Modelling & Analysis  |  Microsoft Excel (Advanced)  |  Google Workspace  |  "
            "OKR Frameworks  |  ERP Systems  |  CRM Platforms  |  Jira / Confluence  |  Data Visualization",
            config, size=Pt(9))
    elif company == "Hiive":
        add_body(doc,
            "Systems Architecture & Automation  |  EHR / Practice Management Platforms  |  "
            "Google Workspace  |  Data Visualization & KPI Dashboards  |  Financial Modeling  |  "
            "OKR Frameworks  |  CRM Platforms  |  Jira / Confluence  |  AI-Augmented Workflows",
            config, size=Pt(9))
    elif company == "Providence_Healthcare":
        add_body(doc,
            "EHR / Practice Management Platforms  |  Financial Modeling & Budgeting  |  "
            "Data Visualization & KPI Dashboards  |  Google Workspace  |  OKR Frameworks  |  "
            "Project Management Tools  |  Regulatory Compliance Systems  |  Quality Improvement Frameworks",
            config, size=Pt(9))
    else:
        add_body(doc,
            "Athenahealth  |  eClinicalWorks  |  CRM Platforms  |  Google Workspace  |  "
            "Financial Modeling  |  OKR Frameworks  |  Jira / Confluence",
            config, size=Pt(9))

    if company == "Methanex":
        role_str = "Director_Strategy"
    elif company == "Hiive":
        role_str = "Associate_Operations_Strategy"
    elif company == "Providence_Healthcare":
        role_str = "Director_Clinical_Operations"
    else:
        role_str = "SrMgr_Integration"

    respath = os.path.join(folder, f"Aman_Kumar_{company}_{role_str}.docx")
    try:
        doc.save(respath)
    except PermissionError:
        respath = os.path.join(lfolder, os.path.basename(respath))
        doc.save(respath)
    doc.save(os.path.join(lfolder, os.path.basename(respath)))
    print(f"Resume: {respath}")

    # --- COVER LETTER ---
    doc = Document()
    set_margins(doc, config["margins"])

    add_body(doc, NAME, config, bold=True, space_after=0)
    add_body(doc, f"{PHONE} | {EMAIL} | {LINKEDIN}", config, size=Pt(9), space_after=0)
    add_body(doc, LOCATION, config, size=Pt(9), space_after=4)
    DATE_LABELS = {"Indeed": "June 20, 2026", "Methanex": "June 21, 2026", "Deloitte": "June 19, 2026", "Hiive": "June 22, 2026", "Providence_Healthcare": "June 22, 2026"}
    add_body(doc, DATE_LABELS.get(company, "June 22, 2026"), config, space_after=8)

    if company == "Methanex":
        add_body(doc, "Methanex Corporation", config, space_after=0)
        add_body(doc, "1800 Waterfront Centre, 200 Burrard Street", config, space_after=0)
        add_body(doc, "Vancouver, BC V6C 3M1", config, space_after=8)
        add_body(doc, "Re: Director, Strategy", config, bold=True, space_after=8)

        body = (
            "Dear Hiring Manager,\n\n"
            "Methanex is the world's largest methanol producer, navigating volatile commodity markets, "
            "the integration of a $2.05B acquisition, and a strategic shift toward low-carbon solutions. "
            "The Director, Strategy role sits at the center of these dynamics. This is exactly where I deliver the most value.\n\n"
            "I spent eight years building the strategic infrastructure of a multi-site organization from scratch. "
            "When I joined, there were 3 people and no playbook. When I left, it was 70 people across 32 locations "
            "with a $17M acquisition that I directed end-to-end. The strategic planning system I designed — annual "
            "strategy sessions cascading through quarterly OKRs with board-level reporting — gave executive leadership "
            "real-time visibility into execution across every location. The financial models I built governed resource "
            "allocation across 12 departments. The acquisition I directed involved 8 workstreams, diligence across "
            "finance, legal, and operations, and an integration that retained 100% of our key talent.\n\n"
            "What made this possible was not a pre-existing framework. I built it — the strategy cycle, the governance "
            "rhythms, the valuation models, the integration playbook — all from zero. I learned that strategy is not "
            "a document you produce once a year. It is a living process that must connect the Board room to the front "
            "line, and it requires someone who can operate at both altitudes without losing coherence.\n\n"
            "I understand Methanex operates in a different industry. But strategy is fractal — the core problems are "
            "the same: Where do we allocate capital? How do we grow? What risks do we manage? How do we align a global "
            "organization around a shared plan? I have solved these problems in my domain, and I am ready to solve them in yours.\n\n"
            "I would welcome the opportunity to discuss how my experience building strategic and financial infrastructure "
            "can support Methanex's next phase of global leadership.\n\n"
            "Best regards,\n"
            f"{NAME}\n{PHONE}\n{EMAIL}"
        )
    elif company == "Hiive":
        add_body(doc, "Hiive", config, space_after=0)
        add_body(doc, "Vancouver, BC (HQ)", config, space_after=8)
        add_body(doc, "Re: Associate, Operations Strategy", config, bold=True, space_after=8)

    elif company == "Providence_Healthcare":
        add_body(doc, "Providence Health Care", config, space_after=0)
        add_body(doc, "Burnaby, BC", config, space_after=8)
        add_body(doc, "Re: Director, Clinical and Operations (LTC PHC & FHA)", config, bold=True, space_after=8)

        body = (
            "Dear Hiring Committee,\n\n"
            "I spent 8 years leading multi-site healthcare operations — and the patient population I served? "
            "Seniors. I have done exactly what this role requires.\n\n"
            "At SkyflyMD, I served as the de facto Director of Operations for a multi-site healthcare organization "
            "that grew from 3 to 70 people across 32 locations. The practice was geriatrics-focused — I managed operations "
            "alongside a geriatrician, coordinating care across clinic locations and senior care homes, managing "
            "billing and compliance for aging populations, and building the systems that supported quality care "
            "for older adults. I managed the full P&L ($4M ARR). I built the operational infrastructure from "
            "scratch — scheduling, billing, compliance, quality assurance, reporting systems. I led interdisciplinary "
            "teams across 12 departments. I directed the $17M acquisition that integrated 8 separate operational "
            "systems into one without losing a single key team member.\n\n"
            "What drew me to Providence is the alignment between my experience and your mission. Multi-site seniors care "
            "at Chenchenstway and your PHC/FHA long-term care sites faces exactly the operational challenges I have been "
            "solving for the past 8 years: how to scale quality care across multiple locations serving aging populations "
            "without losing the personalized, compassionate approach that defines your organization.\n\n"
            "I hold an MBA with 8 years of progressive healthcare operations leadership — including direct experience "
            "serving geriatric populations in multi-facility settings. My combination of formal business education and "
            "hands-on seniors care operations experience provides the equivalent foundation this role requires.\n\n"
            "I would welcome the opportunity to discuss how my experience building and leading multi-site healthcare "
            "operations for aging populations can support Providence and Fraser Health's vision for seniors care.\n\n"
            "Best regards,\n"
            f"{NAME}\n{PHONE}\n{EMAIL}"
        )
    elif company == "Hiive":
        add_body(doc, "Hiive", config, space_after=0)
        add_body(doc, "Vancouver, BC (HQ)", config, space_after=8)
        add_body(doc, "Re: Associate, Operations Strategy", config, bold=True, space_after=8)

        body = (
            "Dear Hiring Manager,\n\n"
            "I spent eight years doing exactly what this role describes: embedding with a revenue-generating team, "
            "identifying bottlenecks in the operational lifecycle, and deploying automated solutions to clear them.\n\n"
            "When I joined SkyflyMD, there was no operational infrastructure — just a team operating on willpower. "
            "By the time I directed the $17M exit, we had:\n\n"
            "- A complete tech stack (EHR, billing, scheduling, analytics) that I designed and implemented from scratch\n"
            "- Real-time KPI dashboards replacing manual spreadsheets\n"
            "- Automated workflows that reduced administrative overhead by 40%\n"
            "- A scalable operating system that supported 70 people across 32 locations — without adding operational complexity\n\n"
            "I did not inherit these systems. I built them. That is what systems builder means to me.\n\n"
            "Hiive is doing the same thing for the private market that I did for healthcare operations: replacing opacity "
            "with transparency, manual processes with automation, fragmentation with integration. The private secondary "
            "market has been running on brokers and spreadsheets for too long. You are building the infrastructure "
            "that changes that.\n\n"
            "I want to help you clear the bottlenecks.\n\n"
            "I am based in Vancouver and ready to be in your HQ five days a week.\n\n"
            "Best regards,\n"
            f"{NAME}\n{PHONE}\n{EMAIL}"
        )
    else:
        add_body(doc, "Indeed", config, space_after=0)
        add_body(doc, "Vancouver, BC", config, space_after=8)
        add_body(doc, "Re: Sr. Manager, Integration & Business Acceleration — Reference ID: 47053", config, bold=True, space_after=8)

        body = (
            "Dear Hiring Manager,\n\n"
            "Your mission is to help people get jobs. Mine is to build the operational infrastructure "
            "that makes organizations scalable, efficient, and ready for their next phase of growth.\n\n"
            "I joined SkyflyMD when it was 3 people in a single location. When I left, it was 70 people "
            "across 32 locations, operating with systems I designed from scratch. The defining moment of "
            "that journey was directing our $17M acquisition — structuring 8 concurrent due diligence "
            "workstreams across finance, legal, operations, and provider contracts. I built the integration "
            "playbook, tracked Day 1 readiness and Day 100 milestones, consolidated 8 separate operational "
            "systems into one unified platform, and retained 100% of our key talent through the transition.\n\n"
            "What made that possible was not a pre-existing framework. There was no playbook. I created it — "
            "the governance rhythms, the reporting cadences, the escalation paths, the decision-making "
            "frameworks — all from scratch, across 5 clinic groups operating under different state regulations.\n\n"
            "What drew me to Indeed is that you are data-driven without being jargon-heavy, and mission-focused "
            "without being sentimental. That is how I operate. Your 'job seeker first' value resonates because "
            "it mirrors how I have always made operational decisions — starting with the end-user and working backward.\n\n"
            "I am not looking for a role that requires a playbook to exist before I start. I am looking for "
            "one that needs a playbook written.\n\n"
            "I would welcome the opportunity to discuss how my experience building and integrating multi-site "
            "operations can support Indeed's continued growth through M&A. Thank you for your time and consideration.\n\n"
            "Best regards,\n"
            f"{NAME}\n{PHONE}\n{EMAIL}"
        )

    add_body(doc, body, config, space_after=0)

    clpath = os.path.join(folder, f"Cover_Letter_{company}_{role_str}.docx")
    try:
        doc.save(clpath)
    except PermissionError:
        clpath = os.path.join(lfolder, os.path.basename(clpath))
        doc.save(clpath)
    doc.save(os.path.join(lfolder, os.path.basename(clpath)))
    print(f"Cover:   {clpath}")

    # --- CASE (Semantic Narrative) ---
    doc = Document()
    set_margins(doc, config["margins"])

    if company == "Methanex" or company == "Hiive" or company == "Providence_Healthcare":
        # Title
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        if company == "Hiive":
            title_text = "CASE — Aman Kumar × Hiive"
            subtitle_text = "The Systems Builder"
        elif company == "Providence_Healthcare":
            title_text = "CASE — Aman Kumar × Providence Health Care"
            subtitle_text = "The Healthcare Operations Leader"
        else:
            title_text = "CASE — Aman Kumar × Methanex"
            subtitle_text = "The Strategist Who Built From Zero"
        run = p.add_run(title_text)
        run.font.name = config["font"]
        run.font.size = Pt(18)
        run.bold = True

        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(subtitle_text)
        run.font.name = config["font"]
        run.font.size = Pt(13)
        run.font.color.rgb = RGBColor(100, 100, 100)

        add_body(doc, "", config, space_after=4)

        if company == "Hiive":
            # Section: The Situation
            add_section_header(doc, "The Situation", config)
            add_body(doc, (
                "Hiive is building the infrastructure for the private secondary market — a market that has operated "
                "on opaque, manual, relationship-driven processes for decades. $250M+ in monthly transaction volume, "
                "$2B+ in live orders, 3,000+ companies on the platform, 95% of US decacorns and tier-1 VCs already "
                "engaged. The platform is winning. But every marketplace hits the same inflection point: the moment "
                "when operational infrastructure becomes the constraint on growth.\n\n"
                "Hiive is at that inflection point now. The question is not whether the market opportunity exists. "
                "It is whether the operational systems can scale to match it — without breaking."
            ), config, size=Pt(10.5))

            # Section: The Candidate
            add_section_header(doc, "The Candidate", config)
            add_body(doc, (
                "Aman Kumar spent eight years doing exactly what Hiive needs now: building the operational infrastructure "
                "that scaled a startup from 3 to 70 people and $4M ARR — and then directed its $17M exit.\n\n"
                "He did not inherit operational systems. He designed and built them from scratch. He did not just use tools — "
                "he selected, implemented, and owned every platform that the business ran on. He did not merely participate "
                "in the company's growth. He was the operational architecture that made growth possible without collapse."
            ), config, size=Pt(10.5))

            # Section: The Alignment
            add_section_header(doc, "The Alignment", config)
            add_bullet(doc,
                " — designed and implemented complete operational tech stack from zero: EHR, billing, scheduling, RCM, analytics. Every system architected to scale without adding complexity.", config,
                bold_prefix="Systems Architecture")
            add_bullet(doc,
                " — identified and eliminated bottlenecks in the revenue lifecycle — automated billing, real-time reconciliation, 40%+ reduction in admin overhead, $0 to $4M ARR without proportional headcount growth", config,
                bold_prefix="Revenue Operations")
            add_bullet(doc,
                " — built KPI dashboards and real-time reporting infrastructure from scratch, replacing manual spreadsheets across 32 locations with automated data feeds and board-ready analytics", config,
                bold_prefix="Data Infrastructure")
            add_bullet(doc,
                " — directed full-cycle $17M acquisition: 8 diligence workstreams, Day 1 readiness, 90-day systems consolidation, 100% key talent retention across 5 clinic groups", config,
                bold_prefix="M&A & Execution")
            add_bullet(doc,
                " — coordinated 12 departments, 5 clinic groups, 32 locations — built governance rhythms, escalation paths, and decision-making frameworks that operated without his direct involvement", config,
                bold_prefix="Cross-Functional Leadership")

            # Section: The Semantic Fit
            add_section_header(doc, "The Semantic Fit", config)
            add_body(doc, (
                "Hiive's operating principles: exceptionalism, high-performance, collaborative ambition, mission-driven, "
                "builder mentality. The culture is not for spectators — it is for people who build.\n\n"
                "Aman's career is a case study in this exact ethos:"
            ), config, size=Pt(10.5))
            add_bullet(doc,
                "Held himself and the entire organization to operational standards that exceeded what anyone asked for — systems designed for the scale that was coming, not the scale that was.", config, bold_prefix="Exceptionalism")
            add_bullet(doc,
                "Did not wait for permission to build. When a process was broken, he designed the replacement, sold it to the team, and deployed it. Builder, not committee member.", config, bold_prefix="Builder Mentality")
            add_bullet(doc,
                "Brought together 12 departments, 5 clinic groups, 32 locations into a unified operating system — replacing fragmentation with integration, opacity with transparency.", config, bold_prefix="Collaborative Ambition")
            add_bullet(doc,
                "Built the systems that allowed the company to grow from startup to acquisition-ready without breaking. Not just the infrastructure — the playbook for using it.", config, bold_prefix="Mission-Driven")

            # Section: The Opportunity
            add_section_header(doc, "The Opportunity", config)
            add_body(doc, (
                "Hiive has 204 people, $250M+ monthly volume, and a market that is about to explode with the 2026 IPO wave. "
                "The operations team is building the infrastructure that will enable Hiive to handle $1B+ monthly volume "
                "without operational friction.\n\n"
                "Aman has done exactly this — at smaller scale, in a different industry — with the same architecture of "
                "thinking: identify the bottleneck, design the solution, build it, automate it, move to the next one. Repeat "
                "until the company's operational infrastructure is no longer the constraint on its growth.\n\n"
                "The industry is the setting, not the skill. The skill is building operational infrastructure that scales. "
                "That is what Aman built at SkyflyMD. That is what Hiive needs now."
            ), config, size=Pt(10.5))

        elif company == "Providence_Healthcare":
            # Section: The Situation
            add_section_header(doc, "The Situation", config)
            add_body(doc, (
                "Providence Health Care is one of Canada's largest faith-based healthcare organizations — 17 sites, "
                "5,000+ employees, 120+ years of serving British Columbians. It operates at the intersection of "
                "compassionate care and operational complexity: acute care at St. Paul's Hospital, seniors care across "
                "multiple long-term care sites, mental health services, research, and a $2.18B new hospital build.\n\n"
                "Within this ecosystem, seniors care faces the most acute operational challenges: growing waitlists, "
                "aging population, workforce shortages, and the transition toward smaller, more personalized care home "
                "models. The Chenchenstway site and the broader PHC/FHA long-term care network need operational "
                "leadership that can coordinate across two partner organizations, manage resources strategically, "
                "and maintain quality across multiple locations."
            ), config, size=Pt(10.5))

            # Section: The Candidate
            add_section_header(doc, "The Candidate", config)
            add_body(doc, (
                "Aman Kumar spent eight years doing exactly what Providence needs now: directing multi-site healthcare "
                "operations that scaled from 3 to 70 people across 32 locations, building the operational infrastructure "
                "from scratch, managing full P&L ownership, and navigating a transformative acquisition — all in "
                "service of a geriatric patient population.\n\n"
                "He did not inherit operational systems. He designed them. He did not manage a single site. He coordinated "
                "12 departments and 5 clinic groups. He did not merely participate in a transaction. He directed the "
                "$17M acquisition end-to-end — from first-day diligence through Day 1 readiness through 90-day integration "
                "across all 32 locations, retaining 100% of key talent.\n\n"
                "And the patient population he served for those eight years? Seniors. Working alongside a geriatrician "
                "who trained at Baylor College of Medicine, managing operations and billing for senior care homes, "
                "coordinating care across clinic locations and skilled nursing facilities. The setting was Arizona. "
                "The operational challenges — coordinating care for aging populations across multiple sites, managing "
                "complex billing, ensuring quality across a distributed network — were the same problems Providence "
                "solves every day."
            ), config, size=Pt(10.5))

            # Section: The Alignment
            add_section_header(doc, "The Alignment", config)
            add_bullet(doc,
                " — led operations across 32 multi-site healthcare locations, coordinating interdisciplinary teams, managing budgets, and driving quality standards across 12 departments and 5 clinic groups", config,
                bold_prefix="Multi-Site Healthcare Operations")
            add_bullet(doc,
                " — managed full P&L ownership for $4M revenue organization — budget planning, variance analysis, resource allocation, capital expenditure across 32 locations", config,
                bold_prefix="Financial Management")
            add_bullet(doc,
                " — drove quality improvement initiatives reducing administrative overhead by 40%+ — automated workflows, standardized processes, data-driven performance management across all sites", config,
                bold_prefix="Quality Improvement")
            add_bullet(doc,
                " — directed end-to-end $17M acquisition: 8 diligence workstreams, Day 1 readiness, 90-day systems consolidation, 100% key talent retention", config,
                bold_prefix="Change Management & Transformation")
            add_bullet(doc,
                " — built governance rhythms, escalation protocols, and communication frameworks that aligned diverse stakeholders across 5 clinic groups, 12 departments, and multiple regulatory contexts", config,
                bold_prefix="Stakeholder Engagement & Partnership")
            add_bullet(doc,
                " — managed full operational infrastructure for a geriatrics-specialized multi-site practice — scheduling, billing (ICD coding), multi-facility coordination across 5+ clinic locations and multiple senior care homes serving aging populations", config,
                bold_prefix="Geriatric Practice & Senior Care Operations")

            # Section: The Semantic Fit
            add_section_header(doc, "The Semantic Fit", config)
            add_body(doc, (
                "Providence Health Care operates on a mission of compassionate care and social justice. "
                "The values are: compassion, social justice, respect, collaboration, excellence. "
                "The guiding principle is \"How you want to be treated.\"\n\n"
                "Aman's career is a case study in this exact value system:"
            ), config, size=Pt(10.5))
            add_bullet(doc,
                "Built operational systems centered on the patient/resident experience — every process designed around the question 'does this improve care?' For eight years, serving an aging population, the answer was always yes.", config, bold_prefix="Compassion")
            add_bullet(doc,
                "Served a vulnerable population (healthcare access) and built the infrastructure that made care accessible across 32 locations — not because it was profitable, because it was needed.", config, bold_prefix="Social Justice")
            add_bullet(doc,
                "Coordinated 12 departments, 5 clinic groups, 32 locations — each with its own culture and history — respecting their autonomy while aligning them around shared standards.", config, bold_prefix="Respect & Collaboration")
            add_bullet(doc,
                "Did not settle for 'good enough.' Built KPI dashboards, automated systems, quality frameworks — the infrastructure of excellence that ran without him.", config, bold_prefix="Excellence")

            # Section: The Opportunity
            add_section_header(doc, "The Opportunity", config)
            add_body(doc, (
                "Providence Health Care and Fraser Health Authority operate seniors care across multiple long-term care "
                "sites in the Lower Mainland. The Director, Clinical and Operations role at Chenchenstway and the PHC/FHA "
                "network sits at the center of this system — leading interdisciplinary teams, managing resources, driving "
                "quality, and coordinating across two major health organizations.\n\n"
                "Aman has done exactly this — in a different healthcare setting, with the SAME patient population — "
                "with a track record that suggests something deeper than domain experience. He is not a healthcare "
                "operator who needs to learn seniors care. He is a seniors care operator who has spent his entire "
                "career serving aging populations.\n\n"
                "The industry is not new to him. It is his identity. The patient population is not new to him. "
                "He has served them for eight years. He has been solving these exact problems — quality, "
                "scale, resources, coordination, serving aging populations with dignity — and he is ready to "
                "solve them for Providence."
            ), config, size=Pt(10.5))

        else:
            # Section: The Situation
            add_section_header(doc, "The Situation", config)
            add_body(doc, (
                "Methanex is the world's largest methanol producer — 10.4M tonnes annually, approximately 20% of the "
                "internationally traded market — operating at the intersection of global commodity volatility, post-merger "
                "integration, and a generational energy transition. The $2.05B acquisition of OCI Global's international "
                "methanol business closed in June 2025, fundamentally reshaping Methanex's geographic and operational "
                "footprint. Low-carbon methanol — M100 as marine fuel, renewable methanol from circular sources, the "
                "Atlas joint venture on the US Gulf Coast — is no longer a long-dated possibility. It is a present-tense "
                "strategic imperative.\n\n"
                "This is the context in which the Director, Strategy operates. Not as a planner. As a navigator."
            ), config, size=Pt(10.5))

            # Section: The Candidate
            add_section_header(doc, "The Candidate", config)
            add_body(doc, (
                "Aman Kumar spent eight years doing exactly what Methanex needs now: building the strategic infrastructure "
                "of a complex, multi-site organization from zero — and then navigating it through a transformative acquisition.\n\n"
                "He did not inherit a strategic planning process. He designed one. He did not take over an existing financial "
                "model. He built it. He did not merely participate in an M&A transaction. He directed it — from first-day "
                "diligence through Day 1 readiness through 100-day integration, retaining 100% of key talent across five "
                "clinic groups and 32 locations."
            ), config, size=Pt(10.5))

            # Section: The Alignment
            add_section_header(doc, "The Alignment", config)
            add_bullet(doc,
                " — built the strategy cycle from scratch: annual ELT sessions, quarterly OKR cascades, board-ready reporting across 32 locations, 5 consecutive cycles", config,
                bold_prefix="Global Strategy Process")
            add_bullet(doc,
                " — multi-scenario P&L models across 12 departments, capital allocation frameworks, DCF and valuation analysis, board-level financial reporting", config,
                bold_prefix="Valuation & Financial Analysis")
            add_bullet(doc,
                " — directed full-cycle $17M acquisition: 8 diligence workstreams, Day 1/100 milestones, 8-system consolidation in 90 days, 100% talent retention", config,
                bold_prefix="M&A Execution")
            add_bullet(doc,
                " — coordinated 12 departments, 5 clinic groups, 32 locations — building governance rhythms, escalation protocols, decision-making frameworks", config,
                bold_prefix="Cross-Functional Leadership")
            add_bullet(doc,
                " — created board-level reporting, investor materials, executive presentations from zero — presented with the rigor Methanex's Board expects", config,
                bold_prefix="Board-Level Communication")

            # Section: The Semantic Fit
            add_section_header(doc, "The Semantic Fit", config)
            add_body(doc, (
                "Methanex operates on a strategic framework: Leadership, Low Cost, Operational Excellence. "
                "The culture is defined by The Power of Agility. The value system is Integrity, Trust, Respect, "
                "Professionalism — underwritten by Responsible Care.\n\n"
                "Aman's career is a case study in this exact operating model:"
            ), config, size=Pt(10.5))
            add_bullet(doc,
                "Built the strategic system that governed 70 people across 32 locations. Did not inherit leadership — created it.", config, bold_prefix="Leadership")
            add_bullet(doc,
                "Managed P&L across 12 departments. Built the financial models that optimized resource allocation. Every dollar had a decision behind it.", config, bold_prefix="Low Cost")
            add_bullet(doc,
                "Designed governance rhythms, hiring frameworks, training programs, quality standards. Built the machine that ran without him.", config, bold_prefix="Operational Excellence")
            add_bullet(doc,
                "Navigated a 3-person startup through growth to a $17M exit. When the acquisition hit, structured 8 workstreams in days.", config, bold_prefix="Power of Agility")
            add_bullet(doc,
                "Coordinated 5 clinic groups, 12 departments, 32 locations — many operating independently before his systems brought them together.", config, bold_prefix="One Team")

            # Section: The Opportunity
            add_section_header(doc, "The Opportunity", config)
            add_body(doc, (
                "Methanex is 1,700 people globally, approximately 150 in Vancouver. The Director, Strategy sits in "
                "that Vancouver HQ, serving as the connective tissue between the Board of Directors, the Executive "
                "Leadership Team, and the operational reality of a global methanol business navigating integration, "
                "volatility, and transition.\n\n"
                "Aman has done exactly this — at smaller scale, in a different industry — with a clarity and rigor "
                "that suggest something deeper than domain experience. He is not a strategist who needs to learn "
                "execution. He is an executive who happens to call himself a strategist because that is where the "
                "intellectual challenge lives.\n\n"
                "Strategy is fractal. The questions are the same at every scale: Where do we allocate capital? How "
                "do we grow? What risks do we need to manage? How do we align a global organization around a shared "
                "plan? Aman has answered these questions in the arena. He is ready to answer them at Methanex's scale."
            ), config, size=Pt(10.5))

        # Footer
        add_body(doc, "", config, space_after=4)
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run("—")
        run.font.name = config["font"]
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor(150, 150, 150)
        add_body(doc, (
            "This document is not a resume. A resume is a record of what you have done. "
            "This is a case for who you are, and why that identity was built for this moment at this company."
        ), config, italic=True, size=Pt(9), space_after=0)

    casepath = os.path.join(folder, f"Case_{company}_{role_str}.docx")
    try:
        doc.save(casepath)
    except PermissionError:
        casepath = os.path.join(lfolder, os.path.basename(casepath))
        doc.save(casepath)
    doc.save(os.path.join(lfolder, os.path.basename(casepath)))
    print(f"Case:    {casepath}")
    print("Done.")

if __name__ == "__main__":
    company = sys.argv[1] if len(sys.argv) > 1 else "Methanex"
    generate(company)

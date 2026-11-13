"""Build portfolio.pdf: a landscape project portfolio with live screenshots.

Run from the repository root: python3 tools/make_portfolio.py portfolio.pdf   (needs reportlab)
"""
import sys
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.colors import HexColor, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm

OUT = sys.argv[1] if len(sys.argv) > 1 else "portfolio.pdf"
IMG = "assets/images/"
W, H = landscape(A4)
M = 16 * mm

INK = HexColor("#111827")
MUTED = HexColor("#5b6774")
BLUE = HexColor("#3157d5")
SOFT = HexColor("#eef2fb")
LINE = HexColor("#d5dceb")
LINK = "#1f5f99"
LI_URL = "https://www.linkedin.com/in/tiansawang-suetrong-95715343b/"


def L(url, text=None):
    return f'<a href="{url}" color="{LINK}"><u>{text or url.split("//")[-1].rstrip("/")}</u></a>'


st = {
    "body": ParagraphStyle("body", fontName="Helvetica", fontSize=10, leading=14.2, textColor=INK),
    "muted": ParagraphStyle("muted", fontName="Helvetica", fontSize=9.4, leading=13, textColor=MUTED),
    "bullet": ParagraphStyle("bullet", fontName="Helvetica", fontSize=9.6, leading=13.4, textColor=INK,
                             leftIndent=10, firstLineIndent=-7, spaceBefore=2.5),
    "label": ParagraphStyle("label", fontName="Helvetica-Bold", fontSize=8.2, leading=11, textColor=BLUE),
    "small": ParagraphStyle("small", fontName="Helvetica", fontSize=8.6, leading=12, textColor=MUTED),
}


def para(c, text, style, x, y, w):
    """Draw a paragraph with its top at y; return the y below it."""
    p = Paragraph(text, st[style])
    _, ph = p.wrap(w, H)
    p.drawOn(c, x, y - ph)
    return y - ph


def label(c, text, x, y, w, gap=7):
    return para(c, text.upper().replace(" ", "&nbsp;"), "label", x, y - gap, w) - 2


def bullets(c, items, x, y, w):
    for t in items:
        y = para(c, "•&nbsp;" + t, "bullet", x, y, w)
    return y


def shot(c, path, x, y_top, w, url_text):
    """Screenshot in a browser frame; return the y below it."""
    img = ImageReader(path)
    iw, ih = img.getSize()
    h = w * ih / iw
    bar = 7 * mm
    c.setFillColor(SOFT)
    c.setStrokeColor(LINE)
    c.roundRect(x, y_top - bar - h, w, bar + h, 5, stroke=1, fill=1)
    for i, col in enumerate(("#ff6b5f", "#ffc35a", "#3ccf63")):
        c.setFillColor(HexColor(col))
        c.circle(x + 5 * mm + i * 4.2 * mm, y_top - bar / 2, 1.3 * mm, stroke=0, fill=1)
    c.setFillColor(white)
    c.roundRect(x + 20 * mm, y_top - bar + 1.6 * mm, w - 26 * mm, bar - 3.2 * mm, 3, stroke=0, fill=1)
    c.setFillColor(MUTED)
    c.setFont("Helvetica", 7.5)
    c.drawString(x + 23 * mm, y_top - bar / 2 - 2.6, url_text)
    c.drawImage(img, x, y_top - bar - h, w, h)
    return y_top - bar - h


def header(c, n, kicker, title):
    c.setFillColor(BLUE)
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(M, H - M - 2 * mm, f"{n:02d}  /  {kicker.upper()}")
    c.setFillColor(INK)
    c.setFont("Helvetica-Bold", 24)
    c.drawString(M, H - M - 13 * mm, title)
    c.setStrokeColor(LINE)
    c.setLineWidth(0.8)
    c.line(M, H - M - 17 * mm, W - M, H - M - 17 * mm)
    return H - M - 21 * mm


def footer(c, page):
    c.setFont("Helvetica", 8)
    c.setFillColor(MUTED)
    c.drawString(M, 9 * mm, "Tiansawang Suetrong  ·  Portfolio  ·  tiansawang1818-pixel.github.io")
    c.drawRightString(W - M, 9 * mm, str(page))


def tags(c, items, x, y, w):
    """Draw pill tags left to right, wrapping; return the y below them."""
    c.setFont("Helvetica", 8)
    cx, row_h, pad = x, 6 * mm, 2.4 * mm
    y -= row_h
    for t in items:
        tw = c.stringWidth(t, "Helvetica", 8) + 2 * pad
        if cx + tw > x + w:
            cx = x
            y -= row_h + 1.6 * mm
        c.setFillColor(SOFT)
        c.setStrokeColor(LINE)
        c.roundRect(cx, y, tw, row_h, 3, stroke=1, fill=1)
        c.setFillColor(INK)
        c.drawString(cx + pad, y + 2.1 * mm, t)
        cx += tw + 1.6 * mm
    return y


c = canvas.Canvas(OUT, pagesize=(W, H))
c.setTitle("Tiansawang Suetrong - Portfolio")
c.setAuthor("Tiansawang Suetrong")
c.setSubject("Software engineering project portfolio")

# ---------- Page 1: cover ----------
c.setFillColor(SOFT)
c.rect(0, 0, W, H, stroke=0, fill=1)
c.setFillColor(BLUE)
c.rect(0, H - 4 * mm, W, 4 * mm, stroke=0, fill=1)
lx, lw = M + 4 * mm, 165 * mm
c.setFillColor(BLUE)
c.setFont("Helvetica-Bold", 9.5)
c.drawString(lx, H - 40 * mm, "PORTFOLIO  ·  SOFTWARE ENGINEERING  |  BACKEND & DATA")
c.setFillColor(INK)
c.setFont("Helvetica-Bold", 44)
c.drawString(lx, H - 58 * mm, "Tiansawang")
c.setFillColor(BLUE)
c.drawString(lx, H - 75 * mm, "Suetrong")
y = para(c, "Digital Science and Technology student at the Faculty of ICT, Mahidol University. I build full-stack "
            "systems end to end, from the interface people use to the API and the data model underneath. "
            "Two of them are live today.", "body", lx, H - 84 * mm, lw)
y = label(c, "Inside", lx, y - 4 * mm, lw)
for n, (t, d) in enumerate([("WasmBot Studio", "No-code business rule bots on Rust WebAssembly"),
                            ("HEAT//SHIFT", "Map-first urban heat decision platform for Bangkok"),
                            ("More work and contact", "Portfolio site, practice projects, skills")], 1):
    y = para(c, f'<font color="#3157d5"><b>{n:02d}</b></font>&nbsp;&nbsp;<b>{t}</b>&nbsp;&nbsp;'
                f'<font color="#5b6774">{d}</font>', "body", lx, y - 2, lw)
y = label(c, "Contact", lx, y - 4 * mm, lw)
for line in [L("mailto:tiansawang1818@gmail.com", "tiansawang1818@gmail.com") + "&nbsp;&nbsp;·&nbsp;&nbsp;+66 84 228 6225",
             "<b>Website</b>&nbsp; " + L("https://tiansawang1818-pixel.github.io/") +
             "&nbsp;&nbsp;&nbsp;<b>GitHub</b>&nbsp; " + L("https://github.com/tiansawang1818-pixel"),
             "<b>LinkedIn</b>&nbsp; " + L(LI_URL, "linkedin.com/in/tiansawang-suetrong-95715343b")]:
    y = para(c, line, "body", lx, y - 1, lw)
pw = 70 * mm
img = ImageReader(IMG + "tiansawang-profile.jpg")
iw, ih = img.getSize()
ph = pw * ih / iw
px, py = W - M - pw - 10 * mm, (H - ph) / 2 + 4 * mm
c.setFillColor(white)
c.setStrokeColor(LINE)
c.roundRect(px - 3 * mm, py - 16 * mm, pw + 6 * mm, ph + 19 * mm, 8, stroke=1, fill=1)
c.drawImage(img, px, py, pw, ph)
c.setFillColor(INK)
c.setFont("Helvetica-Bold", 10)
c.drawString(px, py - 7 * mm, "Mahidol University · ICT")
c.setFillColor(MUTED)
c.setFont("Helvetica", 9)
c.drawString(px, py - 12 * mm, "B.Sc. Digital Science and Technology · Bangkok")
footer(c, 1)
c.showPage()


# ---------- Project pages ----------
def project_page(page, n, kicker, title, intro, img, url_text, extra_img, extra_caption,
                 role, points, stack, links, below=None):
    top = header(c, n, kicker, title)
    sw = 150 * mm
    y = shot(c, IMG + img, M, top, sw, url_text)
    if extra_img:
        ew = 72 * mm
        ey = shot(c, IMG + extra_img, M, y - 5 * mm, ew, url_text)
        para(c, extra_caption, "small", M + ew + 5 * mm, y - 9 * mm, sw - ew - 5 * mm)
    if below:
        below(M, y, sw)
    rx, rw = M + sw + 10 * mm, W - 2 * M - sw - 10 * mm
    ry = para(c, intro, "body", rx, top, rw)
    ry = label(c, "My role", rx, ry - 3 * mm, rw)
    ry = para(c, role, "body", rx, ry, rw)
    ry = label(c, "What I built", rx, ry - 3 * mm, rw)
    ry = bullets(c, points, rx, ry, rw)
    ry = label(c, "Stack", rx, ry - 3 * mm, rw)
    ry = tags(c, stack, rx, ry - 1 * mm, rw)
    para(c, links, "body", rx, ry - 4 * mm, rw)
    footer(c, page)
    c.showPage()


project_page(
    2, 1, "Full stack · No-code platform", "WasmBot Studio",
    "A no-code platform that turns business rules into reusable bots: design them visually, test them on a real "
    "Rust WebAssembly engine, publish immutable versions, then use them anywhere.",
    "wasmbot-live-dashboard.jpg", "wasmbot-studio.vercel.app",
    "wasmbot-live-rules.jpg",
    "<b>Rule editor.</b> Nested AND/OR groups with 12 comparison operators. Both screenshots were captured from the "
    "live app on 11 November 2026.",
    "Full-stack development: interface, Edge Functions, database, security, and deployment.",
    ["Visual AND/OR rule editor with <b>12 operators</b>, executed by a Rust engine compiled to WebAssembly.",
     "Immutable, versioned deployments so draft edits never affect the live bot.",
     "Each bot works as a hosted form, embed, REST API, signed webhook, and typed TypeScript SDK.",
     "Row-level security, scoped API keys stored as HMAC-SHA256 hashes, rate limits, and audit logs.",
     "<b>7 Supabase Edge Functions</b>, verified with <b>71 automated tests</b>."],
    ["TypeScript", "React", "Vite", "Tailwind CSS", "Supabase", "PostgreSQL", "Rust", "WebAssembly"],
    "<b>Live app</b>&nbsp; " + L("https://wasmbot-studio.vercel.app/") + " <font color='#5b6774'>(sign-in required)</font><br/>"
    "<b>Source</b>&nbsp; " + L("https://github.com/tiansawang1818-pixel/wasmbot-studio", "github.com/tiansawang1818-pixel/wasmbot-studio"))

def heat_sources(x, y, w):
    """Grid of the seven monitored data sources under the HEAT screenshot."""
    y = label(c, "Seven real data sources, validated before publishing", x, y - 3 * mm, w)
    srcs = [("BMA boundaries", "50 Bangkok districts"), ("Landsat 8/9", "Surface temperature"),
            ("Sentinel-2", "Vegetation (NDVI)"), ("Dynamic World", "Land cover"),
            ("WorldPop", "Population"), ("Open-Meteo", "Hourly weather context"),
            ("OpenStreetMap", "Candidate public sites"), ("Traceable", "Every value versioned")]
    cols, gap, ch = 4, 3 * mm, 15 * mm
    cw = (w - (cols - 1) * gap) / cols
    for i, (t, d) in enumerate(srcs):
        cx = x + (i % cols) * (cw + gap)
        cy = y - 2 * mm - (i // cols + 1) * ch - (i // cols) * gap
        last = i == len(srcs) - 1
        c.setFillColor(BLUE if last else SOFT)
        c.setStrokeColor(BLUE if last else LINE)
        c.roundRect(cx, cy, cw, ch, 4, stroke=1, fill=1)
        c.setFillColor(white if last else INK)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(cx + 3 * mm, cy + ch - 6 * mm, t)
        c.setFillColor(white if last else MUTED)
        c.setFont("Helvetica", 8)
        c.drawString(cx + 3 * mm, cy + 3.5 * mm, d)


project_page(
    3, 2, "Geospatial · Decision intelligence", "HEAT//SHIFT",
    "A map-first platform for planning where to invest in cooling Bangkok, built on real satellite, weather, "
    "population, and OpenStreetMap data across all 50 districts, with every number traceable to its dataset version.",
    "heat-shift-live.jpg", "heatshift.hostless.app",
    None, None,
    "System and data workflow design: pipeline, database, planning tools, and cloud deployment.",
    ["<b>Six-stage pipeline</b>: staging, validation, processing, publishing, cache invalidation, live map updates.",
     "<b>Seven real sources</b> update automatically, including Landsat 8/9, Sentinel-2, Dynamic World, WorldPop, and OpenStreetMap.",
     "Versioned PostGIS datasets; invalid data never replaces the last good version.",
     "Budget optimizer with Google OR-Tools; forecasts that fail validation are withheld and their errors shown.",
     "Runs 24/7 on free-tier cloud hosting at <b>$0 cost</b>; admin tools behind single sign-on."],
    ["Python", "FastAPI", "Next.js", "MapLibre", "PostgreSQL", "PostGIS", "Redis", "Celery", "Earth Engine"],
    "<b>Live app</b>&nbsp; " + L("https://heatshift.hostless.app/") + "<br/>"
    "<b>Source</b>&nbsp; " + L("https://github.com/tiansawang1818-pixel/HEAT", "github.com/tiansawang1818-pixel/HEAT"),
    below=heat_sources)


# ---------- Page 4: more work, skills, contact ----------
top = header(c, 3, "More work", "Smaller builds and practice")
cw = (W - 2 * M - 10 * mm) / 2
items = [
    ("This portfolio", "HTML · CSS · JavaScript",
     "Buildless, responsive site with dark mode, keyboard navigation, reduced-motion support, and a print layout.",
     "https://github.com/tiansawang1818-pixel/tiansawang1818-pixel.github.io"),
    ("HTML101", "HTML · CSS",
     "Web fundamentals labs covering semantic HTML, page layout, styling, and multi-page sites.",
     "https://github.com/tiansawang1818-pixel/HTML101"),
]
iw_ = 100 * mm  # image width; text columns stay wider
y0 = shot(c, IMG + "portfolio-preview.jpg", M, top, iw_, "tiansawang1818-pixel.github.io")
for i, (t, tech, d, url) in enumerate(items):
    x = M + i * (cw + 10 * mm)
    yy = (y0 - 6 * mm) if i == 0 else top
    if i > 0:
        c.setFillColor(SOFT)
        c.setStrokeColor(LINE)
        c.roundRect(x, y0, iw_, top - y0, 5, stroke=1, fill=1)
        c.setFillColor(BLUE)
        c.setFont("Helvetica-Bold", 26)
        c.drawCentredString(x + iw_ / 2, (top + y0) / 2 - 4 * mm, "</>")
        yy = y0 - 6 * mm
    yy = para(c, f"<b>{t}</b>", "body", x, yy, cw)
    yy = para(c, tech, "small", x, yy - 1, cw)
    yy = para(c, d, "body", x, yy - 3, cw)
    para(c, L(url, "View repository"), "body", x, yy - 3, cw)

by = 62 * mm
c.setStrokeColor(LINE)
c.line(M, by + 8 * mm, W - M, by + 8 * mm)
half = (W - 2 * M - 12 * mm) / 2
yy = label(c, "Skills", M, by + 6 * mm, half, gap=2)
for k, v in [("Programming", "Python, TypeScript, JavaScript, Java, SQL"),
             ("Web Development", "HTML, CSS, Node.js, Express.js, Web Services"),
             ("Databases", "MySQL, Supabase"),
             ("Data and Modeling", "ER modeling, relational database design, data validation"),
             ("Tools", "Git, GitHub, VS Code, Linux, Postman, npm")]:
    yy = para(c, f"<b>{k}:</b> {v}", "body", M, yy - 1, half)
cx = M + half + 12 * mm
yy = label(c, "Let’s talk", cx, by + 6 * mm, half, gap=2)
yy = para(c, "Looking for a software engineering, backend, or data internship. Email is the fastest way to reach me.",
          "body", cx, yy - 1, half)
for line in [L("mailto:tiansawang1818@gmail.com", "tiansawang1818@gmail.com") + "&nbsp;&nbsp;·&nbsp;&nbsp;+66 84 228 6225",
             "<b>Website</b>&nbsp; " + L("https://tiansawang1818-pixel.github.io/"),
             "<b>GitHub</b>&nbsp; " + L("https://github.com/tiansawang1818-pixel"),
             "<b>LinkedIn</b>&nbsp; " + L(LI_URL, "linkedin.com/in/tiansawang-suetrong-95715343b")]:
    yy = para(c, line, "body", cx, yy - 2, half)
footer(c, 4)
c.showPage()
c.save()
print("built", OUT)

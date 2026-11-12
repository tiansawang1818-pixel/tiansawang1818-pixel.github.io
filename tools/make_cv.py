"""Build cv.pdf: the full-length CV (the one-page résumé is tools/make_resume.py).

Run: python3 tools/make_cv.py cv.pdf   (needs reportlab)
"""
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Flowable, KeepTogether
from reportlab.lib.units import mm

OUT = sys.argv[1] if len(sys.argv) > 1 else "cv.pdf"
INK = HexColor("#111111")
MUTED = HexColor("#5b6774")
RULE = HexColor("#b8c4d0")
LI_URL = "https://www.linkedin.com/in/tiansawang-suetrong-95715343b/"


def L(url, text=None):
    return f'<a href="{url}" color="#1f5f99"><u>{text or url.split("//")[-1].rstrip("/")}</u></a>'


name = ParagraphStyle("name", fontName="Helvetica-Bold", fontSize=27, leading=31, textColor=INK)
role = ParagraphStyle("role", fontName="Helvetica-Bold", fontSize=11.5, leading=14, textColor=INK, spaceBefore=6, spaceAfter=2)
contact = ParagraphStyle("contact", fontName="Helvetica", fontSize=9, leading=12.5, textColor=MUTED)
h = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=10.5, leading=13, textColor=INK, spaceBefore=11)
body = ParagraphStyle("body", fontName="Helvetica", fontSize=9.6, leading=13.2, textColor=INK)
ptitle = ParagraphStyle("pt", fontName="Helvetica-Bold", fontSize=10.3, leading=13, textColor=INK, spaceBefore=6)
meta = ParagraphStyle("meta", fontName="Helvetica-Oblique", fontSize=8.8, leading=12, textColor=MUTED)
sublabel = ParagraphStyle("sl", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=MUTED, spaceBefore=4)
bullet = ParagraphStyle("b", parent=body, leftIndent=11, firstLineIndent=-7, spaceBefore=1.2)
gray = ParagraphStyle("g", parent=body, textColor=MUTED)
foot = ParagraphStyle("f", parent=body, fontSize=8, textColor=MUTED)


class Rule(Flowable):
    def __init__(self):
        super().__init__()
        self.height = 5

    def wrap(self, w, h):
        self.width = w
        return w, self.height

    def draw(self):
        self.canv.setStrokeColor(RULE)
        self.canv.setLineWidth(0.8)
        self.canv.line(0, 3, self.width, 3)


def section(t):
    return [Paragraph(t.upper().replace(" ", "&nbsp;"), h), Rule()]


def b(t):
    return Paragraph("•&nbsp;" + t, bullet)


SEP = ' <font color="#5b6774">&nbsp;|&nbsp;</font> '

s = []
s += [Paragraph("TIANSAWANG SUETRONG", name),
      Paragraph("CURRICULUM VITAE&nbsp; | &nbsp;SOFTWARE ENGINEERING, BACKEND &amp; DATA", role),
      Paragraph("Bangkok, Thailand" + SEP + "+66 84 228 6225" + SEP + L("mailto:tiansawang1818@gmail.com", "tiansawang1818@gmail.com"), contact),
      Paragraph("<b>Portfolio</b>&nbsp; " + L("https://tiansawang1818-pixel.github.io/") +
                "&nbsp;&nbsp;&nbsp;<b>GitHub</b>&nbsp; " + L("https://github.com/tiansawang1818-pixel"), contact),
      Paragraph("<b>LinkedIn</b>&nbsp; " + L(LI_URL, "linkedin.com/in/tiansawang-suetrong-95715343b"), contact)]

s += section("Profile")
s.append(Paragraph(
    "Digital Science and Technology student at the Faculty of ICT, Mahidol University, seeking a software engineering, "
    "backend, or data internship. I like owning the whole system: the interface people use, the API in the middle, and "
    "the data model underneath. I have built and deployed two full-stack systems that are live today: a no-code bot "
    "platform running on Rust WebAssembly, and a geospatial decision platform for Bangkok’s urban heat that runs on real "
    "satellite and open data. I care about correctness: every number should be traceable to its source, and a system "
    "should say plainly when its data is missing rather than guess.", body))

s += section("Education")
s.append(Paragraph('Mahidol University <font color="#5b6774" size="9">&nbsp;|&nbsp; 2025 - Present</font>', ptitle))
s.append(Paragraph("Faculty of Information and Communication Technology (ICT)", gray))
s.append(Paragraph("Bachelor of Science in Digital Science and Technology&nbsp; | &nbsp;GPA 3.08", gray))
s.append(Paragraph("<b>Relevant Coursework:</b> Database Systems, Data Structures, Web Programming, Object-Oriented Programming", body))
s.append(Paragraph('Klaeng Wittayasathaworn School <font color="#5b6774" size="9">&nbsp;|&nbsp; 2022 - 2025</font>', ptitle))
s.append(Paragraph("Secondary Education", gray))

s += section("Technical Skills")
for k, v in [("Programming", "Python, TypeScript, JavaScript, Java, SQL"),
             ("Web Development", "HTML, CSS, Node.js, Web Services"),
             ("Databases", "PostgreSQL, MySQL, Supabase"),
             ("Data and Modeling", "ER modeling, relational database design, data validation"),
             ("Tools", "Git, GitHub, VS Code")]:
    s.append(Paragraph(f"<b>{k}:</b> {v}", body))

s += section("Projects")

heat = [Paragraph("HEAT//SHIFT - Map-first urban heat decision platform for Bangkok", ptitle),
        Paragraph("Live pilot, 2026" + SEP + L("https://github.com/tiansawang1818-pixel/HEAT", "GitHub Repository") + SEP +
                  L("https://heatshift.hostless.app/", "Live Website"), meta),
        Paragraph("<i>Python, FastAPI, Next.js, MapLibre, PostgreSQL/PostGIS, Redis/Celery, Google Earth Engine, OR-Tools, Docker, GitHub Actions</i>", meta),
        Paragraph("A platform that helps plan where to invest in cooling Bangkok, using real satellite, weather, population, "
                  "and map data across all 50 districts.", body),
        Paragraph("Data pipeline", sublabel),
        b("Designed a six-stage pipeline: staging, validation, processing, publishing, cache invalidation, and live client "
          "updates over Server-Sent Events; invalid data fails the job and keeps the previous version."),
        b("Connected seven real sources that update automatically: Bangkok district boundaries, Landsat 8/9 land surface temperature, "
          "Sentinel-2 NDVI, Dynamic World land cover, WorldPop population, Open-Meteo weather, and OpenStreetMap."),
        b("Separates when a provider observed the data from when the system last checked it, and stores every published "
          "version so each map value can be traced to its dataset version."),
        Paragraph("Planning and analysis", sublabel),
        b("Built a budget optimizer with Google OR-Tools that compares strategies on candidate sites with referenced costs."),
        b("Withholds forecasts that fail holdout validation and shows their errors, and keeps unverified sites out of the "
          "optimizer instead of inventing costs or benefits."),
        b("Generated printable evidence reports with data versions, uncertainty, and stale-result warnings."),
        KeepTogether([Paragraph("Operations and security", sublabel),
        b("Runs 24/7 on free-tier cloud hosting at $0 cost, with web, API, worker, and scheduler supervised inside one "
          "container under a 768 MiB memory limit.")]),
        b("Protected admin tools with OpenID Connect single sign-on and role checks; production refuses demo data and shared keys."),
        b("Added CI checks that build the hosted image and test it under the same CPU and memory limits as production.")]
s += heat

wb = [Paragraph("WasmBot Studio - No-code business rule bot platform", ptitle),
      Paragraph("Deployed, 2026" + SEP + L("https://github.com/tiansawang1818-pixel/wasmbot-studio", "GitHub Repository") + SEP +
                L("https://wasmbot-studio.vercel.app/", "Live Website"), meta),
      Paragraph("<i>TypeScript, React, Vite, Tailwind CSS, Supabase (Auth, PostgreSQL, Edge Functions), Rust WebAssembly</i>", meta),
      Paragraph("A platform that lets non-developers turn decision rules into secure, shareable bots.", body),
      b("Built a visual editor for nested AND/OR rules with 12 comparison operators, executed by a Rust rule engine "
        "compiled to WebAssembly rather than simulated in the browser."),
      b("Designed immutable, versioned deployments so draft edits never affect the live version."),
      b("Exposed each bot through a hosted form, iframe/script embed, REST API, signed webhooks, and a typed TypeScript SDK."),
      b("Secured data with Supabase Auth, PostgreSQL row-level security, scoped API keys stored as HMAC-SHA256 hashes, "
        "rate limits, domain allowlists, and audit logs."),
      b("Built webhook delivery with AES-GCM encrypted secrets and a transactional outbox with up to three attempts."),
      b("Integrated the WASM engine with seven Supabase Edge Functions and verified the system with 71 automated tests, "
        "including production, authentication, authorization, and security-header checks.")]
s += wb

s.append(Paragraph("Other work", sublabel))
s += [b("<b>Personal portfolio</b> (" + L("https://tiansawang1818-pixel.github.io/", "website") + "): buildless, responsive "
        "site in HTML, CSS, and JavaScript with dark mode, keyboard navigation, reduced-motion support, and a print layout."),
      b("<b>python-calculator</b> (" + L("https://github.com/tiansawang1818-pixel/python-calculator", "GitHub") + "): "
        "unit-testing practice for a calculator class."),
      b("<b>HTML101</b> (" + L("https://github.com/tiansawang1818-pixel/HTML101", "GitHub") + "): web fundamentals labs "
        "covering semantic HTML, layout, styling, and multi-page sites.")]

s += section("Experience and Activities")
s.append(Paragraph('<b>MUICT Open House - Guest Relations</b><font color="#5b6774">&nbsp; | &nbsp;Mahidol University&nbsp; | &nbsp;2026</font>', body))
s.append(Paragraph('<b>Raknong G2 - Staff</b><font color="#5b6774">&nbsp; | &nbsp;Mahidol University&nbsp; | &nbsp;2026</font>', body))

s += section("Languages")
s.append(Paragraph("Thai: Native&nbsp; | &nbsp;English: Intermediate", body))

s += section("Interests")
s.append(Paragraph("<b>Web and software:</b> designing systems that fit together, from the database schema to the button people click.", body))
s.append(Paragraph("<b>Data and geospatial:</b> turning messy real-world data into versioned, trustworthy decisions on a map.", body))
s.append(Paragraph("<b>AI and networks:</b> exploring intelligent applications and how devices communicate.", body))

s += section("References")
s.append(Paragraph("Available upon request.", body))


def footer(c, d):
    c.saveState()
    c.setFont("Helvetica", 8)
    c.setFillColor(MUTED)
    c.drawRightString(A4[0] - 18 * mm, 8 * mm, f"Tiansawang Suetrong - CV - page {c.getPageNumber()}")
    c.restoreState()


doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=15 * mm, bottomMargin=15 * mm,
                        title="Tiansawang Suetrong - Curriculum Vitae", author="Tiansawang Suetrong",
                        subject="Curriculum vitae")
doc.build(s, onFirstPage=footer, onLaterPages=footer)
print("built", OUT)

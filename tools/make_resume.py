import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Flowable
from reportlab.lib.units import mm

OUT = sys.argv[1]
INK = HexColor("#111111")
MUTED = HexColor("#5b6774")
LINK = HexColor("#1f5f99")
RULE = HexColor("#b8c4d0")

def L(url, text=None):
    return f'<a href="{url}" color="#1f5f99"><u>{text or url.split("//")[-1].rstrip("/")}</u></a>'

name = ParagraphStyle("name", fontName="Helvetica-Bold", fontSize=27, leading=31, textColor=INK)
role = ParagraphStyle("role", fontName="Helvetica-Bold", fontSize=11.5, leading=14, textColor=INK, spaceBefore=6, spaceAfter=2)
sub = ParagraphStyle("sub", fontName="Helvetica-Bold", fontSize=9, leading=12, textColor=MUTED)
contact = ParagraphStyle("contact", fontName="Helvetica", fontSize=9, leading=12.5, textColor=MUTED)
h = ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=10.5, leading=13, textColor=INK, spaceBefore=9)
body = ParagraphStyle("body", fontName="Helvetica", fontSize=9.6, leading=13, textColor=INK)
ptitle = ParagraphStyle("pt", fontName="Helvetica-Bold", fontSize=10.3, leading=13, textColor=INK, spaceBefore=4)
meta = ParagraphStyle("meta", fontName="Helvetica-Oblique", fontSize=8.8, leading=12, textColor=MUTED)
bullet = ParagraphStyle("b", parent=body, leftIndent=11, firstLineIndent=-7, spaceBefore=1.2)
gray = ParagraphStyle("g", parent=body, textColor=MUTED)

class Rule(Flowable):
    def __init__(self): super().__init__(); self.height = 5
    def wrap(self, w, h): self.width = w; return w, self.height
    def draw(self):
        self.canv.setStrokeColor(RULE); self.canv.setLineWidth(0.8)
        self.canv.line(0, 3, self.width, 3)

def section(t): return [Paragraph(t.upper().replace(" ", "&nbsp;"), h), Rule()]
def b(t): return Paragraph("•&nbsp;" + t, bullet)
SEP = ' <font color="#5b6774">&nbsp;|&nbsp;</font> '

s = []
s += [Paragraph("TIANSAWANG SUETRONG", name),
      Paragraph("SOFTWARE ENGINEERING&nbsp; | &nbsp;BACKEND &amp; DATA", role),
      Paragraph("Bangkok, Thailand" + SEP + "+66 84 228 6225" + SEP + L("mailto:tiansawang1818@gmail.com", "tiansawang1818@gmail.com"), contact),
      Paragraph("<b>Portfolio</b>&nbsp; " + L("https://tiansawang1818-pixel.github.io/") + "&nbsp;&nbsp;&nbsp;<b>GitHub</b>&nbsp; " + L("https://github.com/tiansawang1818-pixel"), contact),
      Paragraph("<b>LinkedIn</b>&nbsp; " + L("https://www.linkedin.com/in/tiansawang-suetrong-95715343b/", "linkedin.com/in/tiansawang-suetrong-95715343b"), contact)]

s += section("Profile")
s.append(Paragraph("Digital Science and Technology student at Mahidol University seeking a software engineering, backend, or data "
                   "internship. Built and deployed two live full-stack systems: a no-code bot platform on Rust WebAssembly and a "
                   "geospatial platform for Bangkok’s urban heat.", body))

s += section("Technical Skills")
for k, v in [("Programming", "Python, TypeScript, JavaScript, Java, SQL"),
             ("Web Development", "HTML, CSS, Node.js, Express.js, Web Services"),
             ("Databases", "MySQL, Supabase"),
             ("Data and Modeling", "ER modeling, relational database design, data validation"),
             ("Tools", "Git, GitHub, VS Code, Linux, Postman, npm")]:
    s.append(Paragraph(f"<b>{k}:</b> {v}", body))

s += section("Projects")
s.append(Paragraph("HEAT//SHIFT - Live Pilot", ptitle))
s.append(Paragraph("<i>Python | FastAPI | Next.js | PostgreSQL/PostGIS | Redis/Celery | MapLibre</i>" + SEP +
                   L("https://github.com/tiansawang1818-pixel/HEAT", "GitHub Repository") + SEP +
                   L("https://heatshift.hostless.app/", "Live Website"), meta))
s += [b("Built and deployed a map-first platform for planning heat mitigation investment across Bangkok’s 50 districts."),
      b("Designed a six-stage pipeline (staging, validation, processing, publishing, cache invalidation, live client updates) "
        "that monitors seven real sources, including Landsat 8/9, Sentinel-2, Dynamic World, WorldPop, and OpenStreetMap."),
      b("Built versioned PostGIS datasets, a budget optimizer with Google OR-Tools, and evidence reports showing data versions, "
        "uncertainty, and stale-result warnings; admin tools are protected by OIDC single sign-on."),
      b("Runs 24/7 on free-tier cloud hosting at $0 cost.")]

s.append(Paragraph("WasmBot Studio", ptitle))
s.append(Paragraph("<i>TypeScript | React | Supabase | PostgreSQL | Rust WebAssembly</i>" + SEP +
                   L("https://github.com/tiansawang1818-pixel/wasmbot-studio", "GitHub Repository") + SEP +
                   L("https://wasmbot-studio.vercel.app/", "Live Website"), meta))
s += [b("Built a no-code platform for creating rule-based business bots with a visual AND/OR editor supporting 12 operators."),
      b("Designed versioned deployments with immutable snapshots and secured data using Supabase Auth, PostgreSQL "
        "row-level security, scoped API keys, and rate limiting."),
      b("Integrated a Rust WebAssembly rule engine with seven Supabase Edge Functions and validated the deployed system "
        "through automated and end-to-end testing.")]

s += section("Education")
s.append(Paragraph('Mahidol University <font color="#5b6774" size="9">&nbsp;|&nbsp; 2025 - Present</font>', ptitle))
s.append(Paragraph("Faculty of Information and Communication Technology", gray))
s.append(Paragraph("Bachelor of Science in Digital Science and Technology&nbsp; | &nbsp;GPA 3.10", gray))
s.append(Paragraph("<b>Relevant Coursework:</b> Database Systems, Data Structures, Web Programming, Object-Oriented Programming", body))
s.append(Paragraph('Klaeng Wittayasathaworn School <font color="#5b6774" size="9">&nbsp;|&nbsp; 2022 - 2025</font>', ptitle))
s.append(Paragraph("Secondary Education", gray))

s += section("Experience and Activities")
s.append(Paragraph('<b>MUICT Open House - Guest Relations</b><font color="#5b6774">&nbsp; | &nbsp;Mahidol University&nbsp; | &nbsp;2026</font>', body))
s.append(Paragraph('<b>Raknong G2 - Staff</b><font color="#5b6774">&nbsp; | &nbsp;Mahidol University&nbsp; | &nbsp;2026</font>', body))

s += section("Languages")
s.append(Paragraph("Thai: Native&nbsp; | &nbsp;English: Intermediate", body))

doc = SimpleDocTemplate(OUT, pagesize=A4, leftMargin=18*mm, rightMargin=18*mm, topMargin=15*mm, bottomMargin=12*mm,
                        title="Tiansawang Suetrong - Resume", author="Tiansawang Suetrong",
                        subject="Software engineering internship resume")
pages = []
doc.build(s, onLaterPages=lambda c, d: pages.append(c.getPageNumber()))
print("pages:", 1 + len(pages))

#!/usr/bin/env python3
"""Render the 20 November 2026 world-news poster.

Concept: a broadsheet front page — "read the whole world in one page".
Masthead with the date, a UTC timeline of the day, three lead panels, then
50 numbered stories in three columns grouped by beat, and a market ticker
plus a date-check footer. All 50 stories were checked against reports
dated 20 November 2026 (Reuters summary, Investors/WSJ market coverage,
Indian 20 Nov headlines, Philippine Star 20 Nov headlines, BJ Sports).
Deterministic: same input -> same bytes (no clock, no randomness).
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 229)
PANEL = (255, 253, 246)
INK = (25, 23, 19)
RED = (166, 28, 28)
BLUE = (30, 79, 138)
GREEN = (30, 107, 52)
RULE = (190, 178, 155)
MUTED = (96, 88, 74)

FD = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(os.path.join(FD, name), size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)

# (section, headline) — 3 leads are separate; these 47 complete the 50.
STORIES = [
    ("SUMMIT & WAR", "Allies warn of a \u201cYalta-style carve-up\u201d as Trump meets Putin"),
    ("SUMMIT & WAR", "Putin invites European envoys to Moscow on Ukraine talks"),
    ("SUMMIT & WAR", "Zelenskiy: positions strong; two frontline towns held"),
    ("SUMMIT & WAR", "Gazans return to camp as Israel ends tank raid"),
    ("SUMMIT & WAR", "ICJ: Myanmar likely intended to destroy the Rohingya"),
    ("SUMMIT & WAR", "US\u2013Venezuela sign deal to restore military ties"),
    ("ASIA", "Modi meets Prince and Princess of Wales in Delhi"),
    ("ASIA", "Modi opens FICCI centenary convention"),
    ("ASIA", "Seoul court overturns ex-PM Han\u2019s martial-law conviction"),
    ("ASIA", "Fiji declares national disaster as drought bites"),
    ("ASIA", "North Korea expanding Yongbyon enrichment \u2014 IAEA"),
    ("ASIA", "Philippines signs free-trade deal with Chile"),
    ("ASIA", "Arson fire at Yunus ancestral home in Bangladesh"),
    ("ASIA", "APEC Shenzhen: Xi urges open trade, tech cooperation"),
    ("EUROPE & AMERICAS", "Russia warns Wikipedia owner could be \u201cundesirable\u201d"),
    ("EUROPE & AMERICAS", "UK: four convicted in Pelicot-echo drug-rape case"),
    ("EUROPE & AMERICAS", "French minister summons official over alleged leak"),
    ("EUROPE & AMERICAS", "Bukele to seek unprecedented third term"),
    ("EUROPE & AMERICAS", "Rome rebukes Kyiv over blacklisted Italian MPs"),
    ("EUROPE & AMERICAS", "US report: curb China aerospace investment"),
    ("EUROPE & AMERICAS", "Musk: \u201cI\u2019m not MAGA\u201d \u2014 rues $500M on midterms"),
    ("MARKETS", "S&P\u2019s 6-day losing streak; VIX highest since March"),
    ("MARKETS", "AMD dives after short-seller report"),
    ("MARKETS", "Apple is building its own AI agent"),
    ("MARKETS", "Palo Alto to buy Applied Compute for $4.5B"),
    ("MARKETS", "US jobless claims 203,000"),
    ("MARKETS", "Nvidia\u2019s $118B AI guarantees hinge on one Ohio campus"),
    ("TECH & SCIENCE", "Google hires Blue Origin to launch AI satellites (2029)"),
    ("TECH & SCIENCE", "Gemini 4 Neon: $3 per million tokens, tops coding chart"),
    ("TECH & SCIENCE", "OpenAI: AI designed chips \u2014 AMD GPU +14% faster"),
    ("TECH & SCIENCE", "Genie 4: walk through worlds you can rewrite live"),
    ("TECH & SCIENCE", "Astronomers may have watched a star swallow its twin"),
    ("TECH & SCIENCE", "New flying frog species found in Indonesia"),
    ("INDIA", "Sensex 83,021; Nifty tops 25,500"),
    ("INDIA", "State banks post \u20b91 lakh crore profit"),
    ("INDIA", "New PUC renewal rules for older vehicles"),
    ("INDIA", "IAF exercise \u201cSahyata Setu\u201d in Jamnagar"),
    ("INDIA", "NEET leak: charges framed against 14 accused"),
    ("SPORT", "Nicholls 113* lifts NZ to 243/5 vs India"),
    ("SPORT", "South Africa beat Bangladesh by 9 wickets"),
    ("SPORT", "South Africa top the WTC table at 75%"),
    ("SPORT", "England seal ODI series win in Australia"),
    ("SPORT", "Chelsea 1\u20130 PSG \u2014 Buurman 87th-minute winner"),
    ("SPORT", "Alcaraz beats Medvedev 6\u20132, 6\u20134 at ATP Finals"),
    ("SPORT", "Illinois 99\u201378 Duke; Stojakovic scores 46"),
    ("SPORT", "Pochettino begins as Manchester United boss"),
    ("SPORT", "Wattimena beats Littler 10\u20138 at Grand Slam of Darts"),
]

LEADS = [
    ("THE G3 AFTERMATH", RED,
     "Three leaders, one declaration",
     "Trump, Xi and Putin sign a three-way peace declaration in Shenzhen: "
     "nuclear risk cuts, Hormuz kept open. Ukraine and Taiwan are not named; "
     "allies warn of a \u201cYalta-style carve-up\u201d.",
     "G20 invite: Putin to Miami next month"),
    ("THE $81BN DEBUT", BLUE,
     "The biggest IPO ever \u2014 and the market still fell",
     "Anthropic prices at $83, opens at $111.50, closes $97.17 (+17%) in the "
     "largest IPO on record. The cheer lasts minutes: the Dow sheds 1,101 "
     "points, the S&P 2%, the Nasdaq 2.3%.",
     "ANT $97.17  \u00b7  Dow 49,097  \u00b7  VIX at March high"),
    ("AKVAN COMES ASHORE", GREEN,
     "Cyclone Akvan hits India\u2019s east coast",
     "The severe cyclone makes landfall on the Odisha\u2013Andhra coast. "
     "Schools shut, evacuations under way, 10 trains cancelled and 23 "
     "diverted as 90\u2013100 km/h winds lash the shore.",
     "Landfall: Friday 20 November 2026"),
]

TIMELINE = [
    (0.00, "00:00 UTC", "Akvan landfall watch \u2014 Odisha coast"),
    (10 / 24, "10:00 UTC", "Sensex closes +1.2%"),
    (14.5 / 24, "14:30 UTC", "Wall Street opens"),
    (21 / 24, "21:00 UTC", "Dow closes \u22121,101"),
]


def wrap(draw, text, fnt, width):
    """Wrap text to fit width; returns list of lines."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_center(draw, y, text, fnt, fill, x0=0, x1=W):
    tw = draw.textlength(text, font=fnt)
    draw.text(((x0 + x1 - tw) / 2, y), text, font=fnt, fill=fill)


def render(path):
    assert len(STORIES) == 47, len(STORIES)
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 28  # margin

    # ---- masthead ----
    d.line([(mx, 14), (W - mx, 14)], fill=INK, width=2)
    draw_center(d, 24, "T H E   W O R L D   I N   O N E   I M A G E", SANS_B(17), INK)
    draw_center(d, 50, "FRIDAY, 20 NOVEMBER 2026", SERIF_B(46), INK)
    draw_center(d, 108,
                "50 stories \u00b7 one day \u00b7 every story checked against reports of 20 November 2026",
                SANS(14), MUTED)
    d.line([(mx, 132), (W - mx, 132)], fill=INK, width=2)
    d.line([(mx, 136), (W - mx, 136)], fill=INK, width=1)

    # ---- UTC timeline ----
    d.text((W - mx, 148), "THE DAY IN UTC", font=SANS_B(11), fill=RED, anchor="ra")
    bar_y = 176
    d.line([(mx, bar_y), (W - mx, bar_y)], fill=RULE, width=2)
    for frac, t, label in TIMELINE:
        x = mx + frac * (W - 2 * mx)
        d.ellipse([x - 4, bar_y - 4, x + 4, bar_y + 4], fill=RED)
        if frac == 0.0:
            d.text((x, 156), t, font=SANS_B(10), fill=INK, anchor="la")
            d.text((x, bar_y + 8), label, font=SANS(10), fill=MUTED, anchor="la")
        elif frac >= 0.85:
            d.text((x, 156), t, font=SANS_B(10), fill=INK, anchor="ra")
            d.text((x, bar_y + 8), label, font=SANS(10), fill=MUTED, anchor="ra")
        else:
            d.text((x - 1, 156), t, font=SANS_B(10), fill=INK, anchor="ma")
            d.text((x, bar_y + 8), label, font=SANS(10), fill=MUTED, anchor="ma")

    # ---- lead panels ----
    top, ph, pw, gap = 206, 158, 312, 12
    for i, (kick, col, head, body, stat) in enumerate(LEADS):
        x = mx + i * (pw + gap)
        d.rectangle([x, top, x + pw, top + ph], fill=PANEL, outline=RULE, width=1)
        d.rectangle([x, top, x + pw, top + 5], fill=col)
        d.text((x + 10, top + 12), kick, font=SANS_B(10), fill=col)
        y = top + 30
        for ln in wrap(d, head, SERIF_B(19), pw - 20):
            d.text((x + 10, y), ln, font=SERIF_B(19), fill=INK)
            y += 22
        y += 2
        for ln in wrap(d, body, SANS(11), pw - 20)[:4]:
            d.text((x + 10, y), ln, font=SANS(11), fill=INK)
            y += 14
        d.text((x + 10, top + ph - 18), stat, font=SANS_B(10), fill=col)

    # ---- section divider ----
    y = top + ph + 12
    d.line([(mx, y), (W - mx, y)], fill=INK, width=1)
    draw_center(d, y + 5, "T H E   D A Y   I N   5 0   S T O R I E S", SANS_B(13), INK)
    y += 26
    d.line([(mx, y), (W - mx, y)], fill=INK, width=1)

    # ---- story grid: 3 columns, flow layout ----
    grid_top, grid_bottom = y + 10, 946
    col_w = 312
    cols = [mx, mx + col_w + gap, mx + 2 * (col_w + gap)]
    ci, cy = 0, grid_top
    section = None
    for n, (sec, head) in enumerate(STORIES, start=4):
        if sec != section:
            section = sec
            if cy + 16 > grid_bottom:
                ci += 1
                cy = grid_top
            d.text((cols[ci], cy), sec, font=SANS_B(10), fill=RED)
            d.line([(cols[ci], cy + 14), (cols[ci] + col_w, cy + 14)], fill=RULE, width=1)
            cy += 20
        lines = wrap(d, head, SANS(11), col_w - 26)
        need = 15 * min(len(lines), 2)
        if cy + need > grid_bottom:
            ci += 1
            cy = grid_top
            section = None
            d.text((cols[ci], cy), sec, font=SANS_B(10), fill=RED)
            d.line([(cols[ci], cy + 14), (cols[ci] + col_w, cy + 14)], fill=RULE, width=1)
            cy += 20
            section = sec
        d.text((cols[ci], cy), f"{n}.", font=SANS_B(11), fill=RED)
        yy = cy
        for ln in lines[:2]:
            d.text((cols[ci] + 26, yy), ln, font=SANS(11), fill=INK)
            yy += 14
        cy += max(need, 28)

    # ---- footer ticker + date check ----
    fy = 956
    d.rectangle([mx, fy, W - mx, fy + 26], fill=INK)
    draw_center(d, fy + 6,
                "DOW \u22121,101  \u00b7  S&P \u22122.0%  \u00b7  NASDAQ \u22122.3%  \u00b7  ANT $97.17 +17%  \u00b7  "
                "SENSEX +1.2%  \u00b7  NIFTY 25,500+  \u00b7  VIX HIGHEST SINCE MARCH",
                SANS_B(11), PAPER)
    draw_center(d, fy + 34,
                "\u2713 DATE CHECK \u00b7 FRIDAY 20 NOVEMBER 2026 \u00b7 WORLD CHILDREN\u2019S DAY \u00b7 "
                "50 stories from 20 Nov 2026 reports \u00b7 make.fun news-image-20261120",
                SANS(10), MUTED)

    img.save(path, optimize=True)
    return path


if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "assets/entry.png"
    render(out)
    print("wrote", out)

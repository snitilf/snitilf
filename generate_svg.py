"""
i know you want to copy this so here's what this does
builds dark_mode.svg and light_mode.svg from ascii-art.txt and the info lines below

usage: python3 generate_svg.py

every card row is 60 monospace chars wide, so len(key) + len(value) <= 54 or the dots run out
"""
import html
import os

OUT_DIR = os.path.dirname(os.path.abspath(__file__))

# ascii-art.txt is 101 cols wide; the card shows this window of it
CROP_LEFT, CROP_COLS = 27, 50
ASCII_FONT, ASCII_STEP = 12, 11  # px, smaller = more zoomed out

# the art was made for a light background, so flip char density for dark mode
RAMP = ' .-=+*#%@'
INVERT = str.maketrans(RAMP, RAMP[::-1])

def ascii_art():
    with open(os.path.join(OUT_DIR, 'ascii-art.txt')) as f:
        lines = [l.rstrip('\n') for l in f if l.strip()]
    return [l[CROP_LEFT:CROP_LEFT + CROP_COLS] for l in lines]

def invert_art(art):
    return [line.translate(INVERT).rstrip() for line in art]

WIDTH = 60  # monospace chars per right-column line

def key_spans(key):
    return '.'.join(f'<tspan class="key">{part}</tspan>' for part in key.split('.'))

def info_line(y, key, value):
    seg_len = WIDTH - 3 - len(key) - len(value)  # '. ' prefix + ':' after key
    if seg_len >= 3:
        seg = ' ' + '.' * (seg_len - 2) + ' '
    else:
        seg = {0: '', 1: ' ', 2: '. '}[seg_len]
    return (f'<tspan x="390" y="{y}" class="cc">. </tspan>{key_spans(key)}:'
            f'<tspan class="cc">{seg}</tspan><tspan class="value">{html.escape(value)}</tspan>')

def header_line(y, title):
    dashes = WIDTH - len(title) - 4
    return (f'<tspan x="390" y="{y}" class="hdr">{title}</tspan>'
            f'<tspan class="rule"> -{"—" * dashes}-—-</tspan>')

def right_column():
    L = []
    L.append(header_line(30, '@snitilf'))
    L.append(info_line(50, 'Work', 'Ubisoft (prev SunLife, BMO)'))
    L.append(info_line(70, 'School', 'McGill University (CS)'))
    L.append(info_line(90, 'Location', 'Montreal, QC'))
    L.append(info_line(110, 'BIXI.Stats', '1809km'))
    L.append(info_line(150, 'OS', 'macOS Tahoe 26.5.1'))
    L.append(info_line(170, 'Shell', 'zsh wearing a bash costume'))
    L.append(info_line(190, 'Uptime', '3 coffees a day'))
    L.append(info_line(210, 'Sleep', 'Segmentation fault'))
    L.append(info_line(230, 'Audio.Driver', 'Metalcore, rock, deep house'))
    L.append(info_line(270, 'Languages.Programming', 'Python, TypeScript, Rust, Java'))
    L.append(info_line(290, 'Languages.Computer', 'HTML, CSS, SQL, LaTeX, Bash'))
    L.append(info_line(310, 'Languages.Real', 'English, Czech, French'))
    L.append(info_line(330, 'Hobbies.Software', 'Security, ML, Side Quests'))
    L.append(info_line(350, 'Hobbies.GrassTouching', 'Calisthenics, Bouldering, Running'))
    L.append(header_line(390, '- Contact'))
    L.append(info_line(410, 'Email', 'filip.snitil@mail.mcgill.ca'))
    L.append(info_line(430, 'LinkedIn', 'linkedin.com/in/snitilf'))
    L.append(header_line(470, '- Currently'))
    L.append(info_line(490, 'Learning', 'LLM Fine-tuning, RLHF'))
    L.append(info_line(510, 'Building', 'Nordet (coming soon)'))
    return '\n'.join(L)

# graphite - a pure neutral ramp, chroma 0 everywhere. hierarchy comes only from
# lightness, so the eye lands value -> key -> art -> leaders in that order.
#
# on the card edge: github's dark canvases (#010409 high contrast, #0d1117 default,
# #212830 soft dark) all sit at relative luminance .001-.021, so no near-black fill
# can clear even 1.1:1 against them. the 1px border is what makes this read as an
# object on every theme - it holds 1.85-2.01:1 against all three.
THEMES = {
    'dark_mode.svg': dict(bg='#0c0c0b', border='#434041', hdr='#f5f5f5', rule='#303030',
                          key='#989898', value='#ebebeb', cc='#353535',
                          # dark mode inverts glyph density, so the art already has
                          # a wide tonal range - one fill plus a soft vertical
                          # falloff is enough.
                          art=('#bebebd', '#717171'), art_tone=None),
    'light_mode.svg': dict(bg='#f7f7f7', border='#d1d1d1', hdr='#2e2e2e', rule='#cccccc',
                           key='#707070', value='#2a2a2a', cc='#c6c5c5',
                           # light mode does NOT invert, so every glyph in the crop
                           # is heavy ink (no spaces or dots at all) and the face
                           # flattens into a slab. tone each glyph by its density
                           # instead, which restores the portrait.
                           art=None, art_tone=('#eeeeee', '#0b0b0b')),
}

TEMPLATE = '''<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,monospace" width="985px" height="530px" font-size="16px">
<style>
@font-face {{
src: local('Consolas'), local('Consolas Bold');
font-family: 'ConsolasFallback';
font-display: swap;
-webkit-size-adjust: 109%;
size-adjust: 109%;
}}
.hdr {{fill: {hdr}; font-weight: bold;}}
.rule {{fill: {rule};}}
.key {{fill: {key};}}
.value {{fill: {value};}}
.cc {{fill: {cc};}}
text, tspan {{white-space: pre;}}
</style>
{defs}<rect x="0.5" y="0.5" width="984" height="529" rx="14.5" fill="{bg}" stroke="{border}" stroke-width="1"/>
<text x="15" y="30" fill="{art_fill}" font-size="{ascii_font}px">
{ascii_block}
</text>
<text x="390" y="30" fill="{value}">
{right}
</text>
</svg>
'''

GRAD = ('<defs><linearGradient id="a" x1="0" y1="0" x2="0.35" y2="1">'
        '<stop offset="0" stop-color="{0}"/><stop offset="1" stop-color="{1}"/>'
        '</linearGradient></defs>\n')

def lerp_hex(a, b, t):
    a, b = a.lstrip('#'), b.lstrip('#')
    return '#' + ''.join(f'{round(int(a[i:i+2],16)+(int(b[i:i+2],16)-int(a[i:i+2],16))*t):02x}'
                         for i in (0, 2, 4))

def tone_runs(line, y, sparse, dense):
    """one tspan per run of equal glyph, toned by where that glyph sits on RAMP"""
    out, i = [], 0
    while i < len(line):
        j = i
        while j < len(line) and line[j] == line[i]:
            j += 1
        fill = lerp_hex(sparse, dense, RAMP.index(line[i]) / (len(RAMP) - 1))
        out.append(f'<tspan fill="{fill}">{line[i] * (j - i)}</tspan>')
        i = j
    return f'<tspan x="15" y="{y:g}">' + ''.join(out) + '</tspan>'

if __name__ == '__main__':
    art = ascii_art()
    y0 = (530 - len(art) * ASCII_STEP) / 2 + ASCII_FONT - 2

    right = right_column()
    for name, t in THEMES.items():
        t = dict(t)
        lines = invert_art(art) if name.startswith('dark') else art
        tone = t.pop('art_tone')
        grad = t.pop('art')
        if tone:
            block = '\n'.join(tone_runs(l, y0 + i * ASCII_STEP, *tone)
                              for i, l in enumerate(lines))
            defs, art_fill = '', tone[1]
        else:
            block = '\n'.join(f'<tspan x="15" y="{y0 + i * ASCII_STEP:g}">{l}</tspan>'
                              for i, l in enumerate(lines))
            defs, art_fill = GRAD.format(*grad), 'url(#a)'
        with open(os.path.join(OUT_DIR, name), 'w', encoding='utf-8') as f:
            f.write(TEMPLATE.format(ascii_block=block, right=right, defs=defs,
                                    art_fill=art_fill, ascii_font=ASCII_FONT, **t))
    print('wrote dark_mode.svg and light_mode.svg')

"""
i know you want to copy this so here's what this does
builds dark_mode.svg and light_mode.svg from ascii-art.txt and the info lines below

usage: python3 generate_svg.py && python3 today.py

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

def dyn_line(y, key, elem_id, placeholder, just):
    seg = ' ' + '.' * (just - len(placeholder)) + ' '
    return (f'<tspan x="390" y="{y}" class="cc">. </tspan>{key_spans(key)}:'
            f'<tspan class="cc" id="{elem_id}_dots">{seg}</tspan>'
            f'<tspan class="value" id="{elem_id}">{placeholder}</tspan>')

def header_line(y, title):
    dashes = WIDTH - len(title) - 4
    return f'<tspan x="390" y="{y}">{title}</tspan> -{"—" * dashes}-—-'

def blank(y):
    return f'<tspan x="390" y="{y}" class="cc">. </tspan>'

def right_column():
    L = []
    L.append(header_line(30, '@snitilf'))
    L.append(info_line(50, 'School', 'McGill University (CS)'))
    L.append(info_line(70, 'Work', 'Ubisoft'))
    # today.py updates this daily; keep 36 in sync with DOTS_BUDGET there
    L.append(info_line(90, 'Location', 'Montreal, QC'))
    L.append(dyn_line(110, 'Semesters.Remaining', 'semester_data', '2', 36))
    L.append(blank(130))
    L.append(info_line(150, 'OS', 'macOS Tahoe 26.5.1'))
    L.append(info_line(170, 'Shell', 'zsh wearing a bash costume'))
    L.append(info_line(190, 'Uptime', '4 coffees a day'))
    L.append(info_line(210, 'Sleep', 'Segmentation fault'))
    L.append(info_line(230, 'Audio.Driver', 'Metalcore and Rock'))
    L.append(blank(250))
    L.append(info_line(270, 'Languages.Programming', 'Python, TypeScript, Rust, Java'))
    L.append(info_line(290, 'Languages.Computer', 'HTML, CSS, SQL, LaTeX, Bash'))
    L.append(info_line(310, 'Languages.Real', 'English, Czech, French'))
    L.append(info_line(330, 'Hobbies.Software', 'Security, ML, Side Quests'))
    L.append(info_line(350, 'Hobbies.GrassTouching', 'Calisthenics, Bouldering, Running'))
    L.append(blank(370))
    L.append(header_line(390, '- Contact'))
    L.append(info_line(410, 'Email', 'filip.snitil@mail.mcgill.ca'))
    L.append(info_line(430, 'LinkedIn', 'www.linkedin.com/in/snitilf'))
    L.append(blank(450))
    L.append(header_line(470, '- Currently'))
    L.append(info_line(490, 'Learning', 'LLM Fine-tuning, RLHF'))
    L.append(info_line(510, 'Building', 'Whatever Fable 5 lets me build'))
    return '\n'.join(L)

THEMES = {
    'dark_mode.svg': dict(bg='#161b22', fg='#c9d1d9', key='#ffa657', value='#a5d6ff',
                          add='#3fb950', dele='#f85149', cc='#616e7f'),
    'light_mode.svg': dict(bg='#f6f8fa', fg='#24292f', key='#953800', value='#0a3069',
                           add='#1a7f37', dele='#cf222e', cc='#c2cfde'),
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
.key {{fill: {key};}}
.value {{fill: {value};}}
.addColor {{fill: {add};}}
.delColor {{fill: {dele};}}
.cc {{fill: {cc};}}
text, tspan {{white-space: pre;}}
</style>
<rect width="985px" height="530px" fill="{bg}" rx="15"/>
<text x="15" y="30" fill="{fg}" class="ascii" font-size="{ascii_font}px">
{ascii_block}
</text>
<text x="390" y="30" fill="{fg}">
{right}
</text>
</svg>
'''

if __name__ == '__main__':
    art = ascii_art()
    y0 = (530 - len(art) * ASCII_STEP) / 2 + ASCII_FONT - 2

    def art_block(lines):
        return '\n'.join(f'<tspan x="15" y="{y0 + i * ASCII_STEP:g}">{line}</tspan>'
                         for i, line in enumerate(lines))

    right = right_column()
    for name, t in THEMES.items():
        lines = invert_art(art) if name.startswith('dark') else art
        with open(os.path.join(OUT_DIR, name), 'w', encoding='utf-8') as f:
            f.write(TEMPLATE.format(ascii_block=art_block(lines), right=right,
                                    ascii_font=ASCII_FONT, **t))
    print('wrote dark_mode.svg and light_mode.svg')

"""
updates the Semesters.Remaining line in both SVGs
can run daily via GitHub Actions, pure date math, no token needed
"""
import datetime
import re

# last day of each remaining semester (end of finals)
SEMESTER_ENDS = [
    datetime.date(2026, 12, 22),  # Fall 2026
    datetime.date(2027, 4, 30),   # Winter 2027 graduation
]

DOTS_BUDGET = 36  # dots + value = 38 chars, keeping the line 60 wide


def semesters_remaining():
    today = datetime.date.today()
    remaining = sum(1 for end in SEMESTER_ENDS if end >= today)
    return str(remaining) if remaining else 'Graduated'


def justify(value):
    just_len = max(0, DOTS_BUDGET - len(value))
    if just_len <= 2:
        return {0: '', 1: ' ', 2: '. '}[just_len]
    return ' ' + '.' * just_len + ' '


def update(filename, value):
    with open(filename, encoding='utf-8') as f:
        svg = f.read()
    svg = re.sub(r'(id="semester_data_dots">)[^<]*(</tspan>)',
                 lambda m: m.group(1) + justify(value) + m.group(2), svg)
    svg = re.sub(r'(id="semester_data">)[^<]*(</tspan>)',
                 lambda m: m.group(1) + value + m.group(2), svg)
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(svg)


if __name__ == '__main__':
    value = semesters_remaining()
    for f in ('dark_mode.svg', 'light_mode.svg'):
        update(f, value)
    print('Semesters.Remaining =', value)

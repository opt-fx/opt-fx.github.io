#!/usr/bin/env python3
"""The OPT app icon family: one striped sun per app, in the app's colour, with a simple symbol.

Writes icons/<app>.svg, each a 100x100 rounded dark tile with the artwork in <g id="art">.
Apps copy their SVG into their own icons/ folder and render the PNG sizes from it.
Usage: python3 tools/icons.py
"""
import math, os

INK = '#17181b'
SCALE = 1.18          # the sun fills the tile like a native macOS icon

def stripes():
    # kept inside the sun by the clip path, so they never show beyond its edge
    return ('<g clip-path="url(#sun)">' + ''.join(f'<rect x="10" y="{y}" width="80" height="{h}" fill="{INK}"/>'
                   for y, h in [(55.64, 1.76), (62.69, 2.64), (70.09, 3.52), (77.84, 4.58)]) + '</g>')

def knobs(acc):
    out = ''
    for x, a in zip([30.5, 50, 69.5], [-130, -20, 70]):
        r = math.radians(a)
        out += (f'<circle cx="{x}" cy="38" r="8.4" fill="{INK}"/>'
                f'<line x1="{x}" y1="38" x2="{x + math.sin(r) * 6.6:.2f}" y2="{38 - math.cos(r) * 6.6:.2f}" '
                f'stroke="{acc}" stroke-width="2.2" stroke-linecap="round"/>')
    return out

def pads(lit):
    s, g = 10.4, 2
    x0, y0 = 50 - (3 * s + 2 * g) / 2, 38 - (2 * s + g) / 2
    return ''.join(f'<rect x="{x0 + c * (s + g):.2f}" y="{y0 + r * (s + g):.2f}" width="{s}" height="{s}" rx="1.8" '
                   f'fill="{lit if (r, c) == (0, 1) else INK}"/>' for r in range(2) for c in range(3))

def sliced_break():
    # a drum break drawn as level bars, cut in three by two slice markers with flags on top
    groups = [[8, 18, 12], [28, 16, 22, 10], [30, 14, 20]]
    w, gap, cut = 2.8, 1.6, 5.4
    total = sum(len(g) for g in groups) * w + sum(len(g) - 1 for g in groups) * gap + 2 * cut
    x, out, marks = 50 - total / 2, '', []
    for gi, g in enumerate(groups):
        for i, h in enumerate(g):
            out += f'<rect x="{x:.2f}" y="{38 - h / 2:.2f}" width="{w}" height="{h}" rx="1" fill="{INK}"/>'
            x += w + (gap if i < len(g) - 1 else 0)
        if gi < len(groups) - 1:
            marks.append(x + cut / 2); x += cut
    for m in marks:
        out += (f'<rect x="{m - 0.85:.2f}" y="22" width="1.7" height="33" fill="{INK}"/>'
                f'<rect x="{m - 0.85:.2f}" y="19.5" width="6.4" height="4" rx="1" fill="{INK}"/>')
    return out

def wave():
    pts = ' '.join(f'{26 + i},{38 - math.sin(i / 48 * math.pi * 4) * 10 * (1 - i / 48 * 0.55):.1f}' for i in range(49))
    return f'<polyline points="{pts}" fill="none" stroke="{INK}" stroke-width="2.8" stroke-linejoin="round" stroke-linecap="round"/>'

def keys(lit):
    w, g = 7.2, 1.3
    x0 = 50 - (5 * w + 4 * g) / 2
    out = ''
    for i in range(5):
        x = x0 + i * (w + g)
        out += f'<rect x="{x:.2f}" y="22" width="{w}" height="29" rx="1.4" fill="{INK}"/>'
        if i % 2 == 0:
            out += f'<circle cx="{x + w / 2:.2f}" cy="44" r="2.3" fill="{lit}"/>'
    return out

def tin(sun):
    return (f'<rect x="31" y="22" width="38" height="5.4" rx="2.2" fill="{INK}"/>'
            f'<rect x="34" y="29.4" width="32" height="20" rx="2.6" fill="{INK}"/>'
            f'<circle cx="50" cy="39.4" r="5" fill="none" stroke="{sun}" stroke-width="2.2"/>')

def trio():
    return ''.join(f'<rect x="{x - 6.5}" y="31.5" width="13" height="13" rx="2" fill="{c}"/>'
                   for x, c in [(32, '#3fa3e8'), (50, '#f3d23c'), (68, '#e8473d')])

def bars():
    return ''.join(f'<rect x="{x - 3.6}" y="{y - 8}" width="7.2" height="{50 - y + 8}" rx="1.2" fill="{INK}"/>'
                   for x, y in [(34, 30), (44, 40), (54, 24), (64, 34)])

APPS = {
    'seer':          ('#f2933a', knobs('#7a4a26')),
    'pad-loader':    ('#3b8de0', pads('#ffd93a')),
    's950rx':        ('#4cc274', sliced_break()),
    's612-transfer': ('#e3b04b', wave()),
    'quchord':       ('#e5483f', keys('#e5483f')),
    'biscuit-tin':   ('#ecebe6', tin('#ecebe6')),
    'oto-trio':      ('#15402a', trio()),
    'mks7':          ('#a07cf0', bars()),
}

def svg(sun, symbol):
    art = (f'<g id="art" transform="translate(50 50) scale({SCALE}) translate(-50 -50)">'
           '<clipPath id="sun"><circle cx="50" cy="50" r="37"/></clipPath>'
           f'<circle cx="50" cy="50" r="37" fill="{sun}"/>{stripes()}{symbol}</g>')
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">'
            f'<rect x="2" y="2" width="96" height="96" rx="22" fill="{INK}"/>'
            f'<rect x="2.5" y="2.5" width="95" height="95" rx="21.5" fill="none" stroke="#2c2e33" stroke-width="1"/>'
            f'{art}</svg>\n')

if __name__ == '__main__':
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for name, (sun, sym) in APPS.items():
        open(os.path.join(root, 'icons', name + '.svg'), 'w').write(svg(sun, sym))
        print('icons/' + name + '.svg')

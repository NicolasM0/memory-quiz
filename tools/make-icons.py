#!/usr/bin/env python3
"""Génère les icônes de l'application (originales, dessinées géométriquement).

Aucune ressource externe n'est utilisée : les icônes sont entièrement
construites ici, et sont donc couvertes par la licence CC0 du projet.

Usage:
    python3 tools/make-icons.py [--out DOSSIER]

Dépendance : Pillow (uniquement pour regénérer les icônes, pas à l'exécution).
"""
import argparse
import math
import os

from PIL import Image, ImageDraw

BLUE = (79, 157, 235)
MINT = (110, 231, 183)
NAVY = (15, 19, 37)
NAVY2 = (28, 32, 48)
WHITE = (255, 255, 255)
ICE = (226, 235, 252)

# Composition exprimée en fractions de la taille de l'icône.
# Tout le contenu tient dans la « safe zone » circulaire de 80 % de diamètre
# exigée pour les icônes maskable (Android), afin de ne jamais être rogné.
SUPERSAMPLE = 2048
CARD_W, CARD_H, CARD_R = 0.20, 0.44, 0.045
CARDS = ((0.30, -6, ICE, BLUE), (0.56, 8, WHITE, MINT))
DOT_R = 0.045
WAVES_CX, WAVES_RADII = 0.79, (0.035, 0.060, 0.085)


def vertical_gradient(size, top, bottom):
    img = Image.new("RGBA", (size, size))
    draw = ImageDraw.Draw(img)
    for y in range(size):
        t = y / (size - 1)
        color = tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)) + (255,)
        draw.line([(0, y), (size, y)], fill=color)
    return img


def add_radial_glow(size, base, glow, cx=0.5, cy=0.30, radius=0.78):
    img = base.copy()
    px = img.load()
    for y in range(size):
        for x in range(size):
            dist = math.hypot(x / size - cx, y / size - cy) / radius
            if dist < 1:
                a = (1 - dist) ** 2
                r, g, b, _ = px[x, y]
                px[x, y] = (
                    int(r + (glow[0] - r) * a),
                    int(g + (glow[1] - g) * a),
                    int(b + (glow[2] - b) * a),
                    255,
                )
    return img


def make_card(size, fill, outline, border):
    im = Image.new("RGBA", (int(size * CARD_W), int(size * CARD_H)), (0, 0, 0, 0))
    ImageDraw.Draw(im).rounded_rectangle(
        [0, 0, im.width - 1, im.height - 1],
        radius=int(size * CARD_R),
        fill=fill + (255,),
        outline=outline + (255,),
        width=border,
    )
    return im


def paste_rotated(base, tile, angle, cx, cy, size):
    rot = tile.rotate(angle, resample=Image.BICUBIC, expand=True)
    base.alpha_composite(rot, (int(cx * size - rot.width / 2), int(cy * size - rot.height / 2)))


def build(size):
    img = add_radial_glow(size, vertical_gradient(size, NAVY2, NAVY), (58, 84, 150))
    border = max(1, int(0.012 * size))

    for cx, angle, fill, dot in CARDS:
        paste_rotated(img, make_card(size, fill, NAVY, border), angle, cx, 0.50, size)

    draw = ImageDraw.Draw(img)
    dot_r = DOT_R * size
    for cx, _, _, dot in CARDS:
        draw.ellipse(
            [cx * size - dot_r, 0.50 * size - dot_r, cx * size + dot_r, 0.50 * size + dot_r],
            fill=dot + (255,),
        )

    for radius in WAVES_RADII:
        rr = radius * size
        ccx, ccy = WAVES_CX * size, 0.50 * size
        draw.arc(
            [ccx - rr, ccy - rr, ccx + rr, ccy + rr],
            -52, 52,
            fill=MINT + (255,),
            width=max(1, int(0.018 * size)),
        )
    return img


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=".")
    args = parser.parse_args()
    os.makedirs(args.out, exist_ok=True)

    master = build(SUPERSAMPLE)
    for name, size in (("icon.png", 512), ("icon-192.png", 192), ("icon-512.png", 512)):
        path = os.path.join(args.out, name)
        master.convert("RGB").resize((size, size), Image.LANCZOS).save(path)
        print("écrit", path, os.path.getsize(path), "octets")


if __name__ == "__main__":
    main()

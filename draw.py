"""Draw a black-and-white one-page world news summary for 22 November 2026."""

import os
import math
import textwrap

from PIL import Image, ImageDraw, ImageFont


SIZE = 1024
MARGIN = 28
MASTHEAD_HEIGHT = 118
LEAD_HEIGHT = 215
GAP = 16

PAPER = "#FFFFFF"
INK = "#111111"
PALE = "#E9E9E9"
RULE = "#8A8A8A"
MUTED = "#444444"

SERIF_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FALLBACK_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


STORIES = [
    (
        "COP31 talks stall on fossil fuels",
        "Final draft drops the words 'fossil fuels'; EU says no deal beats a bad deal.",
    ),
    (
        "Iran strikes Bahrain, hits tankers",
        "Civilian site burns; two tankers struck in the Hormuz strait.",
    ),
    (
        "AI sell-off sinks Wall Street",
        "S&P 500 falls 3.7% into correction; Nvidia tumbles 13.8%.",
    ),
    (
        "6.7 quake shakes Peru's Andes",
        "One dead, 16 hurt; 853 left homeless in Junin.",
    ),
    (
        "EU and Indonesia sign trade deal",
        "After 10 years of talks; tariffs on 98% of goods to go.",
    ),
    (
        "Trump, Xi and Putin meet in Shenzhen",
        "First-ever trio summit pledges nuclear-risk talks.",
    ),
]


def font(path, size):
    chosen = path if os.path.exists(path) else FALLBACK_PATH
    return ImageFont.truetype(chosen, size)


def fit_lines(text, face_path, size, max_width, max_lines):
    """Wrap text, shrinking gradually until it fits the box."""
    for candidate_size in range(size, 13, -1):
        current = font(face_path, candidate_size)
        for lines in range(1, max_lines + 1):
            best = None
            for width in range(len(text), 4, -1):
                wrapped = textwrap.wrap(text, width=width)
                if wrapped is None or len(wrapped) != lines:
                    continue
                if not all(current.getlength(line) <= max_width for line in wrapped):
                    continue
                spread = max(current.getlength(line) for line in wrapped)
                balance = sum(abs(current.getlength(line) - spread) for line in wrapped)
                if best is None or balance < best[0]:
                    best = (balance, wrapped)
            if best is not None:
                return best[1], current
    return textwrap.wrap(text, width=max_width // 9), font(face_path, 14)
    words = text.split()
    tiny = font(face_path, 14)
    while words and tiny.getlength(" ".join(words)) > max_width:
        words.pop()
    return [" ".join(words)], tiny


def draw_lines(draw, lines, face, x, top, box_width, fill, leading):
    for line in lines:
        draw.text((x, top), line, font=face, fill=fill)
        top += leading
    return top


def draw_lead_meme(draw, box):
    left, top, right, bottom = box
    center_x = (left + right) // 2
    doc_l = left + 8
    doc_t = top + 12
    doc_r = right - 8
    doc_b = bottom - 38
    draw.rectangle((doc_l, doc_t, doc_r, doc_b), fill=PAPER, outline=INK, width=3)
    for offset in (18, 32, 92, 106):
        draw.line((doc_l + 12, doc_t + offset, doc_r - 22, doc_t + offset),
                  fill=RULE, width=3)
    draw.line((doc_l + 12, doc_t + 64, doc_r - 22, doc_t + 64), fill=PALE, width=8)
    glass_center = (doc_l + 80, doc_t + 59)
    glass_radius = 24
    draw.ellipse((glass_center[0] - glass_radius, glass_center[1] - glass_radius,
                  glass_center[0] + glass_radius, glass_center[1] + glass_radius),
                 outline=INK, width=4)
    draw.line((glass_center[0] + 17, glass_center[1] + 17,
               glass_center[0] + 39, glass_center[1] + 40), fill=INK, width=6)
    label = font(SANS_PATH, 13)
    caption = "WHERE ARE THE WORDS?"
    draw.text((center_x - label.getlength(caption) / 2, bottom - 25), caption,
              font=label, fill=MUTED)


def draw_tanker(draw, box):
    left, top, right, bottom = box
    center = (left + right) // 2
    hull_top = top + 64
    for smoke_x, smoke_y in ((center + 16, top + 34),
                             (center + 30, top + 29),
                             (center + 44, top + 24)):
        draw.ellipse((smoke_x - 6, smoke_y - 6, smoke_x + 6, smoke_y + 6),
                     fill=PALE, outline=RULE, width=2)
    draw.rectangle((left + 8, hull_top, right - 8, hull_top + 21),
                   fill=PAPER, outline=INK, width=3)
    draw.polygon([(left + 8, hull_top + 21), (right - 8, hull_top + 21),
                  (right - 20, hull_top + 31), (left + 20, hull_top + 31)],
                 fill=PALE, outline=INK)
    draw.rectangle((center + 28, hull_top - 23, center + 55, hull_top),
                   fill=PAPER, outline=INK, width=2)
    draw.rectangle((center + 48, hull_top - 37, center + 55, hull_top - 23),
                   fill=INK)
    draw.rectangle((center + 34, hull_top - 33, center + 40, hull_top - 23),
                   fill=INK)
    draw.polygon([(center + 64, hull_top - 3), (center + 74, hull_top - 12),
                  (center + 83, hull_top - 3)], fill=INK)
    flame = [(center - 34, hull_top), (center - 31, hull_top - 14),
             (center - 40, hull_top - 13), (center - 26, hull_top - 34),
             (center - 29, hull_top - 45), (center - 15, hull_top - 35),
             (center - 8, hull_top - 52), (center + 2, hull_top - 36),
             (center + 14, hull_top - 47), (center + 10, hull_top - 27),
             (center + 21, hull_top - 14), (center + 12, hull_top - 12),
             (center + 16, hull_top)]
    draw.polygon(flame, fill=RULE, outline=INK)
    draw.polygon([(center - 12, hull_top - 1), (center - 11, hull_top - 16),
                  (center - 2, hull_top - 33), (center + 4, hull_top - 18),
                  (center + 9, hull_top - 12), (center + 7, hull_top - 1)],
                 fill=MUTED)
    for row in (hull_top + 36, hull_top + 44):
        points = [(x, row + (2 if (x // 16) % 2 == 0 else 0))
                  for x in range(left + 8, right - 7, 16)]
        points.append((right - 8, row))
        draw.line(points, fill=INK, width=2)


def draw_selloff(draw, box):
    left, top, right, bottom = box
    for row in (top + 26, top + 49, top + 72):
        draw.line((left + 8, row, right - 8, row), fill=RULE, width=1)
    for col in (left + 42, left + 84, left + 126):
        draw.line((col, top + 12, col, bottom - 10), fill=RULE, width=1)
    start = (left + 14, top + 14)
    bend = (left + 57, top + 37)
    end = (right - 14, bottom - 14)
    draw.line((start, bend, end), fill=INK, width=6, joint="curve")
    draw.polygon([(end[0] - 11, end[1] - 7), end,
                  (end[0] - 8, end[1] + 9)], fill=INK)
    head_x = int(bend[0] + (end[0] - bend[0]) * 0.30)
    head_y = int(bend[1] + (end[1] - bend[1]) * 0.30)
    draw.line((head_x - 9, head_y - 22, head_x - 13, head_y - 36),
              fill=INK, width=3)
    draw.line((head_x + 9, head_y - 22, head_x + 13, head_y - 36),
              fill=INK, width=3)
    draw.ellipse((head_x - 16, head_y - 40, head_x - 10, head_y - 34), fill=INK)
    draw.ellipse((head_x + 10, head_y - 40, head_x + 16, head_y - 34), fill=INK)
    draw.rectangle((head_x - 24, head_y - 24, head_x + 24, head_y + 17),
                   fill=PAPER, outline=INK, width=4)
    draw.ellipse((head_x - 14, head_y - 14, head_x - 4, head_y - 4), fill=INK)
    draw.ellipse((head_x + 4, head_y - 14, head_x + 14, head_y - 4), fill=INK)
    draw.line((head_x - 8, head_y + 7, head_x + 8, head_y + 7), fill=INK, width=3)


def draw_quake(draw, box):
    left, top, right, bottom = box
    peak = (left + 50, top + 10)
    draw.polygon([(left + 6, bottom - 10), peak, (right - 8, bottom - 10)],
                 fill=PALE, outline=INK)
    crack = [(peak[0], peak[1] + 4), (peak[0] + 14, peak[1] + 22),
             (peak[0] - 4, peak[1] + 36), (peak[0] + 12, peak[1] + 54),
             (peak[0] - 3, peak[1] + 70)]
    draw.line(crack, fill=INK, width=5, joint="curve")
    house_x = right - 45
    house_y = bottom - 36
    draw.polygon([(house_x - 14, house_y + 20), (house_x + 18, house_y + 14),
                  (house_x + 22, house_y - 2), (house_x - 10, house_y + 4)],
                 fill=PAPER, outline=INK)
    draw.polygon([(house_x - 13, house_y + 4), (house_x + 2, house_y - 12),
                  (house_x + 22, house_y - 2)], fill=INK)
    number = font(SERIF_PATH, 25)
    draw.text((left + 8, top + 8), "6.7", font=number, fill=INK)


def draw_handshake(draw, box):
    left, top, right, bottom = box
    center = (left + right) // 2
    label = font(SANS_PATH, 12)
    caption = "10 YEARS"
    label_width = label.getlength(caption)
    label_left = center - label_width / 2 - 7
    draw.rectangle((label_left, top + 3, label_left + label_width + 14,
                    top + 22), fill=PAPER, outline=INK, width=2)
    draw.text((center - label_width / 2, top + 6), caption,
              font=label, fill=INK)
    draw.line((left + 2, top + 42, center - 22, top + 31),
              fill=PAPER, width=17)
    draw.line((left + 2, top + 42, center - 22, top + 31),
              fill=RULE, width=14)
    draw.line((left + 2, top + 42, center - 22, top + 31),
              fill=INK, width=1)
    draw.line((right - 2, top + 58, center + 22, top + 45),
              fill=PAPER, width=17)
    draw.line((right - 2, top + 58, center + 22, top + 45),
              fill=RULE, width=14)
    draw.line((right - 2, top + 58, center + 22, top + 45),
              fill=INK, width=1)
    draw.rounded_rectangle((center - 38, top + 26, center + 2, top + 50),
                           radius=10, fill=PAPER, outline=INK, width=3)
    draw.rounded_rectangle((center - 2, top + 31, center + 36, top + 53),
                           radius=10, fill=PALE, outline=INK, width=3)
    for offset in (0, 7, 14):
        draw.line((center - 22 + offset, top + 31,
                   center - 12 + offset, top + 47), fill=RULE, width=2)
    draw.rectangle((left + 18, top + 72, right - 18, bottom - 8),
                   fill=PAPER, outline=INK, width=3)
    draw.line((center - 24, top + 91, center - 7, top + 102,
               center + 24, top + 78), fill=INK, width=6, joint="curve")


def draw_summit(draw, box):
    left, top, right, bottom = box
    center_x = (left + right) // 2
    center_y = top + 62
    atom_y = top + 17
    draw.ellipse((center_x - 4, atom_y - 4, center_x + 4, atom_y + 4),
                 fill=INK)
    for angle in (60, -60):
        radians = math.radians(angle)
        cos_a, sin_a = math.cos(radians), math.sin(radians)
        points = []
        for step in range(73):
            radians_t = math.radians(step * 5)
            local_x = 19 * math.cos(radians_t)
            local_y = 7 * math.sin(radians_t)
            points.append((center_x + local_x * cos_a - local_y * sin_a,
                           atom_y + local_x * sin_a + local_y * cos_a))
        draw.line(points, fill=INK, width=2, joint="curve")
    for chair_x, chair_y in ((left + 12, center_y - 3),
                             (right - 36, center_y - 3),
                             (center_x - 13, bottom - 16)):
        draw.rounded_rectangle((chair_x, chair_y, chair_x + 24, chair_y + 14),
                               radius=4, fill=PALE, outline=INK, width=2)
    draw.ellipse((center_x - 59, center_y - 21,
                  center_x + 59, center_y + 21),
                 fill=PAPER, outline=INK, width=3)
    for flag_x, flag_y in ((center_x - 34, center_y - 3),
                           (center_x + 6, center_y + 3),
                           (center_x + 33, center_y - 6)):
        draw.line((flag_x, flag_y + 9, flag_x, flag_y - 9), fill=INK, width=2)
        draw.polygon([(flag_x, flag_y - 9), (flag_x + 13, flag_y - 6),
                      (flag_x, flag_y - 2)], fill=MUTED, outline=INK)


MEMES = [draw_lead_meme, draw_tanker, draw_selloff,
         draw_quake, draw_handshake, draw_summit]


def main():
    image = Image.new("RGB", (SIZE, SIZE), PAPER)
    draw = ImageDraw.Draw(image)
    content_right = SIZE - MARGIN
    content_width = content_right - MARGIN

    masthead = font(SERIF_PATH, 72)
    name = "THE WORLD TODAY"
    draw.text((SIZE / 2 - masthead.getlength(name) / 2, 2), name,
              font=masthead, fill=INK)
    rule_y = 96
    draw.line((MARGIN, rule_y, content_right, rule_y), fill=RULE, width=2)
    small = font(SANS_PATH, 20)
    draw.text((MARGIN, rule_y + 6), "SUNDAY, 22 NOVEMBER 2026",
              font=small, fill=MUTED)
    edition = "ONE-IMAGE EDITION"
    draw.text((content_right - small.getlength(edition), rule_y + 6), edition,
              font=small, fill=MUTED)
    masthead_bottom = MARGIN + MASTHEAD_HEIGHT
    draw.line((MARGIN, masthead_bottom, content_right, masthead_bottom),
              fill=INK, width=4)

    lead_top = masthead_bottom + 14
    lead_bottom = lead_top + LEAD_HEIGHT
    lead_text_width = 600
    headline_lines, headline_face = fit_lines(STORIES[0][0], SERIF_PATH, 52,
                                              lead_text_width, 2)
    text_y = draw_lines(draw, headline_lines, headline_face, MARGIN,
                        lead_top, lead_text_width, INK, 62)
    sub_lines, sub_face = fit_lines(STORIES[0][1], SANS_PATH, 22,
                                    lead_text_width, 2)
    draw_lines(draw, sub_lines, sub_face, MARGIN, text_y + 10,
               lead_text_width, MUTED, 30)
    draw_lead_meme(draw, (content_right - 180, lead_top + 8,
                          content_right - 4, lead_bottom - 10))
    draw.line((MARGIN, lead_bottom + 6, content_right, lead_bottom + 6),
              fill=INK, width=2)

    row_top = lead_bottom + 20
    row_height = 284
    column_top = row_top
    inner_gap = 16
    column_width = (content_width - 2 * GAP) // 3
    for index in range(3):
        left = MARGIN + index * (column_width + GAP)
        box = (left, column_top, left + column_width, column_top + row_height)
        draw_cell(draw, box, STORIES[index + 1], MEMES[index + 1], index % 2 == 1)

    wide_top = column_top + row_height + 15
    wide_height = row_height
    wide_width = (content_width - GAP) // 2
    for index in range(2):
        left = MARGIN + index * (wide_width + GAP)
        box = (left, wide_top, left + wide_width, wide_top + wide_height)
        draw_cell(draw, box, STORIES[index + 4], MEMES[index + 4], index % 2 == 0)

    footer = "All six stories happened or were first reported on 22 November 2026."
    footer_face = font(SANS_PATH, 18)
    draw.text((SIZE / 2 - footer_face.getlength(footer) / 2, 992), footer,
              font=footer_face, fill=MUTED)
    image.save(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "entry.png"))


def draw_cell(draw, box, story, meme, shaded=False):
    left, top, right, bottom = box
    draw.rectangle((left, top + 3, right, bottom),
                   fill=PALE if shaded else PAPER)
    draw.line((left, top, right, top), fill=INK, width=3)

    art_height = 110
    art_width = 170
    art_center = (left + right) // 2
    meme(draw, (art_center - art_width // 2, top + 12,
                art_center + art_width // 2, top + 12 + art_height))

    text_left = left + 14
    text_right = right - 14
    text_top = top + 130
    headline_lines, headline_face = fit_lines(story[0], SERIF_PATH, 29,
                                              text_right - text_left, 2)
    next_y = draw_lines(draw, headline_lines, headline_face,
                        text_left, text_top, text_right - text_left, INK, 36)
    sub_lines, sub_face = fit_lines(story[1], SANS_PATH, 20,
                                    text_right - text_left, 2)
    draw_lines(draw, sub_lines, sub_face, text_left, next_y + 8,
               text_right - text_left, MUTED, 26)


if __name__ == "__main__":
    main()

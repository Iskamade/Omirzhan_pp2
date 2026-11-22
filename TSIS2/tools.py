from collections import deque
import math
import pygame

BRUSH_SIZES = {
    1: 2,
    2: 5,
    3: 10,
}


def draw_shape(surface, tool, start_pos, end_pos, color, width):
    """Рисует фигуру между start_pos и end_pos с учётом толщины width."""
    x1, y1 = start_pos
    x2, y2 = end_pos

    if tool == "line":
        pygame.draw.line(surface, color, (x1, y1), (x2, y2), width)

    elif tool == "rect":
        left = min(x1, x2)
        top = min(y1, y2)
        w = abs(x2 - x1)
        h = abs(y2 - y1)
        pygame.draw.rect(surface, color, (left, top, w, h), width)

    elif tool == "circle":
        radius = int(math.hypot(x2 - x1, y2 - y1))
        if radius > 0:
            pygame.draw.circle(surface, color, (x1, y1), radius, width)

    elif tool == "square":
        side = max(abs(x2 - x1), abs(y2 - y1))
        sign_x = 1 if x2 >= x1 else -1
        sign_y = 1 if y2 >= y1 else -1
        left = min(x1, x1 + sign_x * side)
        top = min(y1, y1 + sign_y * side)
        pygame.draw.rect(surface, color, (left, top, side, side), width)

    elif tool == "right_triangle":
        # Прямоугольный треугольник с прямым углом в (x1, y2)
        points = [(x1, y1), (x1, y2), (x2, y2)]
        pygame.draw.polygon(surface, color, points, width)

    elif tool == "equilateral_triangle":
        # Равносторонний треугольник от основания/опорной точки
        base = x2 - x1
        height = int(abs(base) * math.sqrt(3) / 2)
        direction = -1 if y2 < y1 else 1
        top_vertex = (x1 + base // 2, y1 + direction * height)
        points = [(x1, y1), (x1 + base, y1), top_vertex]
        pygame.draw.polygon(surface, color, points, width)

    elif tool == "rhombus":
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        points = [
            (cx, min(y1, y2)),
            (max(x1, x2), cy),
            (cx, max(y1, y2)),
            (min(x1, x2), cy),
        ]
        pygame.draw.polygon(surface, color, points, width)


def flood_fill(surface, start_pos, fill_color):
    """Заливает замкнутую область через get_at() и set_at() (итеративный BFS)."""
    x0, y0 = int(start_pos[0]), int(start_pos[1])
    w, h = surface.get_size()

    if not (0 <= x0 < w and 0 <= y0 < h):
        return

    target_color = surface.get_at((x0, y0))
    fill_rgba = surface.map_rgb(fill_color)
    target_rgba = surface.map_rgb(target_color)

    if target_rgba == fill_rgba:
        return

    visited = set()
    queue = deque([(x0, y0)])
    visited.add((x0, y0))

    while queue:
        cx, cy = queue.popleft()
        if surface.map_rgb(surface.get_at((cx, cy))) != target_rgba:
            continue

        surface.set_at((cx, cy), fill_color)

        for nx, ny in ((cx + 1, cy), (cx - 1, cy), (cx, cy + 1), (cx, cy - 1)):
            if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited:
                visited.add((nx, ny))
                queue.append((nx, ny))
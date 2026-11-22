from datetime import datetime
import os
import pygame
from tools import BRUSH_SIZES, draw_shape, flood_fill

WIDTH, HEIGHT = 1100, 720
TOOLBAR_HEIGHT = 90
CANVAS_TOP = TOOLBAR_HEIGHT
CANVAS_HEIGHT = HEIGHT - TOOLBAR_HEIGHT

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
GRAY = (225, 228, 232)
DARK_GRAY = (70, 75, 85)
ACTIVE_BORDER = (30, 120, 255)

COLORS = [
    (0, 0, 0),
    (220, 50, 47),
    (40, 167, 69),
    (0, 123, 255),
    (255, 193, 7),
    (156, 39, 176),
    (255, 128, 0),
    (255, 255, 255),
]

TOOLS = [
    ("pencil", "Pencil"),
    ("line", "Line"),
    ("eraser", "Eraser"),
    ("fill", "Fill"),
    ("text", "Text"),
    ("rect", "Rect"),
    ("circle", "Circle"),
    ("square", "Square"),
    ("right_triangle", "R.Tri"),
    ("equilateral_triangle", "Eq.Tri"),
    ("rhombus", "Rhombus"),
]


def save_canvas(canvas, folder="saves"):
    os.makedirs(folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(folder, f"canvas_{timestamp}.png")
    pygame.image.save(canvas, filename)
    return filename


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("TSIS 2 — Extended Paint")
    clock = pygame.time.Clock()

    font = pygame.font.SysFont("Arial", 15)
    text_font = pygame.font.SysFont("Arial", 24)
    status_font = pygame.font.SysFont("Arial", 14)

    canvas = pygame.Surface((WIDTH, CANVAS_HEIGHT))
    canvas.fill(WHITE)

    current_tool = "pencil"
    current_color = BLACK
    brush_level = 2  # 1 -> 2px, 2 -> 5px, 3 -> 10px

    drawing = False
    start_pos = None
    last_pos = None

    # Состояние инструмента Text
    typing_text = False
    text_pos = None
    text_buffer = ""

    status_message = "1/2/3 — толщина кисти | Ctrl+S — сохранить PNG"

    # Кнопки инструментов
    tool_buttons = []
    tx = 10
    for tool_id, label in TOOLS:
        rect = pygame.Rect(tx, 8, 76, 32)
        tool_buttons.append((rect, tool_id, label))
        tx += 80

    # Кнопки размеров кисти
    size_buttons = []
    sx = 10
    for level, px_size in BRUSH_SIZES.items():
        rect = pygame.Rect(sx, 48, 70, 28)
        size_buttons.append((rect, level, f"{px_size}px ({level})"))
        sx += 76

    # Кнопки палитры цветов
    color_buttons = []
    cx = 260
    for col in COLORS:
        rect = pygame.Rect(cx, 48, 28, 28)
        color_buttons.append((rect, col))
        cx += 34

    running = True
    while running:
        brush_width = BRUSH_SIZES[brush_level]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                # Сохранение по Ctrl+S
                if (event.mod & pygame.KMOD_CTRL) and event.key == pygame.K_s:
                    saved_path = save_canvas(canvas)
                    status_message = f"Сохранено: {saved_path}"
                    continue

                # Режим ввода текста
                if typing_text:
                    if event.key == pygame.K_RETURN:
                        if text_buffer and text_pos:
                            rendered = text_font.render(text_buffer, True, current_color)
                            canvas.blit(rendered, text_pos)
                            status_message = "Текст добавлен на холст"
                        typing_text = False
                        text_pos = None
                        text_buffer = ""
                    elif event.key == pygame.K_ESCAPE:
                        typing_text = False
                        text_pos = None
                        text_buffer = ""
                        status_message = "Ввод текста отменён"
                    elif event.key == pygame.K_BACKSPACE:
                        text_buffer = text_buffer[:-1]
                    else:
                        if event.unicode and event.unicode.isprintable():
                            text_buffer += event.unicode
                    continue

                # Горячие клавиши выбора размера кисти (1, 2, 3)
                if event.key == pygame.K_1:
                    brush_level = 1
                    status_message = f"Толщина кисти: {BRUSH_SIZES[brush_level]} px"
                elif event.key == pygame.K_2:
                    brush_level = 2
                    status_message = f"Толщина кисти: {BRUSH_SIZES[brush_level]} px"
                elif event.key == pygame.K_3:
                    brush_level = 3
                    status_message = f"Толщина кисти: {BRUSH_SIZES[brush_level]} px"

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos

                # Если был активен ввод текста и кликнули в другом месте — фиксируем или отменяем
                if typing_text and my >= CANVAS_TOP:
                    if text_buffer and text_pos:
                        rendered = text_font.render(text_buffer, True, current_color)
                        canvas.blit(rendered, text_pos)
                    typing_text = False
                    text_pos = None
                    text_buffer = ""

                # Клик по панели инструментов
                if my < TOOLBAR_HEIGHT:
                    for rect, tool_id, _ in tool_buttons:
                        if rect.collidepoint(mx, my):
                            current_tool = tool_id
                            typing_text = False
                            status_message = f"Инструмент: {tool_id}"

                    for rect, level, _ in size_buttons:
                        if rect.collidepoint(mx, my):
                            brush_level = level
                            status_message = f"Толщина кисти: {BRUSH_SIZES[brush_level]} px"

                    for rect, col in color_buttons:
                        if rect.collidepoint(mx, my):
                            current_color = col
                            status_message = f"Выбран цвет: {col}"

                # Клик по холсту
                else:
                    canvas_pos = (mx, my - CANVAS_TOP)

                    if current_tool == "text":
                        typing_text = True
                        text_pos = canvas_pos
                        text_buffer = ""
                        status_message = "Введите текст и нажмите Enter (Esc — отмена)"

                    elif current_tool == "fill":
                        flood_fill(canvas, canvas_pos, current_color)
                        status_message = "Заливка выполнена"

                    elif current_tool in ("pencil", "eraser"):
                        drawing = True
                        last_pos = canvas_pos
                        draw_col = WHITE if current_tool == "eraser" else current_color
                        pygame.draw.circle(canvas, draw_col, canvas_pos, max(1, brush_width // 2))

                    else:
                        # Инструменты с началом и концом (line, rect, circle, square, треугольники, ромб)
                        drawing = True
                        start_pos = canvas_pos
                        last_pos = canvas_pos

            elif event.type == pygame.MOUSEMOTION and drawing:
                mx, my = event.pos
                canvas_pos = (mx, max(0, my - CANVAS_TOP))

                if current_tool == "pencil" and last_pos is not None:
                    pygame.draw.line(canvas, current_color, last_pos, canvas_pos, brush_width)
                    last_pos = canvas_pos

                elif current_tool == "eraser" and last_pos is not None:
                    pygame.draw.line(canvas, WHITE, last_pos, canvas_pos, brush_width)
                    last_pos = canvas_pos

                else:
                    last_pos = canvas_pos

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and drawing:
                mx, my = event.pos
                end_pos = (mx, max(0, my - CANVAS_TOP))

                if current_tool not in ("pencil", "eraser", "fill", "text") and start_pos is not None:
                    draw_shape(canvas, current_tool, start_pos, end_pos, current_color, brush_width)

                drawing = False
                start_pos = None
                last_pos = None

        # Отрисовка экрана
        screen.fill(GRAY)

        # Панель инструментов сверху
        pygame.draw.rect(screen, (240, 242, 245), (0, 0, WIDTH, TOOLBAR_HEIGHT))
        pygame.draw.line(screen, DARK_GRAY, (0, TOOLBAR_HEIGHT), (WIDTH, TOOLBAR_HEIGHT), 1)

        for rect, tool_id, label in tool_buttons:
            is_active = current_tool == tool_id
            pygame.draw.rect(screen, WHITE if is_active else GRAY, rect, border_radius=4)
            pygame.draw.rect(
                screen,
                ACTIVE_BORDER if is_active else DARK_GRAY,
                rect,
                2 if is_active else 1,
                border_radius=4,
            )
            lbl = font.render(label, True, BLACK)
            screen.blit(lbl, lbl.get_rect(center=rect.center))

        for rect, level, label in size_buttons:
            is_active = brush_level == level
            pygame.draw.rect(screen, WHITE if is_active else GRAY, rect, border_radius=4)
            pygame.draw.rect(
                screen,
                ACTIVE_BORDER if is_active else DARK_GRAY,
                rect,
                2 if is_active else 1,
                border_radius=4,
            )
            lbl = font.render(label, True, BLACK)
            screen.blit(lbl, lbl.get_rect(center=rect.center))

        for rect, col in color_buttons:
            pygame.draw.rect(screen, col, rect, border_radius=4)
            is_selected = col == current_color
            pygame.draw.rect(
                screen,
                ACTIVE_BORDER if is_selected else BLACK,
                rect,
                3 if is_selected else 1,
                border_radius=4,
            )

        status_surf = status_font.render(status_message, True, DARK_GRAY)
        screen.blit(status_surf, (550, 54))

        # Холст + живое превью
        display_canvas = canvas.copy()

        if drawing and start_pos is not None and last_pos is not None:
            if current_tool not in ("pencil", "eraser", "fill", "text"):
                draw_shape(display_canvas, current_tool, start_pos, last_pos, current_color, brush_width)

        if typing_text and text_pos is not None:
            preview_surf = text_font.render(text_buffer + "|", True, current_color)
            display_canvas.blit(preview_surf, text_pos)

        screen.blit(display_canvas, (0, CANVAS_TOP))
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
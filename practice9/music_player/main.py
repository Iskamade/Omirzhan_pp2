import pygame
from player import MusicPlayer

WIDTH, HEIGHT = 640, 440
BG_COLOR = (24, 27, 34)
CARD_COLOR = (36, 41, 51)
TEXT_MAIN = (240, 244, 248)
TEXT_MUTED = (155, 165, 180)
ACCENT = (80, 175, 255)
ERROR_COLOR = (255, 110, 110)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Music Player")
    clock = pygame.time.Clock()

    title_font = pygame.font.SysFont("Arial", 28, bold=True)
    body_font = pygame.font.SysFont("Arial", 20)
    small_font = pygame.font.SysFont("Arial", 16)

    player = MusicPlayer("music")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    player.play()
                elif event.key == pygame.K_s:
                    player.stop()
                elif event.key == pygame.K_n:
                    player.next_track()
                elif event.key == pygame.K_b:
                    player.prev_track()
                elif event.key == pygame.K_q:
                    running = False

        screen.fill(BG_COLOR)
        pygame.draw.rect(
            screen, CARD_COLOR, (30, 30, WIDTH - 60, HEIGHT - 60), border_radius=12
        )

        header = title_font.render("Pygame Music Player", True, TEXT_MAIN)
        screen.blit(header, (55, 50))

        track_info = f"Track: {player.current_track_name}"
        if player.tracks:
            track_info += f"  ({player.current_index + 1}/{len(player.tracks)})"
        screen.blit(body_font.render(track_info, True, ACCENT), (55, 105))

        pos_sec = player.get_position_sec()
        status_line = f"Status: {player.status}   |   Position: {pos_sec:.1f}s"
        screen.blit(body_font.render(status_line, True, TEXT_MAIN), (55, 145))

        if player.last_error:
            err_surf = small_font.render(f"Error: {player.last_error}", True, ERROR_COLOR)
            screen.blit(err_surf, (55, 173))

        screen.blit(small_font.render("Playlist:", True, TEXT_MUTED), (55, 202))
        if not player.tracks:
            screen.blit(
                small_font.render(
                    "Put .mp3 or .wav files into music/ folder", True, TEXT_MUTED
                ),
                (55, 229),
            )
        else:
            for idx, track in enumerate(player.tracks[:5]):
                prefix = "▶ " if idx == player.current_index else "   "
                color = ACCENT if idx == player.current_index else TEXT_MUTED
                line = small_font.render(
                    f"{prefix}{idx + 1}. {track.name}", True, color
                )
                screen.blit(line, (55, 229 + idx * 24))

        controls = "Controls: [P] Play   [S] Stop   [N] Next   [B] Back   [Q] Quit"
        screen.blit(
            small_font.render(controls, True, TEXT_MUTED), (55, HEIGHT - 62)
        )

        pygame.display.flip()
        clock.tick(15)

    pygame.quit()


if __name__ == "__main__":
    main()
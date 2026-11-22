from pathlib import Path
import pygame


class MusicPlayer:
    SUPPORTED_EXTS = (".mp3", ".wav", ".ogg")

    def __init__(self, music_dir="music"):
        base_dir = Path(__file__).resolve().parent
        self.music_dir = base_dir / music_dir
        self.tracks = self._load_tracks()
        self.current_index = 0
        self.status = "STOPPED"
        self.last_error = ""

        if not pygame.mixer.get_init():
            pygame.mixer.init()

        if self.tracks:
            self._load_current()

    def _load_tracks(self):
        if not self.music_dir.exists():
            return []
        return [
            p
            for p in sorted(self.music_dir.iterdir())
            if p.is_file() and p.suffix.lower() in self.SUPPORTED_EXTS
        ]

    def _load_current(self):
        if not self.tracks:
            return False
        track_path = self.tracks[self.current_index]
        try:
            pygame.mixer.music.load(str(track_path))
            self.last_error = ""
            return True
        except pygame.error as exc:
            self.last_error = f"{track_path.name}: {exc}"
            print(f"[Audio load error] {self.last_error}")
            return False

    @property
    def current_track_name(self):
        if not self.tracks:
            return "No tracks found"
        return self.tracks[self.current_index].name

    def get_position_sec(self):
        if not self.tracks or self.status == "STOPPED":
            return 0.0
        pos_ms = pygame.mixer.music.get_pos()
        return max(0.0, pos_ms / 1000.0)

    def play(self):
        if not self.tracks:
            self.status = "NO TRACKS"
            return
        if self.status == "PAUSED":
            pygame.mixer.music.unpause()
            self.status = "PLAYING"
            return
        if not self._load_current():
            self.status = "LOAD ERROR"
            return
        pygame.mixer.music.play()
        self.status = "PLAYING"

    def stop(self):
        if not self.tracks:
            return
        pygame.mixer.music.stop()
        self.status = "STOPPED"

    def next_track(self):
        if not self.tracks:
            return
        was_playing = self.status == "PLAYING"
        self.current_index = (self.current_index + 1) % len(self.tracks)
        loaded = self._load_current()
        if was_playing and loaded:
            pygame.mixer.music.play()
            self.status = "PLAYING"
        else:
            self.status = "LOAD ERROR" if not loaded else "STOPPED"

    def prev_track(self):
        if not self.tracks:
            return
        was_playing = self.status == "PLAYING"
        self.current_index = (self.current_index - 1) % len(self.tracks)
        loaded = self._load_current()
        if was_playing and loaded:
            pygame.mixer.music.play()
            self.status = "PLAYING"
        else:
            self.status = "LOAD ERROR" if not loaded else "STOPPED"
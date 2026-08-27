"""No-key SVG, raster, and MP4 rendering through local macOS tools."""

import subprocess
from pathlib import Path

from .art import render_svg


def _run(command: list[str]) -> None:
    subprocess.run(command, check=True, capture_output=True, text=True)


def render_frame(track: str, label: str, state_index: int, png_path: Path) -> None:
    """Render one 16:9 research frame with separate track visual language."""
    png_path.parent.mkdir(parents=True, exist_ok=True)
    svg_path = png_path.with_suffix(".svg")
    svg_path.write_text(render_svg({"id": "prototype", "text": label}, track, state_index), encoding="utf-8")
    _run(["sips", "-s", "format", "png", str(svg_path), "--out", str(png_path)])


def assemble_mp4(frame_glob: str, frame_count: int, duration_seconds: int, mp4_path: Path) -> None:
    """Create a 24fps H.264 MP4 whose duration follows the route plan."""
    mp4_path.parent.mkdir(parents=True, exist_ok=True)
    framerate = frame_count / duration_seconds
    _run(["ffmpeg", "-y", "-framerate", str(framerate), "-i", frame_glob, "-r", "24", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(mp4_path)])


def contact_sheet(frame_glob: str, frame_count: int, png_path: Path) -> None:
    """Create a simple row contact sheet for visual QA."""
    _run(["ffmpeg", "-y", "-framerate", "1", "-i", frame_glob, "-frames:v", str(frame_count), "-vf", f"tile={frame_count}x1:padding=8:margin=8", str(png_path)])

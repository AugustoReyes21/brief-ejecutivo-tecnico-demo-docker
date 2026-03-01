#!/usr/bin/env python3
import os
import shlex
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
ARTIFACTS = ROOT / "artifacts" / "video"
HTML = ARTIFACTS / "html"
SHOTS = ARTIFACTS / "screenshots"
AUDIO = ARTIFACTS / "audio"
OUTPUT = ARTIFACTS / "brief-demo.mp4"
CHROME = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")


SLIDES = [
    {
        "name": "slide-01-title",
        "source": f"file://{HTML / 'slide-01-title.html'}",
        "narration": (
            "Hola. Esta es mi entrega del brief ejecutivo técnico con demo práctica en Docker Compose. "
            "El caso aplicado es un e commerce omnicanal. "
            "La propuesta usa ERP como system of record y una integración event driven para el flujo de creación de pedidos."
        ),
    },
    {
        "name": "slide-02-repo",
        "source": "https://github.com/AugustoReyes21/brief-ejecutivo-tecnico-demo-docker",
        "narration": (
            "Aquí se observa el repositorio público en GitHub con la estructura pedida por la rúbrica. "
            "Incluye README, el archivo docker compose, la carpeta docs y los servicios de la demo."
        ),
    },
    {
        "name": "slide-03-brief",
        "source": "https://github.com/AugustoReyes21/brief-ejecutivo-tecnico-demo-docker/blob/main/docs/brief.md",
        "narration": (
            "En el brief en Markdown está la adaptación del mapa de arquitectura al caso. "
            "También se ve el diagrama Mermaid, el gobierno mínimo viable basado en COBIT, "
            "el análisis de riesgo con NIST CSF dos punto cero y las métricas DORA más métricas operativas."
        ),
    },
    {
        "name": "slide-04-demo-request",
        "source": f"file://{HTML / 'slide-04-demo-request.html'}",
        "narration": (
            "La demo corre con docker compose up y levanta storefront service, Redis y ERP service. "
            "Después se crea una orden con un post al front office. "
            "Ese servicio publica el evento order created en el canal de eventos."
        ),
    },
    {
        "name": "slide-05-demo-result",
        "source": f"file://{HTML / 'slide-05-demo-result.html'}",
        "narration": (
            "Aquí está la evidencia del flujo. "
            "En los logs se ve la publicación del evento por parte de storefront service y el consumo por parte del ERP. "
            "Además, la consulta get orders confirma que el system of record registró la orden."
        ),
    },
    {
        "name": "slide-06-summary",
        "source": f"file://{HTML / 'slide-06-summary.html'}",
        "narration": (
            "En gobierno definí roles, decisiones críticas y políticas mínimas. "
            "En riesgo prioricé controles como eme efe a, roles, secretos, logging y restauración. "
            "En métricas usé deployment frequency, lead time for changes, em te te erre y pruebas exitosas de backup. "
            "Con esto cierro la demostración."
        ),
    },
]


def run(cmd):
    subprocess.run(cmd, check=True)


def ffmpeg_exe():
    import imageio_ffmpeg

    return imageio_ffmpeg.get_ffmpeg_exe()


def chrome_screenshot(url: str, output: Path):
    run(
        [
            str(CHROME),
            "--headless=new",
            "--disable-gpu",
            "--allow-file-access-from-files",
            "--hide-scrollbars",
            "--window-size=1280,720",
            "--virtual-time-budget=8000",
            f"--screenshot={output}",
            url,
        ]
    )


def synthesize_audio(text: str, output: Path):
    run(["say", "-v", "Paulina", "-r", "175", "-o", str(output), text])


def audio_duration_seconds(path: Path) -> float:
    result = subprocess.run(["afinfo", str(path)], check=True, capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if "estimated duration" in line:
            return float(line.split(":")[-1].strip().split()[0])
    raise RuntimeError(f"Could not determine duration for {path}")


def build_segment(image: Path, audio: Path, output: Path):
    ffmpeg = ffmpeg_exe()
    run(
        [
            ffmpeg,
            "-y",
            "-loop",
            "1",
            "-i",
            str(image),
            "-i",
            str(audio),
            "-c:v",
            "libx264",
            "-tune",
            "stillimage",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            "-shortest",
            str(output),
        ]
    )


def concat_segments(segments, output: Path):
    ffmpeg = ffmpeg_exe()
    concat_file = ARTIFACTS / "segments.txt"
    concat_file.write_text(
        "\n".join(f"file {shlex.quote(str(segment))}" for segment in segments) + "\n",
        encoding="utf-8",
    )
    run(
        [
            ffmpeg,
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-c",
            "copy",
            str(output),
        ]
    )


def main():
    if not CHROME.exists():
        raise SystemExit(f"Chrome not found at {CHROME}")

    SHOTS.mkdir(parents=True, exist_ok=True)
    AUDIO.mkdir(parents=True, exist_ok=True)

    segments = []
    for slide in SLIDES:
        image_path = SHOTS / f"{slide['name']}.png"
        audio_path = AUDIO / f"{slide['name']}.aiff"
        segment_path = ARTIFACTS / f"{slide['name']}.mp4"

        chrome_screenshot(slide["source"], image_path)
        synthesize_audio(slide["narration"], audio_path)
        build_segment(image_path, audio_path, segment_path)
        segments.append(segment_path)

    concat_segments(segments, OUTPUT)
    print(f"Video generado en: {OUTPUT}")


if __name__ == "__main__":
    main()

import time
from pathlib import Path
from TTS.api import TTS

# Carpeta principal de salida
OUTPUT_DIR = Path("voice_samples")
OUTPUT_DIR.mkdir(exist_ok=True)

# Modelos a probar
models_to_test = {
    # "en": [
    #     "tts_models/en/vctk/vits",
    #     "tts_models/en/ljspeech/tacotron2-DDC"
    # ],
    "es": [
        "tts_models/es/css10/vits",
        "tts_models/es/mai/tacotron2-DDC"
    ]
}

TEST_TEXTS = {
    "en": "Hello, this is a test of the text to speech system.",
    "es": "Hola, esta es una prueba del sistema de síntesis de voz."
}

def test_model(model_name, language):
    print(f"\n{'='*60}")
    print(f"Probando modelo: {model_name} ({language})")
    print(f"{'='*60}")

    try:
        tts = TTS(model_name)
    except Exception as e:
        print(f"✗ Error cargando modelo: {e}")
        return

    # Carpeta para este modelo
    model_dir = OUTPUT_DIR / model_name.replace("/", "_")
    model_dir.mkdir(exist_ok=True)

    # Detectar si tiene speakers
    speakers = getattr(tts, "speakers", None)

    if not speakers:
        # Si no hay speakers, generamos solo la voz por defecto
        speakers = [None]

    for idx, speaker in enumerate(speakers, 1):
        text = TEST_TEXTS.get(language, TEST_TEXTS["en"])
        if speaker is None:
            filename = model_dir / f"default.wav"
        else:
            filename = model_dir / f"speaker_{speaker}.wav"
        try:
            tts.tts_to_file(text=text, speaker=speaker, file_path=str(filename))
            print(f"  ✓ Generado: {filename.name}")
        except Exception as e:
            print(f"  ✗ Error generando {filename.name}: {e}")

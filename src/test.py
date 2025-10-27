import time
from pathlib import Path
from TTS.api import TTS

# Carpeta principal de salida
OUTPUT_DIR = Path("voice_samples")
OUTPUT_DIR.mkdir(exist_ok=True)

# Archivo de referencia para clonación de voz
CLONING_AUDIO = Path("assets/base_provided.wav")
USE_CLONING = CLONING_AUDIO.exists()

# Modelos a probar
models_to_test = {
    "es": [
        "tts_models/es/css10/vits",
        "tts_models/es/mai/tacotron2-DDC",
        "tts_models/multilingual/multi-dataset/xtts_v2"
    ]
}

TEST_TEXTS = {
    "en": "Hello, this is a test of the text to speech system.",
    "es": "Hola, esta es una voz generada mediante el sistema de prueba de Coqui TTS"
}

def test_model(model_name, language):
    TEST_TEXT = TEST_TEXTS.get(language, TEST_TEXTS["en"])
    print(f"\n{'='*60}")
    print(f"Probando modelo: {model_name}")
    print(f"{'='*60}")

    try:
        tts = TTS(model_name)
    except Exception as e:
        print(f"✗ Error cargando modelo: {e}")
        return

    # Carpeta para este modelo
    model_dir = OUTPUT_DIR / model_name.replace("/", "_")
    model_dir.mkdir(exist_ok=True)

    # Detectar si el modelo tiene speakers
    speakers = getattr(tts, "speakers", None)

    if not speakers:
        # Modelo mono-voz
        speakers = [None]

    for idx, speaker in enumerate(speakers, 1):
        filename = model_dir / (f"speaker_{speaker}.wav" if speaker else "default.wav")
        try:
            kwargs = {"text": TEST_TEXT, "file_path": str(filename)}
            if speaker:
                kwargs["speaker"] = speaker
            # Para modelos multi-lingual (xtts_v2) definimos el language
            if model_name == "tts_models/multilingual/multi-dataset/xtts_v2":
                kwargs["language"] = "en"  # por defecto inglés
                if language == "es":
                    # Forzamos español aunque el modelo no esté entrenado óptimamente
                    kwargs["language"] = "es"
            tts.tts_to_file(**kwargs)
            print(f"  ✓ Generado: {filename.name}")
        except Exception as e:
            print(f"  ✗ Error generando {filename.name}: {e}")

    # Generación por clonación de voz
    if USE_CLONING and model_name in ["tts_models/multilingual/multi-dataset/xtts_v2"]:
        cloned_file = model_dir / "cloned_voice.wav"
        try:
            tts.tts_to_file(
                text=TEST_TEXT,
                speaker_wav=str(CLONING_AUDIO),
                language="es",
                file_path=str(cloned_file)
            )
            print(f"  ✓ Generado clonación de voz: {cloned_file.name}")
        except Exception as e:
            print(f"  ✗ Error generando clonación de voz: {e}")

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
    # "en": [
    #     "tts_models/en/vctk/vits",
    #     "tts_models/en/ljspeech/tacotron2-DDC"
    # ],
    "es": [
        # "tts_models/es/css10/vits",
        # "tts_models/es/mai/tacotron2-DDC",
        #"tts_models/multilingual/multi-dataset/your_tts",
        "tts_models/multilingual/multi-dataset/xtts_v2"
    ]
}

TEST_TEXTS = {
    "en": "Hello, this is a test of the text to speech system.",
    "es": "Hola, esta es una voz clonada generada mediante el archivo base proporcionado"
}

def test_model(model_name, language):
    TEST_TEXT = TEST_TEXTS[language]
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
        speakers = [None]  # Voz por defecto

    for idx, speaker in enumerate(speakers, 1):
        # Generación voz por defecto o speaker específico
        if speaker is None:
            filename = model_dir / "default.wav"
            try:
                tts.tts_to_file(text=TEST_TEXT, speaker=None, file_path=str(filename))
                print(f"  ✓ Generado voz por defecto: {filename.name}")
            except Exception as e:
                print(f"  ✗ Error generando voz por defecto: {e}")
        else:
            filename = model_dir / f"speaker_{speaker}.wav"
            try:
                tts.tts_to_file(text=TEST_TEXT, speaker=speaker, file_path=str(filename))
                print(f"  ✓ Generado speaker {speaker}: {filename.name}")
            except Exception as e:
                print(f"  ✗ Error generando speaker {speaker}: {e}")

    # Generación por clonación de voz
    if USE_CLONING and model_name in ["tts_models/multilingual/multi-dataset/your_tts",
                                      "tts_models/multilingual/multi-dataset/xtts_v2"]:
        filename = model_dir / "cloned_voice.wav"
        try:
            tts.tts_to_file(
                text=TEST_TEXT,
                speaker_wav=str(CLONING_AUDIO),
                language="es",
                file_path=str(filename)
            )
            print(f"  ✓ Generado clonación de voz: {filename.name}")
        except Exception as e:
            print(f"  ✗ Error generando clonación de voz: {e}")
import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path: sys.path.append(PROJECT_ROOT)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "Models")

VISUAL_MODEL_PATH = os.path.join(MODELS_DIR, r"Talk2Mind\Models\Visual_Model.pth")

SPEECH_MODEL_PATH = os.path.join(MODELS_DIR, r"Talk2Mind\Models\Speech_Model_V2.pth")

QUESTIONNAIRE_MODEL_PATH = os.path.join(MODELS_DIR, r"Talk2Mind\Models\Questionnaire_Model.pth")

APP_TITLE = "Talk2Mind"

CAMERA_DURATION = 30
AUDIO_DURATION = 30

from gtts import gTTS
import pytesseract
from PIL import Image
from django.conf import settings
import os
pytesseract.pytesseract.tesseract_cmd=r'C:\Users\hp\AppData\Local\Programs\Tesseract-OCR\tesseract.exe'

def image_to_text(image_path,lang='eng'):
    """Extract text from an image using Tesseract OCR."""
    text = pytesseract.image_to_string(Image.open(image_path),lang=lang)
    return text

def text_to_speech(text, language='en'):
    """Convert text to speech and save it as an audio file."""
    tts = gTTS(text=text, lang=language)
    audio_path = os.path.join(settings.MEDIA_ROOT,'output_audio.mp3')
    tts.save(audio_path)
    return audio_path
from PIL import Image
from pytesseract import pytesseract
pytesseract.tesseract_cmd = r'/opt/homebrew/Cellar/tesseract/5.2.0/bin/tesseract'

print(pytesseract.image_to_string(Image.open('img.jpeg')))
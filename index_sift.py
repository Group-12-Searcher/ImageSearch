from sift.pgmconverter import convertGray
from sift.keyconverter import convertKey
import glob

for imagePath in glob.glob("dataset\dataset\*.jpg"):
    convertGray(imagePath)
for imagePath in glob.glob("sift\*.pgm"):
    convertKey(imagePath)

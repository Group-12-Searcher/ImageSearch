from sift.pgmconverter import convertGray
from sift.keyconverter import convertKey
import glob
from sift.vwhist import vwHist

for imagePath in glob.glob("dataset\dataset\*.jpg"):
    convertGray(imagePath)
for imagePath in glob.glob("sift\*.pgm"):
    vwHist(imagePath)

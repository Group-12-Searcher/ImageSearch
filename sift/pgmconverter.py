# import the necessary packages
from pyimagesearch.colordescriptor import ColorDescriptor
from pyimagesearch.semanticsreader import SemanticsReader
from pyimagesearch.searcher import Searcher
import cv2
from Tkinter import *
import tkFileDialog
from PIL import Image, ImageTk
import os
import subprocess

im = Image.open("0016_2065016987.jpg")
im = im.convert('L')
im.save("0016_2065016987.pgm")

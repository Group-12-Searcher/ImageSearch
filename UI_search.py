# import the necessary packages
from pyimagesearch.colordescriptor import ColorDescriptor
from pyimagesearch.semanticsreader import SemanticsReader
from pyimagesearch.searcher import Searcher
from sift.pgmconverter import convertQueryToGray
import cv2
from Tkinter import *
import tkFileDialog
from PIL import Image, ImageTk
import os
import subprocess
import csv

class UI_class:
    def __init__(self, master, search_path):
        self.search_path = search_path
        self.master = master
        topframe = Frame(self.master)
        topframe.pack()
        # these variables are declared for implementing the flushing of old (query + results)
        self.isUploadingImage = False
        self.result_img_frame = Frame(self.master)
        self.result_img_frame.pack()
        self.query_img_frame = Frame(self.master)
        self.query_img_frame.pack()

        #Buttons
        topspace = Label(topframe).grid(row=0, columnspan=2)
        self.bbutton= Button(topframe, text=" Choose an image ", command=self.browse_query_img)
        self.bbutton.grid(row=1, column=1)
        self.cbutton = Button(topframe, text=" Search ", command=self.show_results_imgs)
        self.cbutton.grid(row=1, column=2)
        downspace = Label(topframe).grid(row=3, columnspan=4)

        self.master.mainloop()


    def browse_query_img(self):
        # user wants to enter a query; flush old (query + results)
        self.isUploadingImage = True
        self.query_img_frame.destroy()
        self.result_img_frame.pack_forget()
        # add new frame for showing new query image
        self.query_img_frame = Frame(self.master)
        self.query_img_frame.pack()
        from tkFileDialog import askopenfilename
        self.filename = tkFileDialog.askopenfile(title='Choose an Image File').name

        # process query image to feature vector
        # initialize the image descriptor
        cd = ColorDescriptor((8, 12, 3))
        sr = SemanticsReader()
        # load the query image and describe it
        query = cv2.imread(self.filename)
        self.queryfeatures = cd.describe(query)

        # process query image to semantics vector
        # generate temp.txt for exe to run on it.
        tempfile = open("semanticFeature\\temp.txt", "w")
        tempfile.write(self.filename)
        tempfile.close()
        # generate the txt file with 1000D for query
        FNULL = open(os.devnull, 'w') #suppress output to stdout
        os.chdir("semanticFeature")
        args = "./image_classification.exe temp.txt"
        #subprocess.call(args, stdout=FNULL, stderr=FNULL)
        subprocess.call(args)
        os.chdir("../")
        # read 1000D vector for semantics
        reqfile = self.filename
        base, ext = os.path.splitext(reqfile)
        self.querysemantics = sr.read(base + ".txt")

        # convert query image to grayscale
        convertQueryToGray(self.filename)
        # generate key file for query
        with open("sift/temp/query.pgm","rb") as ip, open("sift/temp/query.key","wb") as op:
            subprocess.call("sift/siftWin32.exe",stdin=ip,stdout=op)

        # convert query image to list of texts (if any)
        reader = csv.reader(open("dataset\\dataset\\combined_text_tags.txt"), delimiter=" ")
        # find the line belonging to query image, req_line = None if no tags found
        img_name = self.filename.split("/")[-1]
        req_line = None
        for line in reader:
            if (line[0] == img_name):
                req_line = line[6:]
                break
        self.querytext = req_line
        
        # show query image
        image_file = Image.open(self.filename)
        resized = image_file.resize((100, 100), Image.ANTIALIAS)
        im = ImageTk.PhotoImage(resized)
        image_label = Label(self.query_img_frame, image=im)
        image_label.pack()

        self.query_img_frame.mainloop()


    def show_results_imgs(self):
        # user now wants to commence the search; load frame for displaying results of query
        self.isUploadingImage = False;
        # self.result_img_frame = Frame(self.master)
        self.result_img_frame.pack()

        # perform the search
        searcher = Searcher("index.csv", "index_semantics.csv", "index_text.csv")
        results = searcher.search(self.queryfeatures, self.querysemantics, self.querytext)

        # show result pictures
        COLUMNS = 8
        image_count = 0
        for (score, resultID) in results:
            # load the result image and display it
            image_count += 1
            r, c = divmod(image_count - 1, COLUMNS)
            im = Image.open(resultID)
            resized = im.resize((100, 100), Image.ANTIALIAS)
            tkimage = ImageTk.PhotoImage(resized)
            myvar = Label(self.result_img_frame, image=tkimage)
            myvar.image = tkimage
            myvar.grid(row=r, column=c)

        self.result_img_frame.mainloop()

root = Tk()
window = UI_class(root,'dataset')

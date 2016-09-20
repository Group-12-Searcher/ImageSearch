# import the necessary packages
from pyimagesearch.colordescriptor import ColorDescriptor
from pyimagesearch.semanticsreader import SemanticsReader
from pyimagesearch.searcher import Searcher
from sift.pgmconverter import convertQueryToGray
import cv2
from Tkinter import *
import tkFileDialog
import tkMessageBox
from PIL import Image, ImageTk
import os
import subprocess
import csv

class UI_class:
    
    def __init__(self, master, search_path):        
        self.search_path = search_path
        self.master = master
        topframe = Frame(self.master)
        # these variables are declared for implementing the flushing of old (query + results)
        self.isUploadingImage = False

        #Buttons
        self.colorHist = IntVar()
        self.visualKeyword = IntVar()
        self.visualConcept = IntVar()
        self.deepLearning = IntVar()
        self.textFeature = IntVar()
        self.option_vars = [self.colorHist, self.visualKeyword, self.visualConcept, self.deepLearning, self.textFeature]
        self.option_flags = [0,0,0,0,0]
        self.option_weights = [0,0,0,0,0]
        self.option_boxes = []
        self.option_sliders = []
        self.count = 0

        # Color Histogram inputs
        self.ch = Label(topframe).grid(row=1, columnspan=2)
        self.checkButton1 = Checkbutton(master, text="Color Histogram", variable=self.colorHist)
        self.checkButton1.deselect()
        self.option_boxes.append(self.checkButton1)
        self.option_boxes[0].bind("<Button-1>", self.toggle_ch_slider)
        self.ch_scale = Scale(master, from_=0, to=1, resolution=0.01, orient=HORIZONTAL)
        self.ch_scale.config(state=DISABLED, length=800)
        self.ch_scale.bind("<Button-1>", self.register_ch_original_value)
        self.ch_scale.bind("<ButtonRelease-1>", self.ch_adjust_others)
        self.option_sliders.append(self.ch_scale)
        self.checkButton1.pack()
        self.ch_scale.pack()

        # Visual Keywords inputs
        self.vk = Label(topframe).grid(row=1, columnspan=2)
        self.checkButton2 = Checkbutton(master, text="Visual Keyword", variable=self.visualKeyword)
        self.checkButton2.deselect()
        self.option_boxes.append(self.checkButton2)
        self.option_boxes[1].bind("<Button-1>", self.toggle_vk_slider)
        self.checkButton2.pack()
        self.vk_scale = Scale(master, from_=0, to=1, resolution=0.01, orient=HORIZONTAL)
        self.vk_scale.config(state=DISABLED, length=800)
        self.vk_scale.bind("<Button-1>", self.register_vk_original_value)
        self.vk_scale.bind("<ButtonRelease-1>", self.vk_adjust_others)
        self.option_sliders.append(self.vk_scale)
        self.vk_scale.pack()

        # Visual Concepts inputs
        self.vc = Label(topframe).grid(row=1, columnspan=2)
        self.checkButton3 = Checkbutton(master, text="Visual Concept", variable=self.visualConcept)
        self.checkButton3.deselect()
        self.option_boxes.append(self.checkButton3)
        self.option_boxes[2].bind("<Button-1>", self.toggle_vc_slider)
        self.checkButton3.pack()
        self.vc_scale = Scale(master, from_=0, to=1, resolution=0.01, orient=HORIZONTAL)
        self.vc_scale.config(state=DISABLED, length=800)
        self.vc_scale.bind("<Button-1>", self.register_vc_original_value)
        self.vc_scale.bind("<ButtonRelease-1>", self.vc_adjust_others)
        self.option_sliders.append(self.vc_scale)
        self.vc_scale.pack()

        # Deep Learning inputs
        self.dl = Label(topframe).grid(row=1, columnspan=2)
        self.checkButton4 = Checkbutton(master, text="Deep Learning", variable=self.deepLearning)
        self.checkButton4.deselect()
        self.option_boxes.append(self.checkButton4)
        self.option_boxes[3].bind("<Button-1>", self.toggle_dl_slider)
        self.checkButton4.pack()
        self.dl_scale = Scale(master, from_=0, to=1, resolution=0.01, orient=HORIZONTAL)
        self.dl_scale.config(state=DISABLED, length=800)
        self.dl_scale.bind("<Button-1>", self.register_dl_original_value)
        self.dl_scale.bind("<ButtonRelease-1>", self.dl_adjust_others)
        self.option_sliders.append(self.dl_scale)
        self.dl_scale.pack()

        # Text Features inputs
        self.tf = Label(topframe).grid(row=1, columnspan=2)
        self.checkButton5 = Checkbutton(master, text="Text Feature", variable=self.textFeature)
        self.checkButton5.deselect()
        self.option_boxes.append(self.checkButton5)
        self.option_boxes[4].bind("<Button-1>", self.toggle_tf_slider)
        self.checkButton5.pack()
        self.tf_scale = Scale(master, from_=0, to=1, resolution=0.01, orient=HORIZONTAL)
        self.tf_scale.config(state=DISABLED, length=800)
        self.tf_scale.bind("<Button-1>", self.register_tf_original_value)
        self.tf_scale.bind("<ButtonRelease-1>", self.tf_adjust_others)
        self.option_sliders.append(self.tf_scale)
        self.tf_scale.pack()
        
        self.bbutton= Button(topframe, text=" Choose an image ", command=self.browse_query_img)
        self.bbutton.grid(row=1, column=1)
        self.cbutton = Button(topframe, text=" Search ", command=self.show_results_imgs)
        self.cbutton.grid(row=1, column=2)

        self.result_img_frame = Frame(self.master)
        self.result_img_frame.pack()
        self.query_img_frame = Frame(self.master)
        self.query_img_frame.pack()

        downspace = Label(topframe).grid(row=7, columnspan=1)

        topframe.pack()
    
        self.master.mainloop()

    def toggle_ch_slider(self, event):
        if self.option_vars[0].get() == 0:
            self.count = self.count + 1
            self.option_flags[0] = 1
            self.option_sliders[0].config(state=NORMAL)
            for i in range(0, 5):
                if self.option_flags[i] == 1:
                    self.option_sliders[i].set(1.0 / self.count)
        else:
            self.count = self.count - 1
            self.option_flags[0] = 0
            self.option_sliders[0].set(0.0)
            self.option_sliders[0].config(state=DISABLED)
            if self.count != 0:
                for i in range(0, 5):
                    if self.option_flags[i] == 1:
                        self.option_sliders[i].set(1.0 / self.count)

    def toggle_vk_slider(self, event):
        if self.option_vars[1].get() == 0:
            self.count = self.count + 1
            self.option_flags[1] = 1
            self.option_sliders[1].config(state=NORMAL)
            for i in range(0, 5):
                if self.option_flags[i] == 1:
                    self.option_sliders[i].set(1.0 / self.count)
        else:
            self.count = self.count - 1
            self.option_flags[1] = 0
            self.option_sliders[1].set(0.0)
            self.option_sliders[1].config(state=DISABLED)
            if self.count != 0:
                for i in range(0, 5):
                    if self.option_flags[i] == 1:
                        self.option_sliders[i].set(1.0 / self.count)

    def toggle_vc_slider(self, event):
        if self.option_vars[2].get() == 0:
            self.count = self.count + 1
            self.option_flags[2] = 1
            self.option_sliders[2].config(state=NORMAL)
            for i in range(0, 5):
                if self.option_flags[i] == 1:
                    self.option_sliders[i].set(1.0 / self.count)
        else:
            self.count = self.count - 1
            self.option_flags[2] = 0
            self.option_sliders[2].set(0.0)
            self.option_sliders[2].config(state=DISABLED)
            if self.count != 0:
                for i in range(0, 5):
                    if self.option_flags[i] == 1:
                        self.option_sliders[i].set(1.0 / self.count)

    def toggle_dl_slider(self, event):
        if self.option_vars[3].get() == 0:
            self.count = self.count + 1
            self.option_flags[3] = 1
            self.option_sliders[3].config(state=NORMAL)
            for i in range(0, 5):
                if self.option_flags[i] == 1:
                    self.option_sliders[i].set(1.0 / self.count)
        else:
            self.count = self.count - 1
            self.option_flags[3] = 0
            self.option_sliders[3].set(0.0)
            self.option_sliders[3].config(state=DISABLED)
            if self.count != 0:
                for i in range(0, 5):
                    if self.option_flags[i] == 1:
                        self.option_sliders[i].set(1.0 / self.count)

    def toggle_tf_slider(self, event):
        if self.option_vars[4].get() == 0:
            self.count = self.count + 1
            self.option_flags[4] = 1
            self.option_sliders[4].config(state=NORMAL)
            for i in range(0, 5):
                if self.option_flags[i] == 1:
                    self.option_sliders[i].set(1.0 / self.count)
        else:
            self.count = self.count - 1
            self.option_flags[4] = 0
            self.option_sliders[4].set(0.0)
            self.option_sliders[4].config(state=DISABLED)
            if self.count != 0:
                for i in range(0, 5):
                    if self.option_flags[i] == 1:
                        self.option_sliders[i].set(1.0 / self.count)

    def register_ch_original_value(self, event):
        self.option_weights[0] = self.option_sliders[0].get()
        #print("CH: %s" % (self.option_weights[0]))

    def register_vk_original_value(self, event):
        self.option_weights[1] = self.option_sliders[1].get()
        #print("VK: %s" % (self.option_weights[1]))

    def register_vc_original_value(self, event):
        self.option_weights[2] = self.option_sliders[2].get()
        #print("VC: %s" % (self.option_weights[2]))

    def register_dl_original_value(self, event):
        self.option_weights[3] = self.option_sliders[3].get()
        #print("DL: %s" % (self.option_weights[3]))

    def register_tf_original_value(self, event):
        self.option_weights[4] = self.option_sliders[4].get()
        #print("TF: %s" % (self.option_weights[4]))

    def ch_adjust_others(self, value):
        if self.count > 1:
            difference = (self.option_weights[0] - self.option_sliders[0].get()) / (self.count - 1)
            self.option_weights[0] = self.option_sliders[0].get()
            print(difference)
            for i in range(0, 5):
                if i != 0 and self.option_flags[i] == 1:
                    self.option_weights[i] = self.option_weights[i] + difference
                    self.option_sliders[i].set(self.option_weights[i])

    def vk_adjust_others(self, event):
        if self.count > 1:
            difference = (self.option_weights[1] - self.option_sliders[1].get()) / (self.count - 1)
            self.option_weights[1] = self.option_sliders[1].get()
            print(difference)
            for i in range(0, 5):
                if i != 1 and self.option_flags[i] == 1:
                    self.option_weights[i] = self.option_weights[i] + difference
                    self.option_sliders[i].set(self.option_weights[i])

    def vc_adjust_others(self, event):
        if self.count > 1:
            difference = (self.option_weights[2] - self.option_sliders[2].get()) / (self.count - 1)
            self.option_weights[2] = self.option_sliders[2].get()
            print(difference)
            for i in range(0, 5):
                if i != 2 and self.option_flags[i] == 1:
                    self.option_sliders[i].set(self.option_sliders[i].get() + difference)

    def dl_adjust_others(self, event):
        if self.count > 1:
            difference = (self.option_weights[3] - self.option_sliders[3].get()) / (self.count - 1)
            self.option_weights[3] = self.option_sliders[3].get()
            print(difference)
            for i in range(0, 5):
                if i != 3 and self.option_flags[i] == 1:
                    self.option_sliders[i].set(self.option_sliders[i].get() + difference)

    def tf_adjust_others(self, event):
        if self.count > 1:
            difference = (self.option_weights[4] - self.option_sliders[4].get()) / (self.count - 1)
            self.option_weights[4] = self.option_sliders[4].get()
            print(difference)
            for i in range(0, 5):
                if i != 4 and self.option_flags[i] == 1:
                    self.option_sliders[i].set(self.option_sliders[i].get() + difference)

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

    def get_options(self):
        options = {}
        options['ch'] = self.option_sliders[0].get()
        options['vk'] = self.option_sliders[1].get()
        options['vc'] = self.option_sliders[2].get()
        options['dl'] = self.option_sliders[3].get()
        options['tf'] = self.option_sliders[4].get()
        return options

    def show_results_imgs(self):
        
        # user now wants to commence the search; load frame for displaying results of query
        self.isUploadingImage = False;
        # self.result_img_frame = Frame(self.master)
        self.result_img_frame.pack()

        if (self.count == 0):
            tkMessageBox.showwarning("Alert", "Please select at least 1 option.")
            self.result_img_frame.mainloop()

        flags = self.get_options()

        # perform the search
        searcher = Searcher("index.csv", "index_semantics.csv", "index_text.csv", flags)
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

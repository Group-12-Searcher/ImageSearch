# import the necessary packages
from pyimagesearch.colordescriptor import ColorDescriptor
from pyimagesearch.semanticsreader import SemanticsReader
from pyimagesearch.searcher import Searcher
# from deepLearning.inception_v3 import deepSearch
from sift.pgmconverter import convertQueryToGray
import cv2
from Tkinter import *
import tkFileDialog
import tkMessageBox
from PIL import Image, ImageTk
import os
import os.path
import subprocess
import csv
import logResults

class UI_class:
    
    def __init__(self, master, search_path):        
        self.search_path = search_path
        self.master = master
        self.topframe = Frame(self.master)
        # these variables are declared for implementing the flushing of old (query + results)
        self.isUploadingImage = False

        self.filename = None
        self.currFilename = None
        self.searchCount = 0
        self.isSameFile = False

        self.queryfeatures = None
        self.querysemantics = None
        self.querytext = None
        self.querycategory = None

        self.toLogResults = True
        self.queryImageCategory = ''
        #Buttons        
        self.bbutton= Button(self.topframe, text="    Choose an image    ", command=self.browse_query_img)
        self.bbutton.grid(row=1, column=1, columnspan=3)
        self.cbutton = Button(self.topframe, text="          Search         ", command=self.show_results_imgs)
        self.cbutton.grid(row=1, column=4, columnspan=1)
        self.dbutton = Button(self.topframe, text=" X ", command=self.clear_window)
        self.dbutton.grid(row=1, column=6, columnspan=1)
        self.tf_label = Label(self.topframe, text="     Enter search term:  ")
        self.tf_label.grid(row=2, column=1, columnspan=2)
        self.tf_input = Entry(self.topframe)
        self.tf_input.grid(row=2, column=3, columnspan=6)
        rightspace = Label(self.topframe).grid(row=2, column=7, columnspan=1)

        self.result_img_frame = Frame(self.master)
        self.result_img_frame.pack()
        self.query_img_frame = Frame(self.master)
        self.query_img_frame.pack()

        downspace = Label(self.topframe).grid(row=7, columnspan=4)

        self.topframe.pack()

        self.option_flags = [0,0,0,0]
        self.option_weights = [0.0,0.0,0.0,0.0]
        self.count = 0

        self.load_options()
        self.reload_options()
    
        self.master.mainloop()

    def clear_window(self):
        self.option_flags = [0,0,0,0]
        self.option_weights = [0.0,0.0,0.0,0.0]
        self.count = 0
        self.reload_options()
        self.load_options()
        self.reload_options()
        self.query_img_frame.destroy()
        self.result_img_frame.destroy()
        self.tf_input.config(state=NORMAL)
        self.tf_input.delete(0, 'end')
        self.filename = None
        self.currFilename = None

    def reload_options(self):
        self.checkButton1.pack_forget()
        self.ch_scale.pack_forget()
        self.checkButton2.pack_forget()
        self.vk_scale.pack_forget()
        self.checkButton3.pack_forget()
        self.vc_scale.pack_forget()
        # self.checkButton4.pack_forget()
        # self.dl_scale.pack_forget()
        self.checkButton4.pack_forget()
        self.tf_scale.pack_forget()
        self.tf_label.pack_forget()
        self.tf_input.pack_forget()

    def load_options(self):
        self.colorHist = IntVar()
        self.visualKeyword = IntVar()
        self.visualConcept = IntVar()
        # self.deepLearning = IntVar()
        self.textFeature = IntVar()
        self.option_vars = [self.colorHist, self.visualKeyword, self.visualConcept, self.textFeature]
        self.option_boxes = []
        self.option_sliders = []

        # Color Histogram inputs
        self.ch = Label(self.topframe).grid(row=1)
        self.checkButton1 = Checkbutton(self.master, text="Color Histogram", variable=self.colorHist)
        self.checkButton1.deselect()
        self.option_boxes.append(self.checkButton1)
        self.option_boxes[0].bind("<Button-1>", self.toggle_ch_slider)
        self.checkButton1.pack()
        self.ch_scale = Scale(self.master, from_=0, to=1, resolution=0.01, orient=HORIZONTAL)
        self.ch_scale.config(state=DISABLED, length=800)
        self.ch_scale.bind("<Button-1>", self.register_ch_original_value)
        self.ch_scale.bind("<ButtonRelease-1>", self.ch_adjust_others)
        self.option_sliders.append(self.ch_scale)
        self.ch_scale.pack()

        # Visual Keywords inputs
        self.vk = Label(self.topframe).grid(row=1)
        self.checkButton2 = Checkbutton(self.master, text="Visual Keyword", variable=self.visualKeyword)
        self.checkButton2.deselect()
        self.option_boxes.append(self.checkButton2)
        self.option_boxes[1].bind("<Button-1>", self.toggle_vk_slider)
        self.checkButton2.pack()
        self.vk_scale = Scale(self.master, from_=0, to=1, resolution=0.01, orient=HORIZONTAL)
        self.vk_scale.config(state=DISABLED, length=800)
        self.vk_scale.bind("<Button-1>", self.register_vk_original_value)
        self.vk_scale.bind("<ButtonRelease-1>", self.vk_adjust_others)
        self.option_sliders.append(self.vk_scale)
        self.vk_scale.pack()

        # Visual Concepts inputs
        self.vc = Label(self.topframe).grid(row=1)
        self.checkButton3 = Checkbutton(self.master, text="Visual Concept", variable=self.visualConcept)
        self.checkButton3.deselect()
        self.option_boxes.append(self.checkButton3)
        self.option_boxes[2].bind("<Button-1>", self.toggle_vc_slider)
        self.checkButton3.pack()
        self.vc_scale = Scale(self.master, from_=0, to=1, resolution=0.01, orient=HORIZONTAL)
        self.vc_scale.config(state=DISABLED, length=800)
        self.vc_scale.bind("<Button-1>", self.register_vc_original_value)
        self.vc_scale.bind("<ButtonRelease-1>", self.vc_adjust_others)
        self.option_sliders.append(self.vc_scale)
        self.vc_scale.pack()

        # Deep Learning inputs
        '''
        self.dl = Label(self.topframe).grid(row=1)
        self.checkButton4 = Checkbutton(self.master, text="Deep Learning", variable=self.deepLearning)
        self.checkButton4.deselect()
        self.option_boxes.append(self.checkButton4)
        self.option_boxes[3].bind("<Button-1>", self.toggle_dl_slider)
        self.checkButton4.pack()
        self.dl_scale = Scale(self.master, from_=0, to=1, resolution=0.01, orient=HORIZONTAL)
        self.dl_scale.config(state=DISABLED, length=800)
        self.dl_scale.bind("<Button-1>", self.register_dl_original_value)
        self.dl_scale.bind("<ButtonRelease-1>", self.dl_adjust_others)
        self.option_sliders.append(self.dl_scale)
        self.dl_scale.pack()'''

        # Text Features inputs
        self.tf = Label(self.topframe).grid(row=1)
        self.checkButton4 = Checkbutton(self.master, text="Text Feature", variable=self.textFeature)
        self.checkButton4.deselect()
        self.option_boxes.append(self.checkButton4)
        self.option_boxes[3].bind("<Button-1>", self.toggle_tf_slider)
        self.checkButton4.pack()
        self.tf_scale = Scale(self.master, from_=0, to=1, resolution=0.01, orient=HORIZONTAL)
        self.tf_scale.config(state=DISABLED, length=800)
        self.tf_scale.bind("<Button-1>", self.register_tf_original_value)
        self.tf_scale.bind("<ButtonRelease-1>", self.tf_adjust_others)
        self.option_sliders.append(self.tf_scale)
        self.tf_scale.pack()

        self.checkButtons = [self.checkButton1, self.checkButton2, self.checkButton3, self.checkButton4]
        for i in range(0, 4):
            if self.count > 0:
                if self.option_flags[i] == 1:
                    self.checkButtons[i].select()
                    self.option_sliders[i].config(state=NORMAL)
                    self.option_sliders[i].set(self.option_weights[i])
                else:
                    self.checkButtons[i].deselect()

    def toggle_ch_slider(self, event):
        if self.option_vars[0].get() == 0:
            self.count = self.count + 1
            self.option_flags[0] = 1
            self.option_sliders[0].config(state=NORMAL)
            for i in range(0, 4):
                if self.option_flags[i] == 1:
                    self.option_sliders[i].set(1.0 / self.count)
                    self.option_weights[i] = self.option_sliders[i].get()
        else:
            self.count = self.count - 1
            self.option_flags[0] = 0
            self.option_sliders[0].set(0.0)
            self.option_sliders[0].config(state=DISABLED)
            if self.count != 0:
                for i in range(0, 4):
                    if self.option_flags[i] == 1:
                        self.option_sliders[i].set(1.0 / self.count)
                        self.option_weights[i] = self.option_sliders[i].get()

    def toggle_vk_slider(self, event):
        if self.option_vars[1].get() == 0:
            self.count = self.count + 1
            self.option_flags[1] = 1
            self.option_sliders[1].config(state=NORMAL)
            for i in range(0, 4):
                if self.option_flags[i] == 1:
                    self.option_sliders[i].set(1.0 / self.count)
                    self.option_weights[i] = self.option_sliders[i].get()
        else:
            self.count = self.count - 1
            self.option_flags[1] = 0
            self.option_sliders[1].set(0.0)
            self.option_sliders[1].config(state=DISABLED)
            if self.count != 0:
                for i in range(0, 4):
                    if self.option_flags[i] == 1:
                        self.option_sliders[i].set(1.0 / self.count)
                        self.option_weights[i] = self.option_sliders[i].get()

    def toggle_vc_slider(self, event):
        if self.option_vars[2].get() == 0:
            self.count = self.count + 1
            self.option_flags[2] = 1
            self.option_sliders[2].config(state=NORMAL)
            for i in range(0, 4):
                if self.option_flags[i] == 1:
                    self.option_sliders[i].set(1.0 / self.count)
                    self.option_weights[i] = self.option_sliders[i].get()
        else:
            self.count = self.count - 1
            self.option_flags[2] = 0
            self.option_sliders[2].set(0.0)
            self.option_sliders[2].config(state=DISABLED)
            if self.count != 0:
                for i in range(0, 4):
                    if self.option_flags[i] == 1:
                        self.option_sliders[i].set(1.0 / self.count)
                        self.option_weights[i] = self.option_sliders[i].get()

    '''def toggle_dl_slider(self, event):
        if self.option_vars[3].get() == 0:
            self.count = self.count + 1
            self.option_flags[3] = 1
            self.option_sliders[3].config(state=NORMAL)
            for i in range(0, 5):
                if self.option_flags[i] == 1:
                    self.option_sliders[i].set(1.0 / self.count)
                    self.option_weights[i] = self.option_sliders[i].get()
        else:
            self.count = self.count - 1
            self.option_flags[3] = 0
            self.option_sliders[3].set(0.0)
            self.option_sliders[3].config(state=DISABLED)
            if self.count != 0:
                for i in range(0, 5):
                    if self.option_flags[i] == 1:
                        self.option_sliders[i].set(1.0 / self.count)
                        self.option_weights[i] = self.option_sliders[i].get()'''

    def toggle_tf_slider(self, event):
        if self.option_vars[3].get() == 0:
            self.count = self.count + 1
            self.option_flags[3] = 1
            self.option_sliders[3].config(state=NORMAL)
            for i in range(0, 4):
                if self.option_flags[i] == 1:
                    self.option_sliders[i].set(1.0 / self.count)
                    self.option_weights[i] = self.option_sliders[i].get()
        else:
            self.count = self.count - 1
            self.option_flags[3] = 0
            self.option_sliders[3].set(0.0)
            self.option_sliders[3].config(state=DISABLED)
            if self.count != 0:
                for i in range(0, 4):
                    if self.option_flags[i] == 1:
                        self.option_sliders[i].set(1.0 / self.count)
                        self.option_weights[i] = self.option_sliders[i].get()

    def register_ch_original_value(self, event):
        self.option_weights[0] = self.option_sliders[0].get()
        #print("CH: %s" % (self.option_weights[0]))

    def register_vk_original_value(self, event):
        self.option_weights[1] = self.option_sliders[1].get()
        #print("VK: %s" % (self.option_weights[1]))

    def register_vc_original_value(self, event):
        self.option_weights[2] = self.option_sliders[2].get()
        #print("VC: %s" % (self.option_weights[2]))

    '''def register_dl_original_value(self, event):
        self.option_weights[3] = self.option_sliders[3].get()
        #print("DL: %s" % (self.option_weights[3]))'''

    def register_tf_original_value(self, event):
        self.option_weights[3] = self.option_sliders[3].get()
        #print("TF: %s" % (self.option_weights[3]))

    def ch_adjust_others(self, value):
        if self.count > 1:
            self.option_weights[0] = self.option_sliders[0].get()
            remainder = 1.0 - self.option_weights[0]
            if remainder == 0:
                for i in range(0, 4):
                    if i != 0 and self.option_flags[i] == 1:
                        self.count = self.count - 1
                        self.option_flags[i] = 0
                        self.option_sliders[i].set(0.0)
                        self.option_sliders[i].config(state=DISABLED)
                        self.checkButtons[i].deselect()
            else:
                sumOfOtherWeights = 0
                for i in range(0, 4):
                    if i != 0 and self.option_flags[i] == 1:
                        sumOfOtherWeights += self.option_weights[i]
                else:
                    for i in range(0, 4):
                        if i != 0 and self.option_flags[i] == 1:
                            self.option_weights[i] = self.option_weights[i]/sumOfOtherWeights*remainder
                            self.option_sliders[i].set(self.option_weights[i])

    def vk_adjust_others(self, event):
        if self.count > 1:
            self.option_weights[1] = self.option_sliders[1].get()
            remainder = 1.0 - self.option_weights[1]
            if remainder == 0:
                    for i in range(0, 4):
                        if i != 1 and self.option_flags[i] == 1:
                            self.count = self.count - 1
                            self.option_flags[i] = 0
                            self.option_sliders[i].set(0.0)
                            self.option_sliders[i].config(state=DISABLED)
                            self.checkButtons[i].deselect()
            else:
                sumOfOtherWeights = 0
                for i in range(0, 4):
                    if i != 1 and self.option_flags[i] == 1:
                        sumOfOtherWeights += self.option_weights[i]
                for i in range(0, 4):
                    if i != 1 and self.option_flags[i] == 1:
                        self.option_weights[i] = self.option_weights[i]/sumOfOtherWeights*remainder
                        self.option_sliders[i].set(self.option_weights[i])

    def vc_adjust_others(self, event):
        if self.count > 1:
            self.option_weights[2] = self.option_sliders[2].get()
            remainder = 1.0 - self.option_weights[2]
            if remainder == 0:
                    for i in range(0, 4):
                        if i != 2 and self.option_flags[i] == 1:
                            self.count = self.count - 1
                            self.option_flags[i] = 0
                            self.option_sliders[i].set(0.0)
                            self.option_sliders[i].config(state=DISABLED)
                            self.checkButtons[i].deselect()
            else:
                sumOfOtherWeights = 0
                for i in range(0, 4):
                    if i != 2 and self.option_flags[i] == 1:
                        sumOfOtherWeights += self.option_weights[i]
                for i in range(0, 4):
                    if i != 2 and self.option_flags[i] == 1:
                        self.option_weights[i] = self.option_weights[i]/sumOfOtherWeights*remainder
                        self.option_sliders[i].set(self.option_weights[i])

    '''def dl_adjust_others(self, event):
        if self.count > 1:
            self.option_weights[3] = self.option_sliders[3].get()
            remainder = 1.0 - self.option_weights[3]
            if remainder == 0:
                    for i in range(0, 5):
                        if i != 3 and self.option_flags[i] == 1:
                            self.count = self.count - 1
                            self.option_flags[i] = 0
                            self.option_sliders[i].set(0.0)
                            self.option_sliders[i].config(state=DISABLED)
                            self.checkButtons[i].deselect()
            else:
                sumOfOtherWeights = 0
                for i in range(0, 5):
                    if i != 3 and self.option_flags[i] == 1:
                        sumOfOtherWeights += self.option_weights[i]
                for i in range(0, 5):
                    if i != 3 and self.option_flags[i] == 1:
                        self.option_weights[i] = self.option_weights[i]/sumOfOtherWeights*remainder
                        self.option_sliders[i].set(self.option_weights[i])'''
                    
    def tf_adjust_others(self, event):
        if self.count > 1:
            self.option_weights[3] = self.option_sliders[3].get()
            remainder = 1.0 - self.option_weights[3]
            if remainder == 0:
                    for i in range(0, 4):
                        if i != 3 and self.option_flags[i] == 1:
                            self.count = self.count - 1
                            self.option_flags[i] = 0
                            self.option_sliders[i].set(0.0)
                            self.option_sliders[i].config(state=DISABLED)
                            self.checkButtons[i].deselect()
            else:
                sumOfOtherWeights = 0
                for i in range(0, 4):
                    if i != 3 and self.option_flags[i] == 1:
                        sumOfOtherWeights += self.option_weights[i]
                for i in range(0, 4):
                    if i != 3 and self.option_flags[i] == 1:
                        self.option_weights[i] = self.option_weights[i]/sumOfOtherWeights*remainder
                        self.option_sliders[i].set(self.option_weights[i])

    def browse_query_img(self):
        self.tf_input.delete(0, END)
        # user wants to enter a query; flush old (query + results)
        self.isUploadingImage = True
        self.query_img_frame.destroy()
        self.result_img_frame.destroy()
        # add new frame for showing new query image
        self.query_img_frame = Frame(self.master)
        self.query_img_frame.pack()
        self.result_img_frame = Frame(self.master)
        self.result_img_frame.pack()
        from tkFileDialog import askopenfilename
        imageFile = tkFileDialog.askopenfile(title='Choose an Image File')
        while imageFile is None:
            tkMessageBox.showwarning("Alert", "Please select an image.")
            imageFile = tkFileDialog.askopenfile(title='Choose an Image File')
        self.filename = imageFile.name
        self.preprocess_image()

        if (self.toLogResults):
            fileNameCopy = self.filename
            parts = fileNameCopy.split('/')
            self.queryImageCategory = parts[len(parts) - 2]
            # print(self.queryImageCategory)

        # show query image
        if (self.filename is None and self.currFilename is not None):
            image_file = Image.open(self.currFilename)
            resized = image_file.resize((100, 100), Image.ANTIALIAS)
            im = ImageTk.PhotoImage(resized)
            image_label = Label(self.query_img_frame, image=im)
            image_label.pack()
        else:
            if (self.filename is not None):
                image_file = Image.open(self.filename)
                resized = image_file.resize((100, 100), Image.ANTIALIAS)
                im = ImageTk.PhotoImage(resized)
                image_label = Label(self.query_img_frame, image=im)
                image_label.pack()
                print(self.filename)
                print(self.currFilename)
                if (self.filename == self.currFilename):
                    self.isSameFile = True
                #self.currFilename = self.filename
                
        self.reload_options()
        self.load_options()
        if (self.count == 0):
            self.tf_input.config(state=NORMAL)
        else:
            self.tf_input.delete(0, len(self.tf_input.get()))
            self.tf_input.config(state=DISABLED)
        self.query_img_frame.mainloop()

    def preprocess_image(self):
        # process query image to feature vector
        # initialize the image descriptor
        #cd = ColorDescriptor((8, 12, 3))
        cd = ColorDescriptor((3, 3, 2))
        sr = SemanticsReader()

        # load the query image and describe it
        query = cv2.imread(self.filename)
        self.queryfeatures = cd.describe(query)

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

        # process query image to semantics vector
        # generate temp.txt for exe to run on it.
        tempfile = open("semanticFeature\\temp.txt", "w")
        tempfile.write(self.filename)
        tempfile.close()
        # generate the txt file with 1000D for query
        FNULL = open(os.devnull, 'w') #suppress output to stdout
        os.chdir("semanticFeature")
        # Check if txt file with 1000D already exists.
        reqfile = self.filename
        base, ext = os.path.splitext(reqfile)
        req_text_file = base + ".txt"
        if (not os.path.isfile(req_text_file)):
            args = "./image_classification.exe temp.txt"
            #subprocess.call(args, stdout=FNULL, stderr=FNULL)
            subprocess.call(args)
        os.chdir("../")
        # read 1000D vector for semantics
        self.querysemantics = sr.read(base + ".txt")

        # convert query image to grayscale
        convertQueryToGray(self.filename)
        # generate key file for query
        #with open("sift/temp/query.pgm","rb") as ip, open("sift/temp/query.key","wb") as op:
        #   subprocess.call("sift/siftWin32.exe",stdin=ip,stdout=op)

        # Do deep learning
        # self.querycategory = deepSearch(self.filename)

        # show query image
        '''image_file = Image.open(self.filename)
        resized = image_file.resize((100, 100), Image.ANTIALIAS)
        im = ImageTk.PhotoImage(resized)
        image_label = Label(self.query_img_frame, image=im)
        image_label.pack()'''


    def get_options(self):
        options = {}
        options['ch'] = self.option_sliders[0].get()
        options['vk'] = self.option_sliders[1].get()
        options['vc'] = self.option_sliders[2].get()
        # options['dl'] = self.option_sliders[3].get()
        options['tf'] = self.option_sliders[3].get()
        return options

    def show_results_imgs(self):
        if (self.count == 0 and self.tf_input.get() == "" ):
            tkMessageBox.showwarning("Alert", "Please enter a search term, or upload image.")

        else:
            if (self.filename == self.currFilename):
                self.isSameFile = True
            else:
                self.isSameFile = False
            
            # user now wants to commence the search; load frame for displaying results of query
            self.isUploadingImage = False;

            # flush out old results
            self.result_img_frame.destroy()
            self.result_img_frame = Frame(self.master)
            self.result_img_frame.pack()

            flags = self.get_options()
            # print(flags)

            # perform the search
            searcher = Searcher("index.csv", "index_semantics.csv", "index_text.csv", "index_deeplearning.csv", flags, self.tf_input.get())
            results = searcher.search(self.queryfeatures, self.querysemantics, self.querytext, self.querycategory)

            if (len(results) == 0):
                pass
            else:
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

            if (self.toLogResults):
                numRelevant = logResults.get_precision(self.queryImageCategory, results)
                print(numRelevant)

            self.currFilename = self.filename

        self.result_img_frame.mainloop()

root = Tk()
window = UI_class(root,'dataset')

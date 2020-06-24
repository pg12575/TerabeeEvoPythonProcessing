#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from PIL import Image, ImageTk
import tkinter as Tk
import cv2
import time

class ViewThermal():
    def __init__(self, data, portname):

        self.frames = data
        ### Visualization window ###
        self.activate_visualization = True
        windowexist = 0
        if Tk._default_root is None:
            self.window = Tk.Tk()
        else:
            self.window = Tk.Toplevel()
            windowexist = 1
        self.window.wm_geometry("640x720")
        self.canvas_width = 600
        self.canvas_height = 600
        self.canvas2 = Tk.Canvas(self.window, width=self.canvas_width, height=self.canvas_height)
        self.canvas2.pack(side=Tk.TOP)
        self.photo = ImageTk.PhotoImage("P")
        self.img = self.canvas2.create_image(300, 300, image=self.photo)
        self.text2 = Tk.Label(self.window)
        self.text2.config(height=10, width=20, text='', font=("Helvetica", 25))
        self.text2.pack(side=Tk.BOTTOM)
        if portname == "ACM0":
            self.text2.config(text="Top View Dining")
        elif portname == "ACM1":
            self.text2.config(text="Side View Kitchen")
        elif portname == "ACM2":
            self.text2.config(text="Top View Kitchen")
        self.MinAvg = []

        self.MinAvg = []
        self.MaxAvg = []

        r = []
        g = []
        b = []
        with open('colormap.txt', 'r') as f:
            for i in range(256):
                x, y, z = f.readline().split(',')
                r.append(x)
                g.append(y)
                b.append(z.replace(";\n", ""))
        self.colormap = np.zeros((256, 1, 3), dtype=np.uint8)
        self.colormap[:, 0, 0] = b
        self.colormap[:, 0, 1] = g
        self.colormap[:, 0, 2] = r

    def update_GUI(self):

        frame = self.rounded_array.astype(np.uint8)
        frame = cv2.applyColorMap(frame, self.colormap)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        frame = cv2.resize(frame, (self.canvas_width, self.canvas_height), interpolation=cv2.INTER_NEAREST)

        self.photo = ImageTk.PhotoImage(Image.fromarray(frame))
        self.canvas2.itemconfig(self.img, image=self.photo)
        self.window.update()

    def array_2_image(self, frame):
        '''
        This function is creating an Image from numpy array
        '''
        thermal_img = frame
        im = Image.fromarray(np.uint8(thermal_img), mode="P")
        im = im.resize(size=(self.canvas_width, self.canvas_height), resample=Image.NEAREST)
        return im

    def scaleImg(self, data):
        ### Get min/max/TA for averaging ###
        frameMin, frameMax = data.min(), data.max()
        self.MinAvg.append(frameMin)
        self.MaxAvg.append(frameMax)

        ### Need at least 10 frames for better average ###
        if len(self.MaxAvg) >= 10:
            AvgMax = sum(self.MaxAvg) / len(self.MaxAvg)
            AvgMin = sum(self.MinAvg) / len(self.MinAvg)
            ### Delete oldest insertions ###
            self.MaxAvg.pop(0)
            self.MinAvg.pop(0)
        else:
            ### Until list fills, use current frame min/max/ptat ###
            AvgMax = frameMax
            AvgMin = frameMin

        # Scale data
        data[data <= AvgMin] = AvgMin
        data[data >= AvgMax] = AvgMax
        multiplier = 255 / (AvgMax - AvgMin)
        data = data - AvgMin
        data = data * multiplier
        return data

    def run(self):
        ### Get frame and print it ###
        frame = self.frames

        viewframe = np.copy(frame[i+1])



if __name__ == "__main__":
    N = 32
    portname1 = "ACM0"
    portname2 = "ACM1"
    #portname3 = "ACM2"
    #data1 = np.loadtxt("output/frame" + str(portname1) + ".txt")

    data1 = np.fromfile("output/frame" + str(portname1) + ".txt", sep=' ')
    data2 = np.fromfile("output/frame" + str(portname2) + ".txt",  sep=' ')
    #data3 = np.fromfile("output/frame" + str(portname3) + ".txt",  sep=' ')

    data1 = data1.reshape(len(data1)//32, 32)
    data2 = data2.reshape(len(data2)//32, 32)
    #data3 = data3.reshape(len(data3)//32, 32)


    i = 0
    numRows, _ = data1.shape
    numFrames = int(numRows / 32)

    data1 = data1[:numFrames * 32].reshape((numFrames, 32, 32))
    data2 = data2[:numFrames * 32].reshape((numFrames, 32, 32))
    #data3 = data3[:numFrames * 32].reshape((numFrames, 32, 32))


    view1 = ViewThermal(data1, portname1)
    view2 = ViewThermal(data2, portname2)
    #view3 = ViewThermal(data3, portname3)


    while i < (len(data1) - 1):
        viewframe = np.copy(data1[i+1])
        newframe = view1.scaleImg(viewframe)
        newframeR = np.rot90(newframe, k=3)
        newframeR = np.flip(newframeR, axis=0)
        view1.rounded_array = np.round(newframeR, 0)
        view1.update_GUI()

        viewframe2 = np.copy(data2[i + 1])
        newframe2 = view2.scaleImg(viewframe2)
        newframeR2 = np.rot90(newframe2, k=1)
        newframeR2 = np.flip(newframeR2, axis=0)
        view2.rounded_array = np.round(newframeR2, 0)
        view2.update_GUI()

        #viewframe3 = np.copy(data3[i + 1])
        #newframe3 = view3.scaleImg(viewframe3)
        #view3.rounded_array = np.round(newframe3, 0)
        #view3.update_GUI()

        i = i + 1
        #print(i)
        time.sleep(0.1)


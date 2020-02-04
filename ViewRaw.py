import numpy as np
import matplotlib.pylab as plt
from matplotlib.pyplot import figure, draw, pause
import matplotlib
import cv2
from PIL import Image
matplotlib.use("TkAgg")


filename = "output/frameACM0.txt"
N = 32

data = np.loadtxt(filename)
data2 = np.loadtxt("output/frameACM1.txt")


numRows, _ = data.shape
numRows2, _ = data2.shape
numFrames = int(numRows/32)
numFrames2 = int(numRows2/32)

data = data[:numFrames*32].reshape((numFrames, 32, 32))
data2 = data2[:numFrames2*32].reshape((numFrames2, 32, 32))

#plt.imshow(data[15])
#plt.show()
i = 0
img = None

fg = figure()
ax = fg.gca()

fg2 = figure()
ax2 = fg2.gca()

fg3 = figure()
ax3 = fg3.gca()

fg4 = figure()
ax4 = fg4.gca()

MinAvg = []
MaxAvg = []


MinAvg2 = []
MaxAvg2 = []



def scaleImg(data, MinAvg, MaxAvg):
    ### Get min/max/TA for averaging ###
    frameMin, frameMax = data.min(), data.max()
    MinAvg.append(frameMin)
    MaxAvg.append(frameMax)

    ### Need at least 10 frames for better average ###
    if len(MaxAvg) >= 10:
        AvgMax = sum(MaxAvg) / len(MaxAvg)
        AvgMin = sum(MinAvg) / len(MinAvg)
        ### Delete oldest insertions ###
        MaxAvg.pop(0)
        MinAvg.pop(0)
    else:
        ### Until list fills, use current frame min/max/ptat ###
        AvgMax = frameMax
        AvgMin = frameMin

    # Scale data
    data[data <= AvgMin] = AvgMin
    data[data >= AvgMax] = AvgMax
    multiplier = 255/ (AvgMax - AvgMin)
    data = data - AvgMin
    data = data * multiplier
    return data, MinAvg, MaxAvg

def scaleImg2(data, MinAvg2, MaxAvg2):
    ### Get min/max/TA for averaging ###
    frameMin, frameMax = data.min(), data.max()
    MinAvg2.append(frameMin)
    MaxAvg2.append(frameMax)

    ### Need at least 10 frames for better average ###
    if len(MaxAvg) >= 10:
        AvgMax = sum(MaxAvg2) / len(MaxAvg2)
        AvgMin = sum(MinAvg2) / len(MinAvg2)
        ### Delete oldest insertions ###
        MaxAvg2.pop(0)
        MinAvg2.pop(0)
    else:
        ### Until list fills, use current frame min/max/ptat ###
        AvgMax = frameMax
        AvgMin = frameMin

    # Scale data
    data[data <= AvgMin] = AvgMin
    data[data >= AvgMax] = AvgMax
    multiplier = 255/ (AvgMax - AvgMin)
    data = data - AvgMin
    data = data * multiplier
    return data, MinAvg2, MaxAvg2


[newframe, MinAvg, MaxAvg] = scaleImg(data[i], MinAvg, MaxAvg)
[newframe2, MinAvg2, MaxAvg2] = scaleImg(data2[i], MinAvg2, MaxAvg2)
h2 = ax2.imshow((newframe2.astype(np.int)))
print(np.max(newframe))
h = ax.imshow((newframe.astype(np.int)))
ax.set_title("scaled")
ax2.set_title("scaled")
h4 = ax4.imshow(data2[i])
h3 = ax3.imshow(data[i])

while i < len(data):
    #print(i)
    ### Get min/max/TA for averaging ###
    #data3 = np.copy(data[i+1])

    frame = np.copy(data[i+1])
    frame2 = np.copy(data2[i+1])


    [newframe, MinAvg, MaxAvg] = scaleImg(frame, MinAvg, MaxAvg)
    [newframe2, MinAvg2, MaxAvg2] = scaleImg2(frame2, MinAvg2, MaxAvg2)

    h.set_data((newframe.astype(np.int)))
    h2.set_data((newframe2.astype(np.int)))

    h3.set_data(frame)
    h4.set_data(frame2)

    draw(), pause(0.01)
    #   plt.savefig("output/images/" + str(i) + ".png")
    #print(data[i:i+32])

    #plt.draw()
    i = i + 1

#！usr/bin/env python
# -*- coding: utf-8 -*-
import cv2
import numpy as np
# from matplotlib import pyplot as plt
from scipy import signal, io
import os.path,sys
# import xlrd
# import xlwt
# from xlutils.copy import copy

class extract_cf(object):
    def __init__(self,image_dir):
        self.image_dir = image_dir
                
    def extract(self):
        # import pdb;pdb.set_trace()
        if os.listdir(self.image_dir):

            for dng in os.listdir(self.image_dir):
                if os.path.splitext(dng)[1] == '.dng':
                    os.system("/home/fychen/Auth_server/Auth_app/dcraw -v -4 -H 0 -W -w -D -j -T " + os.path.join(self.image_dir,dng))
                    os.remove(os.path.join(self.image_dir,dng))
            lightsignal = []
            for tiff in os.listdir(self.image_dir):
                img = cv2.imread(os.path.join(self.image_dir,tiff))
                img_thd = threshold(img)
                img_mor = morphologyEx(img_thd,'close')
                img_shape = findLightShape(img, img_mor, type='rect')
                lightsignal = np.append(lightsignal,extraction(img_shape))
            return signalPro(lightsignal)
        else:
            return "no files"


def threshold(img,type = 0,*thd):#0: otsu, 1: manu, 2: adaptive
    img_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #转为灰度图
    if type == 1:
        img_thd = cv2.threshold(img_gray,thd,255,cv2.THRESH_BINARY)
    elif type == 2:
        img_thd = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
    else :
        ret, img_thd = cv2.threshold(img_gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    return img_thd

def morphologyEx(img,type):#形态学
    kernel = np.ones((5, 5), np.uint8)
    if type == 'open':
        img_mor = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    elif type == 'close':
        img_mor = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    elif type == 'close+open' or 'open+close':
        img_c = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
        img_mor = cv2.morphologyEx(img_c, cv2.MORPH_OPEN, kernel)
    return img_mor

def findLightShape(img_original,img,type = 'rect'):
    img_cont = img.copy()
    img_cont, contours, hier1 = cv2.findContours(img_cont, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    img_mask = np.zeros(img_cont.shape, np.uint8)
    area = np.zeros(len(contours))
    for i, cnt in enumerate(contours):
        area[i] = cv2.contourArea(cnt)
    maxcnt = np.max(area)
    maxindex = np.where(area == maxcnt)
    if type == 'rect':
        x, y, w, h = cv2.boundingRect(contours[maxindex[0][0]])
        img_mask = cv2.rectangle(img_mask, (x, y), (x + w, y + h), (255, 255, 255), -1)
    elif type == 'irregular':
        img_mask = cv2.drawContours(img_mask, contours, maxindex[0][0], (255, 255, 255), -1, hierarchy=hier1,maxLevel=2)
    img_roi = cv2.bitwise_and(img_original,img_original, mask=img_mask)
    img_roi_gray = cv2.cvtColor(img_roi, cv2.COLOR_BGR2GRAY)
    return img_roi_gray

def extraction(img_shape, cal_type = 0):
    if img_shape.shape[0]>img_shape.shape[1]:
        axis = 0
    else: axis = 1
    rowsum = np.sum(img_shape, axis)
    pixel = img_shape
    pixel[pixel > 0] = 1
    pixelnum = np.sum(pixel, axis)
    rowsum = rowsum[rowsum > 0]
    pixelnum = pixelnum[pixelnum > 0]
    if cal_type == 0:
        lightsignal = rowsum.astype(float)
    elif cal_type ==1:
        lightsignal = rowsum / pixelnum
        lightsignal = lightsignal.astype(float)

    lightsignal = lightsignal[int(len(lightsignal) / 8):int(len(lightsignal) * 7 / 8)]
    lightsignal_odd = lightsignal[0:len(lightsignal):2]
    lightsignal_even = lightsignal[1:len(lightsignal):2]
    gain_odd = np.mean(lightsignal_odd)
    gain_even = np.mean(lightsignal_even)
    lightsignal[0:len(lightsignal):2] = lightsignal[0:len(lightsignal):2] / gain_odd
    lightsignal[1:len(lightsignal):2] = lightsignal[1:len(lightsignal):2] / gain_even
    xx = np.arange(1, len(lightsignal) + 1)
    p = np.polyfit(xx, lightsignal, 6)
    func = np.poly1d(p)
    lightsignal = lightsignal / func(xx)
    return lightsignal
    
def signalPro(lightsignal):
    N = len(lightsignal)
    fs = 3024 * 34.97
    f, Pxx = signal.periodogram(lightsignal, fs, window=signal.get_window('blackman', N), nfft=N)
    amp = 20 * np.log10(np.clip(np.abs(Pxx), 1e-20, 1e100))
    sav = signal.savgol_filter(amp, 5, 2)
    sav_n = sav[100:len(sav) - 200]

    maxF = f[np.where(sav_n == np.max(sav_n))[0][0] + 100]
    return maxF
    
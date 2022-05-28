import wx
import cv2 as cv
import pygame

class AVIShowPanel(wx.Panel):
    def __init__(self,parent,size):
        super(AVIShowPanel, self).__init__(parent,size=size)
        self.capture = None
        self.bmp = None
        self.fps = 8
        self.counter = 0
        self.capture = cv.VideoCapture("D:\\WorkSpace\\Solidworks\\N.2SA\\bak3\\SurfaceXSLDPRT.avi")
        # self.capture = cv.VideoCapture("chendulingvideo.mp4")
        self.width = self.capture.get(3)
        self.height = self.capture.get(4)
        self.fpstimer = wx.Timer(self)
        # self.fpstimer.Start(1000/self.fps)
        self.Bind(wx.EVT_TIMER,self.onNextFrame,self.fpstimer)

    def updateVideo(self):
        self.Freeze()
        state,frame = self.capture.read()
        if state:
            frame = cv.cvtColor(frame,cv.COLOR_BGR2RGB)
            x,y = self.GetClientSize()
            bmp = wx.Image(self.width,self.height,frame).Scale(width=x,height=y,
                                                               quality=wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
            self.bmp = wx.StaticBitmap(self,-1,bmp)
            self.Refresh()
            self.Layout()
        else:
            self.capture.set(cv.CAP_PROP_POS_FRAMES,0)
        self.Thaw()

    def onNextFrame(self, evt):
        self.updateVideo()

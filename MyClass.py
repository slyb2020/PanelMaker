#!/usr/bin/env python
# encoding: utf-8
"""
@author: slyb
@license: (C) Copyright 2017-2020, 天津定智科技有限公司.
@contact: slyb@tju.edu.cn
@file: MyClass.py.py
@time: 2019/6/16 14:05
@desc:
"""
# from OrderInfoEditDialog import *
# from ScheduleDemoDialog import *
import wx.adv
import wx.lib.agw.aquabutton as AB
import wx.lib.agw.flatmenu as FM
import wx.lib.agw.foldpanelbar as fpb
import wx.lib.agw.pybusyinfo as PBI
from six import BytesIO
# from AVIShow import AVIShowPanel
from wx.adv import AnimationCtrl
from wx.lib.agw.artmanager import ArtManager, DCSaver
from wx.lib.agw.fmresources import ControlFocus, ControlPressed

from DBOperation import GetWallIDList, GetWallStructureByWallID, GetSurfaceXParameterByTypeID, \
    GetSurfaceYParameterByTypeID,GetRockWoolParameterByTypeID,GetReinforcementParameterByTypeID,InsertWallInfoToDB,\
    InsertSurfaceXInfoToDB,InsertSurfaceYInfoToDB,InsertRockWoolInfoToDB
from ExcelOperation import ModifySurfaceXConfigurationExcelFile,ModifySurfaceYConfigurationExcelFile,\
    ModifyRockWoolConfigurationExcelFile,ModifyReinforcementConfigurationExcelFile
from ID_DEFINE import *
from MyLog import MyLogCtrl
from Wizard import *


# dirName = os.path.dirname(os.path.abspath(__file__))
# bitmapDir = os.path.join(dirName, 'bitmaps\\')
# sys.path.append(os.path.split(dirName)[0])


def switchRGBtoBGR(colour):
    return wx.Colour(colour.Blue(), colour.Green(), colour.Red())


def CreateBackgroundBitmap():
    mem_dc = wx.MemoryDC()
    bmp = wx.Bitmap(200, 300)
    mem_dc.SelectObject(bmp)
    mem_dc.Clear()
    # colour the menu face with background colour
    top = wx.Colour("blue")
    bottom = wx.Colour("light blue")
    filRect = wx.Rect(0, 0, 200, 300)
    mem_dc.GradientFillConcentric(filRect, top, bottom, wx.Point(100, 150))
    mem_dc.SelectObject(wx.NullBitmap)
    return bmp


class FM_MyRenderer(FM.FMRenderer):
    def __init__(self):
        FM.FMRenderer.__init__(self)

    def DrawMenuButton(self, dc, rect, state):
        self.DrawButton(dc, rect, state)

    def DrawMenuBarButton(self, dc, rect, state):
        self.DrawButton(dc, rect, state)

    def DrawButton(self, dc, rect, state, colour=None):
        if state == ControlFocus:
            penColour = switchRGBtoBGR(ArtManager.Get().FrameColour())
            brushColour = switchRGBtoBGR(ArtManager.Get().BackgroundColour())
        elif state == ControlPressed:
            penColour = switchRGBtoBGR(ArtManager.Get().FrameColour())
            brushColour = switchRGBtoBGR(ArtManager.Get().HighlightBackgroundColour())
        else:  # ControlNormal, ControlDisabled, default
            penColour = switchRGBtoBGR(ArtManager.Get().FrameColour())
            brushColour = switchRGBtoBGR(ArtManager.Get().BackgroundColour())
        dc.SetPen(wx.Pen(penColour))
        dc.SetBrush(wx.Brush(brushColour))
        dc.DrawRoundedRectangle(rect.x, rect.y, rect.width, rect.height, 4)

    def DrawMenuBarBackground(self, dc, rect):
        vertical = ArtManager.Get().GetMBVerticalGradient()
        dcsaver = DCSaver(dc)
        # fill with gradient
        startColour = self.menuBarFaceColour
        endColour = ArtManager.Get().LightColour(startColour, 90)
        dc.SetPen(wx.Pen(endColour))
        dc.SetBrush(wx.Brush(endColour))
        dc.DrawRectangle(rect)

    def DrawToolBarBg(self, dc, rect):
        if not ArtManager.Get().GetRaiseToolbar():
            return
        # fill with gradient
        startColour = self.menuBarFaceColour()
        dc.SetPen(wx.Pen(startColour))
        dc.SetBrush(wx.Brush(startColour))
        dc.DrawRectangle(0, 0, rect.GetWidth(), rect.GetHeight())


ArtIDs = ["None",
          "wx.ART_ADD_BOOKMARK",
          "wx.ART_DEL_BOOKMARK",
          "wx.ART_HELP_SIDE_PANEL",
          "wx.ART_HELP_SETTINGS",
          "wx.ART_HELP_BOOK",
          "wx.ART_HELP_FOLDER",
          "wx.ART_HELP_PAGE",
          "wx.ART_GO_BACK",
          "wx.ART_GO_FORWARD",
          "wx.ART_GO_UP",
          "wx.ART_GO_DOWN",
          "wx.ART_GO_TO_PARENT",
          "wx.ART_GO_HOME",
          "wx.ART_FILE_OPEN",
          "wx.ART_PRINT",
          "wx.ART_HELP",
          "wx.ART_TIP",
          "wx.ART_REPORT_VIEW",
          "wx.ART_LIST_VIEW",
          "wx.ART_NEW_DIR",
          "wx.ART_HARDDISK",
          "wx.ART_FLOPPY",
          "wx.ART_CDROM",
          "wx.ART_REMOVABLE",
          "wx.ART_FOLDER",
          "wx.ART_FOLDER_OPEN",
          "wx.ART_GO_DIR_UP",
          "wx.ART_EXECUTABLE_FILE",
          "wx.ART_NORMAL_FILE",
          "wx.ART_TICK_MARK",
          "wx.ART_CROSS_MARK",
          "wx.ART_ERROR",
          "wx.ART_QUESTION",
          "wx.ART_WARNING",
          "wx.ART_INFORMATION",
          "wx.ART_MISSING_IMAGE",
          "SmileBitmap"
          ]


##########################################################################
def GetCollapsedIconData():
    return \
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\
\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\
\x00\x01\x8eIDAT8\x8d\xa5\x93-n\xe4@\x10\x85?g\x03\n6lh)\xc4\xd2\x12\xc3\x81\
\xd6\xa2I\x90\x154\xb9\x81\x8f1G\xc8\x11\x16\x86\xcd\xa0\x99F\xb3A\x91\xa1\
\xc9J&\x96L"5lX\xcc\x0bl\xf7v\xb2\x7fZ\xa5\x98\xebU\xbdz\xf5\\\x9deW\x9f\xf8\
H\\\xbfO|{y\x9dT\x15P\x04\x01\x01UPUD\x84\xdb/7YZ\x9f\xa5\n\xce\x97aRU\x8a\
\xdc`\xacA\x00\x04P\xf0!0\xf6\x81\xa0\xf0p\xff9\xfb\x85\xe0|\x19&T)K\x8b\x18\
\xf9\xa3\xe4\xbe\xf3\x8c^#\xc9\xd5\n\xa8*\xc5?\x9a\x01\x8a\xd2b\r\x1cN\xc3\
\x14\t\xce\x97a\xb2F0Ks\xd58\xaa\xc6\xc5\xa6\xf7\xdfya\xe7\xbdR\x13M2\xf9\
\xf9qKQ\x1fi\xf6-\x00~T\xfac\x1dq#\x82,\xe5q\x05\x91D\xba@\xefj\xba1\xf0\xdc\
zzW\xcff&\xb8,\x89\xa8@Q\xd6\xaaf\xdfRm,\xee\xb1BDxr#\xae\xf5|\xddo\xd6\xe2H\
\x18\x15\x84\xa0q@]\xe54\x8d\xa3\xedf\x05M\xe3\xd8Uy\xc4\x15\x8d\xf5\xd7\x8b\
~\x82\x0fh\x0e"\xb0\xad,\xee\xb8c\xbb\x18\xe7\x8e;6\xa5\x89\x04\xde\xff\x1c\
\x16\xef\xe0p\xfa>\x19\x11\xca\x8d\x8d\xe0\x93\x1b\x01\xd8m\xf3(;x\xa5\xef=\
\xb7w\xf3\x1d$\x7f\xc1\xe0\xbd\xa7\xeb\xa0(,"Kc\x12\xc1+\xfd\xe8\tI\xee\xed)\
\xbf\xbcN\xc1{D\x04k\x05#\x12\xfd\xf2a\xde[\x81\x87\xbb\xdf\x9cr\x1a\x87\xd3\
0)\xba>\x83\xd5\xb97o\xe0\xaf\x04\xff\x13?\x00\xd2\xfb\xa9`z\xac\x80w\x00\
\x00\x00\x00IEND\xaeB`\x82'


def GetCollapsedIconBitmap():
    return wx.Bitmap(GetCollapsedIconImage())


def GetCollapsedIconImage():
    stream = BytesIO(GetCollapsedIconData())
    return wx.Image(stream)


# ----------------------------------------------------------------------
def GetExpandedIconData():
    return \
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x10\x00\x00\x00\x10\x08\x06\
\x00\x00\x00\x1f\xf3\xffa\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\
\x00\x01\x9fIDAT8\x8d\x95\x93\xa1\x8e\xdc0\x14EO\xb2\xc4\xd0\xd2\x12\xb7(mI\
\xa4%V\xd1lQT4[4-\x9a\xfe\xc1\xc2|\xc6\xc2~BY\x83:A3E\xd3\xa0*\xa4\xd2\x90H!\
\x95\x0c\r\r\x1fK\x81g\xb2\x99\x84\xb4\x0fY\xd6\xbb\xc7\xf7>=\'Iz\xc3\xbcv\
\xfbn\xb8\x9c\x15 \xe7\xf3\xc7\x0fw\xc9\xbc7\x99\x03\x0e\xfbn0\x99F+\x85R\
\x80RH\x10\x82\x08\xde\x05\x1ef\x90+\xc0\xe1\xd8\ryn\xd0Z-\\A\xb4\xd2\xf7\
\x9e\xfbwoF\xc8\x088\x1c\xbbae\xb3\xe8y&\x9a\xdf\xf5\xbd\xe7\xfem\x84\xa4\
\x97\xccYf\x16\x8d\xdb\xb2a]\xfeX\x18\xc9s\xc3\xe1\x18\xe7\x94\x12cb\xcc\xb5\
\xfa\xb1l8\xf5\x01\xe7\x84\xc7\xb2Y@\xb2\xcc0\x02\xb4\x9a\x88%\xbe\xdc\xb4\
\x9e\xb6Zs\xaa74\xadg[6\x88<\xb7]\xc6\x14\x1dL\x86\xe6\x83\xa0\x81\xba\xda\
\x10\x02x/\xd4\xd5\x06\r\x840!\x9c\x1fM\x92\xf4\x86\x9f\xbf\xfe\x0c\xd6\x9ae\
\xd6u\x8d \xf4\xf5\x165\x9b\x8f\x04\xe1\xc5\xcb\xdb$\x05\x90\xa97@\x04lQas\
\xcd*7\x14\xdb\x9aY\xcb\xb8\\\xe9E\x10|\xbc\xf2^\xb0E\x85\xc95_\x9f\n\xaa/\
\x05\x10\x81\xce\xc9\xa8\xf6><G\xd8\xed\xbbA)X\xd9\x0c\x01\x9a\xc6Q\x14\xd9h\
[\x04\xda\xd6c\xadFkE\xf0\xc2\xab\xd7\xb7\xc9\x08\x00\xf8\xf6\xbd\x1b\x8cQ\
\xd8|\xb9\x0f\xd3\x9a\x8a\xc7\x08\x00\x9f?\xdd%\xde\x07\xda\x93\xc3{\x19C\
\x8a\x9c\x03\x0b8\x17\xe8\x9d\xbf\x02.>\x13\xc0n\xff{PJ\xc5\xfdP\x11""<\xbc\
\xff\x87\xdf\xf8\xbf\xf5\x17FF\xaf\x8f\x8b\xd3\xe6K\x00\x00\x00\x00IEND\xaeB\
`\x82'


def GetExpandedIconBitmap():
    return wx.Bitmap(GetExpandedIconImage())


def GetExpandedIconImage():
    stream = BytesIO(GetExpandedIconData())
    return wx.Image(stream)


# ----------------------------------------------------------------------
def GetMondrianData():
    return \
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00 \x00\x00\x00 \x08\x06\x00\
\x00\x00szz\xf4\x00\x00\x00\x04sBIT\x08\x08\x08\x08|\x08d\x88\x00\x00\x00qID\
ATX\x85\xed\xd6;\n\x800\x10E\xd1{\xc5\x8d\xb9r\x97\x16\x0b\xad$\x8a\x82:\x16\
o\xda\x84pB2\x1f\x81Fa\x8c\x9c\x08\x04Z{\xcf\xa72\xbcv\xfa\xc5\x08 \x80r\x80\
\xfc\xa2\x0e\x1c\xe4\xba\xfaX\x1d\xd0\xde]S\x07\x02\xd8>\xe1wa-`\x9fQ\xe9\
\x86\x01\x04\x10\x00\\(Dk\x1b-\x04\xdc\x1d\x07\x14\x98;\x0bS\x7f\x7f\xf9\x13\
\x04\x10@\xf9X\xbe\x00\xc9 \x14K\xc1<={\x00\x00\x00\x00IEND\xaeB`\x82'


def GetMondrianBitmap():
    return wx.Bitmap(GetMondrianImage())


def GetMondrianImage():
    stream = BytesIO(GetMondrianData())
    return wx.Image(stream)


def GetMondrianIcon():
    icon = wx.Icon()
    icon.CopyFromBitmap(GetMondrianBitmap())
    return icon


class MainPanel(wx.Panel):
    def __init__(self, parent, id=wx.ID_ANY, title="", pos=wx.DefaultPosition,
                 size=(1024, 768), style=wx.TAB_TRAVERSAL):
        wx.Panel.__init__(self, parent, id, pos, size, style)
        self.parent = parent

        il = wx.ImageList(16, 16)
        self.idx1 = il.Add(images._rt_smiley.GetBitmap())
        self.idx2 = il.Add(images.GridBG.GetBitmap())
        self.idx3 = il.Add(images.Smiles.GetBitmap())
        self.idx4 = il.Add(images._rt_undo.GetBitmap())
        self.idx5 = il.Add(images._rt_save.GetBitmap())
        self.idx6 = il.Add(images._rt_redo.GetBitmap())

        self._leftWindow1 = wx.adv.SashLayoutWindow(self, ID_WINDOW_LEFT, wx.DefaultPosition,
                                                    wx.Size(200, 1000), wx.NO_BORDER |
                                                    wx.adv.SW_3D | wx.CLIP_CHILDREN)
        self._leftWindow1.SetDefaultSize(wx.Size(220, 1000))
        self._leftWindow1.SetOrientation(wx.adv.LAYOUT_VERTICAL)
        self._leftWindow1.SetAlignment(wx.adv.LAYOUT_LEFT)
        self._leftWindow1.SetSashVisible(wx.adv.SASH_RIGHT, True)
        self._leftWindow1.SetExtraBorderSize(10)
        self._pnl = 0
        # will occupy the space not used by the Layout Algorithm
        self.CreateBottomWindow()
        self.log = MyLogCtrl(self.bottomWindow, -1, "")
        self.work_zone_Panel = WorkZonePanel(self, self, self.log)
        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.ReCreateFoldPanel(0)
        self.Bind(wx.adv.EVT_SASH_DRAGGED_RANGE, self.OnSashDrag, id=ID_WINDOW_LEFT,
                  id2=ID_WINDOW_BOTTOM)  # BOTTOM和LEFT顺序不能换，要想更改哪个先分，只需更改上面窗口定义的顺序

    def CreateBottomWindow(self):
        self.bottomWindow = wx.adv.SashLayoutWindow(self, ID_WINDOW_BOTTOM, style=wx.NO_BORDER | wx.adv.SW_3D)
        self.bottomWindow.SetDefaultSize((1000, 200))
        self.bottomWindow.SetOrientation(wx.adv.LAYOUT_HORIZONTAL)
        self.bottomWindow.SetAlignment(wx.adv.LAYOUT_BOTTOM)
        # win.SetBackgroundColour(wx.Colour(0, 0, 255))
        self.bottomWindow.SetSashVisible(wx.adv.SASH_TOP, True)
        self.bottomWindow.SetExtraBorderSize(5)

    def OnSize(self, event):
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.work_zone_Panel)
        event.Skip()

    def OnSashDrag(self, event):
        if event.GetDragStatus() == wx.adv.SASH_STATUS_OUT_OF_RANGE:
            return
        eID = event.GetId()
        if eID == ID_WINDOW_LEFT:
            self._leftWindow1.SetDefaultSize((event.GetDragRect().width, 1000))
        elif eID == ID_WINDOW_BOTTOM:
            self.bottomWindow.SetDefaultSize((1000, event.GetDragRect().height))
        wx.adv.LayoutAlgorithm().LayoutWindow(self, self.work_zone_Panel)
        self.work_zone_Panel.Refresh()

    def ReCreateFoldPanel(self, fpb_flags, state=0):
        # delete earlier panel
        self._leftWindow1.DestroyChildren()
        self._pnl = fpb.FoldPanelBar(self._leftWindow1, -1, wx.DefaultPosition,
                                     wx.Size(-1, -1), agwStyle=fpb_flags)
        Images = wx.ImageList(16, 16)
        Images.Add(GetExpandedIconBitmap())
        Images.Add(GetCollapsedIconBitmap())

        item = self._pnl.AddFoldPanel("工具面板", collapsed=False,
                                      foldIcons=Images)
        panel = wx.Panel(item, -1, size=(300, 300))
        bitmap = wx.Bitmap("bitmaps/aquabutton.png",
                           wx.BITMAP_TYPE_PNG)
        self.managementWallPanelBTN = AB.AquaButton(panel, wx.ID_ANY, bitmap, "墙板图纸管理", size=(100, 50))
        self.managementWallPanelBTN.Bind(wx.EVT_BUTTON, self.OnNewWallPanelBTN)
        self.managementWallPanelBTN.SetForegroundColour(wx.BLACK)
        self.managementWallPanelBTN.Enable(True)
        self.managementCeilingPanelBTN = AB.AquaButton(panel, wx.ID_ANY, bitmap, "天花板图纸管理", size=(100, 50))
        self.managementCeilingPanelBTN.SetForegroundColour(wx.BLACK)
        self.managementConstructionBTN = AB.AquaButton(panel, wx.ID_ANY, bitmap, "构件图纸管理", size=(100, 50))
        self.managementConstructionBTN.SetForegroundColour(wx.BLACK)
        self.managementRepireDoorBTN = AB.AquaButton(panel, wx.ID_ANY, bitmap, "检修门图纸管理", size=(100, 50))
        self.managementRepireDoorBTN.SetForegroundColour(wx.BLACK)
        self.managementRepireHoleBTN = AB.AquaButton(panel, wx.ID_ANY, bitmap, "检修孔墙板图纸管理", size=(100, 50))
        self.managementRepireHoleBTN.SetForegroundColour(wx.BLACK)
        static = wx.StaticLine(panel, -1)
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add(self.managementWallPanelBTN, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
        vbox.Add(self.managementCeilingPanelBTN, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
        vbox.Add(self.managementConstructionBTN, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
        vbox.Add(self.managementRepireDoorBTN, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
        vbox.Add(self.managementRepireHoleBTN, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
        vbox.Add(static, 0, wx.EXPAND | wx.TOP | wx.BOTTOM, 5)
        panel.SetSizer(vbox)
        self._pnl.AddFoldPanelWindow(item, panel, fpb.FPB_ALIGN_WIDTH, 5, 0)
        self._leftWindow1.SizeWindows()

    def OnNewWallPanelBTN(self,event):
        self.work_zone_Panel.notebook.SetSelection(0)




class WorkZonePanel(wx.Panel):
    def __init__(self, parent, master, log):
        wx.Panel.__init__(self, parent, -1)
        self.master = master
        self.log = log
        self.notebook = wx.Notebook(self, -1, size=(21, 21), style=
                                    wx.BK_DEFAULT
                                    # wx.BK_TOP
                                    # wx.BK_BOTTOM
                                    # wx.BK_LEFT
                                    # wx.BK_RIGHT
                                    # | wx.NB_MULTILINE
                                    )
        il = wx.ImageList(16, 16)
        idx1 = il.Add(images._rt_smiley.GetBitmap())
        self.total_page_num = 0
        self.notebook.AssignImageList(il)
        idx2 = il.Add(images.GridBG.GetBitmap())
        idx3 = il.Add(images.Smiles.GetBitmap())
        idx4 = il.Add(images._rt_undo.GetBitmap())
        idx5 = il.Add(images._rt_save.GetBitmap())
        idx6 = il.Add(images._rt_redo.GetBitmap())
        self.wallManagementPanel=WallManagementPanel(self.notebook, log)
        self.notebook.AddPage(self.wallManagementPanel, "墙板图纸管理")
        self.ceilingManagementPanel=wx.Panel(self.notebook)
        self.notebook.AddPage(self.ceilingManagementPanel, "天花板图纸管理")
        hbox = wx.BoxSizer()
        hbox.Add(self.notebook, 1, wx.EXPAND)
        self.SetSizer(hbox)


class WallManagementPanel(wx.Panel):
    def __init__(self,parent,log):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.log=log
        self.wallType=""      #查看墙板时用的
        self.wallID=""        #查看墙板是用的
        self.newWallType = "" #新建墙板时用的
        self.newWallID = ""   #新建墙板时用的

        hbox = wx.BoxSizer()
        self.controlPanel = wx.Panel(self,size=(320,-1),style=wx.SUNKEN_BORDER)
        hbox.Add(self.controlPanel,0,wx.EXPAND)
        self.SetSizer(hbox)
        self.controlPanel.SetAutoLayout(1)
        self.CreateControlPanel()

    def CreateControlPanel(self):
        vbox = wx.BoxSizer(wx.VERTICAL)
        vbox.Add((-1, 10))
        hhbox = wx.BoxSizer()
        hhbox.Add((10,-1))
        hhbox.Add(wx.StaticText(self.controlPanel,label="墙板类型: "),0,wx.TOP,5)
        choices = ["2SA","2SG","2SG","2SG","2SG"]
        self.wallTypeCOMBO = wx.ComboBox(self.controlPanel, value=self.wallType, choices=choices,size=(60,25))
        self.wallTypeCOMBO.Bind(wx.EVT_COMBOBOX, self.OnWallTypeChanged)
        hhbox.Add(self.wallTypeCOMBO,0)
        hhbox.Add((10,-1))
        hhbox.Add(wx.StaticText(self.controlPanel,label="墙板型号: "),0,wx.TOP,5)
        self.wallIDCOMBO = wx.ComboBox(self.controlPanel, size=(80,25))
        self.wallIDCOMBO.Bind(wx.EVT_COMBOBOX, self.OnWallIDChanged)
        hhbox.Add(self.wallIDCOMBO,1,wx.RIGHT,10)
        vbox.Add(hhbox,0,wx.EXPAND)
        vbox.Add((-1,10))
        self.notebook = wx.Notebook(self.controlPanel, -1, size=(21, 21), style=
                                    # wx.BK_DEFAULT
                                    # wx.BK_TOP
                                    wx.BK_BOTTOM
                                    # wx.BK_LEFT
                                    # wx.BK_RIGHT
                                    | wx.NB_MULTILINE
                                    )
        il = wx.ImageList(16, 16)
        idx1 = il.Add(images._rt_smiley.GetBitmap())
        self.total_page_num = 0
        self.notebook.AssignImageList(il)
        idx2 = il.Add(images.GridBG.GetBitmap())
        idx3 = il.Add(images.Smiles.GetBitmap())
        idx4 = il.Add(images._rt_undo.GetBitmap())
        idx5 = il.Add(images._rt_save.GetBitmap())
        idx6 = il.Add(images._rt_redo.GetBitmap())
        vbox.Add(self.notebook,1,wx.EXPAND)
        self.createNewBTN=wx.Button(self.controlPanel,label="创建新墙板",size=(10,35))
        self.createNewBTN.Bind(wx.EVT_BUTTON,self.OnCreateNewBTN)
        vbox.Add(self.createNewBTN,0,wx.EXPAND)
        self.controlPanel.SetSizer(vbox)
        self.controlPanel.SetAutoLayout(1)
        # self.ReCreateFeaturePanel()

    def OnCreateNewBTN(self,event):
        wizard = wiz(self, -1, "新墙板创建向导", images.WizTest1.GetBitmap())
        self.page = []
        self.pageWall = WallParameterPage(wizard, self, self.log, "Page 1 墙板参数")
        self.pageX = SurfaceXParameterPage(wizard, self, self.log, "Page 2 X 面参数")
        self.pageY = SurfaceYParameterPage(wizard, self, self.log, "Page 3 Y 面参数")
        self.pageRockWool = RockWoolParameterPage(wizard, self, self.log, "Page 4 岩棉参数")
        self.page.append(self.pageWall)
        self.page.append(self.pageX)
        self.page.append(self.pageY)
        self.page.append(self.pageRockWool)
        self.pageConstruction = TitledPage(wizard, "Page 5 构件参数")
        self.pageReinforcement = ReinforcementParameterPage(wizard, self, self.log, "Page 6 加强板参数")
        # self.page1 = page1

        wizard.FitToPage(self.page[0])
        # self.page6.sizer.Add(wx.StaticText(self.page6, -1, "\nThis is the last page."))

        # Set the initial order of the pages
        self.page[0].SetNext(self.page[1])
        self.page[1].SetPrev(self.page[0])
        self.page[1].SetNext(self.page[2])
        self.page[2].SetPrev(self.page[1])
        self.page[2].SetNext(self.page[3])
        self.page[3].SetPrev(self.page[2])

        wizard.GetPageAreaSizer().Add(self.page[0])
        if wizard.RunWizard(self.page[0]):
            InsertWallInfoToDB(self.log,WHICHDB,self.page[0])
            InsertSurfaceXInfoToDB(self.log,WHICHDB,self.page[1])
            InsertSurfaceYInfoToDB(self.log,WHICHDB,self.page[2])
            InsertRockWoolInfoToDB(self.log,WHICHDB,self.page[3])
            wx.MessageBox("墙板图纸已按照您输入的参数成功生成，请打开SolidWorks软件进行查看！", "信息提示")
        else:
            wx.MessageBox("墙板图纸因被操作员取消而没有被成功生成！", "信息提示")

    def OnWallTypeChanged(self,event):
        if self.wallType!=self.wallTypeCOMBO.GetValue():
            self.wallType=self.wallTypeCOMBO.GetValue()
            _,idList = GetWallIDList(self.log, WHICHDB, self.wallType)
            self.wallIDCOMBO.SetItems(idList)

    def OnWallIDChanged(self,event):
        if self.wallID!=self.wallIDCOMBO.GetValue():
            self.RefreshNotebook()

    def RefreshNotebook(self):
        self.wallID = self.wallIDCOMBO.GetValue()
        _,self.wallStructureList = GetWallStructureByWallID(self.log,WHICHDB,self.wallID)
        self.notebook.DeleteAllPages()
        if self.wallStructureList[0]!="":
            self.surfaceXPage=SurfaceXParameterShowPanel(self.notebook,self.log,self.wallStructureList[0])
            self.notebook.AddPage(self.surfaceXPage, "X面参数")
        if self.wallStructureList[1]!="":
            self.surfaceYPage=SurfaceYParameterShowPanel(self.notebook,self.log,self.wallStructureList[1])
            self.notebook.AddPage(self.surfaceYPage, "Y面参数")
        if self.wallStructureList[2]!="":
            self.surfaceZPage=wx.Panel(self.notebook)
            self.notebook.AddPage(self.surfaceZPage, "Z面参数")
        if self.wallStructureList[3]!="":
            self.surfaceVPage=wx.Panel(self.notebook)
            self.notebook.AddPage(self.surfaceVPage, "V面参数")
        if len(self.wallStructureList[4])>0:
            self.constructionPage=wx.Panel(self.notebook)
            self.notebook.AddPage(self.constructionPage, "构件参数")
        if self.wallStructureList[5]!="":
            self.rockWoolPage=RockWoolParameterShowPanel(self.notebook,self.log,self.wallStructureList[1])
            self.notebook.AddPage(self.rockWoolPage, "岩棉参数")
        if self.wallStructureList[6]!="":
            self.reinforcementBoardPage=wx.Panel(self.notebook)
            self.notebook.AddPage(self.reinforcementBoardPage, "加强板参数")

class WallParameterPage(TitledPage):
    def __init__(self,parent,master,log,title):
        super(WallParameterPage, self).__init__(parent,title)
        self.parent = parent
        self.master = master
        self.log = log
        self.wallType = ""
        self.wallID = 1
        self.surfaceXEnable = True
        self.surfaceYEnable = True
        self.surfaceZEnable = False
        self.surfaceVEnable = False
        self.rockWoolEnable = True
        self.constuctionEnable = False
        self.reinforcementEnable = False

        hbox = wx.BoxSizer()
        self.animationPanel = wx.Panel(self, size=(300, 400))
        hbox.Add(self.animationPanel,0,wx.EXPAND)
        vvbox = wx.BoxSizer(wx.VERTICAL)
        hhbox = wx.BoxSizer()
        hhbox.Add((30,-1))

        hhbox.Add(wx.StaticText(self,label="请输入新建墙板的类型及型号：A."),0,wx.TOP,5)
        self.wallTypeCOMBO = wx.ComboBox(self, choices=["2SA",'2SG','2SF'], size=(80,25))
        self.wallTypeCOMBO.Bind(wx.EVT_COMBOBOX,self.OnWallTypeChanged)
        hhbox.Add(self.wallTypeCOMBO, 0)
        hhbox.Add(wx.StaticText(self,label='.'),0,wx.TOP,5)
        self.wallIdTXT = wx.SpinCtrl(self,size=(100,-1),min=0,max=9999)
        hhbox.Add(self.wallIdTXT,0,wx.EXPAND)
        vvbox.Add((-1,10))
        vvbox.Add(hhbox,0,wx.EXPAND)
        self.panel = wx.Panel(self,size=(350,235))
        vvbox.Add(self.panel,1,wx.EXPAND)
        hbox.Add(vvbox,1,wx.EXPAND)
        self.sizer.Add(hbox,0,wx.EXPAND)
        self.SetSizer(self.sizer)
        self.panel.SetAutoLayout(1)
        self.SetAutoLayout(1)
        self.Bind(wx.adv.EVT_WIZARD_PAGE_SHOWN,self.OnShowUp)
        self.Bind(wx.adv.EVT_WIZARD_BEFORE_PAGE_CHANGED,self.OnBeforeChanged)
        self.Bind(wx.EVT_CHECKBOX, self.OnCheckBox)
        self.ReCreate()

    def OnBeforeChanged(self,event):
        self.wallType=self.wallTypeCOMBO.GetValue()
        self.wallID=self.wallIdTXT.GetValue()
        if self.wallType=="":
            wx.MessageBox("请选择墙板类型", "提示信息")
            self.wallTypeCOMBO.SetBackgroundColour(wx.Colour(240,123,123))
            self.wallTypeCOMBO.Refresh()
            event.Veto()
        else:
            self.constuctionEnable = self.constuctionEnableCHK.GetValue()
            self.reinforcementEnable = self.reinforcementEnableCHK.GetValue()
            self.wallTypeCOMBO.SetBackgroundColour(wx.WHITE)
            self.master.page=[self.master.pageWall,self.master.pageX,self.master.pageY,self.master.pageRockWool]
            if self.constuctionEnable:
                self.master.page.append(self.master.pageConstruction)
            if self.reinforcementEnable:
                self.master.page.append(self.master.pageReinforcement)
            self.master.page[0].SetNext(self.master.page[1])
            for i in range(1,len(self.master.page)-1):
                self.master.page[i].SetPrev(self.master.page[i-1])
                self.master.page[i].SetNext(self.master.page[i+1])
            self.master.page[-1].SetPrev(self.master.page[-2])

    def OnShowUp(self,event):
        try:
            self.animationCtrl.SetBackgroundColour(self.GetBackgroundColour())
            self.animationCtrl.Play()
        except:
            pass
        event.Skip()

    def ReCreate(self):
        self.panel.Freeze()
        self.panel.DestroyChildren()
        if self.wallType!="":
            vbox=wx.BoxSizer(wx.VERTICAL)
            vbox.Add((-1,30))
            self.surfaceXEnableCHK = wx.CheckBox(self.panel,label="X面",size=(80,-1),name="X面")
            self.surfaceXEnableCHK.SetValue(self.surfaceXEnable)
            vbox.Add(self.surfaceXEnableCHK,0,wx.LEFT,30)
            vbox.Add((-1,20))
            self.surfaceYEnableCHK = wx.CheckBox(self.panel,label="Y面",size=(80,-1),name="Y面")
            self.surfaceYEnableCHK.SetValue(self.surfaceYEnable)
            vbox.Add(self.surfaceYEnableCHK,0,wx.LEFT,30)
            vbox.Add((-1,20))
            self.surfaceZEnableCHK = wx.CheckBox(self.panel,label="Z面",size=(80,-1),name="Z面")
            self.surfaceZEnableCHK.SetValue(self.surfaceZEnable)
            vbox.Add(self.surfaceZEnableCHK,0,wx.LEFT,30)
            vbox.Add((-1,20))
            self.surfaceVEnableCHK = wx.CheckBox(self.panel,label="V面",size=(80,-1),name="V面")
            self.surfaceVEnableCHK.SetValue(self.surfaceVEnable)
            vbox.Add(self.surfaceVEnableCHK,0,wx.LEFT,30)
            vbox.Add((-1,20))
            self.rockWoolEnableCHK = wx.CheckBox(self.panel,label="岩棉",size=(80,-1),name="岩棉")
            self.rockWoolEnableCHK.SetValue(self.rockWoolEnable)
            vbox.Add(self.rockWoolEnableCHK,0,wx.LEFT,30)
            vbox.Add((-1,20))
            self.constuctionEnableCHK = wx.CheckBox(self.panel,label="构件",size=(80,-1),name="构件")
            self.constuctionEnableCHK.SetValue(self.constuctionEnable)
            vbox.Add(self.constuctionEnableCHK,0,wx.LEFT,30)
            vbox.Add((-1,20))
            self.reinforcementEnableCHK = wx.CheckBox(self.panel,label="加强板",size=(80,-1),name="加强板")
            self.reinforcementEnableCHK.SetValue(self.reinforcementEnable)
            vbox.Add(self.reinforcementEnableCHK,0,wx.LEFT,30)
            self.panel.SetSizer(vbox)
            self.panel.Layout()
        self.panel.Thaw()

    def OnWallIDChanged(self,event):
        _,existIDList=GetWallIDList(self.log,WHICHDB,self.wallType)
        self.wallID=self.wallIdTXT.GetValue()
        wallID = "A.%s.%04d"%(self.wallType,self.wallID)
        while wallID in existIDList:
            self.wallID+=1
            wallID = "A.%s.%04d"%(self.wallType,self.wallID)
        self.wallIdTXT.SetValue("%04d"%self.wallID)

    def OnWallTypeChanged(self,event):
        self.wallType=self.wallTypeCOMBO.GetValue()
        if self.wallType!="":
            _, existIDList = GetWallIDList(self.log, WHICHDB, self.wallType)
            wallID = "A.%s.%04d" % (self.wallType, self.wallID)
            while wallID in existIDList:
                self.wallID += 1
                wallID = "A.%s.%04d"%(self.wallType,self.wallID)
            self.wallIdTXT.SetValue("%04d" % self.wallID)
            self.wallIdTXT.Show(True)
            self.wallTypeCOMBO.SetBackgroundColour(wx.WHITE)
            try:
                self.animationCtrl.Destroy()
            except:
                pass
            self.animationCtrl = AnimationCtrl(self.animationPanel)
            ani = self.animationCtrl.CreateAnimation()
            ani.LoadFile(gifDir+"%s.gif"%self.wallType)
            self.animationCtrl.SetAnimation(ani)
            self.animationCtrl.SetBackgroundColour(self.GetBackgroundColour())
            self.animationCtrl.Play()
        self.ReCreate()
        self.Layout()

    def OnCheckBox(self,event):
        obj = event.GetEventObject()
        objName = obj.GetName()
        if objName in ["X面","Y面","岩棉"]:
            obj.SetValue(True)
        elif objName in ["Z面","V面"]:
            obj.SetValue(False)
        else:
            event.Skip()

class SurfaceXParameterPage(TitledPage):
    def __init__(self,parent, master, log, title):
        super(SurfaceXParameterPage, self).__init__(parent,title)
        self.parent = parent
        self.master = master
        self.baseFilename="SurfaceX"
        self.log = log
        self.wallType = self.master.pageWall.wallType
        self.wallID = self.master.pageWall.wallID
        self.leftBendEnable = False
        self.leftBendValue=7
        self.rightBendEnable = False
        self.rightBendValue=7
        self.bottomBendEnable=False
        self.bottomBendValue=0
        self.bottomBendCutEnable=False
        self.bottomBendCutValue = 0
        self.topBendEnable = False
        self.topBendValue = 0
        self.materialEnable = False
        self.material = ""
        self.colourEnable=False
        self.colour=""

        hbox = wx.BoxSizer()
        self.previewPanel = wx.Panel(self,size=(260,235))
        hbox.Add((10,-1))
        hbox.Add(self.previewPanel, 0, wx.EXPAND)
        hbox.Add((5,-1))

        vvbox=wx.BoxSizer(wx.VERTICAL)
        hhbox = wx.BoxSizer()
        hhbox.Add((10,-1))
        self.existLabel=wx.StaticText(self,label="基于现有模型建立：")
        hhbox.Add(self.existLabel,0,wx.TOP,17)
        self.existCOMOBO = wx.ComboBox(self,choices=[],size=(100,-1))
        self.existCOMOBO.Bind(wx.EVT_COMBOBOX,self.OnExistCOMBOChanged)
        hhbox.Add(self.existCOMOBO,0,wx.TOP,10)
        vvbox.Add(hhbox,0,wx.EXPAND)
        vvbox.Add((-1,10))
        vvbox.Add(wx.StaticLine(self,style=wx.HORIZONTAL), 0, wx.EXPAND)
        vvbox.Add((-1,10))
        self.panel = wx.Panel(self,size=(390,235))
        vvbox.Add(self.panel,1,wx.EXPAND)
        hbox.Add(vvbox,1,wx.EXPAND)
        self.sizer.Add(hbox,1,wx.EXPAND)
        self.SetSizer(self.sizer)
        self.panel.SetAutoLayout(1)
        self.Bind(wx.adv.EVT_WIZARD_PAGE_SHOWN,self.OnShowUp)
        self.Bind(wx.adv.EVT_WIZARD_BEFORE_PAGE_CHANGED,self.OnBeforeChanged)
        self.ReCreate()

    def OnBeforeChanged(self,event):
        self.wallType = self.master.pageWall.wallType
        self.wallID = self.master.pageWall.wallID
        self.leftBendValue=self.leftBendTXT.GetValue()
        self.rightBendValue=self.rightBendTXT.GetValue()
        self.topBendValue=self.topBendTXT.GetValue()
        self.bottomBendValue=self.bottomBendTXT.GetValue()
        self.bottomBendCutValue=self.bottomBendCutSPIN.GetValue()
        ModifySurfaceXConfigurationExcelFile(self.leftBendEnable,self.leftBendValue,self.rightBendEnable,self.rightBendValue,self.topBendEnable,self.topBendValue,self.bottomBendEnable,self.bottomBendValue,self.bottomBendCutEnable,self.bottomBendCutValue)
        # Part = swApp.OpenDoc6("D:\\WorkSpace\\Solidworks\\N.2SA\\SurfaceXSLDPRT.SLDPRT", 1, 0, "", longstatus, longwarnings)
        # swApp.ActivateDoc2("SurfaceXSLDPRT.SLDPRT", False, longstatus)
        # Part = swApp.ActiveDoc

    def GetPreviewPicName(self):
        num = 0
        num = num+1 if self.leftBendEnable else num
        num = num+10 if self.rightBendEnable else num
        num = num+100 if self.topBendEnable else num
        num = num+1000 if self.bottomBendEnable else num
        num = num+10000 if self.bottomBendCutEnable else num
        if num>11:
            num=11
        self.previewPicName = self.baseFilename+"%05d.png"%num

    def OnShowUp(self,event):
        _,choices = GetWallIDList(self.log, WHICHDB, self.master.page[0].wallType)
        self.existCOMOBO.SetItems(choices)
        self.ShowPreview()

    def ShowPreview(self):
        self.previewPanel.Freeze()
        self.GetPreviewPicName()
        try:
            self.statBmp.Destroy()
        except:
            pass
        x,y = self.previewPanel.GetClientSize()
        bmp = wx.Image(previewDir+self.previewPicName, wx.BITMAP_TYPE_PNG).Scale(width=x,height=y,quality=wx.IMAGE_QUALITY_HIGH).ConvertToBitmap()
        self.statBmp = wx.StaticBitmap(self.previewPanel, wx.ID_ANY, bmp)
        self.previewPanel.Refresh()
        self.previewPanel.Thaw()

    def ReCreate(self):
        try:
            self.leftBendValue = self.leftBendTXT.GetValue()
            self.rightBendValue = self.rightBendTXT.GetValue()
            self.topBendValue = self.topBendTXT.GetValue()
            self.bottomBendValue = self.bottomBendTXT.GetValue()
            self.bottomBendCutValue = self.bottomBendCutSPIN.GetValue()
        except:
            pass
        self.panel.Freeze()
        self.panel.DestroyChildren()
        vbox = wx.BoxSizer(wx.VERTICAL)

        hhbox=wx.BoxSizer()
        hhbox.Add((10, 1))
        self.leftBendEnableCHK = wx.CheckBox(self.panel,label="有左侧折弯",size=(120,-1))
        self.leftBendEnableCHK.Bind(wx.EVT_CHECKBOX,self.OnLeftBendEnableCHK)
        self.leftBendEnableCHK.SetValue(self.leftBendEnable)
        hhbox.Add(self.leftBendEnableCHK,0,wx.TOP,5)
        self.leftBendEnableCHK.Bind(wx.EVT_CHECKBOX,self.OnLeftBendEnableCHK)
        self.leftBendLabel=wx.StaticText(self.panel,label="X面左侧折弯量：",size=(100,-1))
        self.leftBendLabel.Show(self.leftBendEnable)
        hhbox.Add(self.leftBendLabel,0,wx.TOP,5)
        self.leftBendTXT = wx.SpinCtrl(self.panel,size=(100,-1),min=1,max=50)
        self.leftBendTXT.SetValue(self.leftBendValue)
        self.leftBendTXT.Show(self.leftBendEnable)
        hhbox.Add(self.leftBendTXT,1,wx.RIGHT,10)
        vbox.Add(hhbox, 0, wx.EXPAND)

        vbox.Add((-1,10))

        hhbox=wx.BoxSizer()
        hhbox.Add((10, 1))
        self.rightBendEnableCHK = wx.CheckBox(self.panel,label="有右侧折弯",size=(120,-1))
        self.rightBendEnableCHK.Bind(wx.EVT_CHECKBOX,self.OnRightBendEnableCHK)
        self.rightBendEnableCHK.SetValue(self.rightBendEnable)
        hhbox.Add(self.rightBendEnableCHK,0,wx.TOP,5)
        self.rightBendEnableCHK.Bind(wx.EVT_CHECKBOX,self.OnRightBendEnableCHK)
        self.rightBendLabel=wx.StaticText(self.panel,label="X面右侧折弯量：",size=(100,-1))
        self.rightBendLabel.Show(self.rightBendEnable)
        hhbox.Add(self.rightBendLabel,0,wx.TOP,5)
        self.rightBendTXT = wx.SpinCtrl(self.panel,size=(100,-1),min=1,max=50)
        self.rightBendTXT.SetValue(self.rightBendValue)
        self.rightBendTXT.Show(self.rightBendEnable)
        hhbox.Add(self.rightBendTXT,1,wx.RIGHT,10)
        vbox.Add(hhbox, 0, wx.EXPAND)

        vbox.Add((-1,10))

        hhbox = wx.BoxSizer()
        hhbox.Add((10,1))
        self.bottomBendEnableCHK = wx.CheckBox(self.panel,label="有底部折弯",size=(120,-1))
        self.bottomBendEnableCHK.Bind(wx.EVT_CHECKBOX,self.OnBottomBendEnableCHK)
        self.bottomBendEnableCHK.SetValue(self.bottomBendEnable)
        hhbox.Add(self.bottomBendEnableCHK,0,wx.TOP,5)
        self.bottomBendEnableCHK.Bind(wx.EVT_CHECKBOX,self.OnBottomBendEnableCHK)
        self.bottomBendLabel=wx.StaticText(self.panel,label="底部折弯量：",size=(100,-1))
        self.bottomBendLabel.Show(self.bottomBendEnable)
        hhbox.Add(self.bottomBendLabel,0,wx.TOP,5)
        self.bottomBendTXT = wx.SpinCtrl(self.panel,size=(100,-1),min=0,max=50)
        self.bottomBendTXT.SetValue(self.bottomBendValue)
        self.bottomBendTXT.Show(self.bottomBendEnable)
        hhbox.Add(self.bottomBendTXT,1,wx.RIGHT,10)
        vbox.Add(hhbox,0,wx.EXPAND)

        vbox.Add((-1,10))

        hhbox = wx.BoxSizer()
        hhbox.Add((10,1))
        self.bottomBendCutEnableCHK = wx.CheckBox(self.panel,label="有底部折弯裁切",size=(120,-1))
        self.bottomBendCutEnableCHK.SetValue(self.bottomBendCutEnable)
        self.bottomBendCutEnableCHK.Show(self.bottomBendEnable)
        hhbox.Add(self.bottomBendCutEnableCHK,0,wx.TOP,5)
        self.bottomBendCutEnableCHK.Bind(wx.EVT_CHECKBOX,self.OnBottomBendCutEnableCHK)
        self.bottomBendCutLabel=wx.StaticText(self.panel,label="底部折弯裁切量：",size=(100,-1))
        self.bottomBendCutLabel.Show(self.bottomBendEnable and self.bottomBendCutEnable)
        hhbox.Add(self.bottomBendCutLabel,0,wx.TOP,5)
        self.bottomBendCutSPIN = wx.SpinCtrl(self.panel,size=(100,-1),min=0,max=200)
        self.bottomBendCutSPIN.SetValue(self.bottomBendCutValue)
        self.bottomBendCutSPIN.Show(self.bottomBendEnable and self.bottomBendCutEnable)
        hhbox.Add(self.bottomBendCutSPIN,1,wx.RIGHT,10)
        vbox.Add(hhbox,0,wx.EXPAND)

        vbox.Add((-1,10))

        hhbox = wx.BoxSizer()
        hhbox.Add((10,1))
        self.topBendEnableCHK = wx.CheckBox(self.panel,label="有顶部折弯",size=(120,-1))
        self.topBendEnableCHK.Bind(wx.EVT_CHECKBOX,self.OnTopBendEnableCHK)
        self.topBendEnableCHK.SetValue(self.topBendEnable)
        hhbox.Add(self.topBendEnableCHK,0,wx.TOP,5)
        self.topBendEnableCHK.Bind(wx.EVT_CHECKBOX,self.OnTopBendEnableCHK)
        self.topBendLabel=wx.StaticText(self.panel,label="顶部折弯量：",size=(100,-1))
        self.topBendLabel.Show(self.topBendEnable)
        hhbox.Add(self.topBendLabel,0,wx.TOP,5)
        self.topBendTXT = wx.SpinCtrl(self.panel,size=(100,-1),min=0,max=50)
        self.topBendTXT.SetValue(self.topBendValue)
        self.topBendTXT.Show(self.topBendEnable)
        hhbox.Add(self.topBendTXT,1,wx.RIGHT,10)
        vbox.Add(hhbox,0,wx.EXPAND)

        vbox.Add((-1,10))

        hhbox = wx.BoxSizer()
        hhbox.Add((10,1))
        self.colourEnableCHK = wx.CheckBox(self.panel,label="指定颜色",size=(120,-1))
        self.colourEnableCHK.SetValue(self.colourEnable)
        hhbox.Add(self.colourEnableCHK,0,wx.TOP,5)
        self.colourEnableCHK.Bind(wx.EVT_CHECKBOX,self.OnColourEnableCHK)
        self.colourLabel=wx.StaticText(self.panel,label="X面颜色：",size=(100,-1))
        self.colourLabel.Show(self.colourEnable)
        hhbox.Add(self.colourLabel,0,wx.TOP,5)
        self.colourCOMBO = wx.ComboBox(self.panel,choices=["1","2","3","4","5","6","7","8"],size=(100,-1))
        self.colourCOMBO.Show(self.colourEnable)
        hhbox.Add(self.colourCOMBO,1,wx.RIGHT,10)
        vbox.Add(hhbox,0,wx.EXPAND)

        vbox.Add((-1,10))

        hhbox = wx.BoxSizer()
        hhbox.Add((10,1))
        self.materialEnableCHK = wx.CheckBox(self.panel,label="指定材质",size=(120,-1))
        self.materialEnableCHK.SetValue(self.materialEnable)
        hhbox.Add(self.materialEnableCHK,0,wx.TOP,10)
        self.materialEnableCHK.Bind(wx.EVT_CHECKBOX,self.OnMaterialEnableCHK)
        self.materialLabel=wx.StaticText(self.panel,label="X面材质：",size=(100,-1))
        self.materialLabel.Show(self.materialEnable)
        hhbox.Add(self.materialLabel,0,wx.TOP,5)
        self.materialCOMBO = wx.ComboBox(self.panel,choices=["1","2","3","4","5","6","7","8"],size=(100,-1))
        self.materialCOMBO.Show(self.materialEnable)
        hhbox.Add(self.materialCOMBO,1,wx.RIGHT,10)
        vbox.Add(hhbox,0,wx.EXPAND)


        self.panel.SetSizer(vbox)
        self.panel.Layout()
        self.panel.Thaw()

    def OnExistCOMBOChanged(self,event):
        wallID = self.existCOMOBO.GetValue()
        _,result=GetSurfaceXParameterByTypeID(self.log,WHICHDB, wallID)
        self.leftBendEnable = True if result[0]=='U' else False
        self.leftBendValue=result[1]
        self.rightBendEnable = True if result[2]=='U' else False
        self.rightBendValue=result[3]
        self.topBendEnable = True if result[4]=='U' else False
        self.topBendValue=result[5]
        self.bottomBendEnable=True if result[6]=='U' else False
        self.bottomBendValue=result[7]
        self.bottomBendCutEnable=True if result[8]=='U' else False
        self.bottomBendCutValue = result[9]
        if result[10] != "":
            self.materialEnable = True
            self.material = result[10]
        if result[11] != "":
            self.colourEnable = True
            self.colour = result[11]
        self.ShowPreview()
        self.ReCreate()

    def OnLeftBendEnableCHK(self,event):
        self.leftBendEnable=self.leftBendEnableCHK.GetValue()
        self.leftBendValue=self.leftBendTXT.GetValue() if self.leftBendEnable else 0
        self.ShowPreview()
        self.ReCreate()

    def OnRightBendEnableCHK(self,event):
        self.rightBendEnable=self.rightBendEnableCHK.GetValue()
        self.rightBendValue=self.rightBendTXT.GetValue() if self.rightBendEnable else 0
        self.ShowPreview()
        self.ReCreate()

    def OnColourEnableCHK(self,event):
        self.colourEnable=self.colourEnableCHK.GetValue()
        self.colour=self.colourCOMBO.GetValue() if self.colourEnable else ""
        self.ReCreate()

    def OnMaterialEnableCHK(self,event):
        self.materialEnable=self.materialEnableCHK.GetValue()
        self.material=self.materialCOMBO.GetValue() if self.materialEnable else ""
        self.ReCreate()

    def OnBottomBendEnableCHK(self,event):
        self.bottomBendEnable=self.bottomBendEnableCHK.GetValue()
        self.bottomBendValue=self.bottomBendTXT.GetValue() if self.bottomBendEnable else 0
        if not self.bottomBendEnable:
            self.bottomBendCutEnable=False
        self.ReCreate()

    def OnTopBendEnableCHK(self,event):
        self.topBendEnable=self.topBendEnableCHK.GetValue()
        self.topBendValue=self.topBendTXT.GetValue() if self.topBendEnable else 0
        self.ReCreate()

    def OnBottomBendCutEnableCHK(self,event):
        self.bottomBendCutEnable=self.bottomBendCutEnableCHK.GetValue()
        self.bottomBendCut=self.bottomBendCutSPIN.GetValue() if self.bottomBendEnable and self.bottomBendCutEnable else 0
        self.ReCreate()

class SurfaceYParameterPage(SurfaceXParameterPage):
    def __init__(self,parent, master, log, title):
        self.bottomRaiseEnable = False
        self.bottomRaiseValue = 0
        self.leftExtendEnable = False
        self.leftExtendValue = 0
        self.leftSelvedgeEnable = False
        self.rightExtendEnable = False
        self.rightExtendValue = 0
        self.rightSelvedgeEnable = False
        self.bottomBendCutEnable=False
        self.bottomBendCutValue = 0
        self.bottomRaiseEnable = False
        self.bottomRaiseValue = 0
        super(SurfaceYParameterPage, self).__init__(parent,master,log,title)
        self.baseFilename = "SurfaceY"
        self.Bind(wx.adv.EVT_WIZARD_BEFORE_PAGE_CHANGED,self.OnBeforeChanged)
        self.ReCreate()

    def OnBeforeChanged(self,event):
        self.wallType = self.master.pageWall.wallType
        self.wallID = self.master.pageWall.wallID
        self.leftBendValue=self.leftBendTXT.GetValue()
        self.rightBendValue=self.rightBendTXT.GetValue()
        self.topBendValue=self.topBendTXT.GetValue()
        self.bottomBendValue=self.bottomBendTXT.GetValue()
        self.bottomBendCutValue=self.bottomBendCutSPIN.GetValue()
        self.bottomRaiseValue=self.bottomRaiseTXT.GetValue()
        self.leftExtendValue = self.leftExtendTXT.GetValue()
        self.rightExtendValue = self.rightExtendTXT.GetValue()
        ModifySurfaceYConfigurationExcelFile(self.leftBendEnable,self.leftBendValue,self.rightBendEnable,self.rightBendValue,self.topBendEnable,self.topBendValue,self.bottomBendEnable,self.bottomBendValue,self.bottomBendCutEnable,self.bottomBendCutValue,self.bottomRaiseEnable,self.bottomRaiseValue,self.leftSelvedgeEnable,self.rightSelvedgeEnable)

    def ReCreate(self):
        try:
            self.leftBendValue = self.leftBendTXT.GetValue()
            self.rightBendValue = self.rightBendTXT.GetValue()
            self.topBendValue = self.topBendTXT.GetValue()
            self.bottomBendValue = self.bottomBendTXT.GetValue()
            self.bottomBendCutValue = self.bottomBendCutSPIN.GetValue()
            self.leftExtendValue = self.leftExtendTXT.GetValue()
            self.rightExtendValue = self.rightExtendTXT.GetValue()
            self.bottomRaiseValue = self.bottomRaiseTXT.GetValue()
            self.leftExtendValue = self.leftExtendTXT.GetValue()
            self.rightExtendValue = self.rightExtendTXT.GetValue()
        except:
            pass
        self.panel.Freeze()
        self.panel.DestroyChildren()
        vbox = wx.BoxSizer(wx.VERTICAL)
        hhbox=wx.BoxSizer()
        hhbox.Add((5, 1))
        self.leftExtendEnableCHK = wx.CheckBox(self.panel, label="有左侧延伸", size=(120, -1))
        self.leftExtendEnableCHK.Bind(wx.EVT_CHECKBOX, self.OnLeftExtendEnableCHK)
        self.leftExtendEnableCHK.SetValue(self.leftExtendEnable)
        hhbox.Add(self.leftExtendEnableCHK, 0, wx.TOP, 5)
        self.leftExtendLabel=wx.StaticText(self.panel,label="Y面左侧延伸量：",size=(100,-1))
        self.leftExtendLabel.Show(self.leftExtendEnable)
        hhbox.Add(self.leftExtendLabel,0,wx.TOP,5)
        self.leftExtendTXT = wx.SpinCtrl(self.panel,size=(100,-1),min=1,max=200)
        self.leftExtendTXT.SetValue(self.leftExtendValue)
        self.leftExtendTXT.Show(self.leftExtendEnable)
        hhbox.Add(self.leftExtendTXT,1,wx.RIGHT,10)
        vbox.Add(hhbox, 0, wx.EXPAND)

        vbox.Add((-1,10))

        hhbox=wx.BoxSizer()
        hhbox.Add((5, 1))
        self.leftBendEnableCHK = wx.CheckBox(self.panel,label="有左侧折弯",size=(120,-1))
        self.leftBendEnableCHK.Bind(wx.EVT_CHECKBOX,self.OnLeftBendEnableCHK)
        self.leftBendEnableCHK.SetValue(self.leftBendEnable)
        hhbox.Add(self.leftBendEnableCHK,0,wx.TOP,5)
        self.leftBendLabel=wx.StaticText(self.panel,label="Y面左侧折弯量：",size=(100,-1))
        self.leftBendLabel.Show(self.leftBendEnable)
        hhbox.Add(self.leftBendLabel,0,wx.TOP,5)
        self.leftBendTXT = wx.SpinCtrl(self.panel,size=(100,-1),min=1,max=50)
        self.leftBendTXT.SetValue(self.leftBendValue)
        self.leftBendTXT.Show(self.leftBendEnable)
        hhbox.Add(self.leftBendTXT,1,wx.RIGHT,10)
        vbox.Add(hhbox, 0, wx.EXPAND)

        vbox.Add((-1,10))

        hhbox=wx.BoxSizer()
        hhbox.Add((5, 1))
        self.leftSelvedgeEnableCHK = wx.CheckBox(self.panel,label="有左侧褶边",size=(120,-1))
        self.leftSelvedgeEnableCHK.Bind(wx.EVT_CHECKBOX,self.OnLeftSelvedgeEnableCHK)
        self.leftSelvedgeEnableCHK.SetValue(self.leftSelvedgeEnable)
        hhbox.Add(self.leftSelvedgeEnableCHK,0,wx.TOP,5)
        self.rightSelvedgeEnableCHK = wx.CheckBox(self.panel,label="有右侧褶边",size=(120,-1))
        self.rightSelvedgeEnableCHK.Bind(wx.EVT_CHECKBOX,self.OnRightSelvedgeEnableCHK)
        self.rightSelvedgeEnableCHK.SetValue(self.rightSelvedgeEnable)
        hhbox.Add(self.rightSelvedgeEnableCHK,0,wx.TOP,5)
        vbox.Add(hhbox, 0, wx.EXPAND)

        vbox.Add((-1,10))

        hhbox=wx.BoxSizer()
        hhbox.Add((5, 1))
        self.rightExtendEnableCHK = wx.CheckBox(self.panel,label="有右侧延伸",size=(120,-1))
        self.rightExtendEnableCHK.Bind(wx.EVT_CHECKBOX,self.OnRightExtendEnableCHK)
        self.rightExtendEnableCHK.SetValue(self.rightExtendEnable)
        hhbox.Add(self.rightExtendEnableCHK,0,wx.TOP,5)
        self.rightExtendLabel=wx.StaticText(self.panel,label="Y面右侧延伸量：",size=(100,-1))
        self.rightExtendLabel.Show(self.rightExtendEnable)
        hhbox.Add(self.rightExtendLabel,0,wx.TOP,5)
        self.rightExtendTXT = wx.SpinCtrl(self.panel,size=(100,-1),min=1,max=200)
        self.rightExtendTXT.SetValue(self.rightExtendValue)
        self.rightExtendTXT.Show(self.rightExtendEnable)
        hhbox.Add(self.rightExtendTXT,1,wx.RIGHT,10)
        vbox.Add(hhbox, 0, wx.EXPAND)

        vbox.Add((-1,10))

        hhbox=wx.BoxSizer()
        hhbox.Add((5, 1))
        self.rightBendEnableCHK = wx.CheckBox(self.panel,label="有右侧折弯",size=(120,-1))
        self.rightBendEnableCHK.Bind(wx.EVT_CHECKBOX,self.OnRightBendEnableCHK)
        self.rightBendEnableCHK.SetValue(self.rightBendEnable)
        hhbox.Add(self.rightBendEnableCHK,0,wx.TOP,5)
        self.rightBendLabel=wx.StaticText(self.panel,label="Y面右侧折弯量：",size=(100,-1))
        self.rightBendLabel.Show(self.rightBendEnable)
        hhbox.Add(self.rightBendLabel,0,wx.TOP,5)
        self.rightBendTXT = wx.SpinCtrl(self.panel,size=(100,-1),min=1,max=50)
        self.rightBendTXT.SetValue(self.rightBendValue)
        self.rightBendTXT.Show(self.rightBendEnable)
        hhbox.Add(self.rightBendTXT,1,wx.RIGHT,10)
        vbox.Add(hhbox, 0, wx.EXPAND)

        vbox.Add((-1,10))

        hhbox=wx.BoxSizer()
        hhbox.Add((5, 1))
        self.topBendEnableCHK = wx.CheckBox(self.panel,label="有顶部折弯",size=(120,-1))
        self.topBendEnableCHK.Bind(wx.EVT_CHECKBOX,self.OnTopBendEnableCHK)
        self.topBendEnableCHK.SetValue(self.topBendEnable)
        hhbox.Add(self.topBendEnableCHK,0,wx.TOP,5)
        self.topBendLabel=wx.StaticText(self.panel,label="Y面顶部折弯量：",size=(100,-1))
        self.topBendLabel.Show(self.topBendEnable)
        hhbox.Add(self.topBendLabel,0,wx.TOP,5)
        self.topBendTXT = wx.SpinCtrl(self.panel,size=(100,-1),min=1,max=50)
        self.topBendTXT.SetValue(self.topBendValue)
        self.topBendTXT.Show(self.topBendEnable)
        hhbox.Add(self.topBendTXT,1,wx.RIGHT,10)
        vbox.Add(hhbox, 0, wx.EXPAND)

        vbox.Add((-1,10))

        hhbox = wx.BoxSizer()
        hhbox.Add((5,1))
        self.bottomRaiseEnableCHK = wx.CheckBox(self.panel,label="有Y面底部离地",size=(120,-1))
        self.bottomRaiseEnableCHK.Bind(wx.EVT_CHECKBOX,self.OnBottomRaiseEnableCHK)
        self.bottomRaiseEnableCHK.SetValue(self.bottomRaiseEnable)
        hhbox.Add(self.bottomRaiseEnableCHK,0,wx.TOP,5)
        self.bottomRaiseLabel=wx.StaticText(self.panel,label="底部离地高度：",size=(100,-1))
        self.bottomRaiseLabel.Show(self.bottomRaiseEnable)
        hhbox.Add(self.bottomRaiseLabel,0,wx.TOP,5)
        self.bottomRaiseTXT = wx.SpinCtrl(self.panel,size=(100,-1),min=0,max=500)
        self.bottomRaiseTXT.SetValue(self.bottomRaiseValue)
        self.bottomRaiseTXT.Show(self.bottomRaiseEnable)
        hhbox.Add(self.bottomRaiseTXT,1,wx.RIGHT,10)
        vbox.Add(hhbox,0,wx.EXPAND)

        vbox.Add((-1,10))

        hhbox = wx.BoxSizer()
        hhbox.Add((5,1))
        self.bottomBendEnableCHK = wx.CheckBox(self.panel,label="有底部折弯",size=(120,-1))
        self.bottomBendEnableCHK.Bind(wx.EVT_CHECKBOX,self.OnBottomBendEnableCHK)
        self.bottomBendEnableCHK.SetValue(self.bottomBendEnable)
        hhbox.Add(self.bottomBendEnableCHK,0,wx.TOP,5)
        self.bottomBendLabel=wx.StaticText(self.panel,label="底部折弯量：",size=(100,-1))
        self.bottomBendLabel.Show(self.bottomBendEnable)
        hhbox.Add(self.bottomBendLabel,0,wx.TOP,5)
        self.bottomBendTXT = wx.SpinCtrl(self.panel,size=(100,-1),min=0,max=50)
        self.bottomBendTXT.SetValue(self.bottomBendValue)
        self.bottomBendTXT.Show(self.bottomBendEnable)
        hhbox.Add(self.bottomBendTXT,1,wx.RIGHT,10)
        vbox.Add(hhbox,0,wx.EXPAND)

        vbox.Add((-1,10))

        hhbox = wx.BoxSizer()
        hhbox.Add((5,1))
        self.bottomBendCutEnableCHK = wx.CheckBox(self.panel,label="有底部折弯裁切",size=(120,-1))
        self.bottomBendCutEnableCHK.Bind(wx.EVT_CHECKBOX,self.OnBottomBendCutEnableCHK)
        self.bottomBendCutEnableCHK.SetValue(self.bottomBendCutEnable)
        self.bottomBendCutEnableCHK.Show(self.bottomBendEnable)
        hhbox.Add(self.bottomBendCutEnableCHK,0,wx.TOP,5)
        self.bottomBendCutLabel=wx.StaticText(self.panel,label="底部折弯裁切量：",size=(100,-1))
        self.bottomBendCutLabel.Show(self.bottomBendEnable and self.bottomBendCutEnable)
        hhbox.Add(self.bottomBendCutLabel,0,wx.TOP,5)
        self.bottomBendCutSPIN = wx.SpinCtrl(self.panel,size=(100,-1),min=0,max=200)
        self.bottomBendCutSPIN.SetValue(self.bottomBendCutValue)
        self.bottomBendCutSPIN.Show(self.bottomBendEnable and self.bottomBendCutEnable)
        hhbox.Add(self.bottomBendCutSPIN,1,wx.RIGHT,10)
        vbox.Add(hhbox,0,wx.EXPAND)

        vbox.Add((-1,10))

        hhbox = wx.BoxSizer()
        hhbox.Add((5,1))
        self.colourEnableCHK = wx.CheckBox(self.panel,label="指定颜色",size=(120,-1))
        self.colourEnableCHK.Bind(wx.EVT_CHECKBOX,self.OnColourEnableCHK)
        self.colourEnableCHK.SetValue(self.colourEnable)
        hhbox.Add(self.colourEnableCHK,0,wx.TOP,5)
        self.colourLabel=wx.StaticText(self.panel,label="Y面颜色：",size=(100,-1))
        self.colourLabel.Show(self.colourEnable)
        hhbox.Add(self.colourLabel,0,wx.TOP,5)
        self.colourCOMBO = wx.ComboBox(self.panel,choices=["1","2","3","4","5","6","7","8"],size=(100,-1))
        self.colourCOMBO.Show(self.colourEnable)
        hhbox.Add(self.colourCOMBO,1,wx.RIGHT,10)
        vbox.Add(hhbox,0,wx.EXPAND)

        vbox.Add((-1,10))

        hhbox = wx.BoxSizer()
        hhbox.Add((5,1))
        self.materialEnableCHK = wx.CheckBox(self.panel,label="默认材质",size=(120,-1))
        self.materialEnableCHK.Bind(wx.EVT_CHECKBOX, self.OnMaterialEnableCHK)
        self.materialEnableCHK.SetValue(self.materialEnable)
        hhbox.Add(self.materialEnableCHK,0,wx.TOP,10)
        self.materialLabel=wx.StaticText(self.panel,label="Y面材质：",size=(60,-1))
        self.materialLabel.Show(self.materialEnable)
        hhbox.Add(self.materialLabel,0,wx.TOP,10)
        self.materialCOMBO = wx.ComboBox(self.panel,choices=[],size=(100,-1))
        self.materialCOMBO.SetValue(self.material)
        self.materialCOMBO.Show(self.materialEnable)
        hhbox.Add(self.materialCOMBO,1,wx.TOP,5)
        vbox.Add(hhbox,0,wx.EXPAND|wx.RIGHT,10)


        self.panel.SetSizer(vbox)
        self.panel.Layout()
        self.panel.Thaw()

    def OnPreViewBTN(self, event):
        message = "正在处理请稍候..."
        busy = PBI.PyBusyInfo(message, parent=None, title="系统忙提示",
                              icon=images.Smiles.GetBitmap())

        wx.Yield()
        self.leftBendValue=self.leftBendTXT.GetValue()
        self.rightBendValue=self.rightBendTXT.GetValue()
        self.bottomBendValue=self.bottomBendTXT.GetValue()
        self.bottomBendCutValue=self.bottomBendCutSPIN.GetValue()
        ModifySurfaceYConfigurationExcelFile(self.leftBendEnable,self.leftBendValue,self.rightBendEnable,self.rightBendValue,self.topBendEnable,self.topBendValue,self.bottomBendEnable,self.bottomBendValue,self.bottomBendCutEnable,self.bottomBendCutValue,self.bottomRaiseEnable,self.bottomRaiseValue,self.leftSelvedgeEnable,self.rightSelvedgeEnable)
        # Part = swApp.OpenDoc6("D:\\WorkSpace\\Solidworks\\N.2SA\\SurfaceXSLDPRT.SLDPRT", 1, 0, "", longstatus, longwarnings)
        # swApp.ActivateDoc2("SurfaceXSLDPRT.SLDPRT", False, longstatus)
        # Part = swApp.ActiveDoc
        del busy

    def OnExistCOMBOChanged(self,event):
        wallID = self.existCOMOBO.GetValue()
        _,result=GetSurfaceYParameterByTypeID(self.log,WHICHDB,wallID)
        self.leftBendEnable = True if result[0]=='U' else False
        self.leftBendValue=result[1]
        self.rightBendEnable = True if result[2]=='U' else False
        self.rightBendValue=result[3]
        self.topBendEnable = True if result[4]=='U' else False
        self.topBendValue=result[5]
        self.bottomBendEnable=True if result[6]=='U' else False
        self.bottomBendValue=result[7]
        self.bottomBendCutEnable=True if result[8]=='U' else False
        self.bottomBendCutValue = result[9]
        self.leftExtendEnable=True if result[10]=='U' else False
        self.leftExtendValue = result[11]
        self.rightExtendEnable=True if result[12]=='U' else False
        self.rightExtendValue = result[13]
        self.leftSelvedgeEnable = True if result[14]=='U' else False
        self.rightSelvedgeEnable = True if result[15]=='U' else False
        self.bottomRaiseEnable = True if result[16]=='U' else False
        self.bottomRaiseValue = result[17]
        if result[17] != "":
            self.materialEnable = True
            self.material = result[18]
        if result[18] != "":
            self.colourEnable = True
            self.colour = result[19]
        self.ShowPreview()
        self.ReCreate()

    def OnLeftExtendEnableCHK(self,event):
        self.leftExtendEnable=self.leftExtendEnableCHK.GetValue()
        self.leftExtendValue=self.leftExtendTXT.GetValue() if self.leftExtendEnable else 0
        self.ShowPreview()
        self.ReCreate()

    def OnRightExtendEnableCHK(self,event):
        self.rightExtendEnable=self.rightExtendEnableCHK.GetValue()
        self.rightExtendValue=self.rightExtendTXT.GetValue() if self.rightExtendEnable else 0
        self.ShowPreview()
        self.ReCreate()

    def OnLeftSelvedgeEnableCHK(self,event):
        self.leftSelvedgeEnable = self.leftSelvedgeEnableCHK.GetValue()
        self.ShowPreview()
        self.ReCreate()

    def OnRightSelvedgeEnableCHK(self,event):
        self.rightSelvedgeEnable = self.rightSelvedgeEnableCHK.GetValue()
        self.ShowPreview()
        self.ReCreate()

    def OnBottomBendCutEnableCHK(self,event):
        self.bottomBendCutEnable = self.bottomBendCutEnableCHK.GetValue()
        self.ShowPreview()
        self.ReCreate()

    def OnBottomRaiseEnableCHK(self,event):
        self.bottomRaiseEnable = self.bottomRaiseEnableCHK.GetValue()
        self.ShowPreview()
        self.ReCreate()

class RockWoolParameterPage(SurfaceXParameterPage):
    def __init__(self,parent, master, log, title):
        self.leftSlotEnable = False
        self.leftSlotDepthValue = 20
        self.rightSlotEnable = False
        self.rightSlotDepthValue = 20
        self.topSlotEnable = False
        self.topSlotDepthValue = 20
        self.bottomSlotEnable = False
        self.bottomSlotDepthValue =20
        self.bottomRaiseEnable = False
        self.bottomRaiseValue = 0
        super(RockWoolParameterPage, self).__init__(parent,master,log,title)
        self.baseFilename="RockWool"

    def OnBeforeChanged(self,event):
        self.wallType = self.master.pageWall.wallType
        self.wallID = self.master.pageWall.wallID
        self.leftSlotDepthValue = self.leftSlotSPIN.GetValue()
        self.rightSlotDepthValue = self.rightSlotSPIN.GetValue()
        self.topSlotDepthValue = self.topSlotSPIN.GetValue()
        self.bottomSlotDepthValue = self.bottomSlotSPIN.GetValue()
        self.bottomRaiseValue = self.bottomRaiseTXT.GetValue()
        ModifyRockWoolConfigurationExcelFile(self.leftSlotEnable,self.leftSlotDepthValue,self.rightSlotEnable,self.rightSlotDepthValue,self.topSlotEnable,self.topSlotDepthValue,self.bottomSlotEnable,self.bottomSlotDepthValue,self.bottomRaiseEnable,self.bottomRaiseValue)

    def ReCreate(self):
        self.panel.Freeze()
        self.panel.DestroyChildren()
        vbox = wx.BoxSizer(wx.VERTICAL)
        hhbox=wx.BoxSizer()
        hhbox.Add((5, 1))
        self.leftSlotEnableCHK = wx.CheckBox(self.panel,label="有左侧开槽",size=(120,-1))
        self.leftSlotEnableCHK.Bind(wx.EVT_CHECKBOX,self.OnLeftSlotEnableCHK)
        self.leftSlotEnableCHK.SetValue(self.leftSlotEnable)
        hhbox.Add(self.leftSlotEnableCHK,0,wx.TOP,5)
        self.leftSlotLabel=wx.StaticText(self.panel,label="左侧开槽深度：",size=(100,-1))
        self.leftSlotLabel.Show(self.leftSlotEnable)
        hhbox.Add(self.leftSlotLabel,0,wx.TOP,5)
        self.leftSlotSPIN = wx.SpinCtrl(self.panel,size=(100,-1),min=1,max=50)
        self.leftSlotSPIN.SetValue(self.leftSlotDepthValue)
        self.leftSlotSPIN.Show(self.leftSlotEnable)
        hhbox.Add(self.leftSlotSPIN,1,wx.RIGHT,10)
        vbox.Add(hhbox, 0, wx.EXPAND)

        vbox.Add((-1,10))

        hhbox=wx.BoxSizer()
        hhbox.Add((5, 1))
        self.rightSlotEnableCHK = wx.CheckBox(self.panel,label="有右侧开槽",size=(120,-1))
        self.rightSlotEnableCHK.Bind(wx.EVT_CHECKBOX,self.OnRightSlotEnableCHK)
        self.rightSlotEnableCHK.SetValue(self.rightSlotEnable)
        hhbox.Add(self.rightSlotEnableCHK,0,wx.TOP,5)
        self.rightSlotLabel=wx.StaticText(self.panel,label="右侧开槽深度：",size=(100,-1))
        self.rightSlotLabel.Show(self.rightSlotEnable)
        hhbox.Add(self.rightSlotLabel,0,wx.TOP,5)
        self.rightSlotSPIN = wx.SpinCtrl(self.panel,size=(100,-1),min=1,max=50)
        self.rightSlotSPIN.SetValue(self.rightSlotDepthValue)
        self.rightSlotSPIN.Show(self.rightSlotEnable)
        hhbox.Add(self.rightSlotSPIN,1,wx.RIGHT,10)
        vbox.Add(hhbox, 0, wx.EXPAND)

        vbox.Add((-1,10))

        hhbox=wx.BoxSizer()
        hhbox.Add((5, 1))
        self.topSlotEnableCHK = wx.CheckBox(self.panel,label="有顶部开槽",size=(120,-1))
        self.topSlotEnableCHK.Bind(wx.EVT_CHECKBOX,self.OnTopSlotEnableCHK)
        self.topSlotEnableCHK.SetValue(self.topSlotEnable)
        hhbox.Add(self.topSlotEnableCHK,0,wx.TOP,5)
        self.topSlotLabel=wx.StaticText(self.panel,label="顶部开槽深度：",size=(100,-1))
        self.topSlotLabel.Show(self.topSlotEnable)
        hhbox.Add(self.topSlotLabel,0,wx.TOP,5)
        self.topSlotSPIN = wx.SpinCtrl(self.panel,size=(100,-1),min=1,max=50)
        self.topSlotSPIN.SetValue(self.topSlotDepthValue)
        self.topSlotSPIN.Show(self.topSlotEnable)
        hhbox.Add(self.topSlotSPIN,1,wx.RIGHT,10)
        vbox.Add(hhbox, 0, wx.EXPAND)

        vbox.Add((-1,10))

        hhbox=wx.BoxSizer()
        hhbox.Add((5, 1))
        self.bottomSlotEnableCHK = wx.CheckBox(self.panel,label="有底部开槽",size=(120,-1))
        self.bottomSlotEnableCHK.Bind(wx.EVT_CHECKBOX,self.OnBottomSlotEnableCHK)
        self.bottomSlotEnableCHK.SetValue(self.bottomSlotEnable)
        hhbox.Add(self.bottomSlotEnableCHK,0,wx.TOP,5)
        self.bottomSlotLabel=wx.StaticText(self.panel,label="底部开槽深度：",size=(100,-1))
        self.bottomSlotLabel.Show(self.bottomSlotEnable)
        hhbox.Add(self.bottomSlotLabel,0,wx.TOP,5)
        self.bottomSlotSPIN = wx.SpinCtrl(self.panel,size=(100,-1),min=1,max=50)
        self.bottomSlotSPIN.SetValue(self.bottomSlotDepthValue)
        self.bottomSlotSPIN.Show(self.bottomSlotEnable)
        hhbox.Add(self.bottomSlotSPIN,1,wx.RIGHT,10)
        vbox.Add(hhbox, 0, wx.EXPAND)

        vbox.Add((-1,10))

        hhbox=wx.BoxSizer()
        hhbox.Add((5, 1))
        self.bottomRaiseEnableCHK = wx.CheckBox(self.panel,label="有底部离地",size=(120,-1))
        self.bottomRaiseEnableCHK.Bind(wx.EVT_CHECKBOX,self.OnBottomRaiseEnableCHK)
        self.bottomRaiseEnableCHK.SetValue(self.bottomRaiseEnable)
        hhbox.Add(self.bottomRaiseEnableCHK,0,wx.TOP,5)
        self.bottomRaiseLabel=wx.StaticText(self.panel,label="底部离地高度：",size=(100,-1))
        self.bottomRaiseLabel.Show(self.bottomRaiseEnable)
        hhbox.Add(self.bottomRaiseLabel,0,wx.TOP,5)
        self.bottomRaiseTXT = wx.SpinCtrl(self.panel,size=(100,-1),min=1,max=500)
        self.bottomRaiseTXT.SetValue(self.bottomRaiseValue)
        self.bottomRaiseTXT.Show(self.bottomRaiseEnable)
        hhbox.Add(self.bottomRaiseTXT,1,wx.RIGHT,10)
        vbox.Add(hhbox, 0, wx.EXPAND)

        vbox.Add((-1,10))

        hhbox = wx.BoxSizer()
        hhbox.Add((5,1))
        self.colourEnableCHK = wx.CheckBox(self.panel,label="指定颜色",size=(120,-1))
        self.colourEnableCHK.SetValue(self.colourEnable)
        hhbox.Add(self.colourEnableCHK,0,wx.TOP,5)
        self.colourLabel=wx.StaticText(self.panel,label="Y面颜色：",size=(100,-1))
        self.colourLabel.Show(self.colourEnable)
        hhbox.Add(self.colourLabel,0,wx.TOP,5)
        self.colourCOMBO = wx.ComboBox(self.panel,choices=["1","2","3","4","5","6","7","8"],size=(100,-1))
        self.colourCOMBO.Show(self.colourEnable)
        hhbox.Add(self.colourCOMBO,1,wx.RIGHT,10)
        vbox.Add(hhbox,0,wx.EXPAND)

        vbox.Add((-1,10))

        hhbox = wx.BoxSizer()
        hhbox.Add((5,1))
        self.materialEnableCHK = wx.CheckBox(self.panel,label="默认材质",size=(120,-1))
        self.materialEnableCHK.SetValue(self.materialEnable)
        hhbox.Add(self.materialEnableCHK,0,wx.TOP,10)
        self.materialLabel=wx.StaticText(self.panel,label="Y面材质：",size=(60,-1))
        self.materialLabel.Show(self.materialEnable)
        hhbox.Add(self.materialLabel,0,wx.TOP,10)
        self.materialCOMBO = wx.ComboBox(self.panel,choices=[],size=(100,-1))
        self.materialCOMBO.SetValue(self.material)
        self.materialCOMBO.Show(self.materialEnable)
        hhbox.Add(self.materialCOMBO,1,wx.TOP,5)
        vbox.Add(hhbox,0,wx.EXPAND|wx.RIGHT,10)


        self.panel.SetSizer(vbox)
        self.panel.Layout()
        self.panel.Thaw()

    def OnLeftSlotEnableCHK(self,event):
        self.leftSlotEnable = self.leftSlotEnableCHK.GetValue()
        self.leftSlotDepthValue=self.leftSlotSPIN.GetValue() if self.leftSlotEnable else 0
        self.ShowPreview()
        self.ReCreate()

    def OnRightSlotEnableCHK(self,event):
        self.rightSlotEnable = self.rightSlotEnableCHK.GetValue()
        self.rightSlotDepthValue=self.rightSlotSPIN.GetValue() if self.rightSlotEnable else 0
        self.ShowPreview()
        self.ReCreate()

    def OnTopSlotEnableCHK(self,event):
        self.topSlotEnable = self.topSlotEnableCHK.GetValue()
        self.topSlotDepthValue=self.topSlotSPIN.GetValue() if self.topSlotEnable else 0
        self.ShowPreview()
        self.ReCreate()

    def OnBottomSlotEnableCHK(self,event):
        self.bottomSlotEnable = self.bottomSlotEnableCHK.GetValue()
        self.bottomSlotDepthValue=self.bottomSlotSPIN.GetValue() if self.bottomSlotEnable else 0
        self.ShowPreview()
        self.ReCreate()

    def OnBottomRaiseEnableCHK(self,event):
        self.bottomRaiseEnable = self.bottomRaiseEnableCHK.GetValue()
        self.bottomRaiseDepthValue=self.bottomRaiseTXT.GetValue() if self.bottomRaiseEnable else 0
        self.ShowPreview()
        self.ReCreate()

    def OnExistCOMBOChanged(self,event):
        wallID = self.existCOMOBO.GetValue()
        _,result=GetRockWoolParameterByTypeID(self.log,WHICHDB,wallID)
        self.leftSlotEnable = True if result[0]=='U' else False
        self.leftSlotDepthValue=result[1]
        self.rightSlotEnable = True if result[2]=='U' else False
        self.rightSlotDepthValue=result[3]
        self.topSlotEnable = True if result[4]=='U' else False
        self.topSlotDepthValue=result[5]
        self.bottomSlotEnable = True if result[6]=='U' else False
        self.bottomSlotDepthValue=result[7]
        self.bottomRaiseEnable = True if result[8]=='U' else False
        self.bottomRaiseValue=result[9]
        if result[10] != "":
            self.materialEnable = True
            self.material = result[10]
        if result[11] != "":
            self.colourEnable = True
            self.colour = result[11]
        self.ShowPreview()
        self.ReCreate()

class ReinforcementParameterPage(SurfaceXParameterPage):
    def __init__(self,parent, master, log, title):
        self.bottomReinforcementEnable = False
        self.middleReinforcementEnable = False
        self.topReinforcementEnable = False
        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0
        self.e = 0
        self.f = 0
        self.bottomX1 = 0
        self.bottomX2 = 0
        self.middleX1 = 0
        self.middleX2 = 0
        self.topX1 = 0
        self.topX2 = 0
        super(ReinforcementParameterPage, self).__init__(parent,master,log,title)
        self.baseFilename="Reinforcement"
        self.Bind(wx.EVT_CHECKBOX,self.OnCheck)

    def OnBeforeChanged(self,event):
        self.a=self.aTXT.GetValue()
        self.b=self.bTXT.GetValue()
        self.c=self.cTXT.GetValue()
        self.d=self.dTXT.GetValue()
        self.e=self.eTXT.GetValue()
        self.f=self.fTXT.GetValue()
        self.bottomX1=self.bottomX1TXT.GetValue()
        self.bottomX2=self.bottomX2TXT.GetValue()
        self.middleX1=self.middleX1TXT.GetValue()
        self.middleX2=self.middleX2TXT.GetValue()
        self.topX1=self.topX1TXT.GetValue()
        self.topX2=self.topX2TXT.GetValue()
        ModifyReinforcementConfigurationExcelFile(self.bottomReinforcementEnable,self.middleReinforcementEnable,self.topReinforcementEnable,self.a,self.b,self.c,self.d,self.e,self.f,self.bottomX1,self.bottomX2,self.middleX1,self.middleX2,self.topX1,self.topX2)

    def ReCreate(self):
        self.panel.Freeze()
        self.panel.DestroyChildren()
        vbox = wx.BoxSizer(wx.VERTICAL)
        hhbox=wx.BoxSizer()
        hhbox.Add((5, 1))
        self.bottomReinforcementEnableCHK = wx.CheckBox(self.panel,label="底部")
        self.bottomReinforcementEnableCHK.SetValue(self.bottomReinforcementEnable)
        hhbox.Add(self.bottomReinforcementEnableCHK,0,wx.TOP,5)
        self.aLabel=wx.StaticText(self.panel,label="a：")
        self.aLabel.Show(self.bottomReinforcementEnable)
        hhbox.Add(self.aLabel,0,wx.TOP,5)
        self.aTXT = wx.TextCtrl(self.panel,size=(40,-1))
        self.aTXT.SetValue(str(self.a))
        self.aTXT.Show(self.bottomReinforcementEnable)
        hhbox.Add(self.aTXT,0,wx.RIGHT,5)

        self.bLabel=wx.StaticText(self.panel,label="b：")
        self.bLabel.Show(self.bottomReinforcementEnable)
        hhbox.Add(self.bLabel,0,wx.TOP,5)
        self.bTXT = wx.TextCtrl(self.panel,size=(40,-1))
        self.bTXT.SetValue(str(self.b))
        self.bTXT.Show(self.bottomReinforcementEnable)
        hhbox.Add(self.bTXT,0,wx.RIGHT,5)

        self.bottomX1Label=wx.StaticText(self.panel,label="X1：")
        self.bottomX1Label.Show(self.bottomReinforcementEnable)
        hhbox.Add(self.bottomX1Label,0,wx.TOP,5)
        self.bottomX1TXT = wx.TextCtrl(self.panel,size=(40,-1))
        self.bottomX1TXT.SetValue(str(self.bottomX1))
        self.bottomX1TXT.Show(self.bottomReinforcementEnable)
        hhbox.Add(self.bottomX1TXT,0,wx.RIGHT,5)

        self.bottomX2Label=wx.StaticText(self.panel,label="X2：")
        self.bottomX2Label.Show(self.bottomReinforcementEnable)
        hhbox.Add(self.bottomX2Label,0,wx.TOP,5)
        self.bottomX2TXT = wx.TextCtrl(self.panel,size=(70,-1))
        self.bottomX2TXT.SetValue(str(self.bottomX2))
        self.bottomX2TXT.Show(self.bottomReinforcementEnable)
        hhbox.Add(self.bottomX2TXT, 1, wx.RIGHT, 5)
        vbox.Add(hhbox, 0, wx.EXPAND)

        vbox.Add((-1,10))

        hhbox=wx.BoxSizer()
        hhbox.Add((5, 1))
        self.middleReinforcementEnableCHK = wx.CheckBox(self.panel,label="中部")
        self.middleReinforcementEnableCHK.SetValue(self.middleReinforcementEnable)
        hhbox.Add(self.middleReinforcementEnableCHK,0,wx.TOP,5)
        self.cLabel=wx.StaticText(self.panel,label="c：")
        self.cLabel.Show(self.middleReinforcementEnable)
        hhbox.Add(self.cLabel,0,wx.TOP,5)
        self.cTXT = wx.TextCtrl(self.panel,size=(40,-1))
        self.cTXT.SetValue(str(self.c))
        self.cTXT.Show(self.middleReinforcementEnable)
        hhbox.Add(self.cTXT,0,wx.RIGHT,5)

        self.dLabel=wx.StaticText(self.panel,label="d：")
        self.dLabel.Show(self.middleReinforcementEnable)
        hhbox.Add(self.dLabel,0,wx.TOP,5)
        self.dTXT = wx.TextCtrl(self.panel,size=(40,-1))
        self.dTXT.SetValue(str(self.d))
        self.dTXT.Show(self.middleReinforcementEnable)
        hhbox.Add(self.dTXT,0,wx.RIGHT,5)

        self.middleX1Label=wx.StaticText(self.panel,label="X1：")
        self.middleX1Label.Show(self.middleReinforcementEnable)
        hhbox.Add(self.middleX1Label,0,wx.TOP,5)
        self.middleX1TXT = wx.TextCtrl(self.panel,size=(40,-1))
        self.middleX1TXT.SetValue(str(self.middleX1))
        self.middleX1TXT.Show(self.middleReinforcementEnable)
        hhbox.Add(self.middleX1TXT,0,wx.RIGHT,5)

        self.middleX2Label=wx.StaticText(self.panel,label="X2：")
        self.middleX2Label.Show(self.middleReinforcementEnable)
        hhbox.Add(self.middleX2Label,0,wx.TOP,5)
        self.middleX2TXT = wx.TextCtrl(self.panel,size=(70,-1))
        self.middleX2TXT.SetValue(str(self.middleX2))
        self.middleX2TXT.Show(self.middleReinforcementEnable)
        hhbox.Add(self.middleX2TXT, 1, wx.RIGHT, 5)
        vbox.Add(hhbox, 0, wx.EXPAND)

        vbox.Add((-1,10))

        hhbox=wx.BoxSizer()
        hhbox.Add((5, 1))
        self.topReinforcementEnableCHK = wx.CheckBox(self.panel,label="顶部")
        self.topReinforcementEnableCHK.SetValue(self.topReinforcementEnable)
        hhbox.Add(self.topReinforcementEnableCHK,0,wx.TOP,5)
        self.eLabel=wx.StaticText(self.panel,label="e：")
        self.eLabel.Show(self.topReinforcementEnable)
        hhbox.Add(self.eLabel,0,wx.TOP,5)
        self.eTXT = wx.TextCtrl(self.panel,size=(40,-1))
        self.eTXT.SetValue(str(self.e))
        self.eTXT.Show(self.topReinforcementEnable)
        hhbox.Add(self.eTXT,0,wx.RIGHT,5)

        self.fLabel=wx.StaticText(self.panel,label="f：")
        self.fLabel.Show(self.topReinforcementEnable)
        hhbox.Add(self.fLabel,0,wx.TOP,5)
        self.fTXT = wx.TextCtrl(self.panel,size=(40,-1))
        self.fTXT.SetValue(str(self.f))
        self.fTXT.Show(self.topReinforcementEnable)
        hhbox.Add(self.fTXT,0,wx.RIGHT,5)

        self.topX1Label=wx.StaticText(self.panel,label="X1：")
        self.topX1Label.Show(self.topReinforcementEnable)
        hhbox.Add(self.topX1Label,0,wx.TOP,5)
        self.topX1TXT = wx.TextCtrl(self.panel,size=(40,-1))
        self.topX1TXT.SetValue(str(self.topX1))
        self.topX1TXT.Show(self.topReinforcementEnable)
        hhbox.Add(self.topX1TXT,0,wx.RIGHT,5)

        self.topX2Label=wx.StaticText(self.panel,label="X2：")
        self.topX2Label.Show(self.topReinforcementEnable)
        hhbox.Add(self.topX2Label,0,wx.TOP,5)
        self.topX2TXT = wx.TextCtrl(self.panel,size=(100,-1))
        self.topX2TXT.SetValue(str(self.topX2))
        self.topX2TXT.Show(self.topReinforcementEnable)
        hhbox.Add(self.topX2TXT, 1, wx.RIGHT, 5)
        vbox.Add(hhbox, 0, wx.EXPAND)

        vbox.Add((-1,10))

        hhbox = wx.BoxSizer()
        hhbox.Add((5,1))
        self.colourEnableCHK = wx.CheckBox(self.panel,label="指定颜色",size=(120,-1))
        self.colourEnableCHK.SetValue(self.colourEnable)
        hhbox.Add(self.colourEnableCHK,0,wx.TOP,5)
        self.colourLabel=wx.StaticText(self.panel,label="Y面颜色：",size=(100,-1))
        self.colourLabel.Show(self.colourEnable)
        hhbox.Add(self.colourLabel,0,wx.TOP,5)
        self.colourCOMBO = wx.ComboBox(self.panel,choices=["1","2","3","4","5","6","7","8"],size=(100,-1))
        self.colourCOMBO.Show(self.colourEnable)
        hhbox.Add(self.colourCOMBO,1,wx.RIGHT,10)
        vbox.Add(hhbox,0,wx.EXPAND)

        vbox.Add((-1,10))

        hhbox = wx.BoxSizer()
        hhbox.Add((5,1))
        self.materialEnableCHK = wx.CheckBox(self.panel,label="默认材质",size=(120,-1))
        self.materialEnableCHK.SetValue(self.materialEnable)
        hhbox.Add(self.materialEnableCHK,0,wx.TOP,10)
        self.materialLabel=wx.StaticText(self.panel,label="Y面材质：",size=(60,-1))
        self.materialLabel.Show(self.materialEnable)
        hhbox.Add(self.materialLabel,0,wx.TOP,10)
        self.materialCOMBO = wx.ComboBox(self.panel,choices=[],size=(100,-1))
        self.materialCOMBO.SetValue(self.material)
        self.materialCOMBO.Show(self.materialEnable)
        hhbox.Add(self.materialCOMBO,1,wx.TOP,5)
        vbox.Add(hhbox,0,wx.EXPAND|wx.RIGHT,10)


        self.panel.SetSizer(vbox)
        self.panel.Layout()
        self.panel.Thaw()

    def OnCheck(self,event):
        self.bottomReinforcementEnable = self.bottomReinforcementEnableCHK.GetValue()
        self.a=self.aTXT.GetValue() if self.bottomReinforcementEnable else 0
        self.b=self.bTXT.GetValue() if self.bottomReinforcementEnable else 0
        self.bottomX1 = self.bottomX1TXT.GetValue() if self.bottomReinforcementEnable else 0
        self.bottomX2 = self.bottomX2TXT.GetValue() if self.bottomReinforcementEnable else 0
        self.middleReinforcementEnable = self.middleReinforcementEnableCHK.GetValue()
        self.c=self.cTXT.GetValue() if self.middleReinforcementEnable else 0
        self.c=self.dTXT.GetValue() if self.middleReinforcementEnable else 0
        self.middleX1 = self.middleX1TXT.GetValue() if self.middleReinforcementEnable else 0
        self.middleX2 = self.middleX2TXT.GetValue() if self.middleReinforcementEnable else 0
        self.topReinforcementEnable = self.topReinforcementEnableCHK.GetValue()
        self.e=self.eTXT.GetValue() if self.topReinforcementEnable else 0
        self.f=self.fTXT.GetValue() if self.topReinforcementEnable else 0
        self.topX1 = self.topX1TXT.GetValue() if self.topReinforcementEnable else 0
        self.topX2 = self.topX2TXT.GetValue() if self.topReinforcementEnable else 0
        self.ShowPreview()
        self.ReCreate()

    def OnExistCOMBOChanged(self,event):
        wallID = self.existCOMOBO.GetValue()
        _,result=GetReinforcementParameterByTypeID(self.log,WHICHDB,wallID)
        self.bottomReinforcementEnable = True if result[0]=='U' else False
        self.middleReinforcementEnable = True if result[1]=='U' else False
        self.topReinforcementEnable = True if result[2]=='U' else False
        self.a=result[3]
        self.b=result[4]
        self.c=result[5]
        self.d=result[6]
        self.e=result[7]
        self.f=result[8]
        self.bottomX1=result[9]
        self.bottomX2=result[10]
        self.middleX1=result[11]
        self.middleX2=result[12]
        self.topX1=result[13]
        self.topX2=result[14]
        if result[15] != "":
            self.materialEnable = True
            self.material = result[15]
        if result[16] != "":
            self.colourEnable = True
            self.colour = result[16]
        self.ShowPreview()
        self.ReCreate()

class SurfaceXParameterShowPanel(wx.Panel):
    def __init__(self,parent,log,wallID):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.log=log
        self.wallID = wallID
        self.leftBendEnable = False
        self.leftBendValue=0
        self.rightBendEnable = False
        self.rightBendValue=0
        self.bottomBendEnable=False
        self.bottomBendValue=0
        self.bottomBendCutEnable=False
        self.bottomBendCutValue = 0
        self.materialEnable = False
        self.material = ""
        self.colourEnable=False
        self.colour=""

        _,result=GetSurfaceXParameterByTypeID(self.log,WHICHDB,self.wallID)
        self.leftBendEnable = True if result[0]=='U' else False
        self.leftBendValue=result[1]
        self.rightBendEnable = True if result[2]=='U' else False
        self.rightBendValue=result[3]
        self.topBendEnable = True if result[4]=='U' else False
        self.topBendValue=result[5]
        self.bottomBendEnable=True if result[6]=='U' else False
        self.bottomBendValue=result[7]
        self.bottomBendCutEnable=True if result[8]=='U' else False
        self.bottomBendCutValue = result[9]
        if result[10] != "":
            self.materialEnable = True
            self.material = result[10]
        if result[11] != "":
            self.colourEnable = True
            self.colour = result[11]
        self.Freeze()
        vbox = wx.BoxSizer(wx.VERTICAL)

        vbox.Add((-1,10))

        hhbox=wx.BoxSizer()
        hhbox.Add((5, 1))
        self.leftBendEnableCHK = wx.CheckBox(self,label="有左侧折弯",size=(90,-1))
        self.leftBendEnableCHK.Enable(False)
        self.leftBendEnableCHK.SetValue(self.leftBendEnable)
        hhbox.Add(self.leftBendEnableCHK,0,wx.TOP,5)
        self.leftBendLabel=wx.StaticText(self,label="X面左侧折弯量：",size=(100,-1))
        self.leftBendLabel.Show(self.leftBendEnable)
        hhbox.Add(self.leftBendLabel,0,wx.TOP,5)
        self.leftBendTXT = wx.SpinCtrl(self,size=(100,-1),min=1,max=50)
        self.leftBendTXT.SetValue(7)
        self.leftBendTXT.Show(self.leftBendEnable)
        self.leftBendTXT.Enable(False)
        hhbox.Add(self.leftBendTXT,1,wx.RIGHT,10)
        vbox.Add(hhbox, 0, wx.EXPAND)

        vbox.Add((-1,10))

        hhbox=wx.BoxSizer()
        hhbox.Add((5, 1))
        self.rightBendEnableCHK = wx.CheckBox(self,label="有右侧折弯",size=(90,-1))
        self.rightBendEnableCHK.Enable(False)
        self.rightBendEnableCHK.SetValue(self.rightBendEnable)
        hhbox.Add(self.rightBendEnableCHK,0,wx.TOP,5)
        self.rightBendLabel=wx.StaticText(self,label="X面右侧折弯量：",size=(100,-1))
        self.rightBendLabel.Show(self.rightBendEnable)
        hhbox.Add(self.rightBendLabel,0,wx.TOP,5)
        self.rightBendTXT = wx.SpinCtrl(self,size=(100,-1),min=1,max=50)
        self.rightBendTXT.Enable(False)
        self.rightBendTXT.SetValue(7)
        self.rightBendTXT.Show(self.rightBendEnable)
        hhbox.Add(self.rightBendTXT,1,wx.RIGHT,10)
        vbox.Add(hhbox, 0, wx.EXPAND)

        vbox.Add((-1,10))

        hhbox=wx.BoxSizer()
        hhbox.Add((5, 1))
        self.topBendEnableCHK = wx.CheckBox(self,label="有顶部折弯",size=(90,-1))
        self.topBendEnableCHK.Enable(False)
        self.topBendEnableCHK.SetValue(self.topBendEnable)
        hhbox.Add(self.topBendEnableCHK,0,wx.TOP,5)
        self.topBendLabel=wx.StaticText(self,label="X面顶部折弯量：",size=(100,-1))
        self.topBendLabel.Show(self.topBendEnable)
        hhbox.Add(self.topBendLabel,0,wx.TOP,5)
        self.topBendTXT = wx.SpinCtrl(self,size=(100,-1),min=1,max=50)
        self.topBendTXT.Enable(False)
        self.topBendTXT.SetValue(7)
        self.topBendTXT.Show(self.topBendEnable)
        hhbox.Add(self.topBendTXT,1,wx.RIGHT,10)
        vbox.Add(hhbox, 0, wx.EXPAND)

        vbox.Add((-1,10))

        hhbox = wx.BoxSizer()
        hhbox.Add((5,1))
        self.bottomBendEnableCHK = wx.CheckBox(self,label="有底部折弯",size=(90,-1))
        self.bottomBendEnableCHK.Enable(False)
        self.bottomBendEnableCHK.SetValue(self.bottomBendEnable)
        hhbox.Add(self.bottomBendEnableCHK,0,wx.TOP,5)
        self.bottomBendLabel=wx.StaticText(self,label="底部折弯量：",size=(100,-1))
        self.bottomBendLabel.Show(self.bottomBendEnable)
        hhbox.Add(self.bottomBendLabel,0,wx.TOP,5)
        self.bottomBendTXT = wx.SpinCtrl(self,size=(100,-1),min=0,max=50)
        self.bottomBendTXT.Enable(False)
        self.bottomBendTXT.SetValue(12)
        self.bottomBendTXT.Show(self.bottomBendEnable)
        hhbox.Add(self.bottomBendTXT,1,wx.RIGHT,10)
        vbox.Add(hhbox,0,wx.EXPAND)

        vbox.Add((-1,10))

        hhbox = wx.BoxSizer()
        hhbox.Add((5,1))
        self.bottomBendCutEnableCHK = wx.CheckBox(self,label="有底部折弯裁切",size=(90,-1))
        self.bottomBendCutEnableCHK.Enable(False)
        self.bottomBendCutEnableCHK.SetValue(self.bottomBendCutEnable)
        self.bottomBendCutEnableCHK.Show(self.bottomBendEnable)
        hhbox.Add(self.bottomBendCutEnableCHK,0,wx.TOP,5)
        self.bottomBendCutLabel=wx.StaticText(self,label="底部折弯裁切量：",size=(100,-1))
        self.bottomBendCutLabel.Show(self.bottomBendEnable and self.bottomBendCutEnable)
        hhbox.Add(self.bottomBendCutLabel,0,wx.TOP,5)
        self.bottomBendCutSPIN = wx.SpinCtrl(self,size=(100,-1),min=0,max=100)
        self.bottomBendCutSPIN.Enable(False)
        self.bottomBendCutSPIN.SetValue(self.bottomBendCutValue)
        self.bottomBendCutSPIN.Show(self.bottomBendEnable and self.bottomBendCutEnable)
        hhbox.Add(self.bottomBendCutSPIN,1,wx.RIGHT,10)
        vbox.Add(hhbox,0,wx.EXPAND)

        vbox.Add((-1,10))

        hhbox = wx.BoxSizer()
        hhbox.Add((5,1))
        self.colourEnableCHK = wx.CheckBox(self,label="指定颜色",size=(90,-1))
        self.colourEnableCHK.Enable(False)
        self.colourEnableCHK.SetValue(self.colourEnable)
        hhbox.Add(self.colourEnableCHK,0,wx.TOP,5)
        self.colourLabel=wx.StaticText(self,label="X面颜色：",size=(100,-1))
        self.colourLabel.Show(self.colourEnable)
        hhbox.Add(self.colourLabel,0,wx.TOP,5)
        self.colourCOMBO = wx.ComboBox(self,choices=["1","2","3","4","5","6","7","8"],size=(100,-1))
        self.colourCOMBO.Enable(False)
        self.colourCOMBO.Show(self.colourEnable)
        hhbox.Add(self.colourCOMBO,1,wx.RIGHT,10)
        vbox.Add(hhbox,0,wx.EXPAND)

        vbox.Add((-1,10))

        hhbox = wx.BoxSizer()
        hhbox.Add((5,1))
        self.materialEnableCHK = wx.CheckBox(self,label="默认材质",size=(90,-1))
        self.materialEnableCHK.Enable(False)
        self.materialEnableCHK.SetValue(self.materialEnable)
        hhbox.Add(self.materialEnableCHK,0,wx.TOP,10)
        self.materialLabel=wx.StaticText(self,label="X面材质：",size=(60,-1))
        self.materialLabel.Show(self.materialEnable)
        hhbox.Add(self.materialLabel,0,wx.TOP,10)
        self.materialCOMBO = wx.ComboBox(self,choices=[],size=(100,-1))
        self.materialCOMBO.SetValue(self.material)
        self.materialCOMBO.Enable(False)
        self.materialCOMBO.Show(self.materialEnable)
        hhbox.Add(self.materialCOMBO,1,wx.TOP,5)
        vbox.Add(hhbox,0,wx.EXPAND|wx.RIGHT,10)


        self.SetSizer(vbox)
        self.Layout()
        self.Thaw()

class SurfaceYParameterShowPanel(wx.Panel):
    def __init__(self,parent,log,wallID):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.log=log
        self.wallID = wallID
        _,result=GetSurfaceYParameterByTypeID(self.log,WHICHDB,wallID)
        self.leftBendEnable = True if result[0]=='U' else False
        self.leftBendValue=result[1]
        self.rightBendEnable = True if result[2]=='U' else False
        self.rightBendValue=result[3]
        self.topBendEnable = True if result[4]=='U' else False
        self.topBendValue=result[5]
        self.bottomBendEnable=True if result[6]=='U' else False
        self.bottomBendValue=result[7]
        self.bottomBendCutEnable=True if result[8]=='U' else False
        self.bottomBendCutValue = result[9]
        self.leftExtendEnable=True if result[10]=='U' else False
        self.leftExtendValue = result[11]
        self.rightExtendEnable=True if result[12]=='U' else False
        self.rightExtendValue = result[13]
        self.leftSelvedgeEnable=True if result[14]=='U' else False
        self.rightSelvedgeEnable=True if result[15]=='U' else False
        self.bottomRaiseEnable=True if result[16]=='U' else False
        self.bottomRaiseValue = result[17]
        if result[17] != "":
            self.materialEnable = True
            self.material = result[18]
        if result[18] != "":
            self.colourEnable = True
            self.colour = result[19]
        self.Freeze()
        vbox = wx.BoxSizer(wx.VERTICAL)

        vbox.Add((-1,10))

        hhbox=wx.BoxSizer()
        hhbox.Add((5, 1))
        self.leftExtenEnableCHK = wx.CheckBox(self,label="有左侧延伸",size=(120,-1))
        self.leftExtenEnableCHK.Enable(False)
        self.leftExtenEnableCHK.SetValue(self.leftExtendEnable)
        hhbox.Add(self.leftExtenEnableCHK,0,wx.TOP,5)
        self.leftExtendLabel=wx.StaticText(self,label="Y面左侧延伸量：",size=(100,-1))
        self.leftExtendLabel.Show(self.leftExtendEnable)
        hhbox.Add(self.leftExtendLabel,0,wx.TOP,5)
        self.leftExtendTXT = wx.SpinCtrl(self,size=(100,-1),min=1,max=200)
        self.leftExtendTXT.SetValue(self.leftExtendValue)
        self.leftExtendTXT.Show(self.leftExtendEnable)
        self.leftExtendTXT.Enable(False)
        hhbox.Add(self.leftExtendTXT,1,wx.RIGHT,10)
        vbox.Add(hhbox, 0, wx.EXPAND)

        vbox.Add((-1,10))

        hhbox=wx.BoxSizer()
        hhbox.Add((5, 1))
        self.leftBendEnableCHK = wx.CheckBox(self,label="有左侧折弯",size=(120,-1))
        self.leftBendEnableCHK.Enable(False)
        self.leftBendEnableCHK.SetValue(self.leftBendEnable)
        hhbox.Add(self.leftBendEnableCHK,0,wx.TOP,5)
        self.leftBendLabel=wx.StaticText(self,label="Y面左侧折弯量：",size=(100,-1))
        self.leftBendLabel.Show(self.leftBendEnable)
        hhbox.Add(self.leftBendLabel,0,wx.TOP,5)
        self.leftBendTXT = wx.SpinCtrl(self,size=(100,-1),min=1,max=50)
        self.leftBendTXT.SetValue(self.leftBendValue)
        self.leftBendTXT.Show(self.leftBendEnable)
        self.leftBendTXT.Enable(False)
        hhbox.Add(self.leftBendTXT,1,wx.RIGHT,10)
        vbox.Add(hhbox, 0, wx.EXPAND)

        vbox.Add((-1,10))

        hhbox=wx.BoxSizer()
        hhbox.Add((5, 1))
        self.leftSelvedgeEnableCHK = wx.CheckBox(self,label="有左侧褶边",size=(120,-1))
        self.leftSelvedgeEnableCHK.Enable(False)
        self.leftSelvedgeEnableCHK.SetValue(self.leftSelvedgeEnable)
        hhbox.Add(self.leftSelvedgeEnableCHK,0,wx.TOP,5)
        self.rightSelvedgeEnableCHK = wx.CheckBox(self,label="有右侧褶边",size=(120,-1))
        self.rightSelvedgeEnableCHK.Enable(False)
        self.rightSelvedgeEnableCHK.SetValue(self.rightSelvedgeEnable)
        hhbox.Add(self.rightSelvedgeEnableCHK,0,wx.TOP,5)
        vbox.Add(hhbox, 0, wx.EXPAND)

        vbox.Add((-1,10))

        hhbox=wx.BoxSizer()
        hhbox.Add((5, 1))
        self.rightExtenEnableCHK = wx.CheckBox(self,label="有右侧延伸",size=(120,-1))
        self.rightExtenEnableCHK.Enable(False)
        self.rightExtenEnableCHK.SetValue(self.rightExtendEnable)
        hhbox.Add(self.rightExtenEnableCHK,0,wx.TOP,5)
        self.rightExtendLabel=wx.StaticText(self,label="Y面右侧延伸量：",size=(100,-1))
        self.rightExtendLabel.Show(self.rightExtendEnable)
        hhbox.Add(self.rightExtendLabel,0,wx.TOP,5)
        self.rightExtendTXT = wx.SpinCtrl(self,size=(100,-1),min=1,max=200)
        self.rightExtendTXT.SetValue(self.rightExtendValue)
        self.rightExtendTXT.Show(self.rightExtendEnable)
        self.rightExtendTXT.Enable(False)
        hhbox.Add(self.rightExtendTXT,1,wx.RIGHT,10)
        vbox.Add(hhbox, 0, wx.EXPAND)

        vbox.Add((-1,10))

        hhbox=wx.BoxSizer()
        hhbox.Add((5, 1))
        self.rightBendEnableCHK = wx.CheckBox(self,label="有右侧折弯",size=(120,-1))
        self.rightBendEnableCHK.Enable(False)
        self.rightBendEnableCHK.SetValue(self.rightBendEnable)
        hhbox.Add(self.rightBendEnableCHK,0,wx.TOP,5)
        self.rightBendLabel=wx.StaticText(self,label="Y面右侧折弯量：",size=(100,-1))
        self.rightBendLabel.Show(self.rightBendEnable)
        hhbox.Add(self.rightBendLabel,0,wx.TOP,5)
        self.rightBendTXT = wx.SpinCtrl(self,size=(100,-1),min=1,max=50)
        self.rightBendTXT.Enable(False)
        self.rightBendTXT.SetValue(self.rightBendValue)
        self.rightBendTXT.Show(self.rightBendEnable)
        hhbox.Add(self.rightBendTXT,1,wx.RIGHT,10)
        vbox.Add(hhbox, 0, wx.EXPAND)

        vbox.Add((-1,10))

        hhbox=wx.BoxSizer()
        hhbox.Add((5, 1))
        self.topBendEnableCHK = wx.CheckBox(self,label="有顶部折弯",size=(120,-1))
        self.topBendEnableCHK.Enable(False)
        self.topBendEnableCHK.SetValue(self.topBendEnable)
        hhbox.Add(self.topBendEnableCHK,0,wx.TOP,5)
        self.topBendLabel=wx.StaticText(self,label="Y面顶部折弯量：",size=(100,-1))
        self.topBendLabel.Show(self.topBendEnable)
        hhbox.Add(self.topBendLabel,0,wx.TOP,5)
        self.topBendTXT = wx.SpinCtrl(self,size=(100,-1),min=1,max=50)
        self.topBendTXT.Enable(False)
        self.topBendTXT.SetValue(self.topBendValue)
        self.topBendTXT.Show(self.topBendEnable)
        hhbox.Add(self.topBendTXT,1,wx.RIGHT,10)
        vbox.Add(hhbox, 0, wx.EXPAND)

        vbox.Add((-1,10))

        hhbox = wx.BoxSizer()
        hhbox.Add((5,1))
        self.bottomRaiseEnableCHK = wx.CheckBox(self,label="有Y面底部离地",size=(120,-1))
        self.bottomRaiseEnableCHK.Enable(False)
        self.bottomRaiseEnableCHK.SetValue(self.bottomRaiseEnable)
        hhbox.Add(self.bottomRaiseEnableCHK,0,wx.TOP,5)
        self.bottomRaiseLabel=wx.StaticText(self,label="底部离地高度：",size=(100,-1))
        self.bottomRaiseLabel.Show(self.bottomRaiseEnable)
        hhbox.Add(self.bottomRaiseLabel,0,wx.TOP,5)
        self.bottomRaiseTXT = wx.SpinCtrl(self,size=(100,-1),min=0,max=500)
        self.bottomRaiseTXT.Enable(False)
        self.bottomRaiseTXT.SetValue(self.bottomRaiseValue)
        self.bottomRaiseTXT.Show(self.bottomRaiseEnable)
        hhbox.Add(self.bottomRaiseTXT,1,wx.RIGHT,10)
        vbox.Add(hhbox,0,wx.EXPAND)

        vbox.Add((-1,10))

        hhbox = wx.BoxSizer()
        hhbox.Add((5,1))
        self.bottomBendEnableCHK = wx.CheckBox(self,label="有底部折弯",size=(120,-1))
        self.bottomBendEnableCHK.Enable(False)
        self.bottomBendEnableCHK.SetValue(self.bottomBendEnable)
        hhbox.Add(self.bottomBendEnableCHK,0,wx.TOP,5)
        self.bottomBendLabel=wx.StaticText(self,label="底部折弯量：",size=(100,-1))
        self.bottomBendLabel.Show(self.bottomBendEnable)
        hhbox.Add(self.bottomBendLabel,0,wx.TOP,5)
        self.bottomBendTXT = wx.SpinCtrl(self,size=(100,-1),min=0,max=50)
        self.bottomBendTXT.Enable(False)
        self.bottomBendTXT.SetValue(self.bottomBendValue)
        self.bottomBendTXT.Show(self.bottomBendEnable)
        hhbox.Add(self.bottomBendTXT,1,wx.RIGHT,10)
        vbox.Add(hhbox,0,wx.EXPAND)

        vbox.Add((-1,10))

        hhbox = wx.BoxSizer()
        hhbox.Add((5,1))
        self.bottomBendCutEnableCHK = wx.CheckBox(self,label="有底部折弯裁切",size=(120,-1))
        self.bottomBendCutEnableCHK.Enable(False)
        self.bottomBendCutEnableCHK.SetValue(self.bottomBendCutEnable)
        self.bottomBendCutEnableCHK.Show(self.bottomBendEnable)
        hhbox.Add(self.bottomBendCutEnableCHK,0,wx.TOP,5)
        self.bottomBendCutLabel=wx.StaticText(self,label="底部折弯裁切量：",size=(100,-1))
        self.bottomBendCutLabel.Show(self.bottomBendEnable and self.bottomBendCutEnable)
        hhbox.Add(self.bottomBendCutLabel,0,wx.TOP,5)
        self.bottomBendCutSPIN = wx.SpinCtrl(self,size=(100,-1),min=0,max=100)
        self.bottomBendCutSPIN.Enable(False)
        self.bottomBendCutSPIN.SetValue(self.bottomBendCutValue)
        self.bottomBendCutSPIN.Show(self.bottomBendEnable and self.bottomBendCutEnable)
        hhbox.Add(self.bottomBendCutSPIN,1,wx.RIGHT,10)
        vbox.Add(hhbox,0,wx.EXPAND)

        vbox.Add((-1,10))

        hhbox = wx.BoxSizer()
        hhbox.Add((5,1))
        self.colourEnableCHK = wx.CheckBox(self,label="指定颜色",size=(120,-1))
        self.colourEnableCHK.Enable(False)
        self.colourEnableCHK.SetValue(self.colourEnable)
        hhbox.Add(self.colourEnableCHK,0,wx.TOP,5)
        self.colourLabel=wx.StaticText(self,label="Y面颜色：",size=(100,-1))
        self.colourLabel.Show(self.colourEnable)
        hhbox.Add(self.colourLabel,0,wx.TOP,5)
        self.colourCOMBO = wx.ComboBox(self,choices=["1","2","3","4","5","6","7","8"],size=(100,-1))
        self.colourCOMBO.Enable(False)
        self.colourCOMBO.Show(self.colourEnable)
        hhbox.Add(self.colourCOMBO,1,wx.RIGHT,10)
        vbox.Add(hhbox,0,wx.EXPAND)

        vbox.Add((-1,10))

        hhbox = wx.BoxSizer()
        hhbox.Add((5,1))
        self.materialEnableCHK = wx.CheckBox(self,label="默认材质",size=(120,-1))
        self.materialEnableCHK.Enable(False)
        self.materialEnableCHK.SetValue(self.materialEnable)
        hhbox.Add(self.materialEnableCHK,0,wx.TOP,10)
        self.materialLabel=wx.StaticText(self,label="Y面材质：",size=(60,-1))
        self.materialLabel.Show(self.materialEnable)
        hhbox.Add(self.materialLabel,0,wx.TOP,10)
        self.materialCOMBO = wx.ComboBox(self,choices=[],size=(100,-1))
        self.materialCOMBO.SetValue(self.material)
        self.materialCOMBO.Enable(False)
        self.materialCOMBO.Show(self.materialEnable)
        hhbox.Add(self.materialCOMBO,1,wx.TOP,5)
        vbox.Add(hhbox,0,wx.EXPAND|wx.RIGHT,10)


        self.SetSizer(vbox)
        self.Layout()
        self.Thaw()

class RockWoolParameterShowPanel(wx.Panel):
    def __init__(self,parent,log,wallID):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.log=log
        self.wallID = wallID
        self.leftSlotEnable = False
        self.leftSlotDepthValue = 20
        self.rightSlotEnable = False
        self.rightSlotDepthValue=20
        self.topSlotEnable = False
        self.topSlotDepthValue=0
        self.bottomSlotEnable=False
        self.bottomSlotDepthValue = 0
        self.bottomRaiseEnable = False
        self.bottomRaiseValue = 0

        self.materialEnable = False
        self.material = ""
        self.colourEnable=False
        self.colour=""

        _,result=GetRockWoolParameterByTypeID(self.log,WHICHDB,self.wallID)
        self.leftSlotEnable = True if result[0]=='U' else False
        self.leftSlotDepthValue=result[1]
        self.rightSlotEnable = True if result[2]=='U' else False
        self.rightSlotDepthValue=result[3]
        self.topSlotEnable = True if result[4]=='U' else False
        self.topSlotDepthValue=result[5]
        self.bottomSlotEnable=True if result[6]=='U' else False
        self.bottomSlotDepthValue=result[7]
        self.bottomRaiseEnable=True if result[8]=='U' else False
        self.bottomRaiseValue = result[9]
        if result[10] != "":
            self.materialEnable = True
            self.material = result[10]
        if result[11] != "":
            self.colourEnable = True
            self.colour = result[11]
        self.Freeze()
        vbox = wx.BoxSizer(wx.VERTICAL)

        vbox.Add((-1,10))

        hhbox=wx.BoxSizer()
        hhbox.Add((5, 1))
        self.leftSlotEnableCHK = wx.CheckBox(self,label="有左侧开槽",size=(120,-1))
        self.leftSlotEnableCHK.Enable(False)
        self.leftSlotEnableCHK.SetValue(self.leftSlotEnable)
        hhbox.Add(self.leftSlotEnableCHK,0,wx.TOP,5)
        self.leftSlotLabel=wx.StaticText(self,label="左侧开槽深度：",size=(100,-1))
        self.leftSlotLabel.Show(self.leftSlotEnable)
        hhbox.Add(self.leftSlotLabel,0,wx.TOP,5)
        self.leftSlotDepthSPIN = wx.SpinCtrl(self,size=(100,-1),min=1,max=50)
        self.leftSlotDepthSPIN.SetValue(self.leftSlotDepthValue)
        self.leftSlotDepthSPIN.Show(self.leftSlotEnable)
        self.leftSlotDepthSPIN.Enable(False)
        hhbox.Add(self.leftSlotDepthSPIN,1,wx.RIGHT,10)
        vbox.Add(hhbox, 0, wx.EXPAND)

        vbox.Add((-1,10))

        hhbox=wx.BoxSizer()
        hhbox.Add((5, 1))
        self.rightSlotEnableCHK = wx.CheckBox(self,label="有右侧开槽",size=(120,-1))
        self.rightSlotEnableCHK.Enable(False)
        self.rightSlotEnableCHK.SetValue(self.rightSlotEnable)
        hhbox.Add(self.rightSlotEnableCHK,0,wx.TOP,5)
        self.rightSlotLabel=wx.StaticText(self,label="右侧开槽深度：",size=(100,-1))
        self.rightSlotLabel.Show(self.rightSlotEnable)
        hhbox.Add(self.rightSlotLabel,0,wx.TOP,5)
        self.rightSlotDepthSPIN = wx.SpinCtrl(self,size=(100,-1),min=1,max=50)
        self.rightSlotDepthSPIN.SetValue(self.rightSlotDepthValue)
        self.rightSlotDepthSPIN.Show(self.rightSlotEnable)
        self.rightSlotDepthSPIN.Enable(False)
        hhbox.Add(self.rightSlotDepthSPIN,1,wx.RIGHT,10)
        vbox.Add(hhbox, 0, wx.EXPAND)

        vbox.Add((-1,10))

        hhbox=wx.BoxSizer()
        hhbox.Add((5, 1))
        self.topSlotEnableCHK = wx.CheckBox(self,label="有顶部开槽",size=(120,-1))
        self.topSlotEnableCHK.Enable(False)
        self.topSlotEnableCHK.SetValue(self.topSlotEnable)
        hhbox.Add(self.topSlotEnableCHK,0,wx.TOP,5)
        self.topSlotLabel=wx.StaticText(self,label="顶部开槽深度：",size=(100,-1))
        self.topSlotLabel.Show(self.topSlotEnable)
        hhbox.Add(self.topSlotLabel,0,wx.TOP,5)
        self.topSlotDepthSPIN = wx.SpinCtrl(self,size=(100,-1),min=1,max=50)
        self.topSlotDepthSPIN.Enable(False)
        self.topSlotDepthSPIN.SetValue(self.topSlotDepthValue)
        self.topSlotDepthSPIN.Show(self.topSlotEnable)
        hhbox.Add(self.topSlotDepthSPIN,1,wx.RIGHT,10)
        vbox.Add(hhbox, 0, wx.EXPAND)

        vbox.Add((-1,10))

        hhbox = wx.BoxSizer()
        hhbox.Add((5,1))
        self.bottomRaiseEnableCHK = wx.CheckBox(self,label="有Y面底部离地",size=(120,-1))
        self.bottomRaiseEnableCHK.Enable(False)
        self.bottomRaiseEnableCHK.SetValue(self.bottomRaiseEnable)
        hhbox.Add(self.bottomRaiseEnableCHK,0,wx.TOP,5)
        self.bottomRaiseLabel=wx.StaticText(self,label="底部离地高度：",size=(100,-1))
        self.bottomRaiseLabel.Show(self.bottomRaiseEnable)
        hhbox.Add(self.bottomRaiseLabel,0,wx.TOP,5)
        self.bottomRaiseTXT = wx.SpinCtrl(self,size=(100,-1),min=0,max=500)
        self.bottomRaiseTXT.Enable(False)
        self.bottomRaiseTXT.SetValue(self.bottomRaiseValue)
        self.bottomRaiseTXT.Show(self.bottomRaiseEnable)
        hhbox.Add(self.bottomRaiseTXT,1,wx.RIGHT,10)
        vbox.Add(hhbox,0,wx.EXPAND)

        vbox.Add((-1,10))

        hhbox = wx.BoxSizer()
        hhbox.Add((5,1))
        self.colourEnableCHK = wx.CheckBox(self,label="指定颜色",size=(120,-1))
        self.colourEnableCHK.Enable(False)
        self.colourEnableCHK.SetValue(self.colourEnable)
        hhbox.Add(self.colourEnableCHK,0,wx.TOP,5)
        self.colourLabel=wx.StaticText(self,label="Y面颜色：",size=(100,-1))
        self.colourLabel.Show(self.colourEnable)
        hhbox.Add(self.colourLabel,0,wx.TOP,5)
        self.colourCOMBO = wx.ComboBox(self,choices=["1","2","3","4","5","6","7","8"],size=(100,-1))
        self.colourCOMBO.Enable(False)
        self.colourCOMBO.Show(self.colourEnable)
        hhbox.Add(self.colourCOMBO,1,wx.RIGHT,10)
        vbox.Add(hhbox,0,wx.EXPAND)

        vbox.Add((-1,10))

        hhbox = wx.BoxSizer()
        hhbox.Add((5,1))
        self.materialEnableCHK = wx.CheckBox(self,label="默认材质",size=(120,-1))
        self.materialEnableCHK.Enable(False)
        self.materialEnableCHK.SetValue(self.materialEnable)
        hhbox.Add(self.materialEnableCHK,0,wx.TOP,10)
        self.materialLabel=wx.StaticText(self,label="Y面材质：",size=(60,-1))
        self.materialLabel.Show(self.materialEnable)
        hhbox.Add(self.materialLabel,0,wx.TOP,10)
        self.materialCOMBO = wx.ComboBox(self,choices=[],size=(100,-1))
        self.materialCOMBO.SetValue(self.material)
        self.materialCOMBO.Enable(False)
        self.materialCOMBO.Show(self.materialEnable)
        hhbox.Add(self.materialCOMBO,1,wx.TOP,5)
        vbox.Add(hhbox,0,wx.EXPAND|wx.RIGHT,10)


        self.SetSizer(vbox)
        self.Layout()
        self.Thaw()

class ReinforcementParameterShowPanel(wx.Panel):
    def __init__(self,parent,log,wallID):
        wx.Panel.__init__(self, parent)
        self.parent = parent
        self.log=log
        self.wallID = wallID
        self.bottomReinforcementEnable = False
        self.reiforcementA = 0
        self.reiforcementB = 0
        self.bottomX1 = 0
        self.bottomX2 = 0
        self.middleReinforcementEnable = False
        self.reiforcementC = 0
        self.reiforcementD = 0
        self.middleX1 = 0
        self.middleX2 = 0
        self.topReinforcementEnable = False
        self.reiforcementE = 0
        self.reiforcementF = 0
        self.middleX1 = 0
        self.middleX2 = 0

        self.materialEnable = False
        self.material = ""
        self.colourEnable=False
        self.colour=""

        _,result=GetReinforcementParameterByTypeID(self.log,WHICHDB,self.wallID)
        self.leftSlotEnable = True if result[0]=='U' else False
        self.leftSlotDepthValue=result[1]
        self.rightSlotEnable = True if result[2]=='U' else False
        self.rightSlotDepthValue=result[3]
        self.topSlotEnable = True if result[4]=='U' else False
        self.topSlotDepthValue=result[5]
        self.bottomSlotEnable=True if result[6]=='U' else False
        self.bottomSlotDepthValue=result[7]
        self.bottomRaiseEnable=True if result[8]=='U' else False
        self.bottomRaiseValue = result[9]
        if result[10] != "":
            self.materialEnable = True
            self.material = result[10]
        if result[11] != "":
            self.colourEnable = True
            self.colour = result[11]
        self.Freeze()
        vbox = wx.BoxSizer(wx.VERTICAL)

        vbox.Add((-1,10))

        hhbox=wx.BoxSizer()
        hhbox.Add((5, 1))
        self.leftSlotEnableCHK = wx.CheckBox(self,label="有左侧开槽",size=(120,-1))
        self.leftSlotEnableCHK.Enable(False)
        self.leftSlotEnableCHK.SetValue(self.leftSlotEnable)
        hhbox.Add(self.leftSlotEnableCHK,0,wx.TOP,5)
        self.leftSlotLabel=wx.StaticText(self,label="左侧开槽深度：",size=(100,-1))
        self.leftSlotLabel.Show(self.leftSlotEnable)
        hhbox.Add(self.leftSlotLabel,0,wx.TOP,5)
        self.leftSlotDepthSPIN = wx.SpinCtrl(self,size=(100,-1),min=1,max=50)
        self.leftSlotDepthSPIN.SetValue(self.leftSlotDepthValue)
        self.leftSlotDepthSPIN.Show(self.leftSlotEnable)
        self.leftSlotDepthSPIN.Enable(False)
        hhbox.Add(self.leftSlotDepthSPIN,1,wx.RIGHT,10)
        vbox.Add(hhbox, 0, wx.EXPAND)

        vbox.Add((-1,10))

        hhbox=wx.BoxSizer()
        hhbox.Add((5, 1))
        self.rightSlotEnableCHK = wx.CheckBox(self,label="有右侧开槽",size=(120,-1))
        self.rightSlotEnableCHK.Enable(False)
        self.rightSlotEnableCHK.SetValue(self.rightSlotEnable)
        hhbox.Add(self.rightSlotEnableCHK,0,wx.TOP,5)
        self.rightSlotLabel=wx.StaticText(self,label="右侧开槽深度：",size=(100,-1))
        self.rightSlotLabel.Show(self.rightSlotEnable)
        hhbox.Add(self.rightSlotLabel,0,wx.TOP,5)
        self.rightSlotDepthSPIN = wx.SpinCtrl(self,size=(100,-1),min=1,max=50)
        self.rightSlotDepthSPIN.SetValue(self.rightSlotDepthValue)
        self.rightSlotDepthSPIN.Show(self.rightSlotEnable)
        self.rightSlotDepthSPIN.Enable(False)
        hhbox.Add(self.rightSlotDepthSPIN,1,wx.RIGHT,10)
        vbox.Add(hhbox, 0, wx.EXPAND)

        vbox.Add((-1,10))

        hhbox=wx.BoxSizer()
        hhbox.Add((5, 1))
        self.topSlotEnableCHK = wx.CheckBox(self,label="有顶部开槽",size=(120,-1))
        self.topSlotEnableCHK.Enable(False)
        self.topSlotEnableCHK.SetValue(self.topSlotEnable)
        hhbox.Add(self.topSlotEnableCHK,0,wx.TOP,5)
        self.topSlotLabel=wx.StaticText(self,label="顶部开槽深度：",size=(100,-1))
        self.topSlotLabel.Show(self.topSlotEnable)
        hhbox.Add(self.topSlotLabel,0,wx.TOP,5)
        self.topSlotDepthSPIN = wx.SpinCtrl(self,size=(100,-1),min=1,max=50)
        self.topSlotDepthSPIN.Enable(False)
        self.topSlotDepthSPIN.SetValue(self.topSlotDepthValue)
        self.topSlotDepthSPIN.Show(self.topSlotEnable)
        hhbox.Add(self.topSlotDepthSPIN,1,wx.RIGHT,10)
        vbox.Add(hhbox, 0, wx.EXPAND)

        vbox.Add((-1,10))

        hhbox = wx.BoxSizer()
        hhbox.Add((5,1))
        self.bottomRaiseEnableCHK = wx.CheckBox(self,label="有Y面底部离地",size=(120,-1))
        self.bottomRaiseEnableCHK.Enable(False)
        self.bottomRaiseEnableCHK.SetValue(self.bottomRaiseEnable)
        hhbox.Add(self.bottomRaiseEnableCHK,0,wx.TOP,5)
        self.bottomRaiseLabel=wx.StaticText(self,label="底部离地高度：",size=(100,-1))
        self.bottomRaiseLabel.Show(self.bottomRaiseEnable)
        hhbox.Add(self.bottomRaiseLabel,0,wx.TOP,5)
        self.bottomRaiseTXT = wx.SpinCtrl(self,size=(100,-1),min=0,max=500)
        self.bottomRaiseTXT.Enable(False)
        self.bottomRaiseTXT.SetValue(self.bottomRaiseValue)
        self.bottomRaiseTXT.Show(self.bottomRaiseEnable)
        hhbox.Add(self.bottomRaiseTXT,1,wx.RIGHT,10)
        vbox.Add(hhbox,0,wx.EXPAND)

        vbox.Add((-1,10))

        hhbox = wx.BoxSizer()
        hhbox.Add((5,1))
        self.colourEnableCHK = wx.CheckBox(self,label="指定颜色",size=(120,-1))
        self.colourEnableCHK.Enable(False)
        self.colourEnableCHK.SetValue(self.colourEnable)
        hhbox.Add(self.colourEnableCHK,0,wx.TOP,5)
        self.colourLabel=wx.StaticText(self,label="Y面颜色：",size=(100,-1))
        self.colourLabel.Show(self.colourEnable)
        hhbox.Add(self.colourLabel,0,wx.TOP,5)
        self.colourCOMBO = wx.ComboBox(self,choices=["1","2","3","4","5","6","7","8"],size=(100,-1))
        self.colourCOMBO.Enable(False)
        self.colourCOMBO.Show(self.colourEnable)
        hhbox.Add(self.colourCOMBO,1,wx.RIGHT,10)
        vbox.Add(hhbox,0,wx.EXPAND)

        vbox.Add((-1,10))

        hhbox = wx.BoxSizer()
        hhbox.Add((5,1))
        self.materialEnableCHK = wx.CheckBox(self,label="默认材质",size=(120,-1))
        self.materialEnableCHK.Enable(False)
        self.materialEnableCHK.SetValue(self.materialEnable)
        hhbox.Add(self.materialEnableCHK,0,wx.TOP,10)
        self.materialLabel=wx.StaticText(self,label="Y面材质：",size=(60,-1))
        self.materialLabel.Show(self.materialEnable)
        hhbox.Add(self.materialLabel,0,wx.TOP,10)
        self.materialCOMBO = wx.ComboBox(self,choices=[],size=(100,-1))
        self.materialCOMBO.SetValue(self.material)
        self.materialCOMBO.Enable(False)
        self.materialCOMBO.Show(self.materialEnable)
        hhbox.Add(self.materialCOMBO,1,wx.TOP,5)
        vbox.Add(hhbox,0,wx.EXPAND|wx.RIGHT,10)


        self.SetSizer(vbox)
        self.Layout()
        self.Thaw()

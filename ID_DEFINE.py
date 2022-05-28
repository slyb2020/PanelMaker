#!/usr/bin/env python
# encoding: utf-8
"""
@author: slyb
@license: (C) Copyright 2017-2020, 天津定智科技有限公司.
@contact: slyb@tju.edu.cn
@file: ID_DEFINE.py.py
@time: 2019/6/16 15:23
@desc:
"""
import wx
import os

SYSTEMNAME = "生产图纸综合管理系统"
VERSION_STRING = "20220206A"

dirName = os.path.dirname(os.path.abspath(__file__))
bitmapDir = os.path.join(dirName, 'bitmaps\\')
previewDir = os.path.join(dirName, 'bitmaps\\Preview\\')
scheduleDir = os.path.join(dirName, '工单\\')
bluePrintDir = os.path.join(dirName, 'Stena 生产图纸\\')
gifDir = os.path.join(dirName,'gif\\')
# sys.path.append(os.path.split(dirName)[0])

WHICHDB = 1

dbHostName = ["127.0.0.1",'127.0.0.1']
dbUserName = ['root','root']
dbPassword = ['','']
dbName = ['智能生产管理系统','智能生产管理系统_调试']
orderDBName = ['订单数据库','订单数据库_调试']
# boxDBName = ['货盘数据库','货盘数据库_调试']
packageDBName = ['货盘数据库','货盘数据库']

MENU_CHECK_IN = wx.NewIdRef()
MENU_CHECK_OUT = wx.NewIdRef()
MENU_STYLE_DEFAULT = wx.NewIdRef()
MENU_STYLE_XP = wx.NewIdRef()
MENU_STYLE_2007 = wx.NewIdRef()
MENU_STYLE_VISTA = wx.NewIdRef()
MENU_STYLE_MY = wx.NewIdRef()
MENU_USE_CUSTOM = wx.NewIdRef()
MENU_LCD_MONITOR = wx.NewIdRef()
MENU_HELP = wx.NewIdRef()
MENU_DISABLE_MENU_ITEM = wx.NewIdRef()
MENU_REMOVE_MENU = wx.NewIdRef()
MENU_TRANSPARENCY = wx.NewIdRef()
MENU_NEW_FILE = 10005
MENU_SAVE = 10006
MENU_OPEN_FILE = 10007
MENU_NEW_FOLDER = 10008
MENU_COPY = 10009
MENU_CUT = 10010
MENU_PASTE = 10011
ID_WINDOW_LEFT = wx.NewId()
ID_WINDOW_BOTTOM = wx.NewId()

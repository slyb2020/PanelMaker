from ID_DEFINE import *
import pymysql as MySQLdb
import time
import datetime
import json

def GetWallIDList(log, whichDB, wallType):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `墙板型号`  from `solidworks墙板配置信息表` where `墙板类型` = '%s' """%wallType
    cursor.execute(sql)
    temp = cursor.fetchall()  # 获得压条信息
    db.close()
    result=[]
    for i in temp:
        result.append(i[0])
    return 0, result

def GetWallStructureByWallID(log, whichDB, wallID):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `X面型号`,`Y面型号`,`Z面型号`,`V面型号`,`构件型号列表`,`岩棉型号`,`加强板型号`  from `solidworks墙板配置信息表` where `墙板型号` = '%s' """%wallID
    cursor.execute(sql)
    temp = cursor.fetchone()  # 获得压条信息
    db.close()
    return 0, temp

def GetSurfaceXParameterByTypeID(log, whichDB,typeID):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `X面左侧折弯使能`,`X面左侧折弯量`,`X面右侧折弯使能`,`X面右侧折弯量`,`X面顶部折弯使能`,`X面顶部折弯量`,`X面底部折弯使能`,`X面底部折弯量`,`X面底部折弯切除使能`,`X面底部折弯切除量`,`X面材质`,`X面颜色`  from `solidworksx面配置信息表` where `型号` = '%s' """%typeID
    cursor.execute(sql)
    temp = cursor.fetchone()  # 获得压条信息
    db.close()
    return 0, temp

def GetSurfaceYParameterByTypeID(log, whichDB,typeID):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `Y面左侧折弯使能`,`Y面左侧折弯量`,`Y面右侧折弯使能`,`Y面右侧折弯量`,`Y面顶部折弯使能`,`Y面顶部折弯量`,
    `Y面底部折弯使能`,`Y面底部折弯量`,`Y面底部折弯切除使能`,`Y面底部折弯切除量`,`Y面左侧延伸使能`,`Y面左侧延伸量`,
    `Y面右侧延伸使能`,`Y面右侧延伸量`,`Y面左侧褶边使能`,`Y面右侧褶边使能`,`Y面底部离地使能`,`Y面底部离地高度`,`Y面材质`,`Y面颜色`  from `solidworksY面配置信息表` where `型号` = '%s' """%typeID
    cursor.execute(sql)
    temp = cursor.fetchone()  # 获得压条信息
    db.close()
    return 0, temp

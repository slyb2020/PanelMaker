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

def GetRockWoolParameterByTypeID(log, whichDB,typeID):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `左侧开槽使能`,`左侧开槽深度`,`右侧开槽使能`,`右侧开槽深度`,`顶部开槽使能`,`顶部开槽深度`,
    `底部开槽使能`,`底部开槽深度`,`底部离地使能`,`底部离地高度`,`材质`,`颜色`  from `solidworks岩棉配置信息表` where `型号` = '%s' """%typeID
    cursor.execute(sql)
    temp = cursor.fetchone()  # 获得压条信息
    db.close()
    return 0, temp

def GetReinforcementParameterByTypeID(log, whichDB,typeID):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    sql = """SELECT `底部加强板使能`,`中部加强板使能`,`顶部加强板使能`,`a`,`b`,`c`,`d`,`e`,`f`,
    `底部X1`,`底部X2`,`中部X1`,`中部X2`,`顶部X1`,`顶部X2`,`材质`,`颜色`  from `solidworks加强板配置信息表` where `型号` = '%s' """%typeID
    cursor.execute(sql)
    temp = cursor.fetchone()  # 获得压条信息
    db.close()
    return 0, temp

def InsertWallInfoToDB(log,whichDB,page):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    wallType = page.wallType
    wallID = "A.%s.%04d"%(wallType,int(page.wallID))
    xType = wallID if page.surfaceXEnable else ""
    yType = wallID if page.surfaceYEnable else ""
    zType = wallID if page.surfaceZEnable else ""
    vType = wallID if page.surfaceVEnable else ""
    constructionTypeList = ""
    rockwoolType = wallID if page.rockWoolEnable else ""
    reinforcementType = wallID if page.reinforcementEnable else ""

    sql = "INSERT INTO `solidworks墙板配置信息表`(`墙板类型`,`墙板型号`,`X面型号`,`Y面型号`,`Z面型号`,`V面型号`,`构件型号列表`,`岩棉型号`,`加强板型号`)" \
                                        "VALUES ('%s',    '%s',     '%s'    ,'%s'   ,'%s'    ,'%s'     ,'%s'       ,'%s'      ,'%s')"\
                                          % (wallType,wallID,xType,yType,zType,vType,constructionTypeList,rockwoolType,reinforcementType)
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        db.rollback()
        print("error")
    db.close()

def InsertSurfaceXInfoToDB(log,whichDB,page):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    wallType = page.wallType
    wallID = "A.%s.%04d"%(wallType,int(page.wallID))
    leftBendEnable = "U" if page.leftBendEnable else "S"
    leftBendValue = page.leftBendValue if page.leftBendEnable else 0
    rightBendEnable = "U" if page.rightBendEnable else "S"
    rightBendValue = page.rightBendValue if page.rightBendEnable else 0
    bottomBendEnable = "U" if page.bottomBendEnable else "S"
    bottomBendValue = page.bottomBendValue if page.bottomBendEnable else 0
    bottomBendCutEnable = "U" if page.bottomBendCutEnable else "S"
    bottomBendCutValue = page.bottomBendCutValue if page.bottomBendCutEnable else 0
    topBendEnable = "U" if page.topBendEnable else "S"
    topBendValue = page.topBendValue if page.topBendEnable else 0
    material = page.material
    colour = page.colour
    sql = "INSERT INTO `solidworksx面配置信息表`(`类型`,`型号`,`X面左侧折弯使能`,`X面左侧折弯量`,`X面右侧折弯使能`,`X面右侧折弯量`," \
          "`X面顶部折弯使能`,`X面顶部折弯量`,`X面底部折弯使能`,`X面底部折弯量`,`X面底部折弯切除使能`,`X面底部折弯切除量`,`X面材质`,`X面颜色`)" \
            "VALUES ('%s','%s','%s',%s,'%s',%s,'%s',%s,'%s',%s,'%s',%s,'%s','%s')"\
            % (wallType,wallID,leftBendEnable,leftBendValue,rightBendEnable,rightBendValue,topBendEnable,topBendValue,
               bottomBendEnable,bottomBendValue,bottomBendCutEnable,bottomBendCutValue,material,colour)
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        db.rollback()
        print("error")
    db.close()

def InsertSurfaceYInfoToDB(log,whichDB,page):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    wallType = page.wallType
    wallID = "A.%s.%04d"%(wallType,int(page.wallID))
    leftBendEnable = 'U' if page.leftBendEnable else 'S'
    leftBendValue = page.leftBendValue if page.leftBendEnable else 0
    rightBendEnable = 'U' if page.rightBendEnable else 'S'
    rightBendValue = page.rightBendValue if page.rightBendEnable else 0
    topBendEnable = 'U' if page.topBendEnable else 'S'
    topBendValue = page.topBendValue if page.topBendEnable else 0
    bottomBendEnable = 'U' if page.bottomBendEnable else 'S'
    bottomBendValue = page.bottomBendValue if page.bottomBendEnable else 0
    bottomBendCutEnable = 'U' if page.bottomBendCutEnable else 'S'
    bottomBendCutValue = page.bottomBendCutValue if page.bottomBendCutEnable else 0
    leftExtendEnable = 'U' if page.leftExtendEnable else 'S'
    leftExtendValue = page.leftExtendValue if page.leftExtendEnable else 0
    rightExtendEnable = 'U' if page.rightExtendEnable else 'S'
    rightExtendValue = page.rightExtendValue if page.rightExtendEnable else 0
    leftSelvedgeEnable = 'U' if page.leftSelvedgeEnable else 'S'
    rightSelvedgeEnable = 'U' if page.rightSelvedgeEnable else 'S'
    bottomRaiseEnable = 'U' if page.bottomRaiseEnable else 'S'
    bottomRaiseValue = page.bottomRaiseValue if page.bottomRaiseEnable else 0
    material = page.material
    colour = page.colour
    sql = "INSERT INTO `solidworksy面配置信息表`(`类型`,`型号`,`Y面左侧折弯使能`,`Y面左侧折弯量`,`Y面右侧折弯使能`,`Y面右侧折弯量`," \
          "`Y面顶部折弯使能`,`Y面顶部折弯量`,`Y面底部折弯使能`,`Y面底部折弯量`,`Y面底部折弯切除使能`,`Y面底部折弯切除量`,`Y面材质`,`Y面颜色`," \
          "`Y面左侧延伸使能`,`Y面左侧延伸量`,`Y面右侧延伸使能`,`Y面右侧延伸量`,`Y面左侧褶边使能`,`Y面右侧褶边使能`,`Y面底部离地使能`,`Y面底部离地高度`)" \
            "VALUES ('%s','%s','%s',%s,'%s',%s," \
          "'%s',%s,'%s',%s,'%s',%s,'%s','%s'," \
          "'%s',%s,'%s',%s,'%s','%s','%s',%s)"\
            % (wallType,wallID,leftBendEnable,leftBendValue,rightBendEnable,rightBendValue,topBendEnable,topBendValue,
               bottomBendEnable,bottomBendValue,bottomBendCutEnable,bottomBendCutValue,material,colour,
               leftExtendEnable,leftExtendValue,rightExtendEnable,rightExtendValue,leftSelvedgeEnable,rightSelvedgeEnable,bottomRaiseEnable,bottomRaiseValue)
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        db.rollback()
        print("error")
    db.close()

def InsertRockWoolInfoToDB(log,whichDB,page):
    try:
        db = MySQLdb.connect(host="%s" % dbHostName[whichDB], user='%s' % dbUserName[whichDB],
                             passwd='%s' % dbPassword[whichDB], db='%s' % dbName[whichDB], charset='utf8')
    except:
        wx.MessageBox("无法连接%s!" % dbName[whichDB], "错误信息")
        if log:
            log.WriteText("无法连接%s!" % dbName[whichDB], colour=wx.RED)
        return -1, []
    cursor = db.cursor()
    wallType = page.wallType
    wallID = "A.%s.%04d"%(wallType,int(page.wallID))

    leftSlotEnable = "U" if page.leftSlotEnable else "S"
    leftSlotValue = page.leftSlotDepthValue if page.leftSlotEnable else 0
    rightSlotEnable = "U" if page.rightSlotEnable else "S"
    rightSlotValue = page.rightSlotDepthValue if page.rightSlotEnable else 0
    topSlotEnable = "U" if page.topSlotEnable else "S"
    topSlotValue = page.topSlotDepthValue if page.topSlotEnable else 0
    bottomSlotEnable = "U" if page.bottomSlotEnable else "S"
    bottomSlotValue = page.bottomSlotDepthValue if page.bottomSlotEnable else 0
    bottomRaiseEnable = "U" if page.bottomRaiseEnable else "S"
    bottomRaiseValue = page.bottomRaiseValue if page.bottomRaiseEnable else 0
    material = page.material
    colour = page.colour
    sql = "INSERT INTO `solidworks岩棉配置信息表`(`类型`,`型号`,`左侧开槽使能`,`左侧开槽深度`,`右侧开槽使能`,`右侧开槽深度`," \
          "`顶部开槽使能`,`顶部开槽深度`,`底部开槽使能`,`底部开槽深度`,`底部离地使能`,`底部离地高度`,`材质`,`颜色`)" \
            "VALUES ('%s','%s','%s',%s,'%s',%s,'%s',%s,'%s',%s,'%s',%s,'%s','%s')"\
            % (wallType,wallID,leftSlotEnable,leftSlotValue,rightSlotEnable,rightSlotValue,topSlotEnable,topSlotValue,
               bottomSlotEnable,bottomSlotValue,bottomRaiseEnable,bottomRaiseValue,material,colour)
    try:
        cursor.execute(sql)
        db.commit()  # 必须有，没有的话插入语句不会执行
    except:
        db.rollback()
        print("error")
    db.close()


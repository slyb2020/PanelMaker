import pandas as pd
import openpyxl
import wx
import wx.grid as gridlib
import numpy as np

def GetSheetNameListFromExcelFileName(fileName):
    wb = openpyxl.load_workbook(fileName)
    sheets = wb.worksheets
    result = []
    for sheet in sheets:
        result.append(sheet.title)
    return result

def GetSheetDataFromExcelFileName(fileName,sheetName):
    wb = openpyxl.load_workbook(fileName)
    ws = wb.get_sheet_by_name(sheetName)
    data = []
    for row in ws.values:
        temp=[]
        for value in row:
            temp.append(value)
        data.append(temp)
    data = np.array(data)
    return data

def ModifySurfaceXConfigurationExcelFile(leftEnable,leftBendValue,rightEnable,rightBendValue,bottomEnable,bottomBendValue,bottomCutEnable,bottomBendCutValue):
    wb = openpyxl.load_workbook("D:\\WorkSpace\\Solidworks\\N.2SA\\SurfaceXSLDPRT.xlsx")
    ws = wb.get_sheet_by_name("Sheet1")
    ws['G3'] = 'U' if leftEnable else "S"
    ws['H3'] = 'U' if rightEnable else "S"
    ws['E3'] = 'U' if bottomEnable else "S"
    ws['F3'] = 'U' if bottomCutEnable else "S"
    ws['I3'] = bottomBendCutValue if bottomCutEnable and bottomCutEnable else 0
    ws['J3'] = bottomBendValue if bottomCutEnable else 0
    ws['K3'] = leftBendValue if leftEnable else 0
    ws['L3'] = rightBendValue if rightEnable else 0
    wb.save('D:\\WorkSpace\\Solidworks\\N.2SA\\SurfaceXSLDPRT.xlsx')
# -*- coding: utf-8 -*-
"""
UpgradeDate:2023-07-28

Author: Zhihao Cao
Paper: Detecting Latent Causation in Time Series
"""
import numpy as np
import xlrd

#print("Import ulils.py")
# SingleVariable embedding
# The number of embedded points = Lenth-E+1 
def MyEmbed_SingleVariable(input,embed_e,tau):
    x = input
    tau = tau
    embed_e = embed_e
    lenth = len(x)-embed_e+1+(1-tau)
    x_tilde = [0] * lenth
    for i in range(lenth):
        x_tilde[i]=[x[i]]                     
        for i2 in range(embed_e-1):
            x_tilde[i].append(x[i2+i+tau])
    return x_tilde

# MultiVariable embedding
# Use supplementary information in embeding process
def MyEmbed_MultiVariable(input,input2,embed_e,tau):
    x = input
    y = input2
    tau = tau
    embed_e = embed_e
    
    lenth = len(x)-embed_e+1+(1-tau)
    x_tilde = [0] * lenth
    for i in range(lenth):
        x_tilde[i]=[x[i]]                     
        for i2 in range(embed_e-1):
            x_tilde[i].append(x[i2+i+tau])
        x_tilde[i].append(y[i])      
    return x_tilde

# Normalization, compress all data to 0-1
def Norm(list):
    list_np = np.array(list)
    list_norm = (list_np - min(list_np))/(max(list_np)-min(list_np))
    return list_norm

# ECCM algorithm considering time lag, not used in this paper
def LagTransformation(lag,x_all):
    # if lag is either possitive or 0 
    if(lag >=0):
        # delete previous data
        del x_all[0:lag]  
        # complement the deleted data with 0
        for i in range(lag):
            x_all.append(0.0)
        return x_all
    # if lag is nagetive 
    else:
        lag_poss = -lag
        # insert data in the front
        for i in range(lag_poss):
            x_all.insert(0,0.0)
        # delete data in the rear    
        del x_all[-lag_poss:] 
        return x_all
'''   
# For module test 
testdata = [1,2,3,4,5,6,7,8,9,10]
testdata2 = [11,12,13,14,15,16,17,18,19,20]
reslut = MyEmbed_MultiVariable(testdata,testdata2,4,tau=1)
reslut2 = np.array(reslut)
'''

def MyReadxlsx(path,libsize_all,column_x,column_y):
    #needed to ajust according to the real data
    #file path
    #path = 'D:\Project\Python\MyCCM\ESM3_Data_moran.xlsx'
    #book=xlrd.open_workbook('D:\Project\Python\CCM\Edata(summer).xlsx') 
    book=xlrd.open_workbook(path) 
    sheet=book.sheet_by_index(0)
    #get data to analysis from .xlsx file according column
    column_x = column_x        #note it starts from 0 not 1, the causes
    column_y = column_y       #results

    #label in diagram shown
    label_1 = sheet.cell(0,column_y).value+"  →  "+sheet.cell(0,column_x).value
    #label_2 = sheet.cell(0,column_x).value+"  →  "+sheet.cell(0,column_y).value

    #the label(name) of data
    column_x_label = sheet.cell(0,column_x).value
    column_y_label = sheet.cell(0,column_y).value

    x_all = []  #list to store the X   
    y_all = []  #list to store the Y      
    for n in range(1,libsize_all):
        x_all.append(sheet.cell(n,column_x).value)   
        y_all.append(sheet.cell(n,column_y).value)
    return x_all,y_all,label_1,column_x_label,column_y_label

def MyReadxlsx2(path,libsize_all,column_x,column_y,column_s):
    #needed to ajust according to the real data
    #file path
    #path = 'D:\Project\Python\MyCCM\ESM3_Data_moran.xlsx'
    #book=xlrd.open_workbook('D:\Project\Python\CCM\Edata(summer).xlsx') 
    book=xlrd.open_workbook(path) 
    sheet=book.sheet_by_index(0)
    #get data to analysis from .xlsx file according column
    column_x = column_x        #note it starts from 0 not 1, the causes
    column_y = column_y       #results
    column_s = column_s
    #label in diagram shown
    #label_1 = sheet.cell(0,column_y).value+"  →  "+sheet.cell(0,column_x).value
    #label_2 = sheet.cell(0,column_x).value+"  →  "+sheet.cell(0,column_y).value

    #the label(name) of data
    column_x_label = sheet.cell(0,column_x).value
    column_y_label = sheet.cell(0,column_y).value
    column_s_label = sheet.cell(0,column_s).value
    
    x_all = []  #list to store the X   
    y_all = []  #list to store the Y
    s_all = []  
    for n in range(1,libsize_all):
        x_all.append(sheet.cell(n,column_x).value)   
        y_all.append(sheet.cell(n,column_y).value)
        s_all.append(sheet.cell(n,column_s).value)
    return x_all,y_all,s_all,column_x_label,column_y_label,column_s_label
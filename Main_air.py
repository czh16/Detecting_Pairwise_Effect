# -*- coding: utf-8 -*-
"""
UpgradeDate:2023-07-28

Author: Zhihao Cao
Paper: Detecting Latent Causation in Time Series
"""

import numpy as np
from numpy import *
import xlrd
import matplotlib.pyplot as plt
import pandas as pd
import math

import sys
# Add *.py to searching path for Spyder
sys.path.append("paper/paper3")     

import utils

# Ues X to predict Y (Y ——> X), denoted as Y|Mx
# Ues X + S to predict Y, denoted as Y|Mx+s
def CCM_forward(x_all,y_all,sup_all,lib,embed_e,tau):
    # lib： lenth of X data to reconstruct the Manifold
    libsize = lib 
    # embed_e: embedding dimension E
    embed_e = embed_e
    # tau: time lag when sampling
    tau = tau   
           
    x = x_all       #list to store the result X
    x = x[0:lib]
    y = y_all       #list to store the reason Y
    y = y[0:lib]
    s = sup_all     #list to store the supplemental factor S
    s = s[0:lib]
    
    y_hat=[]                                  #The predicted Y (^y)
    
    lenth = len(x)-embed_e+1+(1-tau)          #the number of state points in M
    lenth_all = len(x_all)-embed_e+1+(1-tau)
    
    y_tilde = [0] * lenth                     #there is just one dimension
    x_tilde_all = [0] * libsize_all
    y_tilde_all = [0] * libsize_all    
    
    # MultiVariable embedding X + S
    x_tilde = utils.MyEmbed_MultiVariable(x,s,embed_e,tau)
    # SingleVariable embedding
    y_tilde = utils.MyEmbed_SingleVariable(y,embed_e,tau)
    
    # x_tilde_all = utils.MyEmbed(x_all,embed_e,tau)
    x_tilde_all = utils.MyEmbed_MultiVariable(x_all,sup_all,embed_e,tau)
    y_tilde_all = utils.MyEmbed_SingleVariable(y_all,embed_e,tau)
    
    # Euclidean distance Matrix of state points in M
    # lenth_all*lenth, initialize to 0 for all elements
    # Only X limited in sampling lenth is used here
    dist_x = np.mat(np.zeros((lenth_all,lenth)))    
                                                    
    # Calculate the Euclidean distances between every two state points
    for h in range(lenth_all):
        for w in range(lenth):
            # Using 2-norm function                   
            dist_x[h,w] = np.linalg.norm(np.array(x_tilde_all[h]) - np.array(x_tilde[w]))
            
    # Transition form Matrix to List, size = lenth_all*lenth
    dist_x_list = dist_x.tolist()                                                          
    dist_x_list_sort = dist_x_list.copy()
    
    # Index of neighboring points 
    # Structure: [[..],
    #             [..],
    #              ...,
    #             [..]]
    t_x = []                                      
    for t_i in range(lenth_all):
        # t_i refer to the index in distance list                   
        dist_x_list_sort[t_i] = sorted(dist_x_list[t_i])         
        t_n = []
        # From 1 to embed_e+2-1. Not from 0 as 0 refer pint itself
        # The number of neighboring point number is set to e+1
        for t_n_i in range(1, embed_e + 2):        
            t_n.append(dist_x_list[t_i].index(dist_x_list_sort[t_i][t_n_i]))
        t_x.append(t_n)                         
    
    for hat_i in range(lenth_all):
        #sum = 0
        sum_distance = 0
        sum_by_weight = 0
        # Prevent dividing by 0
        shortest_distance =  dist_x_list_sort[hat_i][1] + 0.00001
        # Loop to compute the weighted distance based on the e+1 points
        for i_loop_for_sum in range(embed_e+1):
            #sum = sum + np.array(y_tilde[t_x[hat_i][i_loop_for_sum]])            
            i_distance = dist_x_list_sort[hat_i][i_loop_for_sum+1]            
            #print(i_distance)
            sum_distance = sum_distance + math.exp(-i_distance/shortest_distance)      
        for i_loop_for_weight in range(embed_e+1):
            i_distance = dist_x_list_sort[hat_i][i_loop_for_weight+1]     
            weight =  math.exp(-i_distance/shortest_distance)/sum_distance
            #The sum of all weights in one loop is 1
            #print(weight)           
            sum_by_weight = sum_by_weight + weight*np.array(y_tilde[t_x[hat_i][i_loop_for_weight]])
        
        result = sum_by_weight
        # The predicted y_hat which includes a series of state points
        # Row: lenth 
        # Column: embed_e
        y_hat.append(result)  
                 
    # Calculate the correlation coefficient                                               
    def CalculateRho(y_hat,y_tilde):          
        # Using Pandas package to calculate Rho
        series_y_hat_lastpoint = []
        series_y_tilde_lastpoint = []
        for i_mean in range(len(y_hat)):
            # Last item is used for predicting, not all e+1 points
            series_y_hat_lastpoint.append(y_hat[i_mean][-1])
            series_y_tilde_lastpoint.append(y_tilde[i_mean][-1])
            
        # For show and analysis in Spyder
        global show_y_hat
        global show_y_tilde
        # A series of predicted Y data
        show_y_hat = series_y_hat_lastpoint
        # A series of real Y data
        show_y_tilde = series_y_tilde_lastpoint
        
        # Transition to Pandas format
        pd_series_y_hat_lastpoint = pd.Series(series_y_hat_lastpoint)
        pd_series_y_tilde_lastpoint = pd.Series(series_y_tilde_lastpoint)
        Rho = pd_series_y_hat_lastpoint.corr(pd_series_y_tilde_lastpoint)
        
        if (is_show == 1): 
            print("L=",libsize,",  Rho=",round(Rho,6),"    ",
                  column_y_label,"——>",column_x_label,"  S:",sup_label,"   ",
                  column_y_label,"|M(",column_x_label,"+",sup_label,")")   
        return Rho    

    #print("y_hat[0]",y_hat[0]) 
    #print("y_tilde_all[0]",y_tilde_all[0]) 
    #print(len(y_hat[0]))
    #print(len(y_tilde_all[0]))
    Rho = CalculateRho(y_hat,y_tilde_all)
    return Rho

libsize_all = 1000
# 1: show tooltips
# 0: not show tooltips
is_show = 1
is_show_figure = 0
# Eccm_lag_globle is used for ECCM analysis, default value is 0 here  
Eccm_lag_globle = 0

# For show and analysis in Spyder
show_y_hat = []
show_y_tilde = []

"""
0： cardio
2： no2
3： o3
4： resp
6： so2
"""
# Get data from xlsx file
path = 'paper\\paper3\\data\\air.xlsx'
column_x = 0        # Noted it starts from 0 not 1, the cause
column_y = 0        # Results
column_s = 4        # Results_s
x_all,y_all,sup_all,column_x_label,column_y_label,sup_label = utils.MyReadxlsx2(path,libsize_all,column_x,column_y,column_s)
label_1 = column_y_label + " → "+ column_x_label + "  S:" + sup_label
x_all = utils.LagTransformation(Eccm_lag_globle,x_all)   # ECCM algorithm

'''
import GenerateData
# x_all: Use X to compute Y (Y → X)
# y_all
# sup_all
# column_x_label
# column_y_label
# sup_label
x_all,y_all,sup_all,column_x_label,column_y_label,sup_label = GenerateData.CoupleFormulationFourVariable(libsize_all)    
label_1 = column_y_label + " → "+ column_x_label + "  S:" + sup_label
# This function is not used in the paper
x_all = utils.LagTransformation(Eccm_lag_globle,x_all)   # ECCM algorithm
'''
# Normalization, compress all data to 0-1
x_all = utils.Norm(x_all)
y_all = utils.Norm(y_all)
sup_all = utils.Norm(sup_all)

def main(embed_e,parameter_tau,Eccm_lag):
    # Lag can be either possitive or negative, not used here
    Eccm_lag = Eccm_lag    
    # libsize_lenth should not exceed real lenth, that is, libsize_lenth < libsize_all
    # We can set libsize_all = libsize_lenth for simplicity
    libsize_lenth = 1000
    # Interval to sample libsize_lenth 
    interval_sample = 950
    # Embedded dimension E
    embed_e = embed_e
    # Time lag tau when sampling
    parameter_tau = parameter_tau
    print("Embed_e：",embed_e,"    tau:",parameter_tau)
    
    # Library size set to reconstruct Manifold
    libsizeSet = []
    # Predicting skill Rho
    RhoSetCCM_forward = []
    
    # Set the L in analysis
    for L_ccm in range(50,libsize_lenth+50,interval_sample):            
        libsizeSet.append(L_ccm)
        RhoSetCCM_forward.append(CCM_forward(x_all,y_all,sup_all,L_ccm,embed_e,parameter_tau))
        
    print(column_y_label,"——>",column_x_label,"  S:",sup_label, "   ",
          column_y_label,"|M(",column_x_label,"+",sup_label,")")
    # Choose the last Rho as the best Rho
    Best_Rho = RhoSetCCM_forward[-1]
    print("Best Rho:",round(Best_Rho,6))
    print("~~~~~~~~~~~~~~~~~~~~~~~~")
    if (is_show_figure == 1):    
        # Draw diagram
        plt.plot(libsizeSet,RhoSetCCM_forward,'g-',label=label_1)   
        #plt.ylim(-0.2,1)
        plt.title('Rho'+"      lag:" + str(Eccm_lag) + "   tau:" + str(parameter_tau) + "     E:" + str(embed_e))
        plt.legend(loc='lower right')
        plt.show()
    
# embed_e is the embedded dimension E   
# parameter_tau is the time lag when sampling
# Eccm_lag is used for ECCM analysis
for i_embed_e in range(3,4):
    for j_parameter_tau in range(1,2):
        for k_Eccm_lag in range(0,1):
            #main(embed_e = i, parameter_tau = j,Eccm_lag = Eccm_lag_globle)
            main(embed_e = i_embed_e, parameter_tau = j_parameter_tau, Eccm_lag = k_Eccm_lag)
#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri Aug  5 09:41:39 2016

@author: philipp
"""
# Scatterplot highlighting a particular gene of interest
# =======================================================================
# Imports 
from __future__ import division # floating point division by default
import os
import pandas as pd
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import glob
import yaml
import sys
import time

def GOI_Scatterplot(sample,GOI='None'):
    # ------------------------------------------------
    # Print header
    # ------------------------------------------------
    print('***********************************************************')
    print('PinAPL-Py: Enrichment/Depletion Scatterplot')
    print('***********************************************************')  
    start_total = time.time()  
    
    # ------------------------------------------------
    # Get parameters
    # ------------------------------------------------
    os.chdir('/workingdir/')
    configFile = open('configuration.yaml','r')
    config = yaml.load(configFile)
    configFile.close()
    WorkingDir = config['WorkingDir'] 
    AnalysisDir = WorkingDir + 'Analysis/'
    ListDir = AnalysisDir + 'Candidate_Lists/'
    PlotDir = AnalysisDir + 'ScatterPlots/'
    annotate = config['scatter_annotate']
    alpha = config['alpha']
    pcorr = config['pcorr']
    delta = config['delta_s']
    NonTPrefix = config['NonTargetPrefix']
   
    # ------------------------------------------------
    # Reading counts from sample and control
    # ------------------------------------------------
    print('Reading counts ...')    
    os.chdir(ListDir)
    filename = glob.glob(sample+'_'+str(alpha)+'_'+str(pcorr)+'_sgRNAList.tsv')[0]
    ListFile = pd.read_table(filename, sep='\t',low_memory=False)
    sgIDs = list(ListFile['sgRNA'].values)
    genes = list(ListFile['gene'].values)  
    L = len(sgIDs)
    sample_counts = list(ListFile['counts'].values)
    control_counts = list(ListFile['control mean'].values)
    sig = list(ListFile['significant'].values)  
    # Log transformation
    sample_log = [np.log(sample_counts[k]+delta) for k in range(len(sample_counts))]
    control_log = [np.log(control_counts[k]+delta) for k in range(len(control_counts))]
    
    # ------------------------------------------------
    # Creating gene subsets
    # ------------------------------------------------    
    print('Creating gene subsets ...') 
    K_nonT = [k for k in range(L) if NonTPrefix in genes[k]]
    K_sig = [k for k in range(L) if sig[k]==True]
    K_goi = [k for k in range(L) if genes[k] == GOI]   
    K_rest = list(set(range(L)) - set.union(set(K_nonT),set(K_sig),set(K_goi)))   
    sample_nonT = [sample_log[k] for k in K_nonT]
    control_nonT = [control_log[k] for k in K_nonT]
    sample_sig = [sample_log[k] for k in K_sig]
    control_sig = [control_log[k] for k in K_sig]
    sample_goi = [sample_log[k] for k in K_goi]
    control_goi = [control_log[k] for k in K_goi]
    sample_rest = [sample_log[k] for k in K_rest]
    control_rest = [control_log[k] for k in K_rest]
    goi_sgIDs = [sgIDs[k] for k in K_goi]

    # ------------------------------------------------
    # Plotting
    # ------------------------------------------------       
    print('Generating scatterplot ...')
    if not os.path.exists(PlotDir):
        os.makedirs(PlotDir)      
    os.chdir(PlotDir)   
    plt.figure()
    plt.scatter(control_rest,sample_rest,s=2)
    plt.scatter(control_sig,sample_sig,s=2,color='green',label='Significant')
    if GOI != 'None':
        plt.scatter(control_goi,sample_goi,s=20,color='red',label=GOI)
    if len(K_nonT)>0:
        plt.scatter(control_nonT,sample_nonT,s=2,color=(255/255,0,255/255),label='Non Targeting')
    axes = plt.gca()
    x0 = axes.get_xlim()  
    plt.plot((0,x0[1]-1), (0,x0[1]-1), ls="--", color=(51/255,153/255,1))
    if GOI != 'None':
        plt.suptitle(sample+': '+GOI+' counts', fontsize=14, fontweight='bold')
    else:
        plt.suptitle(sample+': '+' counts', fontsize=14, fontweight='bold')
    plt.xlabel('log counts control', fontsize=14)    
    plt.ylabel('log counts sample', fontsize=14)
    plt.legend(loc='upper left', prop={'size':10})
    if annotate:
        for label, x, y in zip(goi_sgIDs,control_goi,sample_goi):
            plt.annotate(label,xy=(x,y),color='red',fontsize=8)  
    if GOI != 'None':
        plt.savefig(sample+' '+GOI+' counts.png', dpi=300)
    else:
        plt.savefig(sample+' '+' counts.png', dpi=300)        
    plt.close()

    # ------------------------------------------------
    # Printing 
    # ------------------------------------------------
    if GOI != 'None':
        print('-----------------------------------------------')     
        print('sgID\t\tCounts\tControl\tSignificant')    
        print('-----------------------------------------------')       
        if not K_goi:
            print('ERROR: Gene name not found!')
        else:            
            for k in K_goi:        
                println = str(sgIDs[k])+'\t'+str(int(sample_counts[k]))+'\t'+ \
                    str(int(control_counts[k]))+'\t'+str(sig[k])
                print(println)

    # --------------------------------------
    # Final time stamp
    # --------------------------------------        
    end_total = time.time()
    # Final time stamp
    print('------------------------------------------------')
    print('Script completed.')    
    sec_elapsed = end_total - start_total
    if sec_elapsed < 60:
        time_elapsed = sec_elapsed
        print('Time elapsed (Total) [secs]: ' + '%.3f' % time_elapsed +'\n')
    elif sec_elapsed < 3600:
        time_elapsed = sec_elapsed/60
        print('Time elapsed (Total) [mins]: ' + '%.3f' % time_elapsed +'\n')
    else:
        time_elapsed = sec_elapsed/3600
        print('Time elapsed (Total) [hours]: ' + '%.3f' % time_elapsed +'\n')

    
if __name__ == "__main__":
    if len(sys.argv) == 3:
        input1 = sys.argv[1]
        input2 = sys.argv[2]
        GOI_Scatterplot(input1,input2)    
    else:
        input1 = sys.argv[1]
        GOI_Scatterplot(input1)            
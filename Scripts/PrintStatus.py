#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 26 13:50:52 2017

@author: philipp
"""

# Print status messages
import sys


def PrintStatus_Header():
    print('**************************************************')
    print('Launching PinAPL-Py v2.8.1')
    print('P. Spahn et al., UC San Diego (11/2017)')
    print('**************************************************')
    
def PrintStatus_SubHeader(msg):
    print('\n')
    print('**************************************************')
    print(msg)
    print('**************************************************')

def PrintStatus_Done(msg):
    print(msg)
    print('\n')

def PrintStatus_ProcessSample(sample):
    print('Processing sample '+sample+' ... ')

def PrintStatus_CombineReplicates():
    print('Combining gene ranks across replicates ... ')

def PrintStatus_SkipTrim():
    print('Alignment data found. Skipping read trimming ... ')

def PrintStatus_SkipSample(sample):
    print('Alignment data found for sample '+sample+'. Skipping alignment ... ')

def PrintStatus_SkipSeqQC():
    print('Sequence quality folder found. Skipping quality check ... ')

def PrintStatus_AllDone():
    print('\n')
    print('**************************************************')
    print('PinAPL-Py completed.')  

def PrintStatus_TimeStamp(msg):
    print(msg)


   
if __name__ == "__main__":
    input1 = sys.argv[1]
    input2 = sys.argv[2]    
    if input1 == 'Header':
        PrintStatus_Header()
    elif input1 == 'SubHeader':
        PrintStatus_SubHeader(input2)
    elif input1 == 'Done':
        PrintStatus_Done(input2)
    elif input1 == 'ProcessSample':
        PrintStatus_ProcessSample(input2)
    elif input1 == 'CombineReplicates':
        PrintStatus_CombineReplicates()                   
    elif input1 == 'SkipTrim':
        PrintStatus_SkipTrim()           
    elif input1 == 'SkipSample':
        PrintStatus_SkipSample(input2)   
    elif input1 == 'SkipSeqQC':
        PrintStatus_SkipSeqQC()           
    elif input1 == 'AllDone':
        PrintStatus_AllDone()
    elif input1 == 'TimeStamp':
        PrintStatus_TimeStamp(input2)        

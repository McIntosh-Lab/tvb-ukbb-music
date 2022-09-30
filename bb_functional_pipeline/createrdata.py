#!/bin/env python
#
# Script name: createrdata.py
#
# Description: Script for creating the training set using the hand_labels_noise.txt files from the fMRI/rfMRI.ica folder(s)
#
#
# Authors: Kelly Shen, adapted by Sarah Faber
#
# 
#
import bb_pipeline_tools.bb_logging_tool as LT 

def createrdata(): 
	logger = LT.initLogging(__file__, "") 
#	LT.runCommand( logger, "/home/s.faber/create_RData.sh", "createrdata_k")
	LT.runCommand( logger, "/home/s.faber/create_RData_music.sh", "createrdata_k")

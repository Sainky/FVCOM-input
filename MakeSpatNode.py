# -*- coding: utf-8 -*-
"""
Created on Fri Sep  5 08:31:59 2025

@author: XZhou @QIMG (QD. CN)
"""

import numpy as np
from matplotlib.path import Path
from shapely.geometry import Point, Polygon
import os
import matplotlib.pyplot as plt

def findAreaNodes(fpath,meshfnm,marks):
    nodes = []
    node_dep = []
    with open(fpath + meshfnm, 'r') as dmf:
        current_line = []
        for line in dmf:
            if line.startswith('ND'):
                parts = line.strip().split()[1:]
                if float(parts[3])==marks:
                    nodes.append(int(parts[0]))
                    node_dep.append(float(parts[3]))
    nodes_str = ",".join(str(i) for i in nodes)
    nodes_len = len(nodes)
    return nodes_str,nodes_len
#%% 
fpath = r'E:\ProgramData\PyProgram\SGW\\'
meshfnm = 'SgBay_dyearea.2dm'
M_SPERCIFY, M_SPEDYE = findAreaNodes(fpath,meshfnm,marks=100)    
print(M_SPEDYE)


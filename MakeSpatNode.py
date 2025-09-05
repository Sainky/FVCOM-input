# -*- coding: utf-8 -*-
"""
Created on Fri Sep  5 08:31:59 2025

@author: XZhou @QIMG (QD. CN)
"""

import numpy as np

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
fpath = r'Inputfile_path//'
meshfnm = 'MarkedDepthMesh.2dm'
M_SPERCIFY, M_SPEDYE = findAreaNodes(fpath,meshfnm,marks=100)  #eg. marks depth eaual to 100  
print(M_SPEDYE)#M_SPEDYE is node numbers, M_SPERCIFY is a string within comma can be copied to nml file



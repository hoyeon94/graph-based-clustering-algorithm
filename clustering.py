#semi label propagation 알고리즘을 이용하여 주어진 그래프를 clustering 한 후에 그 정보를 csv파일로 저장.
import networkx
import matplotlib.pyplot as plt
import heapq
import numpy as np
import slp
import csv
edge_file = open("musics-copurchase-rep.edgelist", "rb")
copurchased_graph = networkx.read_weighted_edgelist(edge_file)
edge_file.close()
print(len(copurchased_graph.nodes()))
print(len(copurchased_graph.edges()))
labels_list=[ 'B00003WG0M', 'B000001GYJ','B000002ADT','B0000032ZU', 'B00002DESF', 'B000067CLT', 'B00004KD24', 'B00006IJWZ', 'B0000026NF', 'B000003CMR', 'B000002B8G', 'B00005Q6OS', 'B000069KIT', 'B0000024PL', 'B00005OMHN', 'B00005ABMY', 'B000005L86', 'B00002R14Y', 'B0000894RC', 'B000000KQH', 'B00000JNQ5', 'B000002WXS', 'B0000030MF', 'B0000029P0', 'B0000013U7', 'B00000136Z', 'B00004TRU5', 'B000002UAU', 'B0000032SP', 'B00000348H', 'B000002RBV', 'B00000616B', 'B000066EZY', 'B000002WVB', 'B000002VOS', 'B000005J54', 'B00008WI90', 'B0000009S5', 'B000005ZFF', 'B0000060BM', 'B000001QJB', 'B000002NYW', 'B000063T4J', 'B000002WZE', 'B000000L2N', 'B00000J6BR', 'B00000GC0W', 'B00005MK7W']
labels=slp.slp_start(0.9,labels_list,copurchased_graph)
w = csv.writer(open("slp_result.csv", "w"))
label_num_counter=0
for nodes in labels:
    w.writerow(nodes)
    w.writerow([label_num_counter,len(nodes)])
    label_num_counter+=1
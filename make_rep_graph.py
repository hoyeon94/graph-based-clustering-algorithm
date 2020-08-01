import networkx
import matplotlib.pyplot as plt
import csv
import numpy as np
import heapq

#네트워크 정보를 로드
edge_file = open("musics-copurchase.edgelist", "rb")
copurchased_graph = networkx.read_weighted_edgelist(edge_file)
edge_file.close()
degree=dict(networkx.degree(copurchased_graph))

#label propagation 결과 중 대표노드를 로드
f = open('rep_labeled_set.csv', 'r', encoding='utf-8')
rdr = csv.reader(f)
rep_labels=list()
for a in rdr:
    rep_labels=a
    break
f.close()
#label propagation 결과를 로드
f = open('labeled_set.csv', 'r', encoding='utf-8')
rdr = csv.reader(f)
i_know_rep=dict()
for line in rdr:
    if(len(line)==0):
        continue
    arr=np.zeros(len(line))
    for i in range(len(line)):
        arr[i]=degree[line[i]]
    for i in range(len(line)):
        i_know_rep[line[i]]=line[arr.argmax()]
f.close()




temp=list(copurchased_graph.nodes()).copy()
for node in temp:
    if(node not in rep_labels):
        #노드를 삭제하고, 삭제한 노드가 가지고 있던 엣지는 대표노드의 엣지로 변환.
        for neighbor in networkx.neighbors(copurchased_graph,node):
            copurchased_graph.add_edge(neighbor,i_know_rep[node],weight=1)
        copurchased_graph.remove_node(node)
print(len(copurchased_graph.nodes()))
print(len(copurchased_graph.edges()))
writefile = open('musics-copurchase-rep.edgelist', 'wb')
networkx.write_weighted_edgelist(copurchased_graph, writefile)
writefile.close()
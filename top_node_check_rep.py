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
#대표노드를 로드
f = open('rep_labeled_set.csv', 'r', encoding='utf-8')
rdr = csv.reader(f)
rep_labels=list()
for a in rdr:
    rep_labels=a
    break
f.close()
#차수정보를 저장
degree=dict(networkx.degree(copurchased_graph))
#degree가 높은 300개의 노드를 구함.
degree_top_n_list_node=(heapq.nlargest(300, degree, key=degree.get))
degree_top_n_list_value=[]
for keys in degree_top_n_list_node:
    degree_top_n_list_value.append(degree[keys])
degree_top_n_dict=dict(zip(degree_top_n_list_node,degree_top_n_list_value))
temp_source=[]
temp_target=[]
temp_length=[]
for source in degree_top_n_list_node:
    for target in degree_top_n_list_node:
        temp_source.append(source)
        temp_target.append(target)
        temp_length.append(networkx.shortest_path_length(copurchased_graph,source,target))
sum=0
print(1)
for i in range(len(temp_length)):
    sum+=temp_length[i]
avg=sum/len(temp_length)
for i in range(len(temp_length)):
#거리가 3 이하인 노드들은 삭제.
    if (temp_length[i]<4):
        source=temp_source[i]
        target=temp_target[i]
        if(source==target):
            continue
        to_erase=''
        if( (source not in degree_top_n_dict) or (target not in degree_top_n_dict) ):
            continue
        if(degree_top_n_dict[source]<=degree_top_n_dict[target]):
            to_erase=source
        else:
            to_erase=target
        degree_top_n_dict.pop(to_erase)
print(degree_top_n_dict)
print(len(degree_top_n_dict))
temp=list(degree_top_n_dict.keys()).copy()
#대표노드 안에 포함되지 않는 노드는 삭제
for node in temp:
    if(node not in rep_labels):
        degree_top_n_dict.pop(node)
print(degree_top_n_dict)
print(len(degree_top_n_dict))
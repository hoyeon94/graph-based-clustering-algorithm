import csv
import networkx
import numpy as np
edge_file = open("musics-copurchase.edgelist", "rb")
copurchased_graph = networkx.read_weighted_edgelist(edge_file)
edge_file.close()

degree=dict(networkx.degree(copurchased_graph))

#label propation 결과를 로드
f = open('labeled_set.csv', 'r', encoding='utf-8')
rdr = csv.reader(f)
rep_labels=list()
rep_labels_degree=list()
for line in rdr:
    if(len(line)==0):
        continue
    else:
#가장 높은 degree를 가진 노드 하나를 지정.
        line_degree=list()
        for de in line:
            line_degree.append(degree[de])
        line_degree=np.array(line_degree)
        top_arg=line_degree.argmax()
        line=list(line)
        rep_labels.append(line[top_arg])
        rep_labels_degree.append(line_degree[top_arg])
f.close()
#가장 높은 degree를 가진 노드 리스트를 저장.
w = csv.writer(open("rep_labeled_set.csv", "w"))
w.writerow(rep_labels)
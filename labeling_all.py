#label propagation을 하기 위한 코드
#코드

import networkx
import matplotlib.pyplot as plt
import csv
edge_file = open("musics-copurchase.edgelist", "rb")
copurchased_graph = networkx.read_weighted_edgelist(edge_file)
edge_file.close()

#label propagation 실행
g=networkx.algorithms.community.label_propagation.label_propagation_communities(copurchased_graph)

#실행결과 저장
w = csv.writer(open("labeled_set.csv", "w"))

for label_set in g:
    w.writerow(label_set)
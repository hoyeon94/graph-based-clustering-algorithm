import numpy as np
import networkx
import copy


def slp_start(mem_rate,labels_list,network):
    labels_num=len(labels_list)
    degree=dict(networkx.degree(network))
    node_list=list(network.nodes())
    neighbors=dict()
    old_fr=dict()
    #빠른 연산을 위해 미리 각각의 노드마다 이웃 정보를 저장한다.
    for ego in node_list:
        neighbors_node=list(network.neighbors(ego))
        neighbors[ego]=neighbors_node
        old_fr[ego]=np.zeros([labels_num+1])
    new_fr=dict()
    for ego in node_list:
        new_fr[ego]=np.zeros([labels_num+1])

    for i in range(labels_num):
        old_fr[labels_list[i]][i+1]=1
    stable=False
    while not stable:
        stable=True
        for ego in node_list:
            #주변 노드의 frequency 정보를 이용해서 현재 노드의 frequency를 업데이트 한다.
            ego_degree=len(neighbors[ego])
            for neighbor in neighbors[ego]:
                new_fr[ego]+=(old_fr[neighbor]/ego_degree*mem_rate)
            now_index=old_fr[ego].argmax()
            if(now_index!=0):
                new_fr[ego][now_index]+=(1-mem_rate)
            if(new_fr[ego].argmax()!=now_index):
                stable=False
        old_fr=new_fr.copy()
        for ego in node_list:
            new_fr[ego]=np.zeros([labels_num+1])
    labels=list()
    for i in range(labels_num+1):
        labels.append(list())
    for ego in node_list:
        labels[old_fr[ego].argmax()].append(ego)
    return labels


#유저가 사용할 수 있는 gui 기반 추천 프로그램
import PySimpleGUI as sg
import networkx
import get_top_5
from operator import itemgetter
import csv
import numpy as np

#프로그램에 표시될 템플릿을 만드는 함수
def make_template(asin,title,SalesRank,TotalReviews,AvgRating):
    return "asin : "+asin+'\n'+"title : "+title+'\n'+"SalesRank : "+SalesRank+'\n'+"TotalReviews : "+TotalReviews+'\n'+"AvgRating : "+AvgRating+'\n'


#미리 전처리한 상품 정보를 로드
fhr = open('musics.txt', 'r', encoding='utf-8', errors='ignore')
Musics = {}
fhr.readline()
for line in fhr:
    cell = line.split('\t')
    MetaData = {}
    MetaData['Id'] = cell[0].strip()
    ASIN = cell[1].strip()
    MetaData['Title'] = cell[2].strip()
    MetaData['Categories'] = cell[3].strip()
    MetaData['Group'] = cell[4].strip()
    MetaData['Copurchased'] = cell[5].strip()
    MetaData['SalesRank'] = int(cell[6].strip())
    MetaData['TotalReviews'] = int(cell[7].strip())
    MetaData['AvgRating'] = float(cell[8].strip())
    Musics[ASIN] = MetaData
fhr.close()

#네트워크 데이터를 로드
fhr = open("musics-copurchase.edgelist", "rb")
copurchaseGraph = networkx.read_weighted_edgelist(fhr)
fhr.close()

edge_file = open("musics-copurchase-dir.edgelist", "rb")
copurchased_dir_graph = networkx.read_weighted_edgelist(edge_file,create_using=networkx.MultiDiGraph)
edge_file.close()

degree=dict(networkx.degree(copurchaseGraph))

#대표노드 정보를 로드
f = open('rep_labeled_set.csv', 'r', encoding='utf-8')
rdr = csv.reader(f)
rep_labels=list()
for a in rdr:
    rep_labels=a
    break
f.close()

#대표노드에 포함된 노드 정보를 로드
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

#semi label propagation algorithm 결과를 로드
what_rep_labels_in=dict()
f = open('slp_result.csv', 'r', encoding='utf-8')
rdr = csv.reader(f)
rep_labels=list()
i=0

labels=0
for a in rdr:
    if(i%4==2):
        labels=int(a[0])+1
    if(i%4==0):
        for node in a:
            what_rep_labels_in[node]=labels
    i+=1
f.close()

#slp propagation에 사용한 대표노드를 로드.
labels_list=['NULL','B00003WG0M', 'B000001GYJ','B000002ADT','B0000032ZU', 'B00002DESF', 'B000067CLT', 'B00004KD24', 'B00006IJWZ', 'B0000026NF', 'B000003CMR', 'B000002B8G', 'B00005Q6OS', 'B000069KIT', 'B0000024PL', 'B00005OMHN', 'B00005ABMY', 'B000005L86', 'B00002R14Y', 'B0000894RC', 'B000000KQH', 'B00000JNQ5', 'B000002WXS', 'B0000030MF', 'B0000029P0', 'B0000013U7', 'B00000136Z', 'B00004TRU5', 'B000002UAU', 'B0000032SP', 'B00000348H', 'B000002RBV', 'B00000616B', 'B000066EZY', 'B000002WVB', 'B000002VOS', 'B000005J54', 'B00008WI90', 'B0000009S5', 'B000005ZFF', 'B0000060BM', 'B000001QJB', 'B000002NYW', 'B000063T4J', 'B000002WZE', 'B000000L2N', 'B00000J6BR', 'B00000GC0W', 'B00005MK7W']



sg.change_look_and_feel('BluePurple')

layout = [[sg.Text('Your typed chars appear here:'), sg.Text(size=(15,1), key='-OUTPUT-')],
          [sg.Input(key='-IN-')],
          [sg.Text(size=(40,5),key='-PURC-')],
          [sg.Listbox(values=[],
          size=(30, 20), key='-LIST-', enable_events=True),sg.Text(size=(40,10),key='-ITEM-')],
          [sg.Button('Show'), sg.Button('Exit')]]

window = sg.Window('Pattern 2B', layout)


left_list=set()
ego_rec_dict=list()
dir_ego_rec_dict=list()
one_top_node_dict=list()
while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    if event in  (None, 'Exit'):
        break
    if event == 'Show':

        left_list=list()
        ##ego network
        asin=str(values['-IN-'])
        window['-IN-'].update('')
        ego_rec_dict=get_top_5.get_top_5(asin,copurchaseGraph,Musics)
        for i in ego_rec_dict:
            left_list.append(list(i)[1])
        ##dir_ego network
        dir_ego_rec_dict=get_top_5.get_top_5(asin,copurchased_dir_graph,Musics)
        for i in dir_ego_rec_dict:
            left_list.append(list(i)[1])
        #PURCHASED INFO
        window['-PURC-'].update(make_template(asin,str(Musics[asin]['Title']),str(Musics[asin]['SalesRank']),str(Musics[asin]['TotalReviews']),str(Musics[asin]['AvgRating'])))
        #one_top_node
        one_top_node=labels_list[what_rep_labels_in[i_know_rep[asin]]]
        if(labels!=0):
            left_list.append(str(Musics[one_top_node]['Title']))
        else:
            one_top_node_dict=list()
        one_top_node_dict=[(one_top_node,str(Musics[one_top_node]['Title']),str(Musics[one_top_node]['SalesRank']),str(Musics[one_top_node]['TotalReviews']),str(Musics[one_top_node]['AvgRating']))]
        #remove repeat
        left_list=set(left_list)
        left_list=list(left_list)
        
        window['-LIST-'].update(left_list)



    if event == '-LIST-':
        ##for_all_rec
        key=values['-LIST-'][0]
        key=str(key)
        now_item=list()
        for i in ego_rec_dict+dir_ego_rec_dict+one_top_node_dict:
            if(key==list(i)[1]):
                now_item=list(i)
        window['-ITEM-'].update(make_template(str(now_item[0]),str(now_item[1]),str(now_item[2]),str(now_item[3]),str(now_item[4])))
window.close()


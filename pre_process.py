#meta data file을 undirected 그래프로 전처리를 하기 위한 코드

import string
import re
from nltk.corpus import stopwords
from stemming.porter2 import stem
import networkx
import nltk
nltk.download('stopwords')

#파일 열기
datafile = open('amazon-meta.txt', 'r', encoding='utf-8')
products = {}

#파일 읽기
(Id, ASIN, title, categories, group, copurchased, salesrank, totalreviews, avgrating) = ('', '', '', '', '', '', 0, 0, 0.0)
for line in datafile:
#데이터를 한 줄씩 불러옴
    line = line.strip()
    if(line.startswith('Id')):
        Id = line[3:].strip()
    elif(line.startswith('ASIN')):
        ASIN = line[5:].strip()
    elif(line.startswith('title')):
        title = line[6:].strip()
        title = title.split()
        title=  ''.join(title)
    elif(line.startswith('group')):
        group = line[6:].strip()
    elif(line.startswith('salesrank')):
        salesrank = line[10:].strip()
    elif(line.startswith('similar')):
        line_splited = line.split()
        copurchased = ' '.join([i for i in line_splited[2:]])
    elif(line.startswith('categories')):
        line_splited = line.split()
        categories = ' '.join((datafile.readline()).lower() for i in range(int(line_splited[1].strip())))
        categories = re.compile('[%s]' % re.escape(string.digits + string.punctuation)).sub(' ', categories)
        categories = ' '.join(set(categories.split()) - set(stopwords.words('english')))
        categories = ' '.join(stem(word) for word in categories.split())
    elif(line.startswith('reviews')):
        line_splited = line.split()
        totalreviews = line_splited[2].strip()
        avgrating = line_splited[7].strip()
#line=='' 인 경우는 상품의 모든 정보를 임시 변수에 담은 후이므로, product_data 객체 안에 상품의 정보를 넣는다.
    elif(line==''):
       product_data={}
       if(ASIN != ''):
       	products[ASIN] = product_data
       product_data['Id'] = Id
       product_data['title'] = title	
       product_data['categories'] = categories
       product_data['group'] = group
       product_data['copurchased'] = copurchased
       product_data['salesrank'] = int(salesrank)
       product_data['totalreviews'] = int(totalreviews)
       product_data['avgrating'] = float(avgrating)
#정보를 담았던 임시변수를 초기화해주고, 다시 다음 상품을 읽기 위해 for문의 처음으로 되돌아간다.
       (Id, ASIN, title, categories, group, copurchased, salesrank, totalreviews, avgrating) = ('', '', '', '', '', '', 0, 0, 0.0)
datafile.close()



#Music에 관한 상품만 다루기 위해
musics = {}
for asin,data in products.items():
    if (data['group']=='Music'):
        musics[asin] = products[asin]

#네트워크로 표현할 때, 만약 두 노드 중 하나가 가지고 있는 data안에 없다면 분석이 힘들어 지기 때문에, 함께 구입한 상품에서 제거
for asin, data in musics.items():
    musics[asin]['copurchased'] = ' '.join([cp for cp in data['copurchased'].split() if cp in musics.keys()])

#그래프 생성
copurchased_graph = networkx.Graph()
for asin,data in musics.items():
    copurchased_graph.add_node(asin)
    for target in data['copurchased'].split():
        copurchased_graph.add_node(target.strip())
        n1 = set((musics[asin]['categories']).split())
        n2 = set((musics[target]['categories']).split())
        n1_n2_inter = n1 & n2     
        n1_n2_union = n1 | n2 
        cal_weight = 0    
        if(len(n1_n2_union)) > 0:
            cal_weight = round(len(n1_n2_inter)/len(n1_n2_union), 2)
        copurchased_graph.add_edge(asin, target.strip(), weight=cal_weight)


#상품별 객체 data를 파일에 쓰기
writefile = open('musics.txt', 'w', encoding='utf-8')
writefile.write('Id\t' + 'ASIN\t' + 'title\t' + 'categories\t' + 'group\t' + 'copurchased\t' + 'salesrank\t' + 'totalreviews\t' + 'avgrating\t\n')
for asin, data in musics.items():
    writefile.write(data['Id'] + '\t' +asin + '\t' + data['title'] + '\t' + data['categories'] + '\t' + data['group'] + '\t' + data['copurchased'] + '\t' + str(data['salesrank']) + '\t' + str(data['totalreviews']) + '\t' +str(data['avgrating']) + '\n')
writefile.close()

#edge-node data를 파일에 쓰기
writefile = open('musics-copurchase.edgelist', 'wb')
networkx.write_weighted_edgelist(copurchased_graph, writefile)
writefile.close()
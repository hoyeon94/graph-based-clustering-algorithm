# graph-based-clustering-algorithm

아마존 구매이력 데이터를 이용해 그래프를 구성하고, 클러스터링 알고리즘으로<br>
<strong>label propagtion algorithm</strong>(Community detection via semi-synchronous label propagation algorithms. In Business Applications of Social Network Analysis (BASNA), 2010 IEEE International Workshop on (pp. 1-8). IEEE. Cordasco, G., & Gargano, L.)<br>
<strong>semi label propagation algorithm</strong>(Semi-supervised community detection using Label Propagation (Dong Liu, Published 6 August 2014)<br>
을 사용했다.

<h1>코드 정리</h1>

1.데이터 전처리
amazon-meta.txt 파일을 전처리
pre_process.py : 데이터를 전처리하여 undirected network 생성 및 edge list 저장
pre_process_dir.py : 데이터를 전처리하여 directed network 생성 및 edge list 저장

2.label propagation
labeling_all.py : 클러스터링 알고리즘으로 모든 노드를 9662개의 클러스터로 나눈 후 csv 파일을 저장.

3. 대표노드 설정
get_rep_label.py : label propagation 의 결과를 이용하여 9662개의 클러스터에서 대표노드만 뽑아내어 csv 파일로 저장.

4. 네트워크 단순화
make_rep_graph.py : pre_process.py의 결과로 생성된 전체 네트워크를 대표노드만 남기고 단순화하고 edge list를 저장.

5. 초기 중심노드 설정
top_node_check_rep.py : 전체 네트워크에서 degree가 높은 300개의 노드를 추출하고, 그 중에서 대표노드에 포함되지 않는 노드는 제외. 서로 거리가 4 이상인 노드만 남겨둬서 총 48개의 초기 중심노드를 얻을 수 있음.

6. semi supervised label propagation
clustering.py : top_node_check_rep.py의 결과로 나온 초기 중심노드를 이용하여 semi supervised label propagation 실행.
slp.py : semi supervised label propagation 알고리즘을 구현한 모듈.
나누어진 대표노드를 slp_result.csv로 저장.

7. 분석된 ego network에서 추천을 진행하는 모듈
get_top_5.py : 그래프 정보와 메타데이터 정보,그리고 구매되는 상품의 asin 정보를 이용하여 주어진 undirected ego network, directed ego network 내에서 가장 리뷰가 많고 평점이 높은 상품을 list로 반환하는 모듈.

8. 추천하기 위한 ui 코드
gui.py : 추천 알고리즘을 gui로 구현함.

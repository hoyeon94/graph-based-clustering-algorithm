#ego network 분석을 위한 모듈이 담긴 코드
#현재 그래프의 정보와 아마존 데이터를 인자로 받은 후에
#주어진 asin과 같이 구매하면 좋을 상품 5개를 list로 반환한다.

import networkx

def get_top_5(purchased_Asin,graph,Musics):
    #ego network를 구함.
    ego = networkx.ego_graph(graph, purchased_Asin, 3)
    purchasedAsinEgoGraph = networkx.Graph(ego)
    threshold = 0.5
    purchasedAsinEgoTrimGraph = networkx.Graph()
    #threshold 이하의 엣지는 삭제
    for f,t,e in purchasedAsinEgoGraph.edges(data=True):
        if e['weight'] >= threshold:
            purchasedAsinEgoTrimGraph.add_edge(f,t, weight=e['weight'])
    AsMeta = []

    for asin in purchasedAsinEgoTrimGraph.node:
        if(asin==purchased_Asin):
            continue
        ASIN = asin
        Title = Musics[asin]['Title']
        SalesRank = Musics[asin]['SalesRank']
        TotalReviews = Musics[asin]['TotalReviews']
        AvgRating = Musics[asin]['AvgRating']
        AsMeta.append((ASIN, Title, SalesRank, TotalReviews, AvgRating))
    T5_byAvgRating_then_byTotalReviews = sorted(AsMeta, key=lambda x: (x[4], x[3]), reverse=True)[:5]
    #추천하고자 하는 상품의 메타데이터를 반환
    return T5_byAvgRating_then_byTotalReviews


def get_top_5_dir(purchased_Asin,graph,Musics):
    #상품의 directed ego network를 구함.
    distance_one=[]
    ego_weight_cut_network_out=networkx.MultiDiGraph()
    for source,target,edge_data in graph.edges(data=True):
        if(source==purchased_Asin):
            print(source,target)
            ego_weight_cut_network_out.add_weighted_edges_from([(source,target,edge_data['weight'])])
            distance_one.append(target)
    for source,target,edge_data in graph.edges(data=True):
        if(source in distance_one):
            print(source,target)
            ego_weight_cut_network_out.add_weighted_edges_from([(source,target,edge_data['weight'])])
    AsMeta = []
    for asin in ego_weight_cut_network_out.node:
        if(asin==purchased_Asin):
            continue
        ASIN = asin
        Title = Musics[asin]['Title']
        SalesRank = Musics[asin]['SalesRank']
        TotalReviews = Musics[asin]['TotalReviews']
        AvgRating = Musics[asin]['AvgRating']
        AsMeta.append((ASIN, Title, SalesRank, TotalReviews, AvgRating))
    #추천하고자 하는 상품의 메타데이터를 반환
    T5_byAvgRating_then_byTotalReviews = sorted(AsMeta, key=lambda x: (x[4], x[3]), reverse=True)[:5]
    return T5_byAvgRating_then_byTotalReviews
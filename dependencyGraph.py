from pycorenlp import StanfordCoreNLP
import networkx as nx

from Node import Node

def shortestPath(depGraph, start, end):
    dep_path = []
    try:
        dep_path = nx.shortest_path(depGraph, source = start, target = end)
    except Exception as e:
        print e
    return dep_path

def pathRelations(edge_dict, dep_path):
    if not dep_path or len(dep_path) == 1:
        return "None"
    path_str = ""
    for i in range(len(dep_path) - 1):
        path_str += edge_dict[tuple(sorted((dep_path[i], dep_path[i+1])))]
        path_str += "_"
    return path_str

def dependencyPath(sentence, source, target):

    nlp = StanfordCoreNLP('http://localhost:9000')


    # sentence = "Bill sees Jane at Bill's house."
    # source = 1
    # target = 8
    output = nlp.annotate(sentence,
                        properties={
                            'annotators': 'depparse',
                            'outputFormat': 'json',
                            'timeout': 1000,
                        })

    tokens = output['sentences'][0]['tokens']
    # node_list = []
    # node_list = [Node(token) for token in tokens]

    # for node in node_list:
    #     print str(node.index) + "    " + node.originalText

    # root_token = {}
    # root_token['index'] = 0
    # root_token['pos'] = "@ROOT"
    # root_token['word'] = "@ROOT"
    # root_token['originalText'] = "@ROOT"
    # root_token['characterOffsetEnd'] = -1
    # root_token['characterOffsetBegin'] = -1
    # root_token['after'] = ''
    # root_token['before'] = ''

    # node_list.append(Node(root_token))

    tokens_list = [t['originalText'] for t in tokens]

    # print tokens_list
    # print source, target
    # print tokens_list[source], tokens_list[target]

    dependencies = output['sentences'][0]['basicDependencies']

    edge_dict = {}

    for dep in dependencies:
        edge_dict.update({tuple(sorted((int(dep['governor']), int(dep['dependent'])))): dep['dep']})
    # print edge_dict

    edge_list = edge_dict.keys()

    depGraph = nx.Graph()

    depGraph.add_edges_from(edge_list)

    dep_path = shortestPath(depGraph, source + 1 , target + 1)
    # print dep_path
    path_str = pathRelations(edge_dict, dep_path)

    return path_str
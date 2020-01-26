import networkx as nx
from networkx.drawing import nx_pydot
from graph2world.generator import Generator
# from pycorenlp import StanfordCoreNLP


def get_dummy_graph():
    """
    Generate a dummy graph for testing

    Returns:
        Graph: a simple test graph
    """

    g = nx.DiGraph()
    g.add_nodes_from(['kitchen', 'spoon', 'living room'])
    g.add_edge('spoon', 'kitchen', type='in')
    g.add_edge('kitchen', 'living room', type='connected')
    g.add_edge('living room', 'kitchen', type='connected')
    g.nodes['kitchen']['type'] = 'room'
    g.nodes['living room']['type'] = 'room'
    g.nodes['spoon']['type'] = 'object'
    return g


def get_gml_graph(location):
    """
    Load networkx graph from gml file

    Parameters:
        location (str): file path as string to *.gml

    Returns:
        Graph: loaded object in networkx format
    """

    # nlp = StanfordCoreNLP('http://localhost:9000')
    #
    # text = "thousands of images of Napoleon all over London"
    #
    # output = nlp.annotate(text, properties={
    #     'annotators': 'parse',
    #     'outputFormat': 'json'
    # })
    #
    # print(output['sentences'][0]['parse'])
    #
    # dependencies = output['sentences'][0]['basicDependencies']
    # subjects = [x for x in dependencies if x['dep'] == 'nsubj']
    # if len(subjects) >= 1:
    #     print(subjects[0]['governorGloss'])
    # else:
    #     roots = [x for x in dependencies if x['dep'] == 'ROOT']
    #     if len(roots) >= 1:
    #         print(roots[0]['dependentGloss'])
    #     else:
    #         print('no head found!')
    #

    try:
        # g = nx.read_gml(location).to_directed()
        g = nx_pydot.read_dot(location).to_undirected()

        # before returning graph, run
        # some clean-up pre-processing
        temp = sorted(g)
        mapping = {}
        for node in temp:
            node_name = node
            # escape commas, similar to csv
            if ',' in node_name:
                node_name = '"' + node_name + '"'
            # remove period at end of name
            if node_name[-1] == '.':
                node_name = node_name[:-1]
            # capitalize first letter in name
            if not node_name[0].isupper():
                if len(node_name) == 1:
                    node_name = node_name.upper()
                else:
                    node_name = node_name[0].upper() + node_name[1:]

            mapping[node] = node_name
        g = nx.relabel_nodes(g, mapping)

        # # remove double quotes if exist from flavor text
        # for u, v, data in g.edges(data=True):
        #     for i in g[u][v]:
        #         if 'flavortext' in g[u][v][i]:
        #             if g[u][v][i]['flavortext'][0] == '"':
        #                 g[u][v][i]['flavortext'] = g[u][v][i]['flavortext'][1:]
        #     # if g[u][v]['flavortext'][0] == '"':
        #     #     print('caught')

        # also need to make edges bidirectional
        # new_edges = []
        # for u, v, data in g.edges(data=True):
        #     # if data['type'] == 'connected':
        #     #     new_edges.append((v, u))
        #     if 'flavortext' in data:
        #         new_edges.append((v, u, data['type'], data['flavortext']))
        #     else:
        #         new_edges.append((v, u, data['type'], ''))
        # for new_edge in new_edges:
        #     g.add_edge(new_edge[0], new_edge[1], type=new_edge[2], flavortext=new_edge[3])
        return g
    except:
        raise Exception('Could not open file!')


def graph_to_world(graph, zone, output_location=None):
    """
    Primary function, take a networkx graph and save generated Evennia code to location

    Parameters:
        graph (Graph): networkx object
        output_location (str): file path as string to save *.ev
    """

    gen = Generator()
    gen.load_graph(graph, zone)
    if output_location is None:
        gen.to_file()
    else:
        gen.to_file(output_location)

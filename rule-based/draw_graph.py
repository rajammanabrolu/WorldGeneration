import networkx as nx
import subprocess
import pickle
import numpy as np
import os
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
st = StanfordNERTagger('stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz',
                       'stanford-ner/stanford-ner.jar', encoding='utf-8')


def match_graph(loc_dict, max_loc, max_obj_perloc):
    '''
    cut the num of locations,
    and num of maximum objects per loc (make sure that the connected ones are kept)
    and tag the character
    '''
    num_locations = len(loc_dict)
    chosen_locs = np.random.choice(range(num_locations), min(max_loc, num_locations), replace=False)

    # reorder the index
    new_loc_dict = {}
    count = 0
    for l, attr in loc_dict.items():
        cur_index = attr['index']
        obj_list = attr['objects']
        if cur_index in chosen_locs:  # this location is selected
            new_loc_dict[l] = {}
            new_loc_dict[l]['objects'] = obj_list
            new_loc_dict[l]['index'] = count
            count += 1
    loc_dict = new_loc_dict.copy()

    for l, attr in new_loc_dict.items():
        obj_list = attr['objects']
        chosen_objects = list(np.random.choice(obj_list, min(max_obj_perloc, len(obj_list)), replace=False))
        loc_dict[l]['objects'] = chosen_objects

    return loc_dict


def construct_graph(output_file, max_loc, max_obj_perloc):
    with open(output_file + '_loc_dict', 'rb') as filehandle:
        loc_dict = pickle.load(filehandle)
    loc_dict = match_graph(loc_dict, max_loc, max_obj_perloc)

    with open(output_file + '_loc_dict_Matched', 'wb') as filehandle:
        pickle.dump(loc_dict, filehandle)

    graph = nx.DiGraph()
    # location
    prev_l = None
    for l, attr in loc_dict.items():
        index = attr['index']
        graph.add_node(l, type='location', fillcolor='yellow', style='filled')
        if prev_l:
            graph.add_edge(prev_l, l, type='connected')  # location-location
        prev_l = l

    # add objects node
    obj_set = set()
    for l, attr in loc_dict.items():
        # object
        obj_list = attr['objects']
        excluded_list = []
        for i in obj_list:
            if not np.any([i in e for e in excluded_list]) and not np.any([e in i for e in excluded_list]):
                print('current i: ', i)
                if i.lower() not in obj_set:  # add to the node
                    obj_set.add(i.lower())
                    classified_i = st.tag(word_tokenize(i))
                    if 'PERSON' in [j[1] for j in classified_i]:
                        graph.add_node(i.lower(), type='character', fillcolor="orange", style='filled')
                    else:
                        graph.add_node(i.lower(), type='object', fillcolor='white', style='filled')
                graph.add_edge(l, i.lower(), type='in')

    print(len(graph))
    nx.write_gml(graph, output_file + '.gml', stringizer=None)
    return graph


def draw(graph, output_file):
    nx.nx_pydot.write_dot(graph, output_file + '.dot')
    filename = output_file + '.png'
    cmd_str = "sfdp -x -Goverlap=False -Tpng " + output_file + ".dot"
    cmd = cmd_str.format(filename)
    returned_value = subprocess.check_output(cmd, shell=True)
    with open(filename, 'wb') as f:
        f.write(returned_value)


def walk_through_files(path):
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            if filename.endswith('_binary.txt'):
                yield os.path.join(dirpath, filename)


if __name__ == "__main__":
    folder = 'binary_data/'
    match_dict = {
        'myster': {1: (3, 5), 2: (3, 5), 3: (3, 5), 4: (3, 5), 5: (3, 5),
                   6: (3, 5), 7: (3, 5), 8: (3, 5), 9: (3, 5), 10: (3, 5)},
        'fairy': {1: (3, 5), 2: (3, 5), 3: (3, 5), 4: (3, 5), 5: (3, 5),
                  6: (3, 5), 7: (3, 5), 8: (3, 5), 9: (3, 5), 10: (3, 5)}
    }
    for fname in walk_through_files(folder):
        output_file = fname.split('.')[0]
        print(output_file)

        story_type = output_file.split('/')[1]
        story_index = int(output_file.split('/')[2].split('_')[0])
        max_loc, max_obj_perloc = match_dict[story_type][story_index]
        graph = construct_graph(output_file, max_loc, max_obj_perloc)
        draw(graph, output_file)



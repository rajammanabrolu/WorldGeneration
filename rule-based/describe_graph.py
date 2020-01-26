import networkx as nx
import numpy as np
import re
import pickle


def extract_tw_template():
    # read templates.txt
    with open("templates.txt", "r") as f:
        room_intro_templ = {}
        phrase_replace = {}
        objects_replace = {}
        room_desc_templ = {}
        d_templ = {}
        for line_index, line in enumerate(f):
            # room intro template
            if line_index in range(2, 30):  # from the file: line 3-30
                room_intro_templ[line_index-1] = line.split(':')[1]
            elif line_index in range(34, 46):  # from the file: line 35-46
                key_phrase, vals = line.split(':')
                phrase_replace[key_phrase] = vals.split(';')
            elif line_index == 295:  # prefix
                prefix = line.split(':')[1].split(';')
            elif line_index == 310:  # suffixes
                suffix = line.split(':')[1].split(';')
            elif line_index in range(171, 186):  # from the file: 172-186
                key_phrase, vals = line.split(':')
                objects_replace[key_phrase] = vals.split(';')
            elif line_index in range(127, 136):  # from the file: 128-136
                key_index, vals = line.split(':')
                room_desc_templ[key_index] = vals
            elif line_index in range(138, 143):  # from the file: 139-143
                key_index, vals = line.split(':')
                d_templ[key_index] = vals
                if len(vals.split(';')) == 2:
                    d_templ[key_index + '_0'] = vals.split(';')[0]
                    d_templ[key_index + '_1'] = vals.split(';')[1]
                    del d_templ[key_index]

    del room_intro_templ[18]
    del room_desc_templ['c3'], room_desc_templ['c6'], room_desc_templ['c9']

    to_remove = []
    for i in range(len(suffix)):
        if '#' in suffix[i] or len(suffix[i]) < 5 or 'TextWorld' in suffix[i]:
            to_remove += [i]
    suffix_copy = [k for i, k in enumerate(suffix) if i not in to_remove]
    suffix = suffix_copy

    to_remove = []
    for i in range(len(prefix)):
        if '#' in prefix[i] or len(prefix[i]) < 5 or 'TextWorld' in prefix[i]:
            to_remove += [i]
    prefix_copy = [k for i, k in enumerate(prefix) if i not in to_remove]
    prefix = prefix_copy

    room_intro_templ_copy = room_intro_templ.copy()
    for k, v in room_intro_templ_copy.items():
        if len(v.split(';')) >= 2:
            # print(v)
            del room_intro_templ[k]

    return room_intro_templ, room_desc_templ, suffix, prefix, objects_replace, d_templ, phrase_replace


def generate_room_intro(loc_dict):
    # generate for locations
    templ_choice = list(np.random.choice(list(room_intro_templ.keys()), size=len(loc_dict)))
    # print('templ_choice', templ_choice)
    make_up_adjs = ['mysterious', 'weird', 'strange', 'unclear']
    room_intro = []
    for l, attr in loc_dict.items():
        index = attr['index']
        obj_list = attr['objects']
        obj_list = [i.lower() for i in obj_list]

        # room introduction part
        templ_l = room_intro_templ[templ_choice[index]]
        templ_l = templ_l.replace('(name)', l)
        templ_l = templ_l.replace('(name-n)', l)
        adj_count = templ_l.count('(name-adj)')
        # print('chosen template is: {}'.format(templ_l))
        # print(adj_count)
        if adj_count > 0:
            adj_choice = np.random.choice(make_up_adjs)
            templ_l = templ_l.replace('(name-adj)', adj_choice)
        rephase_list = re.findall('\#.*?\#', templ_l)
        if rephase_list:
            for i in rephase_list:
                available = phrase_replace[i.strip('#')]
                choice = np.random.choice(available)
                while '#' in choice:
                    match = re.findall('\#.*?\#', choice)[0]
                    new_avail = phrase_replace[match.strip('#')]
                    new_choice = np.random.choice(new_avail)
                    choice = choice.replace(match, new_choice)
                templ_l = templ_l.replace(i, choice)
        templ_l = templ_l.replace('\n', '').strip()
        templ_l = templ_l.strip(' ').strip('.')
        templ_l += '.'
        room_intro.append(templ_l)
    return room_intro


def gen_room_obj(l, cur_obj, use_prefix=True):
    make_up_adjs = ['mysterious', 'weird', 'strange', 'unclear']
    templ_l = ''

    if use_prefix:
        # prefix part
        pre_i_templ = np.random.choice(prefix)
        pre_i_templ = pre_i_templ.replace('\n', '').strip()
        # pre_i = pre_i_templ + ' ' + obj_list.pop()
        pre_i = pre_i_templ + ' ' + cur_obj
        pre_i.replace('room', l)
        # print('----pre_i----')
        # print(pre_i)
        templ_l += pre_i
        if pre_i == '':
            use_prefix = False
            templ_l = ''

    if not use_prefix:
        room_desc_templ_i = np.random.choice(list(d_templ.values()))
        room_desc_templ_i = room_desc_templ_i.replace('(name)', l)
        room_desc_templ_i = room_desc_templ_i.replace('(name-n)', l)
        if 'list' in room_desc_templ_i:
            # remaining_objects = ', '.join([str(i) for i in obj_list])
            # if len(remaining_objects) < 1:
            #     remaining_objects = 'nothing'
            remaining_objects = cur_obj
        adj_count = room_desc_templ_i.count('(name-adj)')
        if adj_count > 0:
            adj_choice = np.random.choice(make_up_adjs)
            room_desc_templ_i = room_desc_templ_i.replace('(name-adj)', adj_choice)
        rephase_list = re.findall('\#.*?\#', room_desc_templ_i)
        if rephase_list:
            for i in rephase_list:
                if 'list' in i:
                    choice = remaining_objects
                else:
                    available = objects_replace[i.strip('#')]
                    choice = np.random.choice(available)
                    while '#' in choice:
                        match = re.findall('\#.*?\#', choice)[0]
                        new_avail = objects_replace[match.strip('#')]
                        new_choice = np.random.choice(new_avail)
                        choice = choice.replace(match, new_choice)
                room_desc_templ_i = room_desc_templ_i.replace(i, choice)
        room_desc_templ_i = room_desc_templ_i.replace('\n', '').strip()
        templ_l += room_desc_templ_i
    templ_l = templ_l.strip(' ').strip('.')

    # suffix part
    suffix_i_temp = np.random.choice(suffix)
    suffix_i_temp = suffix_i_temp.replace('room', l)
    suffix_i_temp = suffix_i_temp.replace('\n', '').strip()
    suffix_i = suffix_i_temp
    templ_l += suffix_i

    templ_l = templ_l.strip(' ').strip('.')
    templ_l += '.'

    # print(templ_l)
    return templ_l


def gen_desc(G, loc_dict, output_file):
    # node: flavor text on locations only
    room_intro = generate_room_intro(loc_dict)
    # print(room_intro)
    loc_count = 0
    for node_name, node_attr in G.nodes.data():
        if node_attr['type'] == 'location':
            loc_flavor = room_intro[loc_count]
            node_attr['flavortext'] = loc_flavor
            loc_count += 1
        else:  # objects or characters
            node_attr['flavortext'] = ''

    # edges: flavor text between location-obj/characters only
    for source, target, edge_attr in G.edges.data():
        if edge_attr['type'] == 'in':
            loc, obj = source, target
            p = np.random.uniform()
            if p < 0.4:
                room_obj_desc = gen_room_obj(loc, obj, use_prefix=True)
            else:
                room_obj_desc = gen_room_obj(loc, obj, use_prefix=False)
            edge_attr['flavortext'] = room_obj_desc
        else:
            edge_attr['flavortext'] = ''
    filename = output_file + '_flavor'
    nx.nx_pydot.write_dot(G, filename + '.dot')


if __name__ == "__main__":
    room_intro_templ, room_desc_templ, suffix, prefix, objects_replace, d_templ, phrase_replace = extract_tw_template()

    output_file = 'binary_data/fairy/1_binary'
    with open(output_file + '_loc_dict_Matched', 'rb') as filehandle:
        loc_dict = pickle.load(filehandle)
    G = nx.read_gml(output_file + '.gml')
    gen_desc(G, loc_dict, output_file)

    output_file = 'binary/mystery/10_binary'
    with open(output_file + '_loc_dict_Matched', 'rb') as filehandle:
        loc_dict = pickle.load(filehandle)
    G = nx.read_gml(output_file + '.gml')
    gen_desc(G, loc_dict, output_file)


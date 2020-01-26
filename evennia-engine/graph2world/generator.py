import os
import math
from uuid import uuid1
from graph2world.function_words import FUNCTION_WORDS


class Generator:
    def __init__(self):
        # easy map from name 2 id
        self.ids = {}
        # store list of commands
        self.instructions = []

    def append(self, instruction):
        self.instructions.append(instruction)

    def load_graph(self, graph, zone):
        # step 0 - determine half of objects
        object_count = graph.number_of_nodes()
        print('Zone: {0}'.format(zone))
        print('There are {0} objects in the knowledge graph.'.format(object_count))
        print('Set exploration counter to {0}.'.format(math.ceil(object_count / 2.0)))

        # step 1 - create all of our rooms
        for node, data in graph.nodes(data=True):
            if data['type'] == 'location':
                # generate a unique id
                data['id'] = str(uuid1())
                self.ids[node] = data['id']
                # get aliases if found
                aliases = ';'
                if 'aliases' in data:
                    aliases += ';'.join(data['aliases']) + ';'
                # create room
                self.append('dig {0}{1}{2}'.format(node, aliases, data['id']))
                # set description if found
                # teleporting and then setting the description is
                # not the most efficient method, but I was experiencing
                # a bug where the newly created room would not be found
                # by describe, but it always seems to work for teleport
                self.append('tel {0}'.format(data['id']))
                self.append('set {0}/zone = \'{1}\''.format(data['id'], zone))
                if 'flavortext' in data:
                    clean_description = ' '.join(data['flavortext'].split())
                    self.append('describe {0}'.format(clean_description))
                else:
                    self.append('describe A nondescript room.')

        # step 2 - fill rooms with objects
        for node, data in graph.nodes(data=True):
            if data['type'] == 'object' or data['type'] == 'character':
                # generate a unique id
                data['id'] = str(uuid1())
                self.ids[node] = data['id']
                # get aliases if found
                aliases = ';'
                if 'aliases' in data:
                    aliases += ';'.join(data['aliases']) + ';'
                # go to room where object belongs

                # old code to only check for only one, need to comment out
                # if len(graph[node]) == 1:
                #     for key in graph[node]:
                #         self.append('tel {0}'.format(self.ids[key]))
                #     for key in graph[node]:
                #         self.append('tel {0}'.format(self.ids[key]))
                # else:
                #     raise Exception('Each object must be in a single room.')
                # create object
                for key in graph[node]:
                    self.append('tel {0}'.format(self.ids[key]))
                    self.append('create/drop {0}{1}{2}'.format(node, aliases, data['id']))
                    # set description if found
                    if 'flavortext' in data and data['flavortext'] != '""':
                        clean_description = ' '.join(data['flavortext'].split())
                        self.append('describe {0} = {1}'.format(data['id'], clean_description))
                    elif 'flavortext' in graph.get_edge_data(node, key)['0']:
                        clean_description = ' '.join(graph.get_edge_data(node, key)['0']['flavortext'].split())
                        self.append('describe {0} = {1}'.format(data['id'], clean_description))
                # if object is not obtainable, lock it in place
                if 'obtainable' not in data:
                    self.append('lock {0} = get:false()'.format(data['id']))
                    if 'get_err_message' in data:
                        self.append('set {0}/get_err_msg = {1}'.format(data['id'], data['get_err_message']))

        # step 3 - create doors between rooms
        for u, v, data in graph.edges(data=True):
            if data['type'] == 'connected':
                self.create_door(u, v, data, graph)
                self.create_door(v, u, data, graph)

    def create_door(self, u, v, data, graph):
        # generate a unique id
        data['id'] = str(uuid1())
        self.ids[u + '|' + v] = data['id']
        # teleport to u
        self.append('tel {0}'.format(self.ids[u]))
        # get aliases if found
        aliases = ''
        if 'aliases' in data:
            aliases += ';'.join(data['aliases']) + ';'
        # we also want to include the name of v
        aliases += v + ';'
        # and any aliases that it may have
        if 'aliases' in graph.nodes[v]:
            aliases += ';'.join(graph.nodes[v]['aliases']) + ';'
        # add custom aliases of my own creation
        tokenized = str.split(v, ' ')
        custom_aliases = Generator.generate_custom_aliases(tokenized, graph.nodes)
        if len(custom_aliases) > 0:
            aliases += ';'.join(custom_aliases) + ';'
        # create link to v
        self.append('open {0}{1} = {2}'.format(aliases, data['id'], graph.nodes[v]['id']))
        # set description if found
        if 'flavortext' in data:
            clean_description = ' '.join(data['flavortext'].split())
            self.append('describe {0} = {1}'.format(data['id'], clean_description))

    @staticmethod
    def generate_custom_aliases(tokens, node_list):
        washed_tokens = []
        for token in tokens:
            if str.upper(token) in FUNCTION_WORDS:
                washed_tokens.append(None)
            else:
                washed_tokens.append(token)

        output = []
        current_index = 0
        last_clean_index = 0
        washed_tokens = list(reversed(washed_tokens))
        for token in washed_tokens:
            if token is None:
                last_clean_index = current_index + 1
            else:
                alias = ' '.join(reversed(washed_tokens[last_clean_index:current_index + 1]))
                match_found = False
                for item in node_list:
                    if alias == str.lower(item):
                        match_found = True
                if match_found:
                    continue
                else:
                    output.append(alias)
            current_index += 1

        return output

    def to_file(self, path='../engine/world/test.ev'):
        this_folder = os.path.dirname(os.path.abspath(__file__))

        with open(os.path.join(this_folder, path), 'w') as file:
            for command in self.instructions:
                file.write(command + '\n#\n')

    def print(self):
        for command in self.instructions:
            print(command)

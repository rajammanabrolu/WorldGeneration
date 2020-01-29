#!/usr/bin/env python3

import json
import os
import numpy as np
import tensorflow as tf
import matplotlib

matplotlib.use('Agg')

import networkx as nx
import json
import argparse
import matplotlib.pyplot as plt
import random
import gpt_2_simple as gpt2


class World:
    def __init__(self, args):
        # self.graph = nx.read_gml(args.gml)
        self.graph = nx.nx_pydot.read_dot(args.gml)

        self.args = args

        # init GPT-2
        with open(args.input_text) as f:
            self.input_text = f.read()

        self.sess = gpt2.start_tf_sess()

        gpt2.load_gpt2(self.sess, run_name=args.run_name)

    def generate_flavor(self):
        # loc_templates = ["\n\nQ: What is {}?\nA:"]
        # obj_templates = ["\n\nQ: What is {}?\nA:"]
        # person_templates = ["\n\nQ: Who is {}?\nA:"]
        loc_templates = ["\n\nQ: Describe what {} looks like.\nA:"]
        obj_templates = ["\n\nQ: Describe what {} is.\nA:"]
        person_templates = ["\n\nQ: Describe who {} is.\nA:"]

        type2temp = {"location": loc_templates, "object": obj_templates, "character": person_templates, }

        for key in self.graph.nodes():
            node = self.graph.nodes[key]

            # select template
            templates = type2temp[node['type']]

            # find end of sentence after target word
            titles = ["Mr.", "Dr.", "Ms.", "Mrs."]
            end = 0

            before_text = self.input_text[:self.input_text.find(key)].split()
            after_text = self.input_text[self.input_text.find(key):].split()

            for i in range(len(after_text)):
                word = after_text[i]
                if word[-1] == '.' and word not in titles:
                    end = i + 1
                    break
            context = " ".join(before_text + after_text[:end])
            context = self.input_text  # testing

            # generate flavor text
            target = key.translate(str.maketrans('', '', ',.!?'))

            # prepend article
            if target[0].islower():
                target = 'the ' + target

            template = random.choice(templates).format(target)

            primer = context + " " + template

            text = gpt2.generate(self.sess,
                                 length=50,
                                 temperature=args.temperature,
                                 top_k=args.top_k,
                                 seed=args.seed,
                                 prefix=primer,
                                 nsamples=1,
                                 batch_size=1,
                                 run_name=args.run_name, return_as_list=True,
                                 )[0]
            print(primer)

            # cut the prefix ourselves because the people who wrote gpt2simple won't do it for us
            text = text[len(primer):]

            # import ipdb;
            # ipdb.set_trace()

            # TODO detemine where to cut generation
            text = text[:text.find(".") + 1]

            print(template + text)
            # node['flavortext'] = template.format(target) + text
            # t = 'You examine {}. '
            t = ''
            node['flavortext'] = t.format(target) + text.strip()

    def draw(self, filename="graph.png"):
        plt.figure()
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True)
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=self.edge_labels)
        plt.savefig(filename)
        plt.close()

    def export(self, filename="graph.dot"):
        nx.nx_pydot.write_dot(self.graph, filename)
        nx.write_gml(self.graph, "graph.gml", stringizer=None)


def parse_args():
    parser = argparse.ArgumentParser()
    # parser.add_argument('--gml', default='world.gml')
    parser.add_argument('--input_text', default='input_text.txt')
    parser.add_argument('--length', default=50, type=int)
    parser.add_argument('--batch_size', default=1, type=int)
    parser.add_argument('--temperature', default=0.7, type=float)
    parser.add_argument('--top_k', default=1, type=int)
    parser.add_argument('--run_name', default='117M')
    parser.add_argument('--seed', default=0, type=int)
    parser.add_argument('--nsamples', default=5, type=int)

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    random.seed(args.seed)

    args.gml = args.input_text[:-4] + '.dot'

    world = World(args)
    world.generate_flavor()
    world.export()

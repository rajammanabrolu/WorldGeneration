import argparse
from graph2world.g2w import *


file_to_zone = {'demo.dot': 'ABCD', 'dan_fairy.dot': 'SB88', 'dan_mystery.dot': '5F6Z', 'random_fairy.dot': 'X43K', 'random_mystery.dot': 'N766', 'wei_fairy.dot': '9Q4F', 'wei_mystery.dot': '8F66', 'wesley_fairy.dot': 'B78H', 'wesley_mystery.dot': 'R28B'}


def parse_args():
    parser = argparse.ArgumentParser(description='Basic CLI for generating Evennia worlds from GML files.')
    parser.add_argument('-i', '--input-file', type=str, default='graph.gml', help='Input file *.gml to read in')
    parser.add_argument('-o', '--output-file', type=str, default=None, help='Output file *.ev to write to')

    return parser.parse_args()


def main():
    # args = parse_args()
    # g = get_gml_graph(args.input_file)
    # graph_to_world(g, file_to_zone[args.input_file], args.output_file)
    # file = 'dan_fairy.dot'
    # graph_to_world(get_gml_graph(file), file_to_zone[file], '../engine/world/' + file.replace('.dot', '.ev'))
    # file = 'dan_mystery.dot'
    # graph_to_world(get_gml_graph(file), file_to_zone[file], '../engine/world/' + file.replace('.dot', '.ev'))
    # file = 'random_fairy.dot'
    # graph_to_world(get_gml_graph(file), file_to_zone[file], '../engine/world/' + file.replace('.dot', '.ev'))
    # file = 'random_mystery.dot'
    # graph_to_world(get_gml_graph(file), file_to_zone[file], '../engine/world/' + file.replace('.dot', '.ev'))
    # file = 'wesley_fairy.dot'
    # graph_to_world(get_gml_graph(file), file_to_zone[file], '../engine/world/' + file.replace('.dot', '.ev'))
    # file = 'wesley_mystery.dot'
    # graph_to_world(get_gml_graph(file), file_to_zone[file], '../engine/world/' + file.replace('.dot', '.ev'))
    # file = 'wei_mystery.dot'
    # graph_to_world(get_gml_graph(file), file_to_zone[file], '../engine/world/' + file.replace('.dot', '.ev'))
    file = 'demo.dot'
    graph_to_world(get_gml_graph(file), file_to_zone[file], '../engine/world/' + file.replace('.dot', '.ev'))


if __name__ == '__main__':
    main()

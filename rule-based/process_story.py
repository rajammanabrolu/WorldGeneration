import re
import pickle
import networkx as nx
import os

# load nltk packages
import nltk
from nltk.tag import pos_tag, map_tag
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')
nltk.download('universal_tagset')
from nltk.corpus import stopwords
set(stopwords.words('english'))
from nltk.stem import WordNetLemmatizer
from nltk.tokenize.treebank import TreebankWordDetokenizer
detokenizer = TreebankWordDetokenizer()
wnl = WordNetLemmatizer()

# load NeuralCoref and add it to the pipe of SpaCy's model
import spacy
nlp = spacy.load('en')
import neuralcoref
coref = neuralcoref.NeuralCoref(nlp.vocab,
                                greedyness=0.5, max_dist=50,
                                blacklist=False,
                                )
nlp.add_pipe(coref, name='neuralcoref')


def process_tag(phrase, target):
    text = nltk.word_tokenize(phrase)
    posTagged = pos_tag(text)
    simplifiedTags = [(word, map_tag('en-ptb', 'universal', tag)) for word, tag in posTagged]
    res = ''
    for (word, tag) in simplifiedTags:
        if tag in target:
            res += word + ' '
    return res.strip()


def generate_loc_dict(G_edges_data):
    loc_dict = {}
    index_dict = {}
    # take the loc, and then add the entities in
    count = 0
    for triple in G_edges_data:
        print(triple)
        h, t, attribute = triple
        l = attribute['loc']

        if l is not None:
            if l not in loc_dict:
                loc_dict[l] = {}
                loc_dict[l]['objects'] = set()
                loc_dict[l]['index'] = count
                index_dict[count] = l
                count += 1
            if 'L' not in h and len(h) > 0 and len(h.split(' ')) <= 3:
                loc_dict[l]['objects'].add(h)
            if 'L' not in t and len(t) > 0 and len(t.split(' ')) <= 3:
                loc_dict[l]['objects'].add(t)

    # remove the entry with empty locations
    loc_dict_copy = loc_dict.copy()
    for l, attr in loc_dict_copy.items():
        if len(l) == 0:
            del loc_dict[l]

    # remove similar locations: only remove when strict contain
    loc_dict_copy = loc_dict.copy()
    loc_set = set()
    for l, attr in loc_dict_copy.items():
        for key in loc_set:  # existing loc
            if l.lower() in key.lower() or key.lower() in l.lower():
                print('similar locations: current l: {} existing key: {}'.format(l, key))
                l = key
                del loc_dict[l]
        if l.lower() not in loc_set and l not in loc_set:
            loc_set.add(l)

    # for similar objects: replace it to the existing one
    # for those objects who are similar to locations: remove it
    location_lst = list(loc_dict.keys())
    loc_dict_copy = loc_dict.copy()
    obj_set = set()  # for all the objects appeared
    for l, attr in loc_dict_copy.items():
        obj_list = attr['objects']
        updated = set()
        for i in obj_list:
            valid = True
            # if similar to locations, do not add to obj_set
            for j in location_lst:
                if len(set(i.lower().split(' ')).intersection(set(j.lower().split(' ')))) != 0:
                    print('this object is similar to locations:', i, '---to---', j)
                    valid = False
            # if has similarity to other objects, remove the one originally exists in obj_set
            tmp = obj_set.copy()
            for j in obj_set:
                similar_words = set(i.lower().split(' ')).intersection(set(j.lower().split(' ')))
                if len(similar_words) != 0:  # still valid but change it to the existing one
                    print('similar objects:', i, '---to---', j)
                    intersection = ' '.join(similar_words)
                    if i != i.lower() or j != j.lower():  # i or j is upper case
                        i = intersection.title()
                    else:
                        i = intersection
                    tmp.remove(j)
                    # tmp.add(i)
            obj_set = tmp.copy()

            if i.lower() not in obj_set and i not in obj_set:
                obj_set.add(i)

            if valid:
                updated.add(i)
        loc_dict[l]['objects'] = list(updated)
        print('update is {}'.format(updated))

    # remove the entry with empty objects
    loc_dict_copy = loc_dict.copy()
    for l, attr in loc_dict_copy.items():
        if len(attr['objects']) == 0:
            del loc_dict[l]

    # reorder the index
    loc_dict_copy = loc_dict.copy()
    count = 0
    for l, _ in loc_dict_copy.items():
        loc_dict[l]['index'] = count
        count += 1

    print('--------------------loc dict----------------')
    print(loc_dict)
    return loc_dict


def process_htl(h, t, l):
    # tokens
    if l is not None:
        l = detokenizer.detokenize(nltk.word_tokenize(l))
    h = detokenizer.detokenize(nltk.word_tokenize(h))
    t = detokenizer.detokenize(nltk.word_tokenize(t))
    # remove stop words
    if l is not None:
        l = ' '.join([word for word in l.split(' ') if word not in stopwords.words('english')])
    h = ' '.join([word for word in h.split(' ') if word not in stopwords.words('english')])
    t = ' '.join([word for word in t.split(' ') if word not in stopwords.words('english')])
    # lemmatize
    if l is not None:
        l = ' '.join([wnl.lemmatize(word) for word in l.split(' ')])
    h = ' '.join([wnl.lemmatize(word) for word in h.split(' ')])
    t = ' '.join([wnl.lemmatize(word) for word in t.split(' ')])
    return h, t, l


def process_output(output_file, pick_max=False):
    G1 = nx.Graph()

    if pick_max:
        info_line = {}
    location = None
    with open(output_file + '.txt', 'r', encoding='utf-8') as f:
        for line_index, line in enumerate(f):
            print('-------------------------------current line--------------------------------')
            if len(line.strip()) == 0:  # blank line
                pass
            elif not line.startswith('0'):  # the sentence line
                if pick_max and len(info_line) != 0:
                    res, max_score = sorted(info_line.items(), key=lambda kv: kv[1], reverse=True)[0]
                    h, t, location = res
                    # print('here!')
                    # print('res: {}'.format(res))
                    # print('score: {}'.format(max_score))
                    h, t, location = process_htl(h, t, location)
                    # check if we need a new node
                    if len(h) != 0 and h not in G1.nodes():
                        G1.add_node(h, loc=location)

                    if len(t) != 0 and t not in G1.nodes():
                        G1.add_node(t, loc=location)
                    # G1.add_edge(h, t, relation=r, loc=location)
                    G1.add_edge(h, t, loc=location)

                print(line)
                coref_entity = {}
                if line_index == 0:
                    prev_sentence = line
                else:
                    prev_cur = prev_sentence + line
                    # print('----------------prev_cur----------------')
                    # print(prev_cur)
                    doc = nlp(prev_cur)  # identify co-reference
                    if doc._.has_coref:
                        for item in doc._.coref_clusters:
                            main = str(item.main)
                            mention_list = [str(i) for i in list(item.mentions)]
                            # print('main ----------------mention list')
                            # print(main, mention_list)
                            coref_entity[main] = mention_list
                    prev_sentence = line
                if pick_max:
                    info_line = {}
            else:  # the triplets line
                # rule:
                # 1. remove the context if necessary
                # 2. save location information
                # 3. replace by co-reference
                # 4. pos tag on subjects
                print(line)
                # find the first space to separte scores ad triple
                score, triple_str = float(line[:line.find(' ')]), line[line.find(' '):]

                content_list = re.findall('\(.*?\)', triple_str)

                if len(content_list) != 1:  # this is the context
                    assert len(content_list) == 2
                    context_index = triple_str.find('Context')
                    assert context_index != -1
                    context = content_list[0].strip('(')
                # remove context part
                triple_str = content_list[-1]
                triple_str = triple_str.strip('(').strip(')')

                try:
                    h, r, t = tuple([i.strip() for i in triple_str.split(';')])
                    h, r, t = h.strip(), r.strip(), t.strip()

                    # print('-----triple------')
                    # print(h, r, t)

                    if 'T:' in t or len(t) == 0:  # remove the time information
                        pass
                    else:
                        if 'L:' in t:  # we want to save the location information
                            location = t[2:].strip()
                            location = detokenizer.detokenize(nltk.word_tokenize(location))
                            h = process_tag(h, target=['NOUN'])
                        else:
                            if len(coref_entity) != 0:  # replace by co-reference
                                for main, mention_list in coref_entity.items():
                                    for i in mention_list:  # example 'queen' and 'the new queen'
                                        if h in i:
                                            h = main
                                            print('h replaced', h)
                                        if t in i:
                                            t = main
                                            print('t replaced', t)
                            h = process_tag(h, target=['NOUN'])
                            t = process_tag(t, target=['NOUN'])  # keep only nouns in the subject
                            if pick_max:  # add into graph when reaching the next sentence line
                                info_line[(h, t, location)] = score
                        if not pick_max:  # add into graph here

                            h, t, location = process_htl(h, t, location)
                            # check if we need a new node
                            if len(h) != 0 and h not in G1.nodes():
                                G1.add_node(h, loc=location)

                            if len(t) != 0 and t not in G1.nodes():
                                G1.add_node(t, loc=location)
                            # G1.add_edge(h, t, relation=r, loc=location)
                            G1.add_edge(h, t, loc=location)
                except ValueError:
                    print('Irregular ouput from OpenIE')

    G_edges_data = G1.edges.data()
    loc_dict = generate_loc_dict(G_edges_data)
    with open(output_file + '_loc_dict', 'wb') as filehandle:
        pickle.dump(loc_dict, filehandle)


def walk_through_files(path):
    for (dirpath, dirnames, filenames) in os.walk(path):
        for filename in filenames:
            if filename.endswith('_binary.txt'):
                yield os.path.join(dirpath, filename)


if __name__ == "__main__":
    folder, pick_max = 'binary_data/', True
    for fname in walk_through_files(folder):
        print('processing')
        print(fname)
        output_file = fname.split('.')[0]
        print(output_file)
        process_output(output_file, pick_max=pick_max)
        print('finished the file in {}'.format(output_file))




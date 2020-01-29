import pickle
import urllib


def demo():
    load_file = open('fairytale.pickle', 'rb')
    stories = pickle.load(load_file)
    load_file.close()

    print(len(stories))
    # get title clean
    example_title = urllib.parse.unquote(stories[0][0].replace('_', ' '))
    example_plot = stories[0][1]
    print(example_title)
    print(example_plot)


if __name__ == '__main__':
    demo()

import pickle
from scrape.get_page import *
from scrape.get_plot import *


# scrape fairy tales and store output as pickle
# format is list of tuples (Wikipedia title, plot)
def main_fairy_tale():
    # may contain duplicates
    pages = get_pages('/wiki/Category:Fairy_tales_by_continent')
    # this page has a bunch of links as well,
    # many are probably duplicates, but worth trying
    pages.extend(get_custom('/wiki/Lang%27s_Fairy_Books', 'mw-content-text'))
    # remove said duplicates
    pages = list(set(pages))

    compile_pages(pages, 'fairytale')


def compile_pages(pages, file_name):
    compiled = []
    for link in pages:
        # remove /wiki/
        title = link[6:]
        plot = get_plot(title)
        compiled.append((title, plot))

    # preview in console window
    # print(compiled)
    # remove entries where we couldn't find a plot
    bad_compiled = [x for x in compiled if x[1] is None]
    for item in bad_compiled:
        print(item[0])
        print(item[1])
        print('-')
    clean_compiled = [x for x in compiled if x[1] is not None]
    # pickle our stories
    store_file = open(f'{file_name}.pickle', 'wb')
    pickle.dump(clean_compiled, store_file)
    store_file.close()
    print('Scrape Completed!')
    print(f'Exported {len(clean_compiled)} clean records.')
    print(f'Ignored {len(bad_compiled)} unclean records.')


def main_detective():
    pages = []
    # our looping technique doesn't work quite as well here,
    # so instead we just add a bunch of category pages that can be found
    pages.extend(get_page('/wiki/Category:Sherlock_Holmes_short_stories_by_Arthur_Conan_Doyle'))
    pages.extend(get_custom('/wiki/Canon_of_Sherlock_Holmes', 'mw-content-text'))
    pages.extend(get_page('/wiki/Category:Mystery_short_stories'))
    # the below don't work too well, because they are story collections, and often the text is inline
    # pages.extend(get_page('/wiki/Category:Mystery_short_story_collections_by_Isaac_Asimov'))
    # pages.extend(get_page('/wiki/Category:Short_story_collections_by_Leslie_Charteris'))
    # pages.extend(get_page('/wiki/Category:Short_story_collections_by_Agatha_Christie'))
    # pages.extend(get_page('/wiki/Category:Short_story_collections_by_Ruth_Rendell'))
    # pages.extend(get_page('/wiki/Category:Short_story_collections_by_Dorothy_L._Sayers'))
    pages.extend(get_page('/wiki/Category:Mary_Russell_(book_series)'))
    pages.extend(get_page('/wiki/Category:Occult_detective_fiction'))
    pages.extend(get_page('/wiki/Category:Detective_fiction_short_stories'))
    pages.extend(get_page('/wiki/Category:Detective_novels'))
    pages.extend(get_page('/wiki/Category:Children%27s_mystery_novels'))

    # detective novels by country page
    temp = get_custom('/wiki/Category:Detective_novels', 'mw-subcategories', 'novel', True)
    for t in temp:
        if 'novel' in t:
            pages.extend(get_page(t))
    # children's mystery novels
    temp = get_custom('/wiki/Category:Children%27s_mystery_novels', 'mw-subcategories', 'novel', True)
    for t in temp:
        if 'novel' in t:
            pages.extend(get_page(t))
    # mystery novels by writer page
    temp = get_custom('/wiki/Category:Mystery_novels_by_writer', 'mw-subcategories', 'novel', True)
    for t in temp:
        if 'novel' in t:
            pages.extend(get_page(t))
    # remove any duplicates
    pages = list(set(pages))
    # print(len(pages))
    compile_pages(pages, 'mystery')


# test method to just display some of the results
def print_stories(file_name, count=100):
    load_file = open('fairytale.pickle', 'rb')
    stories = pickle.load(load_file)
    load_file.close()

    for i in range(min(count, len(stories))):
        print(stories[i])


# testing, ignore
def scratch_work():
    x = get_plot('The_Groac%27h_of_the_Isle_of_Lok')
    print(x)


if __name__ == '__main__':

    print("scraping fairy tales")
    main_fairy_tale()
    print("done")
    print("scraping fairy tales")
    main_detective()
    print("done")
    # print_stories('mystery', 300)

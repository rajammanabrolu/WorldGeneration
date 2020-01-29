import urllib
import wikipedia
import numpy as np


# left over from the medium example
def get_example_plots():
    example_titles = ['Algol (film)', 'Dr. Jekyll and Mr. Hyde (1920 Haydon film)',
                      'Figures of the Night', 'The Invisible Ray (1920 serial)', 'The Man from Beyond',
                      'Black Oxen', 'Aelita', 'The Hands of Orlac (1924 film)']
    example_plots = []

    for title in example_titles:
        example_plots.append(get_plot(title))

    return zip(example_titles, example_plots)


# create a list of all the names you think/know the section might be called
possibles = ['Plot', 'Synopsis', 'Plot synopsis', 'Plot summary',
             'Story', 'Plotline', 'The Beginning', 'Summary',
             'Content', 'Premise', 'The story', 'Legend summary',
             'Fairy tale', 'Narrative', 'Plot of the fairy tale',
             'Tale', 'Traditional tale', 'Story (The Brothers Grimm)',
             'Plot Summary', 'Story summary', 'Plot introduction']


def get_plot(title):
    # sometimes those names have 'Edit' latched onto the end due to
    # user error on Wikipedia. In that case, it will be 'PlotEdit'
    # so it's easiest just to make another list that accounts for that
    possibles_edit = [i + 'Edit' for i in possibles]
    # then merge those two lists together
    all_possibles = possibles + possibles_edit

    # load the page once and save it as a variable, otherwise it will request
    # the page every time.
    # always do a try, except when pulling from the API, in case it gets confused
    # by the tittle.
    try:
        title = urllib.parse.unquote(title.replace('_', ' '))
        wik = wikipedia.WikipediaPage(title)
    except:
        wik = np.NaN

    # a new try, except for the plot
    plot = None

    try:
        # for all possible titles in all_possibles list
        for j in all_possibles:
            # if that section does exist, i.e. it doesn't return 'None'
            if wik.section(j) is not None:
                # then that's what the plot is! Otherwise try the next one!
                plot = section(wik, j).replace('\n', '').replace("\'", "")
                break
    except:
        pass

    return plot


# default section method has problems (subsections count as sections),
# so I wrote a custom one
def section(wiki, section_title):
    section_text = u"== {} ==".format(section_title)

    try:
        index = wiki.content.index(section_text) + len(section_text)
    except ValueError:
        return None

    try:
        next_index = wiki.content.index("\n== ", index)
    except ValueError:
        next_index = len(wiki.content)

    return wiki.content[index:next_index].replace("===", "\n").lstrip("=").strip()

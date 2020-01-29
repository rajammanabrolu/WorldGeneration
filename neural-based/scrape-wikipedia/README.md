# Brief Explanation

## scrape package

### get_page.py

Search wikipedia group pages to find links to possible stories

### get_page.py

Search Wikipedia page for plot data using Beautiful Soup

## root folder

### main.py

Code which utilizes the scrape package to store data. You only need to run this if you want to re-scrape the data. Otherwise, just use the pickle files.

### demo_load.py

Very simple code showing how to read the output format

### fairytale.pickle

Data stored here as a list of tuples (name, plot)

The name is encoded in html so that the original page can easily be referenced (helpful in debugging). If you need the titles for whatever reason in the correct format, see demo_load.py for how it can easily be cleaned up.

### mystery.pickle

Data format same as above, this time holding the detective / mystery stories. Sources for both can be found in main.py.

import requests
from bs4 import BeautifulSoup


def get_subcategories(soup):
    return get_section_links(soup, 'mw-subcategories', 'fairy', True)


def get_stories(soup):
    return get_section_links(soup, 'mw-pages', 'redlink')


def get_section_links(soup, section_id, filter_text, contains=False):
    links = []

    x = soup.find(id=section_id)
    if x is None:
        return links

    for i in x.find_all(name='li'):
        # pull the actual link for each one
        for link in i.find_all('a', href=True):
            links.append(link['href'])
            break

    cleaned_links = [i for i in links if i[0:6] == '/wiki/']
    if contains:
        cleaned_links = [i for i in cleaned_links if filter_text in str.lower(i)]
    else:
        cleaned_links = [i for i in cleaned_links if filter_text not in str.lower(i)]
    return cleaned_links


def get_custom(url, section_id, filter_text='redlink', contains=False):
    html = requests.get('https://en.wikipedia.org' + url)
    b = BeautifulSoup(html.text, 'lxml')
    return get_section_links(b, section_id, filter_text, contains)


def get_page(url):
    html = requests.get('https://en.wikipedia.org' + url)
    b = BeautifulSoup(html.text, 'lxml')
    output = []

    output.extend(get_stories(b))
    subcategory_links = get_subcategories(b)

    for category in subcategory_links:
        output.extend(get_page(category))

    return output


def get_pages(link):
    return list(set(get_page(link)))

import dataset
import requests
from lxml import html
import time
import sqlalchemy


INFO = {
    'en': {
        'url': 'https://cambodiadaily.com',
        'db': 'sqlite:///archive_en.db'
    },
    'kh': {
        'url': 'https://cambodiadailykhmer.com',
        'db': 'sqlite:///archive_kh.db'
    }
}


def scrape_page(url, table, language):
    page = requests.get(url)
    tree = html.fromstring(page.content)
    article_urls = tree.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "entry-title", " " ))]//a/@href')
    for url in article_urls:
        url = url.strip()
        try:
            table.insert(dict(url=url))
        except sqlalchemy.exc.IntegrityError:
            pass
    if language == 'kh':
        paginated_url = tree.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "alignright", " " ))]//a/@href')
    else:
        paginated_url = tree.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "pagination-next", " " ))]//a/@href')
    time.sleep(5)
    return paginated_url


def scrape_site(url, table, language):
    homepage = requests.get(url)
    tree = html.fromstring(homepage.content)
    date_urls = [url for url in tree.xpath('//*[@id="archivesdropfront"]/select/option/@value') if url]
    for url in date_urls:
        page = 1
        print('scraping: {}'.format(url))
        paginated_url = scrape_page(url, table, language)
        print('...page {}'.format(page))
        while paginated_url:
            page += 1
            url = paginated_url[0]
            print('...page {}'.format(page))
            paginated_url = scrape_page(url, table, language)


def run(language):
    print('beginning scrape of {} site'.format(language))
    db = dataset.connect(INFO[language]['db'])
    table = db.get_table('url', primary_id='url', primary_type='String')
    scrape_site(INFO[language]['url'], table, language)


if __name__ == '__main__':
    run('en')
    run('kh')


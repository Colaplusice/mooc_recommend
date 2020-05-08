import asyncio
import logging

import aiohttp
from bs4 import BeautifulSoup
from crawler_utils.utils import timer

base_url = 'https://mooc.douban.com/top250'
results = {}


class mooc:
    def __init__(self, id, title, description, star, leader, tags, years, country, director_description, image_link):
        self.id = id
        self.star = star
        self.description = description
        self.title = title
        self.leader = leader
        self.tags = tags
        self.years = years
        self.country = country
        self.director_description = director_description
        self.image_link = image_link


async def fetch(url):
    async with aiohttp.ClientSession()as session:
        async with session.get(url) as response:
            print(response.status)
            assert response.status == 200
            return await response.text()


async def write_images(image_link, image_name):
    async with aiohttp.ClientSession()as session:
        async with session.get(image_link) as response:
            assert response.status == 200
            with open('mooc_images/' + image_name + '.png', 'wb')as opener:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    opener.write(chunk)


async def parse(html):
    soup = BeautifulSoup(html, 'html.parser')
    moocs_info = soup.find('ol', {'class': 'grid_view'})
    moocs = []
    for mooc_info in moocs_info.find_all('li'):
        pic = mooc_info.find('div', {'class': 'pic'})
        picture_url = pic.find('img').attrs['src']
        mooc_id = pic.find('em').text
        url = mooc_info.find('div', {"class": "info"})
        title = url.find('span', {'class': 'title'}).text
        # 保存图片文件到本地
        # if picture_url is not None:
        #     await write_images(picture_url, title)
        info = url.find('div', {'class': 'bd'})
        mooc_detail = info.find('p')
        quote = info.find('p', {'class': 'quote'})
        if quote is not None:
            description = quote.find('span').text
        else:
            description = ''
            print(title + 'description is None')
        star = info.find('div', {"class": 'star'}).find('span', {'class': 'rating_num'}).text
        tags = mooc_detail.text.strip().split('\n')[-1].split('/')[-1].split(' ')
        tags = [tag.strip() for tag in tags]
        years = mooc_detail.text.strip().split('\n')[-1].split('/')[0].strip()
        country = mooc_detail.text.strip().split('\n')[-1].split('/')[1].strip()
        temp = mooc_detail.text.strip().split('\n')
        try:
            director_description = temp[0].split('/')[0].strip().split('\xa0')[0].split(':')[1]
        except IndexError:
            director_description = ''
        try:
            leader = temp[0].split('/')[0].strip().split('\xa0')[-1].split(':')[1]
        except IndexError:
            leader = ''
        assert title is not None
        assert star is not None
        assert leader is not None
        assert years is not None
        assert country is not None
        assert director_description is not None
        assert tags is not None
        assert picture_url is not None
        assert mooc_id is not None
        moocs.append(mooc(title=title, description=description, star=star, leader=leader, years=years, country=country, director_description=director_description, tags=tags, image_link=picture_url,
                            id=mooc_id
                            )
                      )
    next_page = soup.find('link', {'rel': 'next'})
    if next_page is not None and next_page.attrs.get('href'):
        next_link = base_url + next_page.attrs['href']
    else:
        print('finished!')
        next_link = None
    return moocs, next_link


def write_moocs(moocs):
    with open('moocs.csv', 'a+')as opener:
        if opener.tell() == 0:
            opener.writelines(','.join(['id', 'title ', 'image_link ', 'country ', 'years ', 'director_description', 'leader', 'star ', 'description', 'tags', '\n']))
        for mooc in moocs:
            opener.write(','.join([mooc.id, mooc.title, mooc.image_link, mooc.country, mooc.years, mooc.director_description, mooc.leader, mooc.star, mooc.description, '/'.join(mooc.tags), '\n']))


async def get_results(url):
    html = await fetch(url)
    moocs, next_link = await parse(html)
    write_moocs(moocs)
    return next_link
    # results[url] = mooc


async def handle_tasks(work_queue):
    while not work_queue.empty():
        current_url = await work_queue.get()
        try:
            next_link = await get_results(current_url)
            print('put link:', next_link)
            if next_link is not None:
                work_queue.put_nowait(next_link)

        except Exception as e:
            logging.exception('Error for {}'.format(current_url), exc_info=True)


# async def main():
#     async with aiohttp.ClientSession() as session:
#         html = await fetch(session, url)
#         links = await parse(html)

@timer
def envent_loop():
    q = asyncio.Queue()
    q.put_nowait(base_url)
    loop = asyncio.get_event_loop()
    tasks = [handle_tasks(q)]
    loop.run_until_complete(asyncio.wait(tasks))


envent_loop()

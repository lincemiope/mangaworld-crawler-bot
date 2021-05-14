import requests
from lxml import html
from utils import str_to_date, is_new
from const import BASE_URL, VOLUME_XPATH

create_uri = lambda tail: f'{BASE_URL}{tail}'

def get_new_chapters(followed_issues, last_check):
    paths = VOLUME_XPATH[1]
    results = {}

    for issue in followed_issues:
        results[issue] = {}
        uri = create_uri(issue)
        response = requests.get(uri)
        source = response.content
        tree = html.fromstring(source)
        volumes = tree.xpath(VOLUME_XPATH[0])

        for volume in volumes:
            title = volume.xpath(paths['title'])[0]
            results[issue][title] = {
                'chapters': []
            }

            chapters_data = volume.xpath(paths['chapters'][0])

            for cd in chapters_data:
                chapter = {
                    'title': cd.xpath(paths['chapters'][1]['title'])[0],
                    'release': str_to_date(cd.xpath(paths['chapters'][1]['release'])[0]),
                    'url': cd.xpath(paths['chapters'][1]['url'])[0]
                }

                if is_new(chapter['release'], last_check):
                    results[issue][title]['chapters'].append(chapter)

            if len(results[issue][title]['chapters']) == 0:
                 del(results[issue][title])

        if len(results[issue]) == 0:
            del(results[issue])

    return results

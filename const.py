DATA_FILE = 'data.json'
TELEGRAM_TOKEN = '1629324484:AAHPpjG3w-repwC0dGL7zZhqO6WD5On9IY0'
URL_PATTERN = r'https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)'
BASE_URL = 'https://www.mangaworld.cc'
CHECK_COOLDOWN = 60 * 15
VOLUME_XPATH = (
    '//div[@class="volume-element pl-2"]', {
        'title': 'div[@class="volume w-100 py-2"]/p/text()',
        'chapters': (
            'div[@class="volume-chapters pl-2"]/div[@class="chapter"]',
            {
                'title': 'a/span/text()',
                'release': 'a/i/text()',
                'url': 'a/@href'
            }
        )
    }
)
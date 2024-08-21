import requests
import svgwrite
from svgwrite import cm, mm
from PIL import Image
from io import BytesIO

MEDIUM_RSS_URL = 'https://medium.com/feed/@dikaelsaputra'
README_PATH = 'README.md'
THUMBNAIL_PATH = 'thumbnail.png'

def fetch_medium_rss():
    response = requests.get(MEDIUM_RSS_URL)
    response.raise_for_status()
    return response.text

def parse_rss(rss_data):
    from xml.etree import ElementTree as ET
    root = ET.fromstring(rss_data)
    item = root.find('.//item')
    title = item.find('title').text
    link = item.find('link').text
    description = item.find('description').text
    media_content = item.find('.//media:content')
    thumbnail_url = media_content.get('url') if media_content is not None else None
    return title, link, description, thumbnail_url

def download_thumbnail(thumbnail_url):
    response = requests.get(thumbnail_url)
    response.raise_for_status()
    img = Image.open(BytesIO(response.content))
    img.save(THUMBNAIL_PATH)

def create_svg(title, link, description):
    dwg = svgwrite.Drawing('content.svg', profile='tiny', size=(210*mm, 297*mm))
    dwg.add(dwg.text(title, insert=(10*mm, 20*mm), fill='purple', font_size='20px', font_weight='bold'))
    dwg.add(dwg.text(description, insert=(10*mm, 40*mm), fill='green', font_size='14px'))
    dwg.add(dwg.text(f'Read more: {link}', insert=(10*mm, 60*mm), fill='blue', font_size='12px'))
    dwg.save()

def update_readme(title, link, description):
    with open(README_PATH, 'w') as f:
        f.write(f'# Terbaru dari Medium\n\n')
        f.write(f'![Medium Thumbnail](path-to-thumbnail.png)\n\n')
        f.write(f'## [{title}]({link})\n\n')
        f.write(f'**Deskripsi:**\n{description}\n\n')
        f.write(f'---\n\n')
        f.write(f'Generated with ❤️ by Medium')

def main():
    rss_data = fetch_medium_rss()
    title, link, description, thumbnail_url = parse_rss(rss_data)
    if thumbnail_url:
        download_thumbnail(thumbnail_url)
    create_svg(title, link, description)
    update_readme(title, link, description)

if __name__ == '__main__':
    main()

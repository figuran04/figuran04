import requests
import feedparser
from bs4 import BeautifulSoup
from html import escape

FEED_URL = "https://medium.com/feed/@dikaelsaputra"

def fetch_medium_posts(feed_url, num_posts=10):
    feed = feedparser.parse(feed_url)
    posts = []

    for entry in feed.entries[:num_posts]:
        title = entry.title
        link = entry.link

        # Mengambil summary dengan BeautifulSoup
        summary_html = entry.summary
        soup = BeautifulSoup(summary_html, 'html.parser')

        # Menyaring img tag dan mengambil src
        img_tag = soup.find('img')
        image_url = img_tag['src'] if img_tag else None

        # Mengambil summary dengan maksimal 200 karakter
        summary = soup.get_text()[:150] + '...' if len(soup.get_text()) > 150 else soup.get_text()

        posts.append((title, link, image_url, summary))

    return posts

def update_readme(posts):
    # Read the existing README content
    with open('README.md', 'r') as f:
        readme_content = f.readlines()

    # Find the section to update
    start_marker = "<!--START_SECTION:medium-->"
    end_marker = "<!--END_SECTION:medium-->"
    start_idx = None
    end_idx = None

    for idx, line in enumerate(readme_content):
        if start_marker in line:
            start_idx = idx
        if end_marker in line:
            end_idx = idx

    # Prepare new content
    new_content = '<div style="overflow-x:auto;">\n'
    new_content += '<table style="width: 100%; border-collapse: collapse; color: white;">\n'
    new_content += '  <tr>\n'
    new_content += '    <th style="border: 1px solid white; padding: 10px;">Image</th>\n'
    new_content += '    <th style="border: 1px solid white; padding: 10px;">Title</th>\n'
    new_content += '    <th style="border: 1px solid white; padding: 10px;">Summary</th>\n'
    new_content += '    <th style="border: 1px solid white; padding: 10px;">Link</th>\n'
    new_content += '  </tr>\n'

    for title, link, image_url, summary in posts:
        new_content += '  <tr>\n'
        new_content += f'    <td style="border: 1px solid white; padding: 10px;"><img src="{image_url}" alt="Post Image" style="width: 100px; height: auto;"></td>\n' if image_url else '<td style="border: 1px solid white; padding: 10px;">No Image</td>\n'
        new_content += f'    <td style="border: 1px solid white; padding: 10px;">{escape(title)}</td>\n'
        new_content += f'    <td style="border: 1px solid white; padding: 10px;">{escape(summary)}</td>\n'
        new_content += f'    <td style="border: 1px solid white; padding: 10px;"><a href="{link}" style="color: white; text-decoration: none;">Read More</a></td>\n'
        new_content += '  </tr>\n'

    new_content += '</table>\n'    
    new_content += '</div>\n'

    # If markers are found, replace the content in between
    if start_idx is not None and end_idx is not None:
        updated_content = readme_content[:start_idx + 1] + [new_content] + readme_content[end_idx:]

    # Write the updated content back to README.md
    with open('README.md', 'w') as f:
        f.writelines(updated_content)

if __name__ == "__main__":
    posts = fetch_medium_posts(FEED_URL)
    update_readme(posts)

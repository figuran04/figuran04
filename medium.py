import feedparser

FEED_URL = "https://medium.com/feed/@dikaelsaputra"

def fetch_medium_posts(feed_url, num_posts=10):
    feed = feedparser.parse(feed_url)
    posts = []

    for entry in feed.entries[:num_posts]:
        title = entry.title
        link = entry.link
        # Debugging: Print the entry to inspect its structure
        print(f"Entry: {entry}")
        image_url = entry.media_thumbnail[0]['url'] if 'media_thumbnail' in entry else None
        summary = entry.summary[:200] + '...' if len(entry.summary) > 200 else entry.summary
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
    new_content = ""
    for title, link, image_url, summary in posts:
        print(f"Title: {title}, Image URL: {image_url}")  # Debugging print
        new_content += f'<div style="display: flex; align-items: center; margin-bottom: 20px;">\n'
        if image_url:
            new_content += f'  <img src="{image_url}" alt="Post Image" style="width: 100px; height: auto; margin-right: 10px;">\n'
        new_content += f'  <div>\n'
        new_content += f'    <a href="{link}" style="font-size: 1.2em; font-weight: bold;">{title}</a>\n'
        new_content += f'    <p>{summary}</p>\n'
        new_content += f'  </div>\n'
        new_content += f'</div>\n\n'

    # If markers are found, replace the content in between
    if start_idx is not None and end_idx is not None:
        updated_content = readme_content[:start_idx + 1] + [new_content] + readme_content[end_idx:]
    else:
        # If markers are not found, append the new content at the end
        updated_content = readme_content + [f"\n{start_marker}\n"] + [new_content] + [f"\n{end_marker}\n"]

    # Write the updated content back to README.md
    with open('README.md', 'w') as f:
        f.writelines(updated_content)

if __name__ == "__main__":
    posts = fetch_medium_posts(FEED_URL)
    update_readme(posts)

import requests
import matplotlib.pyplot as plt
from collections import Counter
from datetime import datetime, timedelta

# Warna tema
primary_color = '#6e44ff'
secondary_color = '#00ff7f'
star_color = '#6e44ff'

def configure_plot(title, x_label, y_label, ax):
    ax.set_title(title, color='white')
    ax.set_xlabel(x_label, color='white')
    ax.set_ylabel(y_label, color='white')
    ax.tick_params(axis='x', colors='white', rotation=45)
    ax.tick_params(axis='y', colors='white')
    ax.grid(True, color='gray', linestyle='--', linewidth=0.5)
    ax.set_facecolor('none')  # Menghapus latar belakang hitam

def fetch_github_data(endpoint, params={}):
    url = f"https://api.github.com/{endpoint}"
    response = requests.get(url, params=params)
    return response.json()

def fetch_commit_count(username, repo_name):
    commits_data = fetch_github_data(f'repos/{username}/{repo_name}/commits')
    return len(commits_data)

def fetch_repos_languages(username):
    repos_data = fetch_github_data(f'users/{username}/repos')
    languages = []
    for repo in repos_data:
        lang_data = fetch_github_data(f'repos/{username}/{repo["name"]}/languages')
        languages.extend(lang_data.keys())
    return Counter(languages)

def fetch_commit_data(username):
    repos_data = fetch_github_data(f'users/{username}/repos')
    commits_per_month = [0] * 13
    current_date = datetime.now()
    for repo in repos_data:
        repo_name = repo['name']
        commits_data = fetch_github_data(f'repos/{username}/{repo_name}/commits')
        for commit in commits_data:
            commit_date = datetime.strptime(commit['commit']['committer']['date'], "%Y-%m-%dT%H:%M:%SZ")
            if commit_date > current_date - timedelta(days=365):
                month_diff = (current_date.year - commit_date.year) * 12 + current_date.month - commit_date.month
                if month_diff < 13:
                    commits_per_month[12 - month_diff] += 1
    return commits_per_month

username = "figuran04"

# Mengambil data untuk chart
repos_data = fetch_github_data(f'users/{username}/repos')
repo_names = [repo['name'] for repo in repos_data]
commit_counts = [fetch_commit_count(username, repo['name']) for repo in repos_data]
fork_counts = [repo['forks_count'] for repo in repos_data]
star_counts = [repo['stargazers_count'] for repo in repos_data]
languages_counter = fetch_repos_languages(username)
languages, counts = zip(*languages_counter.items())
commits_per_month = fetch_commit_data(username)
months = [datetime.now() - timedelta(days=30 * i) for i in range(13)]
month_labels = [month.strftime('%b %Y') for month in months][::-1]  # Urutan bulan dibalik

# Membuat satu figure dengan empat subplot (2x2 grid)
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 12))

# Subplot pertama untuk Commits per Repository
ax1.bar(repo_names, commit_counts, color=primary_color, width=0.4)
configure_plot("Commits per Repository", "Repository", "Commit Count", ax1)

# Subplot kedua untuk Forks dan Stars per Repository
width = 0.4
x = range(len(repo_names))
ax2.bar(x, fork_counts, width=width, color=secondary_color, label='Forks', align='center')
ax2.bar([p + width for p in x], star_counts, width=width, color=star_color, label='Stars', align='center')
configure_plot("Forks & Stars per Repository", "Repository", "Count", ax2)
ax2.set_xticks([p + width / 2 for p in x])
ax2.set_xticklabels(repo_names)
ax2.legend()

# Subplot ketiga untuk Top Languages
explode = [0.1] + [0] * (len(languages) - 1)  # Hanya slice pertama yang meledak
ax3.pie(counts, labels=languages, autopct='%1.1f%%', startangle=140, explode=explode, textprops={'color':'white'})
ax3.set_title("Top Languages", color='white')
ax3.patch.set_facecolor('black')  # Latar belakang tetap hitam untuk pie chart

# Subplot keempat untuk Commits per Month
ax4.plot(month_labels, commits_per_month, marker='o', color=primary_color)
configure_plot("Commits per Month", "Month", "Number of Commits", ax4)

# Menyimpan figure sebagai file PNG dengan latar belakang transparan
plt.tight_layout()
fig.patch.set_alpha(0)  # Transparan
plt.savefig('github_stats.png', format='png', transparent=True)

# plt.show()

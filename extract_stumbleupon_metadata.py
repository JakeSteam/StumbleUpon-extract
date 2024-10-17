import os
from bs4 import BeautifulSoup

# Define the root directory containing the HTML files
root_dir = r'samples'  # Replace with your root directory

# Function to extract metadata from a single HTML file
def extract_metadata(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'lxml')
        list_items = soup.find_all(class_='listLi')
        for item in list_items:
            h4 = item.find('h4')
            avatar = item.find(class_='avatar')
            reviews = item.find(class_='showReview')
            views = item.find(class_='views')
            
            if h4 and avatar:
                metadata = {
                    'avatar_id': avatar.get('id', 'N/A'),
                    'avatar_title': avatar.get('title', 'N/A'),
                    'h4_url': h4.find('a')['href'] if h4.find('a') else 'N/A',
                    'h4_title': h4.get_text(strip=True),
                    'num_reviews': reviews.find('a').get_text(strip=True).split()[0] if reviews and reviews.find('a') else 'N/A',
                    'num_views': views.find('a')['title'].split()[0] if views and views.find('a') else 'N/A'
                }
                print(metadata)

# Traverse directories and process HTML files
for subdir, _, files in os.walk(root_dir):
    for file in files:
        file_path = os.path.join(subdir, file)
        # Check if the file has no extension or has an .html extension
        if not os.path.splitext(file)[1] or file.endswith('.html'):
            extract_metadata(file_path)
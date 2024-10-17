import os
from bs4 import BeautifulSoup

# Define the root directory containing the HTML files
root_dir = 'path/to/your/root/directory'  # Replace with your root directory

# Function to extract metadata from a single HTML file
def extract_metadata(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'lxml')
        list_items = soup.find_all(class_='listLi')
        for item in list_items:
            h4 = item.find('h4')
            if h4:
                metadata = {
                    'id': h4.get('id', 'N/A'),
                    'url': h4.find('a')['href'] if h4.find('a') else 'N/A',
                    'title': h4.get_text(strip=True)
                }
                print(metadata)

# Traverse directories and process HTML files
for subdir, _, files in os.walk(root_dir):
    for file in files:
        file_path = os.path.join(subdir, file)
        # Check if the file has no extension or has an .html extension
        if not os.path.splitext(file)[1] or file.endswith('.html'):
            extract_metadata(file_path)
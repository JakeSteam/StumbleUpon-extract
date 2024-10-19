import os
import csv
from bs4 import BeautifulSoup
from datetime import datetime
from urllib.parse import unquote

root_dir = r'data-raw'
max_files = 9999
stumbleupon_prefix = 'http://www.stumbleupon.com/url/'
output_csv = 'data-parsed/toprated.csv'

def extract_metadata(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'lxml')
        list_items = soup.find_all(class_='listLi')
        metadata_list = []
        for item in list_items:
            user = item.find(class_='avatar')
            reviews = item.find(class_='showReview') or item.find(class_='showStumble')
            raw_url = f'https://{reviews.find("a")["href"][len(stumbleupon_prefix):]}'
            views = item.find(class_='views')
            
            # Assumes relative path `data-raw\20091011113141\www.stumbleupon.com\discover\toprated\index.html`
            path_parts = file_path.split(os.sep)
            
            metadata = {
                'id': item.find('var')['class'][0],
                'url': unquote(unquote(raw_url)),
                'title': item.find("span", class_='img').find("img")["alt"].strip(),
                'review_count': int(''.join(filter(str.isdigit, reviews.find('a').get_text(strip=True).split()[0]))),
                'view_count': int(''.join(filter(str.isdigit, views.find('a')['title'].split()[0]))),
                'date': int(path_parts[-5]),
                'user_id': int(user['id']) if user else -1, 
                'user_name': user['title'] if user else 'Unavailable', 
                'source': path_parts[-2]
            }
            metadata_list.append(metadata)
        return metadata_list

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_csv), exist_ok=True)

# Write metadata to CSV
with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['id', 'url', 'title', 'review_count', 'view_count', 'date', 'user_id', 'user_name', 'source']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_NONNUMERIC)
    
    writer.writeheader()
    
    # Traverse directories and process HTML files
    file_count = 0
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file_count >= max_files:
                break
            file_path = os.path.join(subdir, file)
            # Check if the file has no extension or has an .html extension
            if not os.path.splitext(file)[1] or file.endswith('.html'):
                metadata_list = extract_metadata(file_path)
                for data in metadata_list:
                    writer.writerow(data)
                file_count += 1
                current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"{current_time}: Processed {len(metadata_list)} items from #{file_count}: {file_path}")
        if file_count >= max_files:
            break
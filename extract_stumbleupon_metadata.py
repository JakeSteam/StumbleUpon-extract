import os
import csv
from bs4 import BeautifulSoup

root_dir = r'data-raw'
max_files = 2
stumbleupon_prefix = 'http://www.stumbleupon.com/url/'
output_csv = 'output/urls.csv'

def extract_metadata(file_path):
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
        soup = BeautifulSoup(content, 'lxml')
        list_items = soup.find_all(class_='listLi')
        metadata_list = []
        for item in list_items:
            h4 = item.find('h4')
            avatar = item.find(class_='avatar')
            reviews = item.find(class_='showReview')
            views = item.find(class_='views')
            
            # Assumes relative path `data-raw\20091011113141\www.stumbleupon.com\discover\toprated`
            path_parts = file_path.split(os.sep)
            date = path_parts[-4] 
            source = path_parts[-1] 
            
            # Extract h4_title from img span's img element's alt text
            img_span = item.find('span', class_='img')
            h4_title = img_span.find('img')['alt'] if img_span and img_span.find('img') else 'N/A'
            
            metadata = {
                'avatar_id': avatar.get('id', 'N/A'),
                'avatar_title': avatar.get('title', 'N/A'),
                'h4_url': reviews.find('a')['href'][len(stumbleupon_prefix):] if reviews and reviews.find('a') else 'N/A',
                'h4_title': h4_title,
                'num_reviews': reviews.find('a').get_text(strip=True).split()[0] if reviews and reviews.find('a') else 'N/A',
                'num_views': views.find('a')['title'].split()[0] if views and views.find('a') else 'N/A',
                'date': date,
                'source': source
            }
            metadata_list.append(metadata)
        print(f"Processed {len(list_items)} items from {file_path}")
        return metadata_list

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_csv), exist_ok=True)

# Write metadata to CSV
with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['avatar_id', 'avatar_title', 'h4_url', 'h4_title', 'num_reviews', 'num_views', 'date', 'source']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    
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
        if file_count >= max_files:
            break
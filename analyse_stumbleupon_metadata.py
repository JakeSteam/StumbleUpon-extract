import pandas as pd
from urllib.parse import urlparse

df = pd.read_csv('data-parsed/parsed-cleaned.csv')
df_unique = df.drop_duplicates(subset='url')
df_unique['domain'] = df_unique['url'].apply(lambda url: urlparse(url).netloc.replace('www.', ''))

domain_stats = df_unique.groupby('domain')['view_count'].agg(['count', 'median']).reset_index()

domain_stats_filtered = domain_stats[domain_stats['count'] > 5]

highest_avg_view_count = domain_stats_filtered.sort_values(by='median', ascending=False).head(10)
print(highest_avg_view_count.to_markdown(index=False, floatfmt=".0f"))

most_frequent_domains = domain_stats.sort_values(by='count', ascending=False).head(10)
print(most_frequent_domains.to_markdown(index=False, floatfmt=".0f"))
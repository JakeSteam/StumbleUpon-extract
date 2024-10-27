# StumbleUpon extract tools & data

Fully processed StumbleUpon data extracted from the Wayback Machine, for [an article](https://blog.jakelee.co.uk/bulk-downloading-website-history-and-parsing/).

## What's in this repo?

- `/data-parsed/`
  - `parsed-cleaned.csv`: Final deduplicated extracted data.
  - `parsed.csv`: Data before deduplication.
- `/data-raw/`: Output of `waybackpack`, organised by timestamp and URL.
- `/samples/`: Examples of the downloaded HTML, an individual StumbleUpon link, and the resulting CSV data.
- `clean_stumbleupon_metadata.py`: Tool to deduplicate a CSV by `id` field (convert `parsed.csv` into `parsed-cleaned.csv`).
- `extract_stumbleupon_metadata.py`: Tool to extract contents of downloaded StumbleUpon pages (convert `data-raw` contents into `parsed.csv`).
- `analyse_stumbleupon_metadata.py`: Misc code to analyse the parsed data. This changes as required, full scripts available in original article.

## How to recreate results?

To recreate the final output ([`parsed-cleaned.csv`](/data-parsed/parsed-cleaned.csv)):

1. Install Python dependencies (`pip install beautifulsoup4 lxml pandas`)
2. Run Wayback Machine download script (`waybackpack http://www.stumbleupon.com/discover/toprated/ -d "/Projects/StumbleUpon-extract/data-raw"`)
3. Run parsing script (`python extract_stumbleupon_metadata.py`)
4. Run deduping script (`python clean_stumbleupon_metadata.py`)

# StumbleUpon-extract

Processed wayback machine data for StumbleUpon (`parsed-cleaned.csv`), extracted using [waybackpack](https://github.com/jsvine/waybackpack) for an upcoming post on [Internet History](https://history.jakelee.co.uk).

To recreate data:

1. Install (`pip install beautifulsoup4 lxml pandas`)
2. Run Wayback Machine download script (waybackpack)
3. Run parsing script (`python extract_stumbleupon_metadata.py`)
4. Run deduping script (`python clean_stumbleupon_metadata.py`)

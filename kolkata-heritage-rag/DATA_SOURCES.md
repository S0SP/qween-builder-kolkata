# Data Sources for Kolkata Heritage RAG

## Primary Sources (Recommended)

### 1. Wikipedia Articles (High Quality, Structured)
Scrape these pages for comprehensive heritage info:

| Topic | URL |
|-------|-----|
| Kolkata | https://en.wikipedia.org/wiki/Kolkata |
| Victoria Memorial | https://en.wikipedia.org/wiki/Victoria_Memorial,_Kolkata |
| Howrah Bridge | https://en.wikipedia.org/wiki/Howrah_Bridge |
| Durga Puja | https://en.wikipedia.org/wiki/Durga_Puja |
| Indian Museum | https://en.wikipedia.org/wiki/Indian_Museum |
| Marble Palace | https://en.wikipedia.org/wiki/Marble_Palace_(Kolkata) |
| Kalighat Temple | https://en.wikipedia.org/wiki/Kalighat_Temple |
| St. Paul's Cathedral | https://en.wikipedia.org/wiki/St._Paul%27s_Cathedral,_Kolkata |
| Prince of Wales Museum | https://en.wikipedia.org/wiki/Academy_of_Fine_Arts,_Kolkata |
| New Market | https://en.wikipedia.org/wiki/New_Market,_Kolkata |
| College Street | https://en.wikipedia.org/wiki/College_Street_(Kolkata) |
| Kumartuli | https://en.wikipedia.org/wiki/Kumartuli |
| Rabindra Sadan | https://en.wikipedia.org/wiki/Rabindra_Sadan |
| Nandan | https://en.wikipedia.org/wiki/Nandan_(Kolkata) |
| Park Street | https://en.wikipedia.org/wiki/Park_Street,_Kolkata |

### 2. Official Tourism Sites

| Source | URL |
|--------|-----|
| West Bengal Tourism | https://wbtourism.gov.in/ |
| Incredible India - Kolkata | https://www.incredibleindia.org/content/incredible-india-v2/en/destinations/kolkata.html |
| Kolkata Port Trust | https://www.kolkataporttrust.gov.in/ |

### 3. Cultural Heritage Sites

| Source | URL |
|--------|-----|
| Asiatic Society | https://www.asiaticsocietykolkata.org/ |
| Rabindra Bharati Museum | https://rbmuseum.org.in/ |
| Academy of Fine Arts | https://academyoffineartskolkata.com/ |
| Birla Planetarium | https://www.birlaplanetarium.org/ |

### 4. Historical Documents (Public Domain)

| Source | Description |
|--------|-------------|
| British Library - India Office Records | https://www.bl.uk/collection-guides/india-office-records |
| Internet Archive - Kolkata | https://archive.org/search.php?query=kolkata%20OR%20calcutta |
| Project Gutenberg - Bengal | https://www.gutenberg.org/ebooks/search/?query=bengal |

### 5. News & Articles

| Source | URL |
|--------|-----|
| The Hindu - Kolkata | https://www.thehindu.com/news/cities/kolkata/ |
| Times of India - Kolkata | https://timesofindia.indiatimes.com/city/kolkata |
| The Telegraph - Kolkata | https://www.telegraphindia.com/west-bengal/kolkata |

## Data Collection Script

Use the included scraper:

```bash
python scripts/collect_data.py --sources wikipedia --output data/raw/
```

## Manual Data (Optional)

Create `data/raw/manual/` folder with:
- `landmarks.txt` - Personal notes about favorite spots
- `festivals.txt` - Durga Puja, Kali Puja, Poila Boishakh details
- `food.txt` - Kathi rolls, rasgulla, mishti doi, phuchka
- `literature.txt` - Tagore, Satyajit Ray, Bengali literature

## Recommended Dataset Size

- **MVP**: 10-15 Wikipedia articles (~50 pages)
- **Full**: 30-40 articles + tourism content (~200 pages)
- **Extended**: Add news, historical docs (~500+ pages)

## Data Format

The scraper will output JSON files with:
```json
{
  "source": "wikipedia",
  "title": "Victoria Memorial",
  "url": "https://en.wikipedia.org/wiki/Victoria_Memorial,_Kolkata",
  "content": "...",
  "metadata": {
    "scraped_at": "2024-01-01",
    "language": "en"
  }
}
```

## Bengali Language Sources (Optional)

| Source | URL |
|--------|-----|
| Bengali Wikipedia | https://bn.wikipedia.org/ |
| Anandabazar Patrika | https://www.anandabazar.com/ |
| Ebela | https://www.ebela.in/ |

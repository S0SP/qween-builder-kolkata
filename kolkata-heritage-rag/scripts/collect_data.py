#!/usr/bin/env python3
"""
Data collector for Kolkata Heritage RAG
Scrapes content from Wikipedia and other sources
"""

import argparse
import json
import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
from typing import List, Dict


WIKIPEDIA_URLS = [
    "https://en.wikipedia.org/wiki/Kolkata",
    "https://en.wikipedia.org/wiki/Victoria_Memorial,_Kolkata",
    "https://en.wikipedia.org/wiki/Howrah_Bridge",
    "https://en.wikipedia.org/wiki/Durga_Puja",
    "https://en.wikipedia.org/wiki/Indian_Museum",
    "https://en.wikipedia.org/wiki/Marble_Palace_(Kolkata)",
    "https://en.wikipedia.org/wiki/Kalighat_Temple",
    "https://en.wikipedia.org/wiki/St._Paul%27s_Cathedral,_Kolkata",
    "https://en.wikipedia.org/wiki/College_Street_(Kolkata)",
    "https://en.wikipedia.org/wiki/Kumartuli",
    "https://en.wikipedia.org/wiki/Park_Street,_Kolkata",
    "https://en.wikipedia.org/wiki/New_Market,_Kolkata",
    "https://en.wikipedia.org/wiki/Prinsep_Street",
    "https://en.wikipedia.org/wiki/Maidan_(Kolkata)",
    "https://en.wikipedia.org/wiki/Eco_Park,_Kolkata",
    "https://en.wikipedia.org/wiki/Belur_Math",
    "https://en.wikipedia.org/wiki/Dakshineswar_Kali_Temple",
    "https://en.wikipedia.org/wiki/Kalighat",
    "https://en.wikipedia.org/wiki/Rabindra_Sadan",
    "https://en.wikipedia.org/wiki/Nandan_(Kolkata)",
]


def scrape_wikipedia(url: str) -> Dict:
    """Scrape content from a Wikipedia page."""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract title
        title_tag = soup.find("h1", {"id": "firstHeading"})
        title = title_tag.text if title_tag else url.split("/")[-1]
        
        # Extract main content (bodyContent)
        content_div = soup.find("div", {"id": "mw-content-text"})
        if not content_div:
            return None
        
        # Get all paragraphs
        paragraphs = content_div.find_all("p")
        content = "\n\n".join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])
        
        # Get sections
        sections = []
        headings = content_div.find_all(["h2", "h3", "h4"])
        for heading in headings[:10]:  # Limit to first 10 sections
            section_title = heading.get_text().strip()
            # Get content until next heading
            content_parts = []
            current = heading.find_next_sibling()
            while current and current.name not in ["h2", "h3", "h4"]:
                if hasattr(current, "get_text"):
                    text = current.get_text().strip()
                    if text:
                        content_parts.append(text)
                current = current.find_next_sibling()
            
            if content_parts:
                sections.append({
                    "title": section_title,
                    "content": "\n\n".join(content_parts)
                })
        
        return {
            "source": "wikipedia",
            "title": title,
            "url": url,
            "content": content,
            "sections": sections,
            "metadata": {
                "scraped_at": datetime.now().isoformat(),
                "language": "en",
                "word_count": len(content.split())
            }
        }
    
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None


def collect_all(output_dir: str):
    """Collect data from all sources."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    results = []
    
    print(f"Scraping {len(WIKIPEDIA_URLS)} Wikipedia pages...")
    
    for i, url in enumerate(WIKIPEDIA_URLS, 1):
        print(f"[{i}/{len(WIKIPEDIA_URLS)}] {url}")
        data = scrape_wikipedia(url)
        if data:
            results.append(data)
            # Save individual file
            safe_title = data["title"].replace(" ", "_").replace("/", "_")
            with open(output_path / f"{safe_title}.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
    
    # Save combined dataset
    combined_path = output_path.parent / "combined_data.json"
    with open(combined_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Collected {len(results)} articles")
    print(f"📁 Saved to: {output_path}")
    print(f"📄 Combined file: {combined_path}")
    
    # Stats
    total_words = sum(r["metadata"]["word_count"] for r in results)
    print(f"📊 Total words: {total_words:,}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Collect Kolkata heritage data")
    parser.add_argument("--output", "-o", default="data/raw", help="Output directory")
    args = parser.parse_args()
    
    collect_all(args.output)

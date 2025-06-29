# 🛒 Store Data Enrichment Pipeline with Python

This project implements a robust data enrichment pipeline for collecting and enhancing store location data across Canada. 
It uses OpenStreetMap (OSM) and HERE APIs to extract raw location data and enriches it with additional metadata, 
such as website URLs and brand logos. The result is a structured dataset saved as an Excel file for further analysis or integration.

---

## 🚀 Tech Stack

- Python
- OpenStreetMap Nominatim API (Location data)
- HERE Places API (Business details)
- Anthropic API / Manual mapping (Website/logo enrichment)
- Scrapy (Logo scraping from websites)
- pandas (Data processing)
- openpyxl (Excel output)

---

## 🔐 Environment Variables

Create a `.env` file in the root of the project and add the following:

```env
HERE_API_KEY=your_here_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

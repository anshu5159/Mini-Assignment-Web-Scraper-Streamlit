import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time

visited = set()
report = []

def scrape_page(url, base_url, depth=0, max_depth=1):
    if url in visited or depth > max_depth:
        return
    visited.add(url)

    try:
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        report.append(f"URL: {url}\n\n{text}\n{'='*80}\n")
        
        # Find all anchor tags
        for link in soup.find_all('a', href=True):
            href = link['href']
            full_url = urljoin(base_url, href)
            if base_url in full_url:
                scrape_page(full_url, base_url, depth+1, max_depth)
    except Exception as e:
        report.append(f"Failed to scrape {url}: {e}\n{'='*80}\n")

def main():
    st.title("🌐 Mini Web Scraper with Report")
    url = st.text_input("Enter the website URL:", "https://example.com")
    max_depth = st.slider("Crawl Depth", 1, 3, 1)

    if st.button("Scrape Website"):
        if not urlparse(url).scheme:
            url = "http://" + url
        with st.spinner("Scraping in progress..."):
            visited.clear()
            report.clear()
            scrape_page(url, url, 0, max_depth)
            with open("scrape_report.txt", "w", encoding='utf-8') as f:
                f.writelines(report)
        st.success("Scraping complete! Download your report below.")
        with open("scrape_report.txt", "rb") as file:
            st.download_button("Download Report", file, "scrape_report.txt")

if __name__ == "__main__":
    main()

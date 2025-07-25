import streamlit as st
# to build a interactive web app interface
import requests
# to make HTTP requests to the websites
from bs4 import BeautifulSoup
# to parse HTML and extracting data from the website
from urllib.parse import urljoin, urlparse
# to handle URLs and join relative links

visited = set()
# visited is a null set that keeps track of already visited URLs to avoid infinite loops and repeated crawling.
report = []
# report is a null list to store text content from each page visited. Will be saved to a .txt file

def scrape_page(url, base_url, depth=0, max_depth=1):
    # scrape_page is a recursive function to scrape a webpage and explore its links up to a certain depth
    if url in visited or depth > max_depth:
        # Stops recursion function if the page is already visited or if the maximum crawl depth is reached
        return
    visited.add(url)
    # Adds the current URL to the visited set to avoid re-visiting

    try:
        response = requests.get(url, timeout=5)
        # sends HTTP requests with a 5-second timeout
        soup = BeautifulSoup(response.text, 'html.parser')
        # for parsing the HTML response
        text = soup.get_text(separator=' ', strip=True)
        # get_text() to extract all text
        # separator used to separate lines/blocks with spaces
        # strip=True is used to trim extra whitespace.
        report.append(f"URL: {url}\n\n{text}\n{'='*80}\n")
        # save the content in the report
        
        for link in soup.find_all('a', href=True):
            # for finding all <a> tags with href attribute
            href = link['href']
            full_url = urljoin(base_url, href)
            # urljoin() handles relative links
            if base_url in full_url:
                # to check if the link belongs to the same base domain
                scrape_page(full_url, base_url, depth+1, max_depth)
                # function call scrape_page() for each valid subpage
    except Exception as e:
        report.append(f"Failed to scrape {url}: {e}\n{'='*80}\n")
    # if it encounters any error, the error is logged in the report instead of crashing

def main():
    st.title("Mini Web Scraper and Report Download")
    # to give the app a title
    st.write("This app scrapes a website and generates a report of the text content found on each page.")
    url = st.text_input("Enter the website URL:", value = "https://abc.com")
    # to get user URL input with default value set to "https://abc.com"
    max_depth = st.slider("Choose the depth for scraping", 1, 10, 1)
    # for choosing the max depth of the website to scrape with default value of 1

    if st.button("Submit to Scrape Website"):
        if not urlparse(url).scheme:
            url = "http://" + url
        # in case the user enters a URL without http:// or https://
        with st.spinner("Scraping in progress..."):
            visited.clear()
            report.clear()
            scrape_page(url, url, 0, max_depth)
        # scraping from the URL at depth 0 up to max depth
            with open("scrape_report.txt", "w", encoding='utf-8') as f:
                f.writelines(report)
            # opening a file to write the report
        st.success("Scraping complete! Download your report below.")
        # prints success message
        with open("scrape_report.txt", "rb") as file:
            st.download_button("Download Report", file, "scrape_report.txt")
        # creates a download button to download the report generated

if __name__ == "__main__":
    main()
# to run the code

# save this as linkify.py inside LinkProject
import requests, io, pdfplumber, re
from bs4 import BeautifulSoup

LINK_EVERY = 500  # words

def get_sitemap_links(sitemap_url):
    xml = requests.get(sitemap_url).text
    soup = BeautifulSoup(xml, "xml")
    return {url.text: url.text.split("/")[-2].replace("-", " ")  # rough title
            for url in soup.find_all("loc")}

def pdf_to_text(pdf_path):
    text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text.append(page.extract_text() or "")
    return "\n".join(text)

def insert_links(text, links):
    words = text.split()
    html_chunks = []
    used = set()
    for i in range(0, len(words), LINK_EVERY):
        chunk = words[i:i+LINK_EVERY]
        chunk_text = " ".join(chunk)
        # find first keyword that matches a title
        for url, title in links.items():
            if title in chunk_text.lower() and url not in used:
                anchor = f'<a href="{url}">{title.title()}</a>'
                chunk_text = re.sub(title, anchor, chunk_text, flags=re.I, count=1)
                used.add(url)
                break
        html_chunks.append(chunk_text)
    return "<p>" + "</p><p>".join(html_chunks) + "</p>"

def main():
    pdf_path = "blog.pdf"
    site_url = open("sitemap.txt").read().strip()
    links = get_sitemap_links(site_url)
    raw_text = pdf_to_text(pdf_path)
    html = insert_links(raw_text, links)
    open("linked_blog.html", "w", encoding="utf8").write(html)
    print("✅  Done!  See linked_blog.html in this folder.")

if __name__ == "__main__":
    main()

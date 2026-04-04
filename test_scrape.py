import requests
from bs4 import BeautifulSoup

response = requests.get("https://askajay.ai/thinking", headers={"User-Agent": "Mozilla/5.0"})
soup = BeautifulSoup(response.text, "html.parser")
print("Title:", soup.title.get_text() if soup.title else "No title")

links = soup.find_all('a')
for link in links[:20]:
    print("Link text:", link.get_text(strip=True), "| URL:", link.get('href'))

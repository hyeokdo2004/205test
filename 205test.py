import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urldefrag

URL = "http://115.144.217.205/phpbbs/list.php"
OUT_HTML = "links.html"

def is_valid_href(href: str) -> bool:
    if not href:
        return False
    h = href.strip()
    if not h:
        return False
    if h.lower().startswith(("javascript:", "mailto:", "tel:")):
        return False
    if h == "#":
        return False
    return True

def main():
    res = requests.get(
        URL,
        headers={"User-Agent": "Mozilla/5.0"},
        timeout=10
    )
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "html.parser")

    links = []
    seen = set()

    for a in soup.find_all("a", href=True):
        href = a.get("href")
        if not is_valid_href(href):
            continue

        abs_url = urljoin(URL, href)
        abs_url, _ = urldefrag(abs_url)

        if abs_url not in seen:
            seen.add(abs_url)
            links.append(abs_url)

    html = []
    html.append("<!DOCTYPE html>")
    html.append("<html lang='ko'>")
    html.append("<head>")
    html.append("<meta charset='UTF-8'>")
    html.append("<title>Extracted Links</title>")
    html.append("</head>")
    html.append("<body>")
    html.append(f"<h2>추출된 링크 ({len(links)}개)</h2>")
    html.append("<ul>")

    for link in links:
        html.append(f"<li><a href='{link}' target='_blank'>{link}</a></li>")

    html.append("</ul>")
    html.append("</body>")
    html.append("</html>")

    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write("\n".join(html))

    print(f"HTML 생성 완료: {OUT_HTML}")
    print(f"총 링크 수: {len(links)}")

if __name__ == "__main__":
    main()

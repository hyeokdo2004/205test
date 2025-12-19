import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urldefrag
from datetime import datetime

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
    html.append("<h1>205test 자동 수집</h1>")
    html.append(f"<p>생성 시간: {datetime.now()}</p>")
    html.append(f"<h2>추출된 링크 ({len(links)}개)</h2>")
    html.append("<ul>")

    for link in links:
        html.append(f"<li><a href='{link}' target='_blank'>{link}</a></li>")

    html.append("</ul>")
    html.append("</body>")
    html.append("</html>")

    with open(OUT_HTML, "w", encoding="utf-8") as f:
        f.write("\n".join(html))

    # index.html도 같이 생성 (Pages 루트 확인용)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(
            "<h1>GitHub Actions 정상 동작</h1>"
            f"<p>업데이트: {datetime.now()}</p>"
            "<p><a href='links.html'>links.html 보기</a></p>"
        )

    print(f"HTML 생성 완료: {OUT_HTML}")
    print(f"총 링크 수: {len(links)}")

if __name__ == "__main__":
    main()

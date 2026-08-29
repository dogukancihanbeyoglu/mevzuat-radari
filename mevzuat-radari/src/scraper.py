"""
Resmî Gazete Scraper and Content Parser Module.
Fetches daily index, date range indices, regulation details and formats clean text for AI analysis.
"""
import re
import ssl
import urllib.request
from datetime import datetime, timedelta
from typing import Optional, List, Tuple
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from .models import GazetteIndex, GazetteItem


BASE_URL = "https://www.resmigazete.gov.tr"


def _create_ssl_context() -> ssl.SSLContext:
    """Create an SSL context that handles various certificate environments."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx


def _fetch_html(url: str, encoding: Optional[str] = None) -> Tuple[str, str]:
    """Fetch HTML content with robust error handling and encoding detection."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
    }
    req = urllib.request.Request(url, headers=headers)
    ctx = _create_ssl_context()

    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
        raw = resp.read()
        content_type = resp.headers.get("content-type", "").lower()
        
        used_encoding = "utf-8"
        if encoding:
            used_encoding = encoding
        elif "charset=windows-1254" in content_type or "windows-1254" in content_type:
            used_encoding = "windows-1254"
        elif "charset=iso-8859-9" in content_type:
            used_encoding = "iso-8859-9"
        else:
            if b"windows-1254" in raw.lower() or b"iso-8859-9" in raw.lower():
                used_encoding = "windows-1254"

        try:
            html = raw.decode(used_encoding)
        except UnicodeDecodeError:
            html = raw.decode("windows-1254", errors="ignore")

        return html, used_encoding


def get_gazette_url_for_date(date_str: Optional[str] = None) -> Tuple[str, str]:
    """
    Returns (target_url, formatted_date_str) for a given date.
    Input date format: YYYY-MM-DD or DD.MM.YYYY or None (today).
    """
    if not date_str or date_str.lower() in ("today", "bugun", "bugün"):
        target_date = datetime.now()
        formatted_date = target_date.strftime("%Y-%m-%d")
        return BASE_URL, formatted_date

    parsed_date = None
    for fmt in ("%Y-%m-%d", "%d.%m.%Y", "%Y/%m/%d"):
        try:
            parsed_date = datetime.strptime(date_str, fmt)
            break
        except ValueError:
            continue

    if not parsed_date:
        raise ValueError(f"Geçersiz tarih formatı: '{date_str}'. Beklenen format: YYYY-MM-DD veya DD.MM.YYYY")

    formatted_date = parsed_date.strftime("%Y-%m-%d")
    year = parsed_date.strftime("%Y")
    month = parsed_date.strftime("%m")
    day_str = parsed_date.strftime("%Y%m%d")

    if parsed_date.date() == datetime.now().date():
        return BASE_URL, formatted_date

    archive_url = f"{BASE_URL}/eskiler/{year}/{month}/{day_str}.htm"
    return archive_url, formatted_date


def parse_gazette_index(html: str, target_date: str) -> GazetteIndex:
    """Parse Resmî Gazete fihrist HTML and extract structured items."""
    soup = BeautifulSoup(html, "html.parser")
    
    gazette_number = None
    text_content = soup.get_text()
    match = re.search(r"Sayı\s*:\s*(\d+)", text_content, re.IGNORECASE)
    if match:
        gazette_number = match.group(1)

    items: List[GazetteItem] = []
    current_section = "Yürütme ve İdare"
    current_category = "Genel"
    current_institution = None

    known_sections = ["YASAMA BÖLÜMÜ", "YÜRÜTME VE İDARE BÖLÜMÜ", "YARGI BÖLÜMÜ", "İLAN BÖLÜMÜ"]
    known_categories = [
        "CUMHURBAŞKANI KARARLARI",
        "CUMHURBAŞKANLIĞI KARARNAMELERİ",
        "ATAMA KARARLARI",
        "YÖNETMELİKLER",
        "TEBLİĞLER",
        "KURUL KARARLARI",
        "GENELGELER",
        "ANAYASA MAHKEMESİ KARARLARI",
        "YARGITAY KARARLARI",
        "DANIŞTAY KARARLARI",
    ]

    for element in soup.find_all(["div", "p", "h1", "h2", "h3", "h4", "a", "span"]):
        txt = element.get_text(strip=True)
        if not txt:
            continue

        upper_txt = txt.upper()

        for s in known_sections:
            if s in upper_txt and len(upper_txt) < 40:
                current_section = s
                break

        for c in known_categories:
            if c in upper_txt and len(upper_txt) < 50:
                current_category = c.capitalize()
                break

        if txt.endswith("Bakanlığından:") or txt.endswith("Kurumundan:") or txt.endswith("Kurulundan:"):
            current_institution = txt.replace(":", "").strip()

        if element.name == "a" and element.get("href"):
            href = element["href"].strip()
            
            if href.startswith("#") or "fihrist" in href or "tarih" in href or href == "/":
                continue

            full_url = urljoin(BASE_URL, href)
            is_pdf = full_url.lower().endswith(".pdf")
            is_htm = full_url.lower().endswith(".htm") or full_url.lower().endswith(".html")

            if (is_pdf or is_htm) and len(txt) > 5 and not txt.startswith("PDF Görüntüle") and not txt.startswith("Önceki Sayı"):
                clean_title = re.sub(r"^[–\-—\s]+", "", txt).strip()

                cat = current_category
                if "Yönetmeliği" in clean_title or "Yönetmelik" in clean_title:
                    cat = "Yönetmelik"
                elif "Tebliği" in clean_title or "Tebliğ" in clean_title:
                    cat = "Tebliğ"
                elif "Kararı" in clean_title or "Kararlar" in clean_title:
                    cat = "Karar"

                doc_num = None
                doc_match = re.search(r"\((Karar|Tebliğ|Sayı)\s*(?:Sayısı|No)?\s*:\s*([^)]+)\)", clean_title, re.IGNORECASE)
                if doc_match:
                    doc_num = doc_match.group(2).strip()

                item = GazetteItem(
                    title=clean_title,
                    url=full_url,
                    category=cat,
                    institution=current_institution,
                    section=current_section,
                    doc_number=doc_num,
                    is_pdf=is_pdf,
                )
                if not any(existing.url == item.url for existing in items):
                    items.append(item)

    return GazetteIndex(
        date=target_date,
        gazette_number=gazette_number,
        total_items=len(items),
        items=items,
    )


def fetch_gazette_index(date_str: Optional[str] = None) -> GazetteIndex:
    """Public function to fetch and parse Gazette Index for a given date."""
    url, target_date = get_gazette_url_for_date(date_str)
    try:
        html, _ = _fetch_html(url)
        return parse_gazette_index(html, target_date)
    except Exception:
        return GazetteIndex(date=target_date, total_items=0, items=[])


def fetch_gazette_date_range(start_date_str: str, end_date_str: str) -> List[GazetteIndex]:
    """
    Fetches Gazette Indices for all days in the range [start_date, end_date].
    """
    start_dt = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_dt = datetime.strptime(end_date_str, "%Y-%m-%d")

    if start_dt > end_dt:
        start_dt, end_dt = end_dt, start_dt

    indices: List[GazetteIndex] = []
    curr = start_dt
    while curr <= end_dt:
        d_str = curr.strftime("%Y-%m-%d")
        idx = fetch_gazette_index(d_str)
        if idx.total_items > 0:
            indices.append(idx)
        curr += timedelta(days=1)

    return indices


def fetch_regulation_content(url: str) -> str:
    """Fetch the clean text of a specific regulation document."""
    if url.lower().endswith(".pdf"):
        return f"[PDF Belgesi] Bu mevzuat PDF formatındadır. Doğrudan bağlantı: {url}"

    html, _ = _fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")

    for s in soup(["script", "style", "nav", "header", "footer"]):
        s.extract()

    text = soup.get_text(separator="\n")
    cleaned_lines = [line.strip() for line in text.split("\n") if line.strip()]
    return "\n".join(cleaned_lines)

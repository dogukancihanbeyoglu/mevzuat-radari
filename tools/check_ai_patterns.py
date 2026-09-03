#!/usr/bin/env python3
"""
Academic Integrity & AI Pattern Auditor
Audits a text/markdown file for:
1. Direct quotation percentage (Threshold: < 5%)
2. Repetitive AI tropes / buzzwords (GPTZero / Turnitin risk markers)
3. Sentence length variability / burstiness (Organic human writing vs uniform AI cadence)
"""

import sys
import re
import argparse
import statistics

AI_CLICHES = [
    r"\bdelve(?:s|d)? into\b",
    r"\btapestry\b",
    r"\bcrucial role\b",
    r"\btestament to\b",
    r"\bpivotal\b",
    r"\bbeacon\b",
    r"\bit is important to note\b",
    r"\bplays an essential role\b",
    r"\bunderscores the importance\b",
    r"\bnoteworthy that\b",
    r"\ba wide array of\b",
    r"\bin summary,\b",
    r"\bin conclusion,\b"
]

def analyze_text(text):
    total_words = len(re.findall(r'\b\w+\b', text))
    if total_words == 0:
        print("[!] Metin boş!")
        return
        
    # 1. Direct Quotation Analysis
    quotes = re.findall(r'["“](.*?)["”]', text)
    quote_word_count = sum(len(re.findall(r'\b\w+\b', q)) for q in quotes)
    quote_percentage = (quote_word_count / total_words) * 100

    # 2. Sentence Length & Burstiness
    raw_sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in raw_sentences if len(s.strip().split()) > 2]
    
    sentence_lengths = [len(s.split()) for s in sentences]
    if sentence_lengths:
        mean_len = statistics.mean(sentence_lengths)
        std_len = statistics.stdev(sentence_lengths) if len(sentence_lengths) > 1 else 0
        burstiness_score = std_len / mean_len if mean_len > 0 else 0
    else:
        mean_len = 0
        std_len = 0
        burstiness_score = 0

    # 3. AI Cliches Check
    found_cliches = []
    for pattern in AI_CLICHES:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            found_cliches.append((pattern.replace(r"\b", "").replace("?:s|d)?", ""), len(matches)))

    # Output Report
    print("=" * 65)
    print("AKADEMİK TEZ DÜRÜSTLÜK & YAPAY ZEKÂ RİSK DENETİM RAPORU")
    print("=" * 65)
    print(f"Toplam Kelime Sayısı    : {total_words}")
    print(f"Toplam Cümle Sayısı     : {len(sentences)}")
    print(f"Ortalama Cümle Uzunluğu : {mean_len:.1f} kelime")
    print(f"Cümle Varyansı (Burst.) : {burstiness_score:.2f} (Önerilen: > 0.45)")
    print("-" * 65)
    
    # Direct Quote Assessment
    quote_status = "UYGUN (PASS)" if quote_percentage <= 5.0 else "UYARI: %5 LİMİTİNİ AŞIYOR (FAIL)"
    print(f"1. Doğrudan Alıntı Oranı : %{quote_percentage:.1f} | Eşik: <= %5.0 | Durum: {quote_status}")
    if quote_percentage > 5.0:
        print("   -> Öneri: Tırnak içi blok alıntıları yazarın kendi cümleleriyle aktarın (paraphrasing).")
        
    # AI Burstiness Assessment
    ai_burst_status = "DOĞAL / İNSANSI (PASS)" if burstiness_score >= 0.40 else "RİSKLİ / MEKANİK (AI BENZERİ)"
    print(f"2. Cümle Ritmi Değişkenliği : {ai_burst_status}")
    if burstiness_score < 0.40:
        print("   -> Öneri: Cümleler birbirine çok benzer boyutta. Kısa ve uzun cümleleri harmanlayın.")

    # Cliches Assessment
    print(f"3. Tespit Edilen AI Klişeleri: {len(found_cliches)} farklı şablon")
    if found_cliches:
        for c, count in found_cliches:
            print(f"   - '{c}': {count} kez geçiyor (Kaldırılması önerilir)")
    else:
        print("   -> Harika! Bilinen yapay zekâ şablon kelimelerine rastlanmadı.")
        
    print("=" * 65)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audit thesis draft against AI cliches and quote thresholds")
    parser.add_argument("--file", help="Path to text or markdown file")
    parser.add_argument("--text", help="Direct text string to analyze")
    args = parser.parse_args()
    
    content = ""
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            content = f.read()
    elif args.text:
        content = args.text
    else:
        print("Lütfen --file veya --text parametresi girin.")
        sys.exit(1)
        
    analyze_text(content)

import requests
from typing import List, Dict, Optional
import os
from openai import OpenAI
from urllib.parse import urlparse
import re
import logging

openai_api_key = os.environ.get("OPENAI_API_KEY")
google_api_key = os.environ.get("GOOGLE_API_KEY")
cse_id = os.environ.get("GOOGLE_CSE_ID")


class GoogleSearch:
    def __init__(self, api_key: str, cse_id: str):
        self.api_key = api_key
        self.cse_id = cse_id
        self.openai_client = OpenAI(api_key=openai_api_key)
        self.drug_corrections = {
            "ariprazol": "aripiprazol",
            "ariprazole": "aripiprazole",
            # Diğer düzeltmeler eklenebilir
        }

    def create_search_queries(self, question: str, drug_name: str, num_queries: int = 3) -> List[str]:
        # İlaç adı düzeltmesi
        corrected_drug_name = self.drug_corrections.get(drug_name.lower(), drug_name)

        prompt = f"""
Aşağıdaki Türkçe soruya ve '{corrected_drug_name}' ilacına odaklanarak
kullanılabilecek {num_queries} farklı web arama sorgusu oluşturun.
Sorgular, arama motorlarında etkili sonuçlar verecek şekilde optimize edilmeli.
TIRNAK İŞARETİ KULLANMAYIN.
Kısa ve öz sorgular oluşturun.

Soru: {question}

Sorgular:
"""
        for i in range(1, num_queries + 1):
            prompt += f"\n{i}. "

        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.3,
        )

        queries = response.choices[0].message.content.strip().split("\n")
        return [q.strip().lstrip("0123456789. ") for q in queries if q.strip()]

    def search_web(self, query: str, num_results: int = 5) -> List[Dict]:
        url = "https://www.googleapis.com/customsearch/v1"

        # Tırnak işaretlerini kaldır
        clean_query = query.replace('"', '')

        params = {
            "q": clean_query,
            "cx": self.cse_id,
            "key": self.api_key,
            "num": num_results,
            "lr": "lang_tr",  # Türkçe sonuçları tercih et
            "gl": "tr",  # Türkiye bölgesi sonuçlarını tercih et
            "fields": "items(title,link,snippet)"
        }

        try:
            print(f"Arama sorgusu: {clean_query}")
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if "error" in data:
                print(f"API Hatası: {data['error']['message']}")
                return []

            if "items" not in data:
                print(f"Sonuç bulunamadı. Sorgu: '{clean_query}'")
                return []

            results = [
                {"title": item["title"], "url": item["link"], "snippet": item.get("snippet", "")}
                for item in data.get("items", [])
            ]
            return results

        except requests.exceptions.RequestException as e:
            print(f"Google API isteği hatası: {e}")
            return []
        except ValueError as e:
            print(f"JSON işleme hatası: {e}")
            return []

    def analyze_and_summarize(self, question: str, results: List[Dict], drug_name: str, max_tokens: int = 500) -> str:
        if not results:
            return "Üzgünüm, arama sonuçları bulunamadı."

        context = "\n".join(
            [f"Başlık: {result['title']}\nURL: {result['url']}\nÖzet: {result['snippet']}"
             for result in results[:5]]
        )

        prompt = f"""
Aşağıdaki arama sonuçlarına dayanarak, kullanıcının sorusuna kapsamlı bir cevap oluştur.
Lütfen sadece '{drug_name}' ilacı ile ilgili bilgileri kullan.
Yanıtta güvenilir kaynakları belirt.

Soru: {question}

Arama Sonuçları:
{context}

Cevap:
"""
        response = self.openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500,
            temperature=0.3,
        )

        answer = response.choices[0].message.content.strip()
        return answer

    def _simplify_urls(self, text: str) -> str:
        def simplify(match):
            url = match.group(0)
            parsed_url = urlparse(url)
            return parsed_url.netloc

        return re.sub(r'https?://[^\s]+', simplify, text)
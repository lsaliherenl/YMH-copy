import requests
from typing import List, Dict, Optional
import os
from openai import OpenAI
from urllib.parse import urlparse
import re

# API anahtarlarını ortam değişkenlerinden al
openai_api_key = os.environ.get('OPENAI_API_KEY')
google_api_key = os.environ.get('GOOGLE_API_KEY')
cse_id = os.environ.get('GOOGLE_CSE_ID')

OpenAI.api_key = openai_api_key


class GoogleSearch:
    """Google Custom Search API ile arama yapma ve sonuçları işleme."""

    def __init__(self, api_key: str, cse_id: str):
        self.api_key = api_key
        self.cse_id = cse_id

    def create_search_queries(self, question: str, num_queries: int = 3) -> List[str]:
        """Kullanıcı sorusuna göre web araması sorguları oluşturur."""

        prompt = f"""
        Aşağıdaki Türkçe soruyu cevaplamak için kullanılabilecek {num_queries} farklı web arama sorgusu oluşturun.
        Sorgular, arama motorlarında etkili sonuçlar verecek şekilde optimize edilmelidir.
        Her sorgu, farklı bir yaklaşım veya anahtar kelime kombinasyonu kullanmalıdır.

        Soru: {question}

        Sorgular:
        """
        for i in range(1, num_queries + 1):
            prompt += f"\n{i}. "

        response = OpenAI().chat.completions.create(  # OpenAI() nesnesi oluştur
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
            temperature=0.2,
        )

        queries = response.choices[0].message.content.strip().split("\n")
        return [q.strip().lstrip("0123456789. ") for q in queries]

    def search_web(self, query: str, num_results: int = 5) -> List[Dict]:
        """Verilen sorgu ile Google Custom Search'te arama yapar ve sonuçları döndürür."""

        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "q": query,
            "cx": self.cse_id,
            "key": self.api_key,
            "num": num_results,
            "fields": "items(title,link,snippet)",
        }
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            results = [{'title': item['title'], 'url': item['link'], 'snippet': item.get('snippet', '')} for item in
                       data.get('items', [])]  # Snippet'i güvenli al
            return results
        except requests.exceptions.RequestException as e:
            print(f"Google CSE API hatası: {e}")
            return []
        except ValueError as e:
            print(f"JSONDecodeError: {e}, Response Text: {response.text}")
            return []

    def analyze_and_summarize(self, question: str, results: List[Dict], max_tokens: int = 500) -> Optional[str]:
        """Arama sonuçlarını analiz eder ve özetler."""
        if not results:
            return "Üzgünüm, arama sonuçları bulunamadı."

        context = "\n".join([f"{result['title']}: {result['url']}\n{result['snippet']}" for result in results[:3]])  # İlk 3 sonucu kullan
        prompt = f"""
        Aşağıdaki arama sonuçlarına dayanarak, kullanıcının sorusuna en uygun ve öz bir cevap oluşturun.
        Lütfen sadece MAJEZIK ilacı ile ilgili bilgileri kullanın. Diğer ilaçlar veya genel bilgilerden bahsetmeyin.
        Kaynakları belirtin ve cevaplarınızı Türkçe verin. Mümkünse, kaynak URL'sini kısaltın veya ana sayfayı verin.

        Soru: {question}

        Arama Sonuçları:
        {context}

        Cevap:
        """

        response = OpenAI().chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.2,
        )

        answer = response.choices[0].message.content.strip()

        # URL'leri kısalt veya ana sayfayı al
        answer = self._simplify_urls(answer)

        return answer

    def _simplify_urls(self, text: str) -> str:
        """Metindeki URL'leri kısaltır veya ana sayfayı alır."""

        def simplify(match):
            url = match.group(0)
            parsed_url = urlparse(url)
            return parsed_url.netloc  # Sadece site adını döndür

        return re.sub(r'https?://[^\s]+', simplify, text)
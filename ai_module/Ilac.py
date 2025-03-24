import requests
import json
from bs4 import BeautifulSoup
import re

class Drug:
    def __init__(self, drug_name):
        self.drug_name = drug_name  # İngilizce etken madde/ilaç adı
        self.brand_name = None
        self.generic_name = None
        self.substance_name = None
        self.indications_and_usage = None
        self.warnings = None
        self.dosage_and_administration = None
        self.adverse_reactions = None
        # ... İsteğe bağlı diğer özellikler ...

    def get_fda_info(self):
        """FDA openFDA API'sinden ilaç bilgilerini çeker ve sınıf özelliklerine kaydeder."""
        url = "https://api.fda.gov/drug/label.json"
        params = {
            "search": f'openfda.substance_name:"{self.drug_name}"',  # SADECE etken madde
            "limit": 1
        }
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()

            if 'results' not in data or not data['results']:
                print(f"'{self.drug_name}' için bilgi bulunamadı.")
                return False  # Başarısız

            result = data['results'][0]

            # Bilgileri sınıfın özniteliklerine kaydet
            self.brand_name = result.get('openfda', {}).get('brand_name', [None])[0]
            self.generic_name = result.get('openfda', {}).get('generic_name', [None])[0]
            self.substance_name = result.get('openfda', {}).get('substance_name', [None])[0]
            self.indications_and_usage = result.get('indications_and_usage', [None])[0]
            self.warnings = result.get('warnings', [None])[0]
            self.dosage_and_administration = result.get('dosage_and_administration', [None])[0]
            self.adverse_reactions = result.get('adverse_reactions', [None])[0]
            # ... Diğer alanları da ekle ...
            return True  # Başarılı

        except (requests.exceptions.RequestException, json.JSONDecodeError, KeyError, IndexError) as e:
            print(f"Hata: {e}")
            return False

    def clean_data(self):
        """Çekilen ilaç bilgilerini temizler (HTML etiketleri, vb.)."""

        def clean_string(text):
            """Metin temizleme işlemini yapan yardımcı fonksiyon (private)."""
            if text:
                soup = BeautifulSoup(text, 'html.parser')
                text = soup.get_text(separator=" ")
                text = re.sub(r'\s+', ' ', text).strip()
            return text

        # Sınıfın metin türündeki özniteliklerini temizle
        if self.indications_and_usage:
            self.indications_and_usage = clean_string(self.indications_and_usage)
        if self.warnings:
            self.warnings = clean_string(self.warnings)
        if self.dosage_and_administration:
            self.dosage_and_administration = clean_string(self.dosage_and_administration)
        if self.adverse_reactions:
            self.adverse_reactions = clean_string(self.adverse_reactions)
        # ... Diğer metin türündeki öznitelikleri de temizle ...
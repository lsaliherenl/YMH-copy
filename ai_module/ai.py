import os
from openai import OpenAI

class AIAssistant:
    def __init__(self, api_key, model_name="gpt-3.5-turbo"):
        self.client = OpenAI(api_key=api_key)
        self.model_name = model_name

    @staticmethod
    def create_prompt(drug_info, question):
        """
        İlaç bilgilerini ve kullanıcı sorusunu kullanarak, GPT-3.5-turbo için
        bir prompt oluşturur.  Prompt'u İNGİLİZCE hazırlar, soruyu TÜRKÇE ekler.
        """

        prompt = f"The following information is from the FDA label for the drug with active ingredient: {drug_info.get('substance_name', 'UNKNOWN')}.\n\n"

        # İlaç bilgilerini ekle (eğer varsa)
        if drug_info.get('indications_and_usage'):
            prompt += f"INDICATIONS AND USAGE:\n{drug_info['indications_and_usage']}\n\n"
        if drug_info.get('dosage_and_administration'):
            prompt += f"DOSAGE AND ADMINISTRATION:\n{drug_info['dosage_and_administration']}\n\n"
        if drug_info.get('warnings'):
            prompt += f"WARNINGS:\n{drug_info['warnings']}\n\n"

        # Eğer 'adverse_reactions' BOŞSA veya YOKSA, ve soru yan etkilerle ilgiliyse,
        # UYARILAR bölümünden bilgi EKLE.
        if not drug_info.get('adverse_reactions') and "yan etkileri" in question.lower():
            prompt += "ADVERSE REACTIONS: Information about adverse reactions is primarily found within the WARNINGS section above. Please carefully review the WARNINGS section.\n\n"
        elif drug_info.get('adverse_reactions'):  # Eğer adverse_reactions VARSA
            prompt += f"ADVERSE REACTIONS:\n{drug_info['adverse_reactions']}\n\n"

        # Modele talimatları ver (Türkçe)
        prompt += "Aşağıdaki Türkçe soruyu, YALNIZCA yukarıda verilen İngilizce FDA bilgilerine dayanarak, Türkçe ve MÜMKÜN OLDUĞUNCA KAPSAMLI olarak yanıtlayın. Eğer sorunun cevabı yukarıdaki bilgilerde YOKSA, 'Bilgi bulunamadı' deyin:\n\n"
        prompt += f"Soru: {question}\n\nCevap:"

        return prompt


    def get_response(self, prompt):
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "Sen, kullanıcılara, verilen İngilizce ilaç bilgilerine dayanarak, Türkçe olarak doğru ve eksiksiz bilgi sağlayan yardımcı bir asistansın. Sadece verilen bilgileri kullan, tahmin yürütme veya bilgi ekleme. Bilgi yoksa, 'Bilgi bulunamadı' de."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.2,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"GPT API Hatası: {e}")
            return None
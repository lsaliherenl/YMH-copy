from Ilac import Drug
from ai import AIAssistant
import os

# API anahtarını ortam değişkeninden al
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    print("HATA: OpenAI API anahtarı bulunamadı. Lütfen OPENAI_API_KEY ortam değişkenini ayarlayın.")
    exit()

# AIAssistant nesnesini oluştur
ai = AIAssistant(api_key)

# Kullanıcıdan ilaç adını ve soruyu al (İngilizce ilaç adı, Türkçe soru)
# --- Ana Akış (İnteraktif) ---
while True:
    drug_name_en = input("Lütfen ilacın İngilizce adını veya etken maddesini girin (çıkmak için 'çıkış'): ")
    if drug_name_en.lower() == 'çıkış':
        break

    user_question_tr = input("Lütfen sorunuzu Türkçe olarak girin: ")

    # 1. İlaç nesnesini oluştur
    drug = Drug(drug_name_en)

    # 2. FDA'dan bilgileri çek ve temizle
    if drug.get_fda_info():
        drug.clean_data()

        # 3. Prompt'u oluştur ve GPT-3.5-turbo'dan cevabı al
        drug_info = {
            "substance_name": drug.substance_name,
            "indications_and_usage": drug.indications_and_usage,
            "warnings": drug.warnings,
            "dosage_and_administration": drug.dosage_and_administration,
            "adverse_reactions": drug.adverse_reactions
        }

        prompt = AIAssistant.create_prompt(drug_info, user_question_tr)
        response = ai.get_response(prompt)

        # 4. Cevabı göster
        print("\n--- CEVAP ---")
        if response:
            print(response)
        else:
            print("GPT-3.5-turbo'dan cevap alınamadı.")

    else:
        print(f"FDA'da '{drug_name_en}' için bilgi bulunamadı.")
import os
from Ilac import Drug
from ai import AIAssistant
from typing import Dict, Optional

def get_openai_api_key() -> str:
    """
    OpenAI API anahtarını ortam değişkeninden alır.

    Returns:
        str: OpenAI API anahtarı.
        Raises:
            ValueError: Eğer OPENAI_API_KEY ortam değişkeni bulunamazsa.
    """
    api_key: str = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API anahtarı bulunamadı. Lütfen OPENAI_API_KEY ortam değişkenini ayarlayın.")
    return api_key

def get_drug_and_question() -> tuple[str, str]:
    """
    Kullanıcıdan ilaç adını ve soruyu alır.

    Returns:
        tuple[str, str]: İngilizce ilaç adı ve Türkçe soru.
    """
    drug_name_en: str = input("Lütfen ilacın İngilizce adını veya etken maddesini girin (çıkmak için 'çıkış'): ")
    if drug_name_en.lower() == 'çıkış':
        exit()  # Programı sonlandır
    user_question_tr: str = input("Lütfen sorunuzu Türkçe olarak girin: ")
    return drug_name_en, user_question_tr

def main():
    """
    Ana uygulama akışı.
    """
    try:
        api_key: str = get_openai_api_key()
        ai_assistant: AIAssistant = AIAssistant(api_key)

        while True:
            drug_name_en, user_question_tr = get_drug_and_question()

            drug: Drug = Drug(drug_name_en)

            if drug.get_fda_info():
                drug.clean_data()

                drug_info: Dict[str, Optional[str]] = {
                    "substance_name": drug.substance_name if drug.substance_name is not None else "",
                    "indications_and_usage": drug.indications_and_usage if drug.indications_and_usage is not None else "",
                    "warnings": drug.warnings if drug.warnings is not None else "",
                    "dosage_and_administration": drug.dosage_and_administration if drug.dosage_and_administration is not None else "",
                    "adverse_reactions": drug.adverse_reactions if drug.adverse_reactions is not None else ""
                }

                prompt: str = AIAssistant.create_prompt(drug_info, user_question_tr)
                response: Optional[str] = ai_assistant.get_response(prompt)

                print("\n--- CEVAP ---")
                if response:
                    print(response)
                else:
                    print("GPT-3.5-turbo'dan cevap alınamadı.")

            else:
                print(f"FDA'da '{drug_name_en}' için bilgi bulunamadı.")

    except ValueError as ve:
        print(f"HATA: {ve}")
    except Exception as e:
        print(f"Bilinmeyen bir hata oluştu: {e}")

if __name__ == "__main__":
    main()
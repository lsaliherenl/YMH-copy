from flask import Flask, request, jsonify, render_template
import os
from Ilac import Drug
from ai import AIAssistant
from google_research.google_search import GoogleSearch
from typing import Dict, Optional, List
from datetime import datetime, timedelta
from dotenv import load_dotenv
from openai import OpenAI

# .env dosyasını yükle
load_dotenv()

app = Flask(__name__)

# Konuşma geçmişini saklamak için basit bir bellek
conversation_memory = {}

def get_openai_api_key() -> str:
    """
    OpenAI API anahtarını ortam değişkeninden alır.
    """
    api_key: str = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OpenAI API anahtarı bulunamadı. Lütfen OPENAI_API_KEY ortam değişkenini ayarlayın.")
    return api_key

def get_google_api_keys() -> tuple[str, str]:
    """
    Google API anahtarlarını ortam değişkenlerinden alır.
    """
    google_api_key: str = os.environ.get("GOOGLE_API_KEY")
    cse_id: str = os.environ.get("GOOGLE_CSE_ID")

    if not google_api_key:
        raise ValueError("Google API anahtarı bulunamadı. Lütfen GOOGLE_API_KEY ortam değişkenini ayarlayın.")
    if not cse_id:
        raise ValueError("Google CSE ID bulunamadı. Lütfen GOOGLE_CSE_ID ortam değişkenini ayarlayın.")

    return google_api_key, cse_id

def get_conversation_history(session_id: str) -> List[Dict]:
    """
    Belirli bir oturum için konuşma geçmişini döndürür.
    """
    if session_id in conversation_memory:
        # 1 saatten eski konuşmaları temizle
        current_time = datetime.now()
        conversation_memory[session_id] = [
            conv for conv in conversation_memory[session_id]
            if current_time - conv['timestamp'] < timedelta(hours=1)
        ]
        return conversation_memory[session_id]
    return []

def add_to_conversation_history(session_id: str, drug_name: str, question: str, response: str):
    """
    Konuşma geçmişine yeni bir mesaj ekler.
    """
    if session_id not in conversation_memory:
        conversation_memory[session_id] = []
    
    conversation_memory[session_id].append({
        'timestamp': datetime.now(),
        'drug_name': drug_name,
        'question': question,
        'response': response
    })

def generate_natural_response(drug_name: str, raw_response: str, conversation_history: List[Dict], question: str) -> str:
    """
    FDA veya Google'dan gelen ham yanıtı alıp daha doğal, sohbet tarzında bir yanıt oluşturur.
    """
    api_key: str = get_openai_api_key()
    client = OpenAI(api_key=api_key)
    
    # Konuşma geçmişini OpenAI formatına dönüştür
    messages = [
        {"role": "system", "content": f"""
        Sen ilaçlar hakkında bilgi veren, samimi ve yardımsever bir sağlık asistanısın.
        Kullanıcının sorduğu sorulara aşağıdaki bilgilere dayanarak cevap vereceksin.
        Cevaplarında resmi tıbbi dil yerine, daha samimi ve anlaşılır bir dil kullan.
        İlaç bilgilerini sunarken fazla teknik terimleri açıkla ve kullanıcının endişelerini dinle.
        Bilgi kaynağının FDA veya web aramaları olduğunu belirtmene gerek yok.
        Cevaplarında kısa ve öz ol, ancak önemli bilgileri atlamadan ve samimi bir dilde yanıtla.
        
        Şu anda kullanıcı seninle {drug_name} ilacı hakkında konuşuyor.
        """}
    ]
    
    # Konuşma geçmişini ekle
    for entry in conversation_history:
        if 'role' in entry and 'content' in entry:
            messages.append({"role": entry['role'], "content": entry['content']})
    
    # Kullanıcının mevcut sorusunu ekle
    messages.append({"role": "user", "content": question})
    
    # Ham yanıtı ekle
    messages.append({"role": "system", "content": f"Aşağıdaki ham bilgiler mevcut soru için bulundu, bunu kullanıcıya samimi şekilde ilet: {raw_response}"})
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=1500,
        temperature=0.7,
    )
    
    return response.choices[0].message.content

def simple_chat_response(message: str, conversation_history: List[Dict]) -> str:
    """
    İlaç araması yapmadan basit sohbet yanıtları üretir.
    """
    api_key: str = get_openai_api_key()
    client = OpenAI(api_key=api_key)
    
    messages = [
        {"role": "system", "content": """
        Sen samimi ve yardımsever bir sağlık asistanısın. Sağlık ve ilaçlar konusunda genel bilgiler verebilirsin,
        ancak spesifik ilaç tavsiyeleri yapmamalısın. Kullanıcıyla doğal bir sohbet akışı içinde
        konuşmalısın. Eğer kullanıcı belirli bir ilaç hakkında bilgi isterse, ona yardımcı olmak istediğini
        ama önce ilaç adını açıkça belirtmesi gerektiğini söyle.
        
        Yanıtlarını kısa ve anlaşılır tut, tıbbi terimleri kullanmaktan kaçın. Kullanıcıya
        bir doktor veya eczacıya danışması gerektiğini hatırlatabilirsin.
        """}
    ]
    
    # Konuşma geçmişini ekle
    for entry in conversation_history:
        if 'role' in entry and 'content' in entry:
            messages.append({"role": entry['role'], "content": entry['content']})
    
    # Kullanıcının mevcut mesajını ekle
    messages.append({"role": "user", "content": message})
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=500,
        temperature=0.7,
    )
    
    return response.choices[0].message.content

@app.route('/')
def index():
    """
    Ana sayfa - web arayüzünü gösterir.
    """
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """
    Genel sohbet için API endpoint'i.
    
    Beklenen JSON formatı:
    {
        "message": "Kullanıcı mesajı",
        "session_id": "Oturum ID'si (opsiyonel)",
        "conversation_history": "Önceki konuşma geçmişi (opsiyonel)"
    }
    """
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({
                'error': 'Geçersiz istek formatı. message alanı gerekli.'
            }), 400

        message = data['message']
        session_id = data.get('session_id', 'default')
        client_conversation_history = data.get('conversation_history', [])
        
        # Konuşma geçmişini al
        server_conversation_history = get_conversation_history(session_id)
        
        # Konuşma geçmişini birleştir (client varsa onu öncelikle kullan)
        conversation_history = client_conversation_history if client_conversation_history else server_conversation_history
        
        # Basit sohbet yanıtı oluştur
        chat_response = simple_chat_response(message, conversation_history)
        
        # Konuşma geçmişini güncelle
        if session_id not in conversation_memory:
            conversation_memory[session_id] = []
            
        conversation_memory[session_id].append({
            'timestamp': datetime.now(),
            'role': 'user',
            'content': message
        })
        
        conversation_memory[session_id].append({
            'timestamp': datetime.now(),
            'role': 'assistant',
            'content': chat_response
        })
        
        return jsonify({
            'response': chat_response,
            'conversation_history': conversation_history
        })
        
    except Exception as e:
        return jsonify({'error': f"Bilinmeyen bir hata oluştu: {str(e)}"}), 500

@app.route('/api/drug-info', methods=['POST'])
def get_drug_info():
    """
    İlaç bilgisi ve soru için API endpoint'i.
    
    Beklenen JSON formatı:
    {
        "drug_name_en": "İngilizce ilaç adı",
        "question_tr": "Türkçe soru",
        "session_id": "Oturum ID'si (opsiyonel)",
        "conversation_history": "Önceki konuşma geçmişi (opsiyonel)"
    }
    """
    try:
        # JSON verisini al
        data = request.get_json()
        
        if not data or 'drug_name_en' not in data or 'question_tr' not in data:
            return jsonify({
                'error': 'Geçersiz istek formatı. drug_name_en ve question_tr alanları gerekli.'
            }), 400

        drug_name_en = data['drug_name_en'].strip()
        question_tr = data['question_tr'].strip()
        session_id = data.get('session_id', 'default')
        client_conversation_history = data.get('conversation_history', [])

        # İlaç adının kısa olup olmadığını kontrol et (çok uzunsa muhtemelen ilaç adı değildir)
        if len(drug_name_en.split()) > 3:
            return jsonify({
                'error': 'İlaç adı çok uzun. Lütfen daha kısa bir ilaç adı belirtin.',
                'web_response': 'İlaç adı çok uzun görünüyor. Lütfen araştırmak istediğiniz ilacın adını daha kısa ve net belirtin.'
            })

        # Konuşma geçmişini al
        server_conversation_history = get_conversation_history(session_id)
        
        # Konuşma geçmişini birleştir (client varsa onu öncelikle kullan)
        conversation_history = client_conversation_history if client_conversation_history else server_conversation_history

        # API anahtarlarını al
        api_key_openai = get_openai_api_key()
        api_key_google, cse_id_google = get_google_api_keys()

        # Servisleri başlat
        ai_assistant = AIAssistant(api_key_openai)
        google_search = GoogleSearch(api_key_google, cse_id_google)

        # FDA bilgilerini al
        drug = Drug(drug_name_en)
        response_data = {
            'drug_name': drug_name_en,
            'question': question_tr,
            'fda_response': None,
            'web_response': None,
            'conversation_history': conversation_history
        }

        raw_response = None

        # FDA'dan ilaç bilgilerini çek
        fda_success = drug.get_fda_info()
        
        if fda_success:
            drug.clean_data()

            drug_info = {
                "substance_name": drug.substance_name if drug.substance_name is not None else "",
                "indications_and_usage": drug.indications_and_usage if drug.indications_and_usage is not None else "",
                "warnings": drug.warnings if drug.warnings is not None else "",
                "dosage_and_administration": drug.dosage_and_administration if drug.dosage_and_administration is not None else "",
                "adverse_reactions": drug.adverse_reactions if drug.adverse_reactions is not None else ""
            }

            prompt = AIAssistant.create_prompt(drug_info, question_tr)
            response_fda = ai_assistant.get_response(prompt)
            
            if response_fda:
                raw_response = response_fda
                # Daha doğal bir yanıt oluştur
                natural_response = generate_natural_response(drug_name_en, response_fda, conversation_history, question_tr)
                response_data['fda_response'] = natural_response
                add_to_conversation_history(session_id, drug_name_en, question_tr, natural_response)
            else:
                response_data['fda_response'] = "FDA verilerinden cevap alınamadı."

        # FDA'da bilgi bulunamazsa web araması yap
        if not raw_response:
            try:
                # İlaç adı ve soruyu birleştirerek ara
                combined_query = f"{drug_name_en} {question_tr}"
                search_queries = google_search.create_search_queries(combined_query, drug_name_en)
                all_results = []
                for query in search_queries:
                    results = google_search.search_web(query)
                    all_results.extend(results)

                if all_results:
                    answer_google = google_search.analyze_and_summarize(question_tr, all_results, drug_name_en)
                    if answer_google:
                        raw_response = answer_google
                        # Daha doğal bir yanıt oluştur
                        natural_response = generate_natural_response(drug_name_en, answer_google, conversation_history, question_tr)
                        response_data['web_response'] = natural_response
                        add_to_conversation_history(session_id, drug_name_en, question_tr, natural_response)
                    else:
                        response_data['web_response'] = f"Üzgünüm, {drug_name_en} hakkında bu soruya cevap bulamadım. Farklı bir ilaç adı veya soru deneyebilirsiniz."
                else:
                    response_data['web_response'] = f"Üzgünüm, {drug_name_en} adında bir ilaç bulamadım. İlaç adının doğru yazıldığından emin olun veya başka bir ilaç adı deneyin."
            except Exception as e:
                response_data['web_response'] = f"Web arama sırasında hata oluştu: {str(e)}"

        # Herhangi bir yanıt alınamadıysa, genel bir yanıt ver
        if not response_data['fda_response'] and not response_data['web_response']:
            response_data['web_response'] = f"Üzgünüm, {drug_name_en} hakkında bilgi bulamadım. Lütfen ilaç adının doğru yazıldığından emin olun veya başka bir ilaç sorun."

        return jsonify(response_data)

    except ValueError as ve:
        return jsonify({'error': str(ve)}), 400
    except Exception as e:
        return jsonify({'error': f"Bilinmeyen bir hata oluştu: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 
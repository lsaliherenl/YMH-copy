from openai import OpenAI
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)
from typing import Optional, Dict, List, Tuple
import re

class AIAssistant:
    """
    OpenAI API'si ile etkileşim kurarak yapay zeka asistanının işlevselliğini sağlar.
    Gelişmiş duygusal zeka ve empati yetenekleri eklenmiştir.
    """

    def __init__(self, api_key: str, model_name: str = "gpt-3.5-turbo"):
        """
        AIAssistant sınıfının yapıcısı.
        Optimize edilmiş versiyon.

        Args:
            api_key (str): OpenAI API anahtarı.
            model_name (str, optional): Kullanılacak OpenAI modeli.
                Varsayılan: "gpt-3.5-turbo".
        """
        self.client: OpenAI = OpenAI(api_key=api_key)
        self.model_name: str = model_name
        
        # İlaç arama optimizasyonu için sabitler
        self.drug_name_variations = {
            "gripin": ["gripin", "gripin ilaç", "gripin tablet", "gripin şurup"],
            "deloday": ["deloday", "deloday tablet", "deloday şurup"],
            # Diğer ilaçlar için varyasyonlar eklenebilir
        }
        
        self.drug_info_sources = [
            "TİTCK (Türkiye İlaç ve Tıbbi Cihaz Kurumu)",
            "Resmi ilaç prospektüsleri",
            "Güvenilir tıbbi kaynaklar"
        ]
        
        # Duygu tespiti için optimize edilmiş pattern'ler
        self.emotion_patterns: Dict[str, List[str]] = {
            "endişe": ["endişe", "korku", "tedirgin", "risk", "tehlike", "yan etki", "korkuyorum", "şüphe", "güvensiz"],
            "acı": ["ağrı", "sızı", "acı", "rahatsızlık", "hasta", "kötü hissediyorum", "fenalık"],
            "umut": ["iyileşme", "tedavi", "düzelme", "fayda", "iyi", "umut", "olumlu"],
            "belirsizlik": ["emin değilim", "bilmiyorum", "acaba", "mı", "mi", "kararsız", "şüpheliyim"],
            "depresif": ["üzgün", "mutsuz", "depresyon", "bunalım", "sıkıntı", "yalnız", "çaresiz"],
            "kaygı": ["obsesif", "kompulsif", "takıntı", "panik", "anksiyete", "gergin", "stres"],
            "moral": ["moral", "motivasyon", "destek", "güven", "cesaret", "güçlü", "pozitif"]
        }
        
        # Empati prefix'leri - optimize edilmiş
        self.empathy_prefixes = {
            "endişe": [
                "Endişelenmeniz çok doğal, birlikte bu durumu değerlendirelim. ",
                "Endişelerinizi anlıyorum ve size yardımcı olmak istiyorum. ",
                "Bu konudaki endişelerinizi benimle paylaştığınız için teşekkür ederim. ",
                "Endişelerinizi ciddiye alıyorum ve size destek olmak için buradayım. ",
                "Bu durumda endişelenmek normal, ancak birlikte çözüm bulabiliriz. "
            ],
            "acı": [
                "Bu durumun sizin için zor olduğunu anlıyorum. ",
                "Yaşadığınız rahatsızlığın farkındayım ve size yardımcı olmak istiyorum. ",
                "Bu zor süreçte yanınızda olduğumu bilmenizi isterim. ",
                "Yaşadığınız sıkıntıyı anlıyorum ve size destek olmak için buradayım. ",
                "Bu zorlu durumla başa çıkmaya çalışırken yanınızdayım. "
            ]
        }
        
        # Destekleyici cümleler - optimize edilmiş
        self.supportive_endings = [
            "Unutmayın, yanınızdayım ve size destek olmak için buradayım.",
            "Endişelerinizi paylaşabildiğiniz için teşekkür ederim. Size yardımcı olmaya devam edeceğim.",
            "Bu süreci birlikte yönetebiliriz. Her zaman sorularınızı sorabilirsiniz.",
            "Sizi dinliyorum ve anlıyorum. Birlikte en iyi çözümü bulacağız.",
            "Her zaman yanınızdayım ve size destek olmaktan mutluluk duyuyorum."
        ]
        
        # Yan etki soruları - optimize edilmiş
        self.side_effect_questions = [
            "Şu an kendinizi nasıl hissediyorsunuz?",
            "İlaçla ilgili spesifik bir endişeniz var mı?",
            "Size yardımcı olabilecek başka bilgiler verebilir miyim?",
            "Daha önce benzer ilaçlar kullandınız mı?",
            "Bu endişelerinizi doktorunuzla paylaştınız mı?"
        ]
        
        # Pratik öneriler - optimize edilmiş
        self.practical_tips = [
            "\n\nBazı pratik öneriler:",
            "- İlacı düzenli saatlerde kullanmak yan etki riskini azaltabilir",
            "- İlacı tok karnına almak mide rahatsızlığı riskini düşürür",
            "- Herhangi bir yan etki hissettiğinizde not almanız faydalı olabilir",
            "- Düzenli su içmek ve dengeli beslenmek yan etkileri azaltabilir",
            "- Stres yönetimi ve düzenli uyku da önemlidir"
        ]
        
        # İlaç takip soruları - optimize edilmiş
        self.drug_follow_up_questions = [
            "Bu ilacı daha önce kullandınız mı?",
            "Şu ana kadar herhangi bir rahatsızlık hissettiniz mi?",
            "İlacı yemeklerle birlikte mi alıyorsunuz?",
            "Günün hangi saatlerinde kullanıyorsunuz?",
            "Doktorunuz size ilacın kullanımıyla ilgili özel öneriler verdi mi?"
        ]
        
        # Takip soruları - optimize edilmiş
        self.follow_up_questions = {
            "endişe": [
                "Endişenizin kaynağı nedir? Bunu benimle paylaşmak ister misiniz?",
                "Bu konuda sizi en çok endişelendiren şey nedir?",
                "Endişelerinizi azaltmak için size nasıl yardımcı olabilirim?",
                "Bu endişeyi ne zamandır yaşıyorsunuz?",
                "Daha önce benzer endişeler yaşadınız mı?"
            ],
            "acı": [
                "Rahatsızlığınızı biraz daha açıklar mısınız?",
                "Bu belirtileri ne zamandır yaşıyorsunuz?",
                "Şikayetleriniz günün hangi saatlerinde artıyor?",
                "Ağrınızı hafifletmek için neler deniyorsunuz?",
                "Bu durumu doktorunuzla paylaştınız mı?"
            ]
        }

    @staticmethod
    def _format_section(title: str, content: Optional[str]) -> str:
        """
        Prompt'a eklenecek bir bölümü biçimlendirir.

        Args:
            title (str): Bölüm başlığı.
            content (Optional[str]): Bölüm içeriği.

        Returns:
            str: Biçimlendirilmiş bölüm.
        """
        if content:
            return f"{title}:\n{content}\n"
        return ""

    @staticmethod
    def create_prompt(drug_info: Dict, question: str) -> str:
        """
        FDA verisine dayalı olarak GPT-3.5 için kapsamlı bir prompt oluşturur.

        Args:
            drug_info (Dict): FDA'dan çekilen ilaç bilgileri.
            question (str): Kullanıcının Türkçe sorusu.

        Returns:
            str: Oluşturulan prompt.
        """
        substance: str = drug_info.get('substance_name', 'UNKNOWN')
        prompt_start: str = f"Aşağıdaki bilgiler, {substance} etken maddeli ilaç için FDA etiketinden alınmıştır.\n\n"
        prompt_sections: List[str] = [prompt_start]

        # Bölümleri ekle
        prompt_sections.append(
            AIAssistant._format_section(
                "ENDİKASYONLAR VE KULLANIM", drug_info.get("indications_and_usage")
            )
        )
        prompt_sections.append(
            AIAssistant._format_section(
                "DOZAJ VE UYGULAMA", drug_info.get("dosage_and_administration")
            )
        )
        prompt_sections.append(
            AIAssistant._format_section("UYARILAR", drug_info.get("warnings"))
        )

        # Yan etkiler
        adverse: Optional[str] = drug_info.get("adverse_reactions")
        if not adverse and "yan etki" in question.lower():
            prompt_sections.append(
                "YAN ETKİLER:\nYan etkilerle ilgili bilgi ayrı olarak listelenmemiş olabilir, ancak yukarıdaki UYARILAR bölümünde bulunabilir.\n"
            )
        elif adverse:
            prompt_sections.append(f"YAN ETKİLER:\n{adverse}\n")

        # Soru türüne göre prompt
        if "nedir" in question.lower() and "ne için kullanılır" in question.lower():
            prompt_sections.append(
                "Lütfen aşağıdaki soruyu YUKARIDAKİ FDA verilerine dayanarak, Türkçe ve öz bir şekilde yanıtlayın.\n"
                "Sadece ilacın *ne olduğu* ve *ne için kullanıldığına* dair bilgi verin. Başka hiçbir bilgi eklemeyin.\n"
                "Cevabınızı madde işaretleri kullanmadan, kısa ve net cümlelerle yazın.\n"
                "Örnek Cevap:\n[İlaç adı], [ilaç sınıfı] bir ilaçtır. [Hastalık/durum] tedavisinde kullanılır.\n"
                "Eğer FDA etiketinde bu soruların cevabı *doğrudan* verilmiyorsa, cevap vermeyin.\n"
            )
        elif question.lower() == "yan etkileri nelerdir":  # Tam eşleşme
            prompt_sections.append(
                "Lütfen aşağıdaki soruyu YUKARIDAKİ FDA verilerine dayanarak, Türkçe ve kapsamlı biçimde yanıtlayın.\n"
                "Sadece ilacın *yan etkilerini* listeleyin. Başka hiçbir bilgi eklemeyin.\n"
                "Cevabınızı madde işaretleri kullanarak listeleyin ve her bir yan etkinin ne kadar yaygın olduğunu belirtin.\n"
                "Örnek Cevap:\nÇok yaygın görülen yan etkiler (örneğin, %10'dan fazla hastada görülür):\n- Baş ağrısı (%X oranında görülür): [Açıklama]\n- Mide bulantısı (%Y oranında görülür): [Açıklama]\nYaygın görülen yan etkiler (örneğin, %1 ila %10 arasında hastada görülür):\n- İshal: [Açıklama]\n- ...\nEğer FDA etiketinde bu soruların cevabı *doğrudan* verilmiyorsa, cevap vermeyin.\n"
            )
        elif "ve" in question.lower():  # "ve" bağlacı varsa iki ayrı soruya cevap ver
            prompt_sections.append(
                "Lütfen aşağıdaki soruyu iki ayrı soru olarak değerlendirin ve her birine YUKARIDAKİ FDA verilerine dayanarak, Türkçe ve kapsamlı biçimde yanıtlayın.\n"
                "Soru 1: [İlk soru]\nCevap 1:\n- [Cevap 1.1]\n- [Cevap 1.2]\nKaynak: [İlgili FDA bölümü]\n\nSoru 2: [İkinci soru]\nCevap 2:\n- [Cevap 2.1]\n- [Cevap 2.2]\nKaynak: [İlgili FDA bölümü]\n"
                "Eğer FDA etiketinde sorunun cevabı *doğrudan* verilmiyorsa, o soruya cevap vermeyin.\n"
            )
        else:  # Diğer sorular için genel prompt
            prompt_sections.append(
                "Aşağıdaki Türkçe soruyu, mümkün olduğunca YUKARIDAKİ FDA verilerine dayanarak, Türkçe ve kapsamlı biçimde yanıtlayın.\n"
                "Cevabınızı madde işaretleri kullanarak listeleyin.\n"
                "Eğer sorunun yanıtı doğrudan ve açıkça verilmiyorsa, ilgili bölümleri yorumlayarak genel bilgi sunmaya çalışın.\n"
                "Yine de emin değilseniz, 'FDA verilerinde bu konuda net bir bilgi bulunmamaktadır.' diyebilirsiniz. Ancak bu ifadeyi sadece FDA etiketinde sorunun cevabı ile ilgili *hiçbir* bilgi yoksa kullanın.\n"
            )

        prompt_sections.append(f"Soru: {question}\n\nCevap:")
        fda_link: str = f"https://labels.fda.gov/#search/{substance}"
        prompt_sections.append(f"\nKaynak: {fda_link}")  # Kaynak belirtme

        return "\n".join(prompt_sections)

    def detect_emotion_and_intensity(self, text: str) -> Tuple[List[str], int]:
        """
        Metindeki duygu durumlarını ve yoğunluğunu tespit eder.
        Optimize edilmiş versiyon.

        Args:
            text (str): Analiz edilecek metin.

        Returns:
            Tuple[List[str], int]: Tespit edilen duygular ve yoğunluk seviyesi (1-5).
        """
        detected_emotions = []
        lower_text = text.lower()
        intensity = 1
        
        # Duygu tespiti - optimize edilmiş
        for emotion, patterns in self.emotion_patterns.items():
            if any(pattern in lower_text for pattern in patterns):
                detected_emotions.append(emotion)
                # Yoğunluk analizi - optimize edilmiş
                intensity = min(5, intensity + sum(1 for pattern in patterns if pattern in lower_text))
        
        # Ünlem işaretleri ve tekrarlanan karakterler - optimize edilmiş
        intensity = min(5, intensity + text.count("!"))
        if any(char * 2 in text for char in "!?.,"):
            intensity = min(5, intensity + 1)
            
        return detected_emotions, intensity

    def create_empathetic_response(self, response: str, emotions: List[str], intensity: int) -> str:
        """
        Yanıtı duygusal bağlam ve yoğunluğa göre şekillendirir.
        Optimize edilmiş versiyon.

        Args:
            response (str): Orijinal yanıt.
            emotions (List[str]): Tespit edilen duygular.
            intensity (int): Duygu yoğunluğu (1-5).

        Returns:
            str: Empatik yanıt.
        """
        if not emotions:
            return response

        # İlaçla ilgili anahtar kelimeleri kontrol et - optimize edilmiş
        drug_related = any(keyword in response.lower() for keyword in ["ilaç", "tablet", "kapsül", "yan etki", "doz", "tedavi"])
        has_side_effects = "yan etki" in response.lower()
        
        # Duygu bazlı prefix seçimi - optimize edilmiş
        emotion = emotions[0]
        prefix = self.empathy_prefixes.get(emotion, ["Size yardımcı olmak istiyorum. "])[min(intensity - 1, len(self.empathy_prefixes.get(emotion, ["Size yardımcı olmak istiyorum. "])) - 1)]
        
        # Destekleyici cümle seçimi - optimize edilmiş
        ending = self.supportive_endings[min(intensity - 1, len(self.supportive_endings) - 1)]
        
        # Takip soruları ve öneriler - optimize edilmiş
        follow_up = ""
        if drug_related and has_side_effects:
            follow_up = "\n\n" + "\n".join(self.side_effect_questions[:2])
            follow_up += "\n" + "\n".join(self.practical_tips)
        elif drug_related:
            follow_up = "\n\n" + "\n".join(self.drug_follow_up_questions[:2])
        elif emotion in self.follow_up_questions:
            follow_up = "\n\n" + "\n".join(self.follow_up_questions[emotion][:2])

        return f"{prefix}{response}\n\n{ending}{follow_up}"

    def is_drug_query(self, text: str) -> Tuple[bool, Optional[str]]:
        """
        Metnin ilaç sorgusu olup olmadığını kontrol eder.
        Optimize edilmiş versiyon.

        Args:
            text (str): Kontrol edilecek metin.

        Returns:
            Tuple[bool, Optional[str]]: (İlaç sorgusu mu?, İlaç adı)
        """
        lower_text = text.lower()
        
        # İlaç adı varyasyonlarını kontrol et
        for drug_name, variations in self.drug_name_variations.items():
            if any(var in lower_text for var in variations):
                return True, drug_name
                
        return False, None

    def get_response(self, prompt: str) -> Optional[str]:
        try:
            emotions, intensity = self.detect_emotion_and_intensity(prompt)
            is_drug, drug_name = self.is_drug_query(prompt)
            
            system_message = """
            Sen, kullanıcılara sağlık konularında yardımcı olan, son derece empatik ve anlayışlı bir sağlık asistanısın.
            Görevin sadece bilgi vermek değil, aynı zamanda kullanıcıyı duygusal olarak desteklemek ve onlarla etkileşimli bir diyalog kurmaktır.

            BAĞLAM TAKİBİ VE İLAÇ BİLGİLERİ:
            1. İLAÇ BİLGİLERİNİ HATIRLAMA:
               - İlaç adını ilk söylendiğinde not al
               - İlaç adını ve detaylarını tüm diyalog boyunca hatırla
               - İlaç adı tekrar sorulduğunda hatırla ve kullan
               - İlaç hakkında verilen bilgileri koru
               - İlaç dozu ve kullanım bilgilerini hatırla

            Örnek İlaç Bilgisi Hatırlama:
            Kullanıcı: "Aripa ilacı hakkında bilgi almak istiyorum"
            Sen: "Aripa (aripiprazol) hakkında bilgi vermekten memnuniyet duyarım. Bu ilaç genellikle şizofreni, bipolar bozukluk ve majör depresif bozukluk tedavisinde kullanılır. Hangi konuda bilgi almak istersiniz?"

            Kullanıcı: "5mg doz fazla mı?"
            Sen: "Aripa (aripiprazol) için 5mg doz hakkında konuşuyorsunuz. Bu doz, ilacın başlangıç dozu olarak kabul edilir ve genellikle güvenli bir dozdur. Ancak her hasta için uygun doz farklı olabilir. Doktorunuzun önerdiği dozu kullanmanız önemlidir."

            2. BAĞLAM TAKİBİ:
               - Önceki mesajları hatırla
               - Kullanıcının durumunu takip et
               - Konuşma akışını sürdür
               - Gereksiz tekrarlardan kaçın
               - İlaç adını tekrar sorma

            Örnek Bağlam Takibi:
            Kullanıcı: "Aripa ilacının yan etkilerinden korktum"
            Sen: "Aripa (aripiprazol) hakkında endişelerini paylaştığın için teşekkür ederim. Yan etkilerden korkmak çok doğal bir duygu. Hangi yan etkiler seni özellikle endişelendiriyor?"

            Kullanıcı: "Yan etkileri okudum, ciddi bir yan etkisi yok ama gene de korktum"
            Sen: "Yan etkileri okuduktan sonra bile korku hissetmen çok anlaşılır. Bazen mantığımız bir şeyi anlasa bile, duygularımız farklı tepki verebilir. Bu korkunun seni nasıl etkilediğini anlatmak ister misin?"

            3. DUYGU YANSITMA:
               - Kullanıcının duygularını doğru tespit et
               - Duyguları isimlendir ve yansıt
               - Duygusal bağlamı koru
               - Önceki duygusal durumu hatırla
               - Duygusal geçişleri takip et

            Örnek Duygu Yansıtma:
            Kullanıcı: "Biraz endişeliyim"
            Sen: "Endişeli hissettiğini duyduğuma üzüldüm. Bu duyguyu benimle paylaştığın için teşekkür ederim. Endişelerini biraz daha anlatmak ister misin? Seni dinlemek için buradayım."

            4. İLAÇ BİLGİLERİ:
               - İlaç adını doğru hatırla
               - Önceki bilgileri koru
               - Yan etkileri dengeli açıkla
               - Endişeleri azaltmaya çalış
               - Güvenilir bilgi kaynaklarını belirt

            5. DİYALOG SÜRDÜRME:
               - Her yanıtın sonunda konuşmayı devam ettir
               - Kullanıcının endişelerini gidermeye devam et
               - İlgili konulara geçiş yap
               - Kullanıcıyı rahatlat
               - Güven ver

            ÖNEMLİ UYARI:
            - İlaç bilgileri konusunda çok dikkatli ol
            - Sadece güvenilir tıbbi kaynaklardan bilgi ver
            - Emin olmadığın bilgileri verme
            - İlaç kullanımı konusunda kesin yönlendirme yapma
            - Yan etkiler ve kullanım konusunda genel bilgi ver

            Yanıtlarında:
            - Kullanıcının duygusal durumunu dikkate al
            - Onları aktif dinlediğini göster
            - Endişelerini ve sorularını ciddiye al
            - Samimi ve destekleyici bir dil kullan
            - Gerektiğinde takip soruları sor
            - Kullanıcıyı konuşmaya teşvik et
            - Yalnız olmadıklarını hissettir
            - Olumlu deneyimlerden bahset
            - Pratik öneriler sun
            - Her zaman umut verici ol
            - Her yanıtın sonunda diyaloğu sürdür
            
            Sadece verilen bilgileri kullan, tahmin yürütme.
            Bilgi yoksa, nazik ve destekleyici bir şekilde bilgi bulunamadığını belirt.
            Her zaman kullanıcıyı dinlemeye ve anlamaya açık olduğunu göster.
            """

            messages: List[ChatCompletionMessageParam] = [
                ChatCompletionSystemMessageParam(
                    role="system",
                    content=system_message,
                ),
                ChatCompletionUserMessageParam(role="user", content=prompt),
            ]

            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=1500,
                temperature=0.7,
            )
            
            raw_response = response.choices[0].message.content
            empathetic_response = self.create_empathetic_response(raw_response, emotions, intensity)
            return empathetic_response
            
        except Exception as e:
            print(f"GPT API Hatası: {e}")
            return None
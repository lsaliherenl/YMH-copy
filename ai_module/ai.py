from openai import OpenAI
from openai.types.chat import (
    ChatCompletionMessageParam,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
)
from typing import Optional, Dict, List

class AIAssistant:
    """
    OpenAI API'si ile etkileşim kurarak yapay zeka asistanının işlevselliğini sağlar.
    """

    def __init__(self, api_key: str, model_name: str = "gpt-3.5-turbo"):
        """
        AIAssistant sınıfının yapıcısı.

        Args:
            api_key (str): OpenAI API anahtarı.
            model_name (str, optional): Kullanılacak OpenAI modeli.
                Varsayılan: "gpt-3.5-turbo".
        """
        self.client: OpenAI = OpenAI(api_key=api_key)
        self.model_name: str = model_name

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

    def get_response(self, prompt: str) -> Optional[str]:
        """
        Oluşturulan prompt'u OpenAI API'sine gönderir ve cevabı alır.

        Args:
            prompt (str): OpenAI'ye gönderilecek prompt.

        Returns:
            Optional[str]: OpenAI'den alınan cevap veya None (hata durumunda).
        """
        try:
            messages: List[ChatCompletionMessageParam] = [
                ChatCompletionSystemMessageParam(
                    role="system",
                    content="Sen, kullanıcılara, verilen İngilizce ilaç "
                    "bilgilerine dayanarak, Türkçe olarak doğru ve eksiksiz "
                    "bilgi sağlayan yardımcı bir asistansın. Sadece verilen "
                    "bilgileri kullan, tahmin yürütme veya bilgi ekleme. "
                    "Bilgi yoksa, 'Bilgi bulunamadı' de.",
                ),
                ChatCompletionUserMessageParam(role="user", content=prompt),
            ]

            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=1000,
                temperature=0.2,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"GPT API Hatası: {e}")
            return None
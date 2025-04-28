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
        prompt_start: str = (
            "The following information is from the FDA label for the drug "
            f"with active ingredient: {substance}.\n"
        )
        prompt_sections: List[str] = [prompt_start]

        # Bölümleri ekle
        prompt_sections.append(
            AIAssistant._format_section(
                "INDICATIONS AND USAGE", drug_info.get("indications_and_usage")
            )
        )
        prompt_sections.append(
            AIAssistant._format_section(
                "DOSAGE AND ADMINISTRATION", drug_info.get("dosage_and_administration")
            )
        )
        prompt_sections.append(
            AIAssistant._format_section("WARNINGS", drug_info.get("warnings"))
        )

        # Yan etkiler
        adverse: Optional[str] = drug_info.get("adverse_reactions")
        if not adverse and "yan etki" in question.lower():
            prompt_sections.append(
                "ADVERSE REACTIONS:\nInformation about adverse reactions is not "
                "separately listed but may be found in the WARNINGS section above.\n"
            )
        elif adverse:
            prompt_sections.append(f"ADVERSE REACTIONS:\n{adverse}\n")

        # Son talimat (Türkçe)
        prompt_sections.append(
            "Aşağıdaki Türkçe soruyu, mümkün olduğunca YUKARIDAKİ FDA "
            "verilerine dayanarak, Türkçe ve kapsamlı biçimde yanıtlayın.\n"
            "Eğer sorunun yanıtı doğrudan açıkça verilmiyorsa, ilgili bölümleri "
            "yorumlayarak genel bilgi sunmaya çalışın.\n"
            "Yine de emin değilseniz, 'FDA verilerinde net bilgi bulunamadı.' "
            "diyebilirsiniz.\n"
        )

        prompt_sections.append(f"Soru: {question}\n\nCevap:")
        fda_link: str = f"https://labels.fda.gov/#search/{substance}"
        prompt_sections.append(f"\nDaha fazla bilgi için FDA etiketi: {fda_link}")

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
                max_tokens=500,
                temperature=0.2,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"GPT API Hatası: {e}")
            return None
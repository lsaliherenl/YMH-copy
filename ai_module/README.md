# AI Sağlık Asistanı

Bu proje, ilaç bilgisi ve sağlık danışmanlığı sağlayan bir yapay zeka asistanıdır.

## Güvenlik Notları

- API anahtarlarınızı asla GitHub'a yüklemeyin
- `.env` dosyasını `.gitignore`'a eklediğinizden emin olun
- Test raporları hassas bilgiler içerebilir, bunları da yüklemeyin

## Kurulum

1. Gerekli paketleri yükleyin:
```bash
pip install -r requirements.txt
```

2. `.env.example` dosyasını `.env` olarak kopyalayın ve API anahtarlarınızı ekleyin:
```bash
cp .env.example .env
```

3. Uygulamayı başlatın:
```bash
python app.py
```

## Test

Testleri çalıştırmak için:
```bash
python test_data/test_runner.py
```

## Katkıda Bulunma

1. Bu depoyu fork edin
2. Yeni bir branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add some amazing feature'`)
4. Branch'inizi push edin (`git push origin feature/amazing-feature`)
5. Bir Pull Request oluşturun

## Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakın.

## Modül Özellikleri:
- FDA API üzerinden ilaç verisi çekme
- OpenAI GPT-3.5 ile Türkçe soru-cevap sistemi
- Veri temizleme ve düzenleme
- Komut satırından kullanım

## Dosyalar:
- `ai.py`: OpenAI API ve prompt sistemi
- `Ilac.py`: FDA veri çekme ve temizleme
- `main.py`: Ana çalışma akışı
- `requirements.txt`: Gerekli kütüphaneler

## Not:
Bu klasör, projenin **Yapay Zeka** bileşeninden sorumlu kişi [@berkayhsrt](https://github.com/berkay123001) tarafından geliştirilmiştir.

## Geliştirme Günlüğü 📓

• [Bu Hafta Yapılanlar - 23 Mart](devlogs/BuHaftaYapılanlar_23Mart.txt)  
• [Gelecek Geliştirme Alanları](devlogs/GelecekGelistirmeAlanlari.txt)


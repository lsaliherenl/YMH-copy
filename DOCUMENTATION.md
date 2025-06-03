# BIOWORKS Projesi Dokümantasyonu

## Proje Genel Bakış
Bu proje, Spring Boot tabanlı bir REST API ve frontend uygulamasından oluşan bir web uygulamasıdır.

## Teknoloji Yığını

### Backend
- Java 17
- Spring Boot 3.2.3
- Spring Security
- Spring Data JPA
- PostgreSQL
- Lombok
- Maven

### Frontend
- HTML/CSS/JavaScript
- BIOWORKS(new) klasöründe frontend uygulaması

### AI Modülü
- Python
- Flask
- Docker
- Google Research API

## Detaylı Proje Yapısı

```
.
├── .git/                    # Git versiyon kontrol sistemi
├── .vscode/                 # VS Code IDE ayarları
├── ai_module/              # Yapay zeka modülü
│   ├── templates/          # Web arayüzü şablonları
│   │   └── index.html     # Ana web sayfası
│   ├── google_research/   # Google araştırma entegrasyonu
│   │   ├── google_search.py # Google arama işlemleri
│   │   └── utils.py       # Yardımcı fonksiyonlar
│   ├── Fine-tuning-data/  # Model ince ayar verileri
│   ├── devlogs/          # Geliştirme günlükleri
│   ├── test_data/        # Test verileri
│   ├── ai.py             # Ana AI modeli
│   ├── app.py            # Flask uygulaması
│   ├── main.py           # Ana uygulama girişi
│   ├── Ilac.py           # İlaç işlemleri modülü
│   ├── test_app.py       # Uygulama testleri
│   ├── test_error_handling.py # Hata yönetimi testleri
│   ├── requirements.txt   # Python bağımlılıkları
│   ├── environment.yml    # Conda ortam yapılandırması
│   ├── Dockerfile        # Docker yapılandırması
│   ├── .dockerignore     # Docker hariç tutma listesi
│   ├── .gitignore       # Git hariç tutma listesi
│   └── README.md        # AI modülü dokümantasyonu
├── BIOWORKS(new)/         # Güncel frontend uygulaması
│   ├── photos/            # Proje görselleri
│   ├── html-css/         # Frontend kaynak kodları
│   ├── devlogs/          # Geliştirme günlükleri
│   ├── package-lock.json # NPM bağımlılık kilidi
│   └── README.md        # Frontend dokümantasyonu
├── src/                    # Kaynak kodları
│   └── main/
│       ├── java/          # Java kaynak kodları
│       │   └── com/
│       │       └── melihawci/
│       │           └── springrestapi/
│       │               ├── config/     # Konfigürasyon sınıfları
│       │               ├── controller/ # REST API kontrolcüleri
│       │               ├── dto/        # Veri transfer nesneleri
│       │               ├── model/      # Veritabanı modelleri
│       │               ├── repository/ # Veritabanı repository'leri
│       │               ├── service/    # İş mantığı servisleri
│       │               └── SpringRestApiApplication.java
│       └── resources/     # Uygulama kaynakları
├── target/                # Derleme çıktıları
├── Dockerfile            # Docker konfigürasyonu
├── index.html           # Yönlendirme Sayfası
├── pom.xml             # Maven proje yapılandırması
└── README.md          # Proje açıklaması
```

## Bağımlılıklar

### Backend Bağımlılıkları
- spring-boot-starter-web
- spring-boot-starter-data-jpa
- spring-boot-starter-security
- postgresql
- lombok
- spring-boot-starter-test

### AI Modülü Bağımlılıkları
- Python 3.x
- Flask
- Google Research API
- Conda (opsiyonel)

## Kurulum ve Çalıştırma

1. Gereksinimler:
   - Java 17
   - Maven
   - PostgreSQL
   - Node.js (Frontend için)
   - Python 3.x (AI modülü için)
   - Docker (opsiyonel)

2. Backend Kurulumu:
   ```bash
   mvn clean install
   mvn spring-boot:run
   ```

3. Frontend Kurulumu:
   ```bash
   cd BIOWORKS(new)
   npm install
   npm start
   ```

4. AI Modülü Kurulumu:
   ```bash
   cd ai_module
   pip install -r requirements.txt
   # veya Conda kullanarak:
   conda env create -f environment.yml
   python main.py
   ```

## Docker Desteği
Proje Docker ile containerize edilebilir. Her modül için ayrı Dockerfile mevcuttur.

## Güvenlik
- Spring Security entegrasyonu mevcuttur
- JWT tabanlı kimlik doğrulama sistemi
- AI modülü için güvenlik kontrolleri

## Geliştirme
- VS Code IDE desteği mevcuttur
- Lombok kullanılarak kod tekrarı azaltılmıştır
- RESTful API prensipleri uygulanmıştır
- AI modülü için test senaryoları mevcuttur

## Notlar
- Proje geliştirme aşamasındadır
- Daha detaylı dokümantasyon için ilgili klasörlerdeki README dosyalarına bakınız 
# BIOWORKS - Geliştirme Günlüğü - 2024-05-04 (28 Nisan - 4 Mayıs)

Bu hafta (28 Nisan - 4 Mayıs) BIOWORKS projesinde yapılan geliştirmeler:

## Genel İlerleme

Bu hafta, BIOWORKS projesinin temel HTML ve CSS yapısı üzerine odaklanıldı. Kullanıcıların etkileşimde bulunabileceği çeşitli sayfalar oluşturuldu.

## Tamamlanan İşler

* **Giriş Sayfası (`login.html`):**
    * Kullanıcıların e-posta ve şifrelerini girerek sisteme giriş yapmalarını sağlayan temel arayüz oluşturuldu.
    * "Beni Hatırla" seçeneği eklendi.
    * "Şifremi Unuttum" ve "Kayıt Ol" bağlantıları eklendi.
    * "Misafir Olarak Devam Et" seçeneği eklendi.
* **Kayıt Sayfası (`register.html`):**
    * Kullanıcıların ad, soyad, yaş, cinsiyet, e-posta ve şifre bilgilerini girebilecekleri kayıt formu oluşturuldu.
    * Şifre doğrulama alanı eklendi.
    * "Giriş Yap" sayfasına yönlendirme bağlantısı eklendi.
* **Şifremi Unuttum Sayfası (`forgot_password.html`):**
    * Kullanıcıların şifre sıfırlama talebinde bulunabilecekleri sayfa oluşturuldu.
    * E-posta adresi giriş alanı ve şifre sıfırlama bağlantısı gönderme butonu eklendi.
    * "Giriş Yap" ve "Kayıt Ol" sayfalarına yönlendirme bağlantıları eklendi.
* **Ana Sayfa (`main_page.html`):**
    * Sol tarafta sohbet geçmişinin görüntüleneceği temel arayüz oluşturuldu.
    * Üst menüde "Ana Sayfa", "Hakkımızda", "İletişim" ve "Profil" sayfalarına bağlantılar eklendi.
    * Mesaj gönderme alanı oluşturuldu.
* **Profil Sayfası (`profile.html`):**
    * Kullanıcıların profil bilgilerini görüntüleyebileceği temel sayfa oluşturuldu (içerik henüz eklenmedi).
* **Hakkımızda Sayfası (`about_us.html`):**
    * Uygulama hakkında bilgilerin yer alacağı temel sayfa oluşturuldu (içerik henüz eklenmedi).
* **İletişim Sayfası (`communication.html`):**
    * Kullanıcıların iletişim bilgilerine ulaşabileceği temel sayfa oluşturuldu (içerik henüz eklenmedi).
* **Stil Dosyaları (`style.css`, `main_page.css`):**
    * Tüm sayfaların genel görünümünü ve düzenini sağlamak için temel CSS stilleri oluşturuldu.
    * Ana sayfaya özel stiller (`main_page.css`) eklendi.
    * Font Awesome kütüphanesi entegre edildi (ikonlar için).

## Karşılaşılan Zorluklar

* CSS düzenlemelerinde bazı uyumluluk sorunları yaşandı, ancak çözüldü.
* Ana sayfa düzeninin istenen şeffaflık ve bulanıklık efektlerine sahip olması biraz zaman aldı.

## Gelecek Hafta Planları

* Veritabanı entegrasyonuna başlanacak.
* Kullanıcı etkileşimlerini yönetecek JavaScript kodları yazılacak.
* Profil, Hakkımızda ve İletişim sayfalarının içeriği doldurulacak.
* Duyarlılık (responsive) tasarım iyileştirmeleri yapılacak.

## Ek Notlar

Bu hafta projenin iskeleti tamamlandı. Gelecek hafta daha çok işlevsellik eklemeye odaklanacağız.

## Katkıda Bulunanlar

* [Salih Eren Çavuşoğlu , Berkay Hasret]
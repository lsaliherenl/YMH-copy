# BIOWORKS Web Uygulaması

Bu proje, kullanıcıların etkileşimde bulunabileceği çeşitli web sayfalarını içermektedir. Giriş, kayıt, şifremi unuttum gibi temel kullanıcı kimlik doğrulama işlemlerinin yanı sıra, ana sayfa, profil, hakkında ve iletişim sayfalarını da içermektedir.

---

## Proje Açıklaması

Bu web uygulaması, kullanıcıların hesaplarını yönetmelerine ve çeşitli bilgilere erişmelerine olanak tanır. Kullanıcıların sisteme güvenli bir şekilde erişim sağlaması ve etkileşimde bulunması için tasarlanmıştır.

---

## İçerik

Proje aşağıdaki dosyaları içermektedir:

* `index.html` (veya `login.html`): Kullanıcıların e-posta ve şifrelerini girerek sisteme giriş yapmalarını sağlayan giriş sayfası. Misafir olarak devam etme ve şifremi unuttum seçenekleri de bulunur.
* `register.html` : Kullanıcıların ad, soyad, yaş, cinsiyet, e-posta ve şifre bilgilerini girerek yeni bir hesap oluşturmalarını sağlayan kayıt sayfası.
* `forgot_password.html` : Kullanıcıların şifrelerini sıfırlamak için e-posta adreslerini girebilecekleri şifremi unuttum sayfası.
* `main_page.html` : Kullanıcıların giriş yaptıktan sonra yönlendirileceği ana sayfa. Sohbet geçmişi ve etkileşim alanı içerir.
* `about_us.html` : Uygulama hakkında bilgi veren "Hakkımızda" sayfası.
* `communication.html` : Kullanıcıların iletişim bilgilerine ulaşabileceği "İletişim" sayfası.
* `profile.html` : Kullanıcıların kendi profillerini görüntüleyebileceği ve düzenleyebileceği "Profil" sayfası.
* `style.css` : Tüm sayfaların genel görünümünü ve düzenini kontrol eden CSS stil dosyası.
* `main_page.css`: Ana sayfaya özel stilleri içeren CSS dosyası.

---

## Özellikler

* **Giriş Sayfası:**

    * E-posta ve şifre alanları.
    * "Beni Hatırla" seçeneği.
    * "Şifremi Unuttum" bağlantısı (`forgot_password.html` sayfasına yönlendirir).
    * "Kayıt Ol" sayfasına yönlendirme bağlantısı (`register.html` sayfasına yönlendirir).
    * "Misafir Olarak Devam Et" seçeneği (`main_page.html` sayfasına yönlendirir).
    * Giriş formu düzeni ve stili güncellendi.

* **Kayıt Sayfası:**

    * Ad, soyad, yaş, cinsiyet, e-posta ve şifre alanları.
    * Şifre doğrulama alanı.
    * "Giriş Yap" sayfasına yönlendirme bağlantısı (`login.html` sayfasına yönlendirir).
    * Kayıt formu düzeni ve stili güncellendi.

* **Şifremi Unuttum Sayfası:**

    * E-posta adresi alanı.
    * Şifre sıfırlama bağlantısı gönderme butonu.
    * "Giriş Yap" ve "Kayıt Ol" sayfalarına yönlendirme bağlantıları.
    * Şifremi Unuttum sayfası düzeni ve stili güncellendi.

* **Ana Sayfa:**

    * Sol tarafta sohbet geçmişi bölümü.
    * Mesaj gönderme alanı.
    * Üst menüde "Ana Sayfa", "Hakkımızda", "İletişim" ve "Profil" sayfalarına bağlantılar.
    * Ana sayfa düzeni ve stilleri (`main_page.css`) iyileştirildi.
    * Font Awesome ikonları entegre edildi.

* **Hakkımızda Sayfası:**

    * Uygulama hakkında bilgilerin yer alacağı sayfa (içerik henüz eklenmedi).

* **İletişim Sayfası:**

    * Kullanıcıların iletişim kurabileceği bilgilerin yer alacağı ve mesaj gönderebileceği sayfa.
    * İletişim formu eklendi.
    * İletişim sayfası stilize edildi (`communication.css`).

* **Profil Sayfası:**

    * Kullanıcıların profil bilgilerini görüntüleyebileceği ve düzenleyebileceği sayfa.
    * Profil fotoğrafı değiştirme, şifre güncelleme ve çıkış yapma bölümleri eklendi.
    * Profil sayfası stilize edildi (`profile.css`).

* **Stil:**

    * Modern ve kullanıcı dostu tasarım.
    * Duyarlı (responsive) tasarım (farklı ekran boyutlarına uyum sağlar).
    * "BIOWORKS" marka adı ve vurgulu renkler.
    * Ana sayfada bulanıklık efektli şeffaf tasarım öğeleri.
    * Genel stil iyileştirmeleri ve düzenlemeler yapıldı.
    * Sayfalara özel stil dosyaları (`main_page.css`, `profile.css`, `communication.css`) kullanıldı.

---

## Kurulum

1.  Bu projeyi GitHub'dan klonlayın veya indirin.
2.  Dosyaları bir web sunucusuna (örneğin, Apache, Nginx) veya yerel bir geliştirme ortamına (örneğin, XAMPP, WAMP) yerleştirin.
3.  `index.html` veya `login.html` dosyasını bir tarayıcıda açarak uygulamayı başlatın.

---

## Kullanım

* **Giriş Yapmak İçin:**
    1.  `index.html` veya `login.html` sayfasına gidin.
    2.  E-posta adresinizi ve şifrenizi girin.
    3.  "Giriş Yap" düğmesine tıklayın.
    4.  İsterseniz "Beni Hatırla" seçeneğini işaretleyebilirsiniz.
    5.  Şifrenizi unuttuysanız, "Şifremi Unuttum" bağlantısına tıklayarak şifre sıfırlama sayfasına gidebilirsiniz.
    6.  Hesabınız yoksa, "Kayıt Ol" bağlantısına tıklayarak kayıt sayfasına gidebilirsiniz.
    7.  Hesap oluşturmadan devam etmek isterseniz, "Misafir Olarak Devam Et" düğmesine tıklayabilirsiniz.
* **Kayıt Olmak İçin:**
    1.  `register.html` sayfasına gidin.
    2.  Gerekli tüm bilgileri (ad, soyad, yaş, cinsiyet, e-posta, şifre, şifre tekrarı) girin.
    3.  "Kayıt Ol" düğmesine tıklayın.
    4.  Zaten bir hesabınız varsa, "Giriş Yap" bağlantısına tıklayarak giriş sayfasına gidebilirsiniz.
* **Şifremi Unuttum:**
    1.  `forgot_password.html` sayfasına gidin.
    2.  E-posta adresinizi girin.
    3.  "Şifre Sıfırlama Bağlantısı Gönder" düğmesine tıklayın.
    4.  Giriş yapmak için "Giriş Yap" veya kayıt olmak için "Kayıt Ol" bağlantılarını kullanabilirsiniz.
* **Ana Sayfa:**
    1.  Sol tarafta sohbet geçmişinizi görüntüleyebilirsiniz.
    2.  Alt kısımdaki metin alanına mesajınızı yazıp gönderebilirsiniz.
    3.  Üst menüden "Ana Sayfa", "Hakkımızda", "İletişim" ve "Profil" sayfalarına erişebilirsiniz.
* **Diğer Sayfalar:**
    * "Hakkımızda", "İletişim" ve "Profil" sayfalarını ilgili menü bağlantılarından ziyaret edebilirsiniz.

---

## Ekran Görüntüleri

* Ekran Görüntüleri Gözükmüyorsa "photos>>z-site_preview" Kısmından İnceleyebilirsiniz. 

* **Giriş Sayfası:**

    * ![Giriş Sayfası Ekran Görüntüsü](photos/z-site_preview/giris-yap_v1.png)
    * Giriş sayfası düzeni ve formu güncellendi.

* **Kayıt Sayfası:**

    * ![Kayıt Sayfası Ekran Görüntüsü](photos/z-site_preview/kayit-ol_v1.png)
    * Kayıt formu ve alanları güncellendi.

* **Şifremi Unuttum Sayfası:**

    * ![Şifremi Unuttum Sayfası Ekran Görüntüsü](photos/z-site_preview/sifremi-unuttum_v1.png)
    * Şifremi Unuttum sayfası düzeni güncellendi.

* **Ana Sayfa:**
    * ![Ana Sayfa Ekran Görüntüsü v1](photos/z-site_preview/ana-sayfa_v1.png)
    * ![Ana Sayfa Ekran Görüntüsü v2](photos/z-site_preview/ana-sayfa_v2.png)
    * Ana sayfa düzeni, üst menü ve sohbet bölümü güncellendi.

* **Profil Sayfası:**

    * ![Profil Sayfası Ekran Görüntüsü v1](photos\z-site_preview\profil_v1.png)
    * ![Profil Sayfası Ekran Görüntüsü v2](photos\z-site_preview\profil_v2.png)
    * Profil sayfası oluşturuldu ve düzenlendi.
    * Profil fotoğrafı değiştirme, şifre güncelleme ve çıkış yapma özellikleri eklendi.

* **İletişim Sayfası:**

    * ![İletişim Sayfası Ekran Görüntüsü v1](photos/z-site_preview/iletisim_v1.png)
    * ![İletişim Sayfası Ekran Görüntüsü v2](photos/z-site_preview/iletisim_v2.png)
    * İletişim sayfası oluşturuldu ve iletişim formu eklendi.
    * İletişim sayfası stilize edildi.

* **Hakkımızda Sayfası:**

    * ![Hakkımızda Sayfası Ekran Görüntüsü v1](photos/z-site_preview/hakkimizda_v1.png)
    * Hakkımızda sayfası oluşturuldu ve düzenlendi.


---

## Teknolojiler

* HTML5
* CSS3
* Font Awesome (ikonlar için)

---

## Geliştirme

Bu projeye katkıda bulunmak isterseniz, lütfen aşağıdaki adımları izleyin:

1.  Projeyi fork edin.
2.  Yeni bir branch oluşturun (`git checkout -b yeni-ozellik`).
3.  Değişikliklerinizi yapın.
4.  Değişikliklerinizi commit'leyin (`git commit -m "Yeni özellik eklendi"`).
5.  Branch'inizi push edin (`git push origin yeni-ozellik`).
6.  Pull Request gönderin.

---

## İletişim

Herhangi bir sorunuz veya öneriniz varsa, lütfen benimle iletişime geçmekten çekinmeyin.

---
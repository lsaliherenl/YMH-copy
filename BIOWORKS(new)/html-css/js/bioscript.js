// Şifre göster/gizle fonksiyonu

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.toggle-password').forEach(function(el) {
        el.addEventListener('click', function() {
            var input = document.querySelector(this.getAttribute('toggle'));
            if (input.type === 'password') {
                input.type = 'text';
                input.classList.add('password-visible');
                this.innerHTML = '<i class="fa fa-eye-slash"></i>';
            } else {
                input.type = 'password';
                input.classList.remove('password-visible');
                this.innerHTML = '<i class="fa fa-eye"></i>';
            }
        });
    });

    // Kayıt formu işlevi
    const registerForm = document.querySelector('.login-form');
    if (registerForm) {
        registerForm.addEventListener('submit', async function(e) {
            e.preventDefault();

            // Form verilerini al
            const name = document.getElementById('name')?.value;
            const surname = document.getElementById('surname')?.value;
            const age = document.getElementById('age')?.value;
            const gender = document.getElementById('gender')?.value;
            const email = document.getElementById('email')?.value;
            const password = document.getElementById('password')?.value;
            const confirmPassword = document.getElementById('confirm-password')?.value;

            // Eğer kayıt formundaysak
            if (name && surname && age && gender && email && password && confirmPassword) {
                // Şifre kontrolü
                if (password !== confirmPassword) {
                    alert('Şifreler eşleşmiyor!');
                    return;
                }

                try {
                    // Backend'e kayıt isteği gönder
                    const response = await fetch('http://localhost:8080/api/auth/register', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            username: email, // E-posta adresini kullanıcı adı olarak kullan
                            email: email,
                            password: password,
                            fullName: `${name} ${surname}`
                        })
                    });

                    const data = await response.json();

                    if (response.ok) {
                        // Başarılı kayıt
                        alert('Kayıt başarılı! Giriş sayfasına yönlendiriliyorsunuz.');
                        window.location.href = 'index.html';
                    } else {
                        // Hata durumu
                        alert(data.message || 'Kayıt işlemi başarısız oldu!');
                    }
                } catch (error) {
                    console.error('Kayıt hatası:', error);
                    alert('Bir hata oluştu. Lütfen tekrar deneyin.');
                }
            }
        });
    }
}); 
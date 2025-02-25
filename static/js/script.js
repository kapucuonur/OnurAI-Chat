document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const responseContainer = document.getElementById('response-container');
    const charCounter = document.getElementById('char-counter');
    const themeButton = document.getElementById('theme-button');

    // Enter tuşu ile gönderme işlemi
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter') {
            e.preventDefault(); // Formun varsayılan davranışını engelle
            form.dispatchEvent(new Event('submit')); // Formu gönder
        }
    });

    // Form gönderildiğinde yapılacak işlemler
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const inputText = userInput.value.trim();

        if (inputText) {
            try {
                // Gönderme butonunu devre dışı bırak ve yükleniyor mesajı göster
                form.querySelector('button').disabled = true;
                form.querySelector('button').innerHTML = '⏎';

                const response = await fetch('/ask', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ user_input: inputText })
                });

                const data = await response.json();

                if (response.ok) {
                    responseContainer.style.opacity = '0';
                    responseContainer.innerHTML = `<p><strong>You:</strong> ${inputText}</p>
                                                  <p><strong>Groq:</strong> ${data.response}</p>`;
                    setTimeout(() => {
                        responseContainer.style.opacity = '1';
                    }, 100);
                } else {
                    responseContainer.innerHTML = `<p>An error occurred: ${data.error}</p>`;
                }
            } catch (error) {
                responseContainer.innerHTML = `<p>Error: ${error.message}</p>`;
            } finally {
                // Gönderme butonunu tekrar aktif hale getir ve metni "Send" olarak ayarla
                form.querySelector('button').disabled = false;
                form.querySelector('button').innerHTML = '△';
                // Input alanını temizle
                userInput.value = '';
                // Input alanına odaklan
                userInput.focus();
            }
        }
    });

    // Karakter sayacı
    userInput.addEventListener('input', () => {
        const charCount = userInput.value.length;
        charCounter.textContent = `${charCount}/500`;
    });

    // Tema değiştirme
    themeButton.addEventListener('click', () => {
        document.body.classList.toggle('dark-theme');
    });
});
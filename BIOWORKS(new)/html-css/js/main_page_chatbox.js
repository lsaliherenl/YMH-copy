// main_page.html chatbox için ai_module mantığıyla
let conversationHistory = [];
let currentDrug = null;
let isSearchingForDrug = false;
let sessionId = 'web-session-' + Date.now();

const commonDrugKeywords = [
    'aspirin', 'paracetamol', 'ibuprofen', 'antibiyotik', 'enalapril',
    'vitamin', 'ağrı kesici', 'ateş düşürücü', 'tansiyon', 'kolesterol',
    'majezik', 'prozac', 'xanax', 'zoloft', 'insulin', 'metformin',
    'deloday', 'deltacortril', 'dolorex', 'dikloron', 'deksametazon',
    'dolven', 'arveles', 'nexium', 'augmentin', 'cipro', 'lipitor',
    'coumadin', 'concor', 'nurofen', 'ventolin', 'minoset', 'apranax'
];
const healthRelatedKeywords = [
    'ilaç', 'tablet', 'kapsül', 'etken madde', 'doz', 'dozaj', 'yan etki',
    'kullanım', 'tedavi', 'hastalık', 'semptom', 'reçete', 'eczane',
    'mg', 'miligram', 'içerik', 'faydalı', 'zararlı', 'rahatsızlık'
];
const commonPhrases = [
    'merhaba', 'selam', 'nasılsın', 'teşekkürler', 'sağol', 
    'tamam', 'evet', 'hayır', 'olur', 'olmaz', 'belki',
    'bilgi', 'arıyorum', 'hakkında', 'korkuyorum', 'endişe',
    'yan etki', 'kullanıyorum', 'istiyorum', 'lütfen'
];

function addMessage(message, isUser = false) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = isUser ? 'user-message' : 'assistant-message';
    messageDiv.innerHTML = message.replace(/\n/g, '<br>');
    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function isDrugRelated(message) {
    const lowerMessage = message.toLowerCase();
    if (currentDrug) {
        const drugTerms = [
            'ne için', 'nedir', 'yan etki', 'kullanılır', 'nasıl', 'doz', 'dozaj',
            'etken', 'madde', 'tehlikeli', 'bebek', 'hamile', 'çocuk', 'kullanan',
            'kullanım', 'uyarı', 'dikkat'
        ];
        for (const term of drugTerms) {
            if (lowerMessage.includes(term)) {
                return true;
            }
        }
    }
    for (const drug of commonDrugKeywords) {
        if (lowerMessage.includes(drug)) {
            return true;
        }
    }
    let healthTermCount = 0;
    for (const keyword of healthRelatedKeywords) {
        if (lowerMessage.includes(keyword)) {
            healthTermCount++;
        }
    }
    return healthTermCount >= 2;
}

function extractPotentialDrugName(message) {
    const lowerMessage = message.toLowerCase();
    const words = message.split(' ');
    if (words.length > 5) {
        return null;
    }
    for (const drug of commonDrugKeywords) {
        if (lowerMessage.includes(drug)) {
            return drug;
        }
    }
    const indicators = ['ilacı', 'hakkında', 'adlı', 'isimli', 'ilacını', 'ilacın', 'tablet', 'kapsül'];
    for (let i = 1; i < words.length; i++) {
        const lowerWord = words[i].toLowerCase();
        if (indicators.includes(lowerWord)) {
            const prevWord = words[i-1].toLowerCase();
            if (!commonPhrases.includes(prevWord)) {
                return words[i-1];
            }
        }
    }
    if (lowerMessage.includes('ilacın adı') || lowerMessage.includes('ilaç adı')) {
        const parts = lowerMessage.split('adı');
        if (parts.length > 1) {
            const potentialDrug = parts[1].trim().split(' ')[0];
            if (!commonPhrases.includes(potentialDrug)) {
                return potentialDrug;
            }
        }
    }
    if (words.length === 1 && !commonPhrases.includes(lowerMessage)) {
        return message;
    }
    return null;
}

async function generalChat(message) {
    showLoading(true);
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                message: message,
                session_id: sessionId,
                conversation_history: conversationHistory
            })
        });
        const data = await response.json();
        addMessage(data.response);
        conversationHistory.push({ role: "user", content: message });
        conversationHistory.push({ role: "assistant", content: data.response });
    } catch (error) {
        addMessage("Bir hata oluştu. Lütfen tekrar deneyin.");
    } finally {
        showLoading(false);
    }
}

async function handleConversation(message) {
    addMessage(message, true);
    const drugRelated = isDrugRelated(message);
    if (currentDrug && message.toLowerCase().includes(currentDrug.toLowerCase())) {
        await getIlacInfo(currentDrug, message);
        return;
    }
    if (drugRelated) {
        if (!currentDrug && !isSearchingForDrug) {
            const potentialDrug = extractPotentialDrugName(message);
            if (potentialDrug) {
                currentDrug = potentialDrug;
                addMessage(`Endişelerinizi anlıyorum. ${currentDrug} hakkında size yardımcı olmak için bilgi araştırıyorum...`);
                await getIlacInfo(currentDrug, "ne için kullanılır");
                return;
            } else {
                isSearchingForDrug = true;
                const lowerMessage = message.toLowerCase();
                let response = "";
                if (lowerMessage.includes("endişe") || lowerMessage.includes("korku") || lowerMessage.includes("yan etki")) {
                    response = "Endişelerinizi anlıyorum. Size daha iyi yardımcı olabilmem için, bahsettiğiniz ilacın adını paylaşır mısınız?";
                } else if (lowerMessage.includes("ağrı") || lowerMessage.includes("acı")) {
                    response = "Yaşadığınız rahatsızlığı anlıyorum. Size doğru bilgileri verebilmem için, kullandığınız ilacın adını öğrenebilir miyim?";
                } else if (lowerMessage.includes("moral") || lowerMessage.includes("destek")) {
                    response = "Size destek olmak istiyorum. Hangi ilaç hakkında bilgi almak istediğinizi benimle paylaşır mısınız?";
                } else {
                    response = "Size yardımcı olmak için ilacın adını öğrenmem gerekiyor. Hangi ilaç hakkında bilgi almak istiyorsunuz?";
                }
                addMessage(response);
                return;
            }
        } else if (isSearchingForDrug) {
            const potentialDrug = extractPotentialDrugName(message);
            if (potentialDrug) {
                currentDrug = potentialDrug;
                isSearchingForDrug = false;
                addMessage(`${currentDrug} hakkında size yardımcı olmak için bilgi araştırıyorum. Özellikle merak ettiğiniz bir konu var mı?`);
                await getIlacInfo(currentDrug, "ne için kullanılır");
            } else {
                addMessage("Üzgünüm, tam olarak hangi ilaçtan bahsettiğinizi anlayamadım. İlacın adını tekrar yazabilir misiniz?");
            }
            return;
        }
    }
    await generalChat(message);
}

async function getIlacInfo(drugName, question) {
    showLoading(true);
    try {
        const response = await fetch('/api/drug-info', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                drug_name_en: drugName,
                question_tr: question,
                session_id: sessionId,
                conversation_history: conversationHistory
            })
        });
        const data = await response.json();
        let answer = "Üzgünüm, bu konuda bilgi bulamadım.";
        if (data.fda_response) {
            answer = data.fda_response;
        } else if (data.web_response) {
            answer = data.web_response;
        }
        addMessage(answer);
        conversationHistory.push({ role: "user", content: question });
        conversationHistory.push({ role: "assistant", content: answer });
    } catch (error) {
        addMessage("Bir hata oluştu. Lütfen tekrar deneyin.");
    } finally {
        showLoading(false);
    }
}

function showLoading(show) {
    let loading = document.getElementById('chatbox-loading');
    if (!loading) {
        loading = document.createElement('div');
        loading.id = 'chatbox-loading';
        loading.innerHTML = '<div class="spinner-border text-primary" role="status"><span class="visually-hidden">Yükleniyor...</span></div>';
        document.getElementById('chatMessages').appendChild(loading);
    }
    loading.style.display = show ? 'block' : 'none';
    if (!show) loading.remove();
}

document.querySelector('.send-button').addEventListener('click', async function() {
    const input = document.getElementById('messageInput');
    const message = input.value.trim();
    if (message) {
        await handleConversation(message);
        input.value = '';
    }
});

document.getElementById('messageInput').addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        document.querySelector('.send-button').click();
    }
}); 
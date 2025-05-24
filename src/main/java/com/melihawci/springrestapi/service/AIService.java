package com.melihawci.springrestapi.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class AIService {
    
    @Value("${ai.service.url}")
    private String aiServiceUrl;
    
    private final RestTemplate restTemplate;
    
    public AIService() {
        this.restTemplate = new RestTemplate();
    }
    
    public String getAIResponse(String message) {
        try {
            // Python servisine istek gönder
            String response = restTemplate.postForObject(
                aiServiceUrl + "/chat",
                message,
                String.class
            );
            return response != null ? response : "Üzgünüm, şu anda yanıt veremiyorum.";
        } catch (Exception e) {
            return "Yapay zeka servisi ile iletişim kurulurken bir hata oluştu.";
        }
    }
} 
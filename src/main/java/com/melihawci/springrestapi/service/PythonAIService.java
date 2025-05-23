package com.melihawci.springrestapi.service;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Service
public class PythonAIService implements AIService {
    
    private final RestTemplate restTemplate;
    private final String pythonServiceUrl;

    public PythonAIService(
            @Value("${python.service.url}") String pythonServiceUrl) {
        this.restTemplate = new RestTemplate();
        this.pythonServiceUrl = pythonServiceUrl;
    }

    @Override
    public String getAnswer(String question) {
        // Python servisine istek gönder
        return restTemplate.postForObject(
            pythonServiceUrl + "/ask",
            question,
            String.class
        );
    }
} 
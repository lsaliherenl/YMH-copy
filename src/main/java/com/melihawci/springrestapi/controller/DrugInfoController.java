package com.melihawci.springrestapi.controller;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class DrugInfoController {

    @Value("${ai.service.url}")
    private String aiServiceUrl;

    private final RestTemplate restTemplate = new RestTemplate();

    @PostMapping("/drug-info")
    public ResponseEntity<?> getDrugInfo(@RequestBody Map<String, Object> request) {
        try {
            // AI modülüne istek atılacak veri
            Map<String, Object> aiRequest = new HashMap<>();
            aiRequest.put("drug_name_en", request.get("drug_name_en"));
            aiRequest.put("question_tr", request.get("question_tr"));
            aiRequest.put("session_id", request.get("session_id"));
            aiRequest.put("conversation_history", request.get("conversation_history"));

            // AI modülüne POST isteği gönder
            String aiUrl = aiServiceUrl + "/drug-info";
            ResponseEntity<Map> aiResponse = restTemplate.postForEntity(aiUrl, aiRequest, Map.class);

            // Gelen cevabı frontend'e döndür
            return ResponseEntity.ok(aiResponse.getBody());
        } catch (Exception e) {
            Map<String, String> error = new HashMap<>();
            error.put("error", "AI modülünden cevap alınamadı: " + e.getMessage());
            return ResponseEntity.internalServerError().body(error);
        }
    }
} 
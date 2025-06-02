package com.melihawci.springrestapi.service;

import com.melihawci.springrestapi.dto.ChatResponse;
import com.melihawci.springrestapi.model.ChatHistory;
import com.melihawci.springrestapi.model.User;
import com.melihawci.springrestapi.repository.ChatHistoryRepository;
import com.melihawci.springrestapi.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class ChatService {

    @Autowired
    private ChatHistoryRepository chatHistoryRepository;

    @Autowired
    private UserRepository userRepository;

    @Value("${ai.service.url}")
    private String aiServiceUrl;

    private final RestTemplate restTemplate = new RestTemplate();

    public ChatResponse processMessage(String message, Long userId) {
        try {
            // AI servisine istek gönder
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);

            Map<String, Object> requestBody = new HashMap<>();
            requestBody.put("message", message);
            requestBody.put("session_id", "web-session-" + System.currentTimeMillis());

            HttpEntity<Map<String, Object>> request = new HttpEntity<>(requestBody, headers);

            String aiResponse = restTemplate.postForObject(
                aiServiceUrl + "/chat",
                request,
                String.class
            );

            // Kullanıcıyı bul (misafir ise null)
            User user = userId != null ? userRepository.findById(userId).orElse(null) : null;

            // Sohbet geçmişini kaydet
            ChatHistory chatHistory = new ChatHistory();
            chatHistory.setUser(user);
            chatHistory.setUserMessage(message);
            chatHistory.setAiResponse(aiResponse);
            chatHistory.setTimestamp(LocalDateTime.now());
            chatHistoryRepository.save(chatHistory);

            // Yanıtı hazırla
            ChatResponse response = new ChatResponse();
            response.setId(chatHistory.getId());
            response.setUserMessage(message);
            response.setAiResponse(aiResponse);
            response.setTimestamp(chatHistory.getTimestamp());
            response.setStatus("success");

            return response;
        } catch (Exception e) {
            ChatResponse errorResponse = new ChatResponse();
            errorResponse.setStatus("error");
            errorResponse.setError("AI servisi ile iletişim kurulamadı: " + e.getMessage());
            return errorResponse;
        }
    }

    public List<ChatHistory> getUserChatHistory(Long userId) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new RuntimeException("Kullanıcı bulunamadı"));
        return chatHistoryRepository.findByUserOrderByTimestampDesc(user);
    }
} 
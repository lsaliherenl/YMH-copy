package com.melihawci.springrestapi.service;

import com.melihawci.springrestapi.model.ChatHistory;
import com.melihawci.springrestapi.model.User;
import com.melihawci.springrestapi.repository.ChatHistoryRepository;
import com.melihawci.springrestapi.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;

@Service
public class ChatService {

    @Autowired
    private ChatHistoryRepository chatHistoryRepository;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private AIService aiService;

    public ChatHistory processMessage(String message, Long userId) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new RuntimeException("Kullanıcı bulunamadı"));

        // Yapay zekadan yanıt al
        String aiResponse = aiService.getAIResponse(message);

        // Sohbet geçmişini kaydet
        ChatHistory chatHistory = new ChatHistory();
        chatHistory.setUser(user);
        chatHistory.setUserMessage(message);
        chatHistory.setAiResponse(aiResponse);
        chatHistory.setTimestamp(LocalDateTime.now());

        return chatHistoryRepository.save(chatHistory);
    }

    public List<ChatHistory> getUserChatHistory(Long userId) {
        User user = userRepository.findById(userId)
                .orElseThrow(() -> new RuntimeException("Kullanıcı bulunamadı"));
        return chatHistoryRepository.findByUserOrderByTimestampDesc(user);
    }
} 
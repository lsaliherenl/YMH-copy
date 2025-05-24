package com.melihawci.springrestapi.controller;

import com.melihawci.springrestapi.dto.ChatRequest;
import com.melihawci.springrestapi.dto.ChatResponse;
import com.melihawci.springrestapi.model.ChatHistory;
import com.melihawci.springrestapi.service.ChatService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/chat")
@CrossOrigin(origins = "http://localhost:5500")
public class ChatController {

    @Autowired
    private ChatService chatService;

    @PostMapping("/send")
    public ResponseEntity<ChatResponse> sendMessage(@RequestBody ChatRequest request) {
        try {
            ChatHistory chatHistory = chatService.processMessage(request.getMessage(), request.getUserId());
            
            ChatResponse response = new ChatResponse();
            response.setId(chatHistory.getId());
            response.setUserMessage(chatHistory.getUserMessage());
            response.setAiResponse(chatHistory.getAiResponse());
            response.setTimestamp(chatHistory.getTimestamp());
            response.setStatus("success");
            
            return ResponseEntity.ok(response);
        } catch (RuntimeException e) {
            ChatResponse response = new ChatResponse();
            response.setStatus("error");
            response.setError(e.getMessage());
            return ResponseEntity.badRequest().body(response);
        }
    }

    @GetMapping("/history/{userId}")
    public ResponseEntity<?> getChatHistory(@PathVariable Long userId) {
        try {
            List<ChatHistory> history = chatService.getUserChatHistory(userId);
            List<ChatResponse> responses = history.stream()
                .map(chat -> {
                    ChatResponse response = new ChatResponse();
                    response.setId(chat.getId());
                    response.setUserMessage(chat.getUserMessage());
                    response.setAiResponse(chat.getAiResponse());
                    response.setTimestamp(chat.getTimestamp());
                    response.setStatus("success");
                    return response;
                })
                .collect(Collectors.toList());
            
            return ResponseEntity.ok(responses);
        } catch (RuntimeException e) {
            ChatResponse response = new ChatResponse();
            response.setStatus("error");
            response.setError(e.getMessage());
            return ResponseEntity.badRequest().body(response);
        }
    }
} 
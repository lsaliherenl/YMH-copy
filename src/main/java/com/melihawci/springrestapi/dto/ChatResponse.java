package com.melihawci.springrestapi.dto;

import lombok.Data;
import java.time.LocalDateTime;

@Data
public class ChatResponse {
    private Long id;
    private String userMessage;
    private String aiResponse;
    private LocalDateTime timestamp;
    private String status;
    private String error;
} 
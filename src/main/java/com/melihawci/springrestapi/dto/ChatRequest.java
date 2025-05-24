package com.melihawci.springrestapi.dto;

import lombok.Data;

@Data
public class ChatRequest {
    private String message;
    private Long userId;
} 
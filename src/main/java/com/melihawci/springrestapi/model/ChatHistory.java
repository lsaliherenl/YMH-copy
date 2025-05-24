package com.melihawci.springrestapi.model;

import jakarta.persistence.*;
import lombok.Data;
import java.time.LocalDateTime;

@Data
@Entity
@Table(name = "chat_history")
public class ChatHistory {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne
    @JoinColumn(name = "user_id", nullable = false)
    private User user;

    @Column(nullable = false)
    private String userMessage;

    @Column(nullable = false)
    private String aiResponse;

    @Column(nullable = false)
    private LocalDateTime timestamp;
} 
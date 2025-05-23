package com.melihawci.springrestapi.controller;

import com.melihawci.springrestapi.model.QuestionAnswer;
import com.melihawci.springrestapi.service.AIService;
import com.melihawci.springrestapi.repository.QuestionAnswerRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.List;

@RestController
@RequestMapping("/api/ai")
@CrossOrigin(origins = "*") // Frontend'den gelen isteklere izin ver
public class AIController {

    @Autowired
    private AIService aiService;
    
    @Autowired
    private QuestionAnswerRepository questionAnswerRepository;

    @PostMapping("/ask")
    public ResponseEntity<QuestionAnswer> askQuestion(@RequestBody String question) {
        // Yapay zekadan cevap al
        String answer = aiService.getAnswer(question);
        
        // Soru ve cevabı kaydet
        QuestionAnswer qa = new QuestionAnswer();
        qa.setQuestion(question);
        qa.setAnswer(answer);
        questionAnswerRepository.save(qa);
        
        return ResponseEntity.ok(qa);
    }

    @GetMapping("/history")
    public ResponseEntity<List<QuestionAnswer>> getHistory() {
        return ResponseEntity.ok(questionAnswerRepository.findAllByOrderByTimestampDesc());
    }
} 
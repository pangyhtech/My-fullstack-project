# EC Customer Support AI Agent

<img src="../projectimage/ECCustomersupportAIAgent_v1.0.0.png" width="600" />

An intelligent customer service AI system for e-commerce platforms, featuring hybrid RAG architecture and advanced sentiment analysis.

---

## Core Algorithms

### 1. Knowledge Base Construction
- **Data Synthesis**: Extracts structured product data from 50+ dialogue CSV files
- **JSON Schema**: Organizes 24 product categories with specs, prices, and Q&A pairs
- **Entity Extraction**: Uses regex patterns to parse attributes (price, weight, size, chemicals)

### 2. Dual-Brain RAG Architecture

**Left Brain (Factual Retrieval)**
- Exact matching for product specifications
- Fuzzy Q&A matching using `difflib.SequenceMatcher`
- 100% accuracy for price and spec queries

**Right Brain (Deep Reasoning)**
- TuckER-based Knowledge Graph completion
- Latent semantic associations
- Provides supplementary insights labeled as "AI Inference"

### 3. Sentiment Analysis Engine
- **Model**: Fine-tuned XLM-RoBERTa with Focal Loss
- **Hybrid Logic**:
  - Rule-based overrides for objective queries
  - Strong negative/positive keyword detection
  - Confidence-based fallback mechanism
- **Output**: Dissatisfied / Neutral / Satisfied classification

### 4. Algorithm Optimization
- **False Positive Reduction**: Objective safety net prevents misclassification of neutral queries
- **Class Imbalance Handling**: Focal Loss addresses skewed training data
- **Latency Optimization**: Structured JSON lookup for instant retrieval

---

## Tech Stack
- **Backend**: Flask, PyTorch, Transformers
- **Models**: XLM-RoBERTa, TuckER (Knowledge Graph)
- **Frontend**: JavaScript, Professional E-commerce UI

## Quick Start
```bash
cd monotaro-qa-system
python3 app.py
```

Access at: **http://localhost:8080**

## Features
- Real-time sentiment monitoring
- Structured product knowledge base
- Hybrid RAG + reasoning system
- Professional e-commerce interface
- Dynamic category/product selection

## Architecture Highlights
- **Layer 1**: Knowledge Retrieval (RAG)
- **Layer 2**: Sentiment & Satisfaction Analysis
- **Layer 3**: Flask Backend + Dynamic Frontend
- **Layer 4**: Knowledge Graph Reasoning (TuckER)

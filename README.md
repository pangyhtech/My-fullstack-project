# My Full-Stack Projects

A collection of AI-powered full-stack development projects showcasing modern technologies and rapid development methodologies.

---

## Projects

### EC Customer Support AI Agent
<img src="projectimage/ECCustomersupportAIAgent_v1.0.0.png" width="400" />

An experimental customer service AI system for industrial B2B e-commerce research, featuring sentiment analysis and hybrid RAG architecture. This academic project represents a complete reproduction and optimization of the CoRe-USE model, achieving 73% accuracy in customer satisfaction prediction through innovative techniques including XLM-RoBERTa fine-tuning, Focal Loss optimization, and dynamic data augmentation.

The system integrates a dual-brain architecture: the "Left Brain" provides factual product information through structured knowledge base retrieval, while the "Right Brain" leverages TuckER-based knowledge graph reasoning for semantic understanding. The sentiment analysis engine employs a hybrid approach combining rule-based logic with deep learning, successfully handling class imbalance through Focal Loss (γ=2.0) and achieving significant performance improvements: 488% increase in F1-score and 30x improvement in minority class recall compared to baseline.

Built on synthetic data generated from simulated industrial product catalogs, the system includes 24 product categories with 480 virtual products and 63 semantic relations, demonstrating domain-specific knowledge engineering techniques. The dynamic dialogue generation system ensures training data diversity through Gaussian distribution sampling and SHA256 deduplication, while multi-language support (Japanese/English/Chinese) simulates real-world scenarios.

**Note**: This is an experimental research project using synthetic data, not a production system.

**Tech:** PyTorch, XLM-RoBERTa (270M), TuckER, Flask, Focal Loss  
**Core:** Synthetic Industrial KG, Dual-Brain RAG, Sentiment Analysis, Data Augmentation  
**Performance:** 73% Accuracy, 73.73% F1-Score, 96% F1 for Critical Class

[View Details](ECCustomersupportAIAgent_v1.0.0/)

---

### MBTI Consulting Assistant
<img src="projectimage/MBTI Consulting Assistant1.png" width="400" />

AI-powered MBTI personality consulting assistant built with LangChain.

**Tech:** LangChain, TypeScript, Node.js

[View Details](Base%20on%20langchain%20-MBTI%20Consulting%20Assistant_JP/) | [Article](https://qiita.com/houikkei/items/3bc9a090201f6d80b655)

---

### SweetsPro - iOS E-Commerce App
<img src="projectimage/sweetpro.png" width="400" />

Full-featured iOS shopping app developed in 6 hours with AI assistance.

**Tech:** SwiftUI, Python, MVVM  
**Stats:** 30+ screens, 5000+ lines of code, 6 hours development

[View Details](sweetspro_v1.0.0/) | [Article 1](https://qiita.com/pangyhtech/items/2eba0d74682d22d2f19c) | [Article 2](https://qiita.com/pangyhtech/items/cbfe0c193d54e585c391)

# Veronica: Multi-Modal Academic AI Assistant

Veronica is a locally-hosted, multi-modal AI assistant engineered to bridge physical desktop automation with advanced Retrieval-Augmented Generation (RAG). 

Designed specifically as an autonomous research assistant, this architecture accelerates complex academic workflows—particularly in the mathematical modeling of viscous fluid flow in porous media, Darcy's Law, Brinkman equations, and GATE Data Science & AI preparation. It allows the user to interact via natural voice commands, automate UI interactions, and instantly query highly technical PDF documents through semantic vector search.

## 🧠 System Architecture

The project utilizes a split-environment design to isolate heavy local machine learning tasks from lightweight desktop automation logic:

1. **Local Audio Pipeline:** Uses `faster-whisper` and `kokoro` for blazing-fast local speech-to-text and text-to-speech, completely detached from cloud latency.
2. **Orchestration & RAG (n8n):** The core intelligence runs on a local native n8n instance. It utilizes:
   - **Google Gemini 2.5 Flash** as the primary decision-making agent.
   - **Qdrant Vector Database** (768 dimensions) for semantic memory storage and instantaneous technical document retrieval.
   - **Hugging Face Inference** for high-efficiency document embeddings.
3. **Desktop Automation & Perception:** - **Vision (`veronica_perception.py`):** Captures desktop states directly into a RAM buffer (avoiding SSD read/write overhead) and leverages the `llama-3.2-11b-vision-preview` model via Groq to calculate precise UI coordinate geometry.
   - **Execution (`veronica_hands.py`):** A lightweight Python macro engine that physicalizes the AI's commands on the host machine with built-in failsafe protocols.

## 📂 Repository Structure

* `veronica_ears.py`: Local microphone listener and transcription engine. Routes commands to the n8n webhook.
* `veronica_hands.py`: Executes UI/Keyboard automation based on agentic payloads.
* `veronica_perception.py`: Computer vision logic for real-time screen analysis.
* `veronica_n8n_workflow.json`: The complete agentic logic, RAG pipeline, document chunking configuration, and tool layout.

## 🚀 Setup & Installation

### 1. Python Environment Setup
Due to specific C++ binary requirements for local audio processing, an Anaconda environment is recommended to prevent library conflicts:
```bash
pip install -r requirements.txt
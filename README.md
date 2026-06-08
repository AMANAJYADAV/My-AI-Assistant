# Veronica: Multi-Modal Academic AI Assistant

![Python](https://img.shields.io/badge/Python-3.14%2B-blue?style=flat-square&logo=python)
![n8n](https://img.shields.io/badge/n8n-Orchestration-FF6D5A?style=flat-square&logo=n8n)
![Groq](https://img.shields.io/badge/Groq-LPU_Inference-f55036?style=flat-square)
![Qdrant](https://img.shields.io/badge/Qdrant-Vector_DB-1E1E2E?style=flat-square)
![Windows 11](https://img.shields.io/badge/OS-Windows_11-0078D4?style=flat-square&logo=windows)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

Veronica is a locally-hosted, multi-modal autonomous agent engineered to bridge physical desktop automation with advanced Retrieval-Augmented Generation (RAG). 

Built specifically as a research and study assistant, this architecture accelerates complex academic workflows—particularly in the mathematical modeling of fluid dynamics (viscous fluid flow in porous media, Darcy's Law, Brinkman equations) and GATE Data Science & AI preparation. 

> **Environment & OS Compatibility Note:** This project was natively developed, optimized, and rigorously tested on **Windows 11** using an **Anaconda Python environment**. Because Veronica requires deep, low-level hardware access (microphone processing via `sounddevice` and physical desktop UI control via `pyautogui`), it is not cross-platform out of the box. Users deploying on macOS or Linux distributions will need to manually configure OS-specific audio libraries and ensure environment parity.

---

## Core Architecture: The "Senses"

Veronica operates using a split-environment design, isolating heavy local machine learning tasks from lightweight desktop execution:

*   **Ears (Local Audio):** Blazing-fast local speech-to-text and text-to-speech utilizing `faster-whisper` and `kokoro` inside a dedicated Anaconda environment, completely bypassing cloud latency.
*   **Eyes (Computer Vision):** Captures desktop states directly into a RAM buffer (preserving SSD lifespan). Uses `llama-3.2-11b-vision-preview` via Groq to calculate precise UI coordinate geometry for screen interaction.
*   **Hands (Desktop Automation):** A lightweight Python macro engine (`pyautogui`) that physicalizes the AI's commands on the host OS to launch applications, navigate browsers, and execute native typing.
*   **Brain (Orchestration & Memory):** A local n8n instance routing logic to **Google Gemini 2.5 Flash**. It utilizes a **Qdrant** vector database and **Hugging Face** embeddings to instantly retrieve technical textbook chunks and research paper data.

---

## Repository Layout

| File | Description |
| :--- | :--- |
| `veronica_ears.py` | The continuous local wake-word listener and transcription router. |
| `veronica_perception.py` | Vision logic for real-time, memory-efficient screen analysis. |
| `veronica_hands.py` | Executes physical UI/Keyboard automation based on agent payloads. |
| `veronica_n8n_workflow.json` | The complete n8n agentic logic, RAG pipeline, and tool configuration. |

---

## Quick Start Setup

### 1. Python Environment
Due to specific C++ binary requirements for local audio processing, use an Anaconda environment. Note that `numpy` is strictly pinned to prevent binary incompatibility with older transformer wheels.
```bash
pip install -r requirements.txt

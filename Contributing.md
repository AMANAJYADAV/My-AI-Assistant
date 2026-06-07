# Contributing to Veronica AI

First off, thank you for considering contributing to Veronica! This project is designed to push the boundaries of local AI orchestration, and community help is essential to making it better.

## How Can I Contribute?

### 1. Tackle the Roadmap (High Priority)
We are actively looking for help with:
* **OCR Integration:** Building a custom n8n node or Python middleware to automatically scan and extract text from image-based PDFs before they hit the vector database.
* **Mac/Linux Support:** Currently, the `veronica_hands.py` module relies heavily on Windows `start` commands. We need help expanding the OS logic to natively support macOS and Linux environments.
* **Memory Management:** Optimizing the RAM buffer logic inside `veronica_perception.py` for lower-end machines.

### 2. Report Bugs
If you find a bug (e.g., the mouse macro gets stuck, or the audio loop drops out), please open an Issue on GitHub with:
1. Your OS and Python version.
2. The error traceback from the terminal.
3. Steps to reproduce the bug.

### 3. Submit a Pull Request (PR)
If you wrote code to fix a bug or add a feature:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Make your changes and test them locally using the n8n webhook.
4. Commit your changes (`git commit -m "Add custom OCR processing script"`).
5. Push to the branch (`git push origin feature/your-feature-name`).
6. Open a Pull Request!

## Development Setup
Please refer to the `README.md` for instructions on setting up the Anaconda environment, the pinned NumPy version (`1.26.4`), and importing the n8n JSON workflow.

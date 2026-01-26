## Project Overview

main.py:

This project is an automated GitHub repository analysis tool powered by a large language model.

It retrieves the source code of a public GitHub repository, filters out irrelevant or oversized files, and compiles the remaining code into a structured prompt. This prompt is then sent to a Groq-hosted LLM, which analyzes the codebase and generates a summary of the project’s architecture, evaluates overall code quality and documentation, and provides specific recommendations for improvement.

The tool is intended for quick technical reviews, learning from open-source projects, and gaining high-level insights into unfamiliar codebases.


gemini_main.py:

A simple tool that generates a **guided onboarding guide** for any GitHub repository.

You enter a repo (`owner/repo`), and the tool analyzes the README and project structure to explain what the project does, how it’s organized, and where to start as a new developer.

Runs in **Google Colab** with a simple web UI.

---

## Features

- Fetches README and repo structure from GitHub
- Identifies important files and folders automatically
- Uses Gemini to generate a developer-friendly tour
- Simple Gradio-based UI
- Secure API key handling with Colab Secrets

---

## How to Use (Google Colab)

1. Open the notebook in **Google Colab**
2. Add a secret named `GEMINI_API_KEY`  
   *(optional)* add `GITHUB_TOKEN` to avoid GitHub rate limits
3. Run the notebook cell
4. Enter a GitHub repository: owner/repo
5. Click **Generate Tour**

---

## Tech Stack

- Python
- Google Gemini API
- GitHub API
- Gradio
- Google Colab

---

## Output

The tool produces a Markdown-formatted **Guided Developer Tour** that includes:
- Project overview
- Architecture summary
- Key files and directories
- First steps for contributors

---

   

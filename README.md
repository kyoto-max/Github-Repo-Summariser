## Project Overview

This project is an automated GitHub repository analysis tool powered by a large language model.

It retrieves the source code of a public GitHub repository, filters out irrelevant or oversized files, and compiles the remaining code into a structured prompt. This prompt is then sent to a Groq-hosted LLM, which analyzes the codebase and generates a summary of the project’s architecture, evaluates overall code quality and documentation, and provides specific recommendations for improvement.

The tool is intended for quick technical reviews, learning from open-source projects, and gaining high-level insights into unfamiliar codebases.

# AI Musicology GPT

This project aims to automate the extraction of conversation sessions from raw logs and transform them into reusable prompt modules. The extracted modules can be combined with GPT configuration data to replicate or extend an interactive musicology assistant.

## Goal

The primary goal is to capture chat sessions, parse them into coherent segments, and package them alongside relevant GPT settings. This will make it easier to reproduce discussions, fine-tune assistants, or build reference corpora for future research.

## Prerequisites

- **Python 3.11+**
- `pip` for managing dependencies
- Recommended: a virtual environment such as `venv` or `conda`

### Required Python packages

```
pip install openai pyyaml
```

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourname/ai-musicology-gpt.git
   cd ai-musicology-gpt
   ```
2. Install dependencies as shown above.

## Basic Usage

After installing the dependencies, you can run the session extractor to parse log files. A minimal example:

```bash
python scripts/extract.py --input data/session.log --output prompts/
```

This command parses `session.log` and writes individual prompt modules into the `prompts/` directory.

## Architecture Overview

1. **Session Capture** – Conversation logs are stored as plain text or JSON. Each turn is timestamped and attributed to the speaker.
2. **Parsing** – A parser reads the logs and groups related exchanges into modules. Heuristics or tags define the module boundaries.
3. **Packaging** – Each module is saved alongside relevant GPT configuration (e.g., temperature, max tokens) so it can be replayed or fine-tuned later.

The roadmap includes improving the parser accuracy, adding a web interface for managing modules, and providing utilities for batch processing of large archives.


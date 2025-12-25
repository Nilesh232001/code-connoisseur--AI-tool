# Code Connoisseur (Python Port)

Code Connoisseur is an AI-assisted code review agent designed for Python developers. This repository contains a Python project, providing intelligent code indexing, diff analysis, static analysis, optional AI embeddings, and a lightweight CLI for comprehensive code reviews.

> For reference, a comparison with commercial tools is available in [COMPARISON.md].

## Features

- **Context-aware Reviews** — Analyzes files and directories with understanding of surrounding codebase context
- **Static Code Analysis** — Python AST-based issue detection; optional ESLint integration for JavaScript/TypeScript
- **Symbol & Dependency Extraction** — Automatically identifies functions, classes, imports, and dependencies
- **Semantic Embeddings** — OpenAI embeddings (optional) with local fallback for intelligent code similarity matching
- **Diff-based Analysis** — Compare file versions to provide targeted, change-focused feedback
- **Feedback Persistence** — Store and track review feedback in `.code-connoisseur/feedback.json` for continuous improvement
- **Lightweight & Extensible** — Clean Python codebase with simple integration points for customization

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git (for cloning the repository)

### Step 1: Set Up Virtual Environment

Create and activate a virtual environment (recommended):

```bash
# Create a virtual environment
python -m venv .venv

# Activate on Windows (PowerShell)
.\.venv\Scripts\Activate.ps1

# Activate on Windows (Command Prompt)
.\.venv\Scripts\activate

# Activate on macOS / Linux
source .venv/bin/activate
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure API Keys (Optional)

To use OpenAI embeddings and AI-powered features, create a `.env` file in the project root:

```bash
touch .env  # or create .env file manually
```

Add your API key:

```
OPENAI_API_KEY=sk-your_openai_api_key_here
```

Get your API key from [OpenAI Platform](https://platform.openai.com/api-keys).

> **Note**: Without an OpenAI API key, Code Connoisseur uses a local fallback for embeddings. AI-powered review features require the API key.

### Step 4: Verify Installation

Test the installation:

```bash
python index.py
```

You should see the help message with available commands.

## Quick Start

### Index Your Project

First, index your codebase to create metadata and embeddings:

```bash
python index.py index -d .
```

This creates a `.code-connoisseur` directory containing:
```
.code-connoisseur/
  ├── vectors/           # Embedding metadata for indexed files
  ├── feedback.json      # Review feedback history
  └── config.json        # Configuration settings
```

### Review a File

Review a single file:

```bash
python index.py review src/myfile.py
```

### Review with Diff

Compare a new version against an old version:

```bash
python index.py review src/myfile.py -o src/myfile.py.old
```

### Review a Directory

Review all Python files in a directory:

```bash
python index.py review src/
```

### View Feedback Summary

See feedback and insights from past reviews:

```bash
python index.py feedback
```

## CLI Commands

### `index` — Index Your Codebase

Index files in a directory to create metadata for analysis:

```bash
python index.py index -d .
```

**Options:**
- `-d, --directory <path>` — Directory to index (default: current directory)

**Output:**
Creates `.code-connoisseur/vectors/` with embedding metadata for each indexed file.

### `review` — Review Files or Directories

Analyze code and provide feedback:

```bash
# Review a single file
python index.py review src/mymodule.py

# Review a directory
python index.py review src/

# Review with diff comparison
python index.py review src/mymodule.py -o src/mymodule.py.old
```

**Options:**
- `<path>` — File or directory to review (required)
- `-o, --old <path>` — Path to previous version for diff comparison
- `--root <dir>` — Project root for dependency analysis

**Output:**
Prints analysis results including:
- Identified symbols (functions, classes)
- Detected issues
- Dependency information
- Similarity results from vector search

### `feedback` — View Review Feedback

Display feedback summary and statistics:

```bash
python index.py feedback
```

**Output:**
Shows stored feedback from past reviews, helping you understand patterns in code quality.

### `configure` — Configuration Guide

Display configuration guidance:

```bash
python index.py configure
```

## Usage Examples

### Example 1: Basic File Review

Review a single Python file:

```bash
python index.py review myapp/utils.py
```

### Example 2: Diff Analysis

Compare changes between two versions:

```bash
python index.py review myapp/models.py -o myapp/models.py.bak
```

The tool will show:
- Added/removed/modified lines
- Impact on related code
- Potential issues in changes

### Example 3: Directory Review

Review multiple files with context:

```bash
python index.py review src/ --root .
```

Uses the root directory for better dependency analysis.

### Example 4: Workflow with Git

Review uncommitted changes:

```bash
# Stage changes
git add myfile.py

# Get the original from git
git show HEAD:myfile.py > myfile.py.orig

# Review the changes
python index.py review myfile.py -o myfile.py.orig

# Clean up
rm myfile.py.orig
```

## How It Works

### Indexing Process

1. Scans specified directory for Python and JavaScript/TypeScript files
2. Parses each file to extract symbols (functions, classes, imports)
3. Generates embeddings (OpenAI or local fallback)
4. Stores metadata in `.code-connoisseur/vectors/`

### Review Process

1. **Diff Analysis**: Compares old vs. new versions (if provided)
2. **Symbol Extraction**: Identifies functions, classes, dependencies
3. **Static Analysis**: Checks for code quality issues
4. **Semantic Search**: Finds similar code in the indexed codebase
5. **Results**: Returns structured analysis for further processing or display

## Project Architecture

### Core Modules

| Module | Purpose |
|--------|---------|
| [src/cli.py](src/cli.py) | Command-line interface and argument parsing |
| [src/agent.py](src/agent.py) | `ReviewAgent` orchestrates analysis and reviews |
| [src/codeParser.py](src/codeParser.py) | Regex-based JS/TS symbol extraction |
| [src/pythonParser.py](src/pythonParser.py) | Python AST-based symbol extractor |
| [src/tsParser.py](src/tsParser.py) | TypeScript parsing wrapper |
| [src/diffAnalyzer.py](src/diffAnalyzer.py) | File diff analysis using `difflib` |
| [src/codeAnalyzer.py](src/codeAnalyzer.py) | Static analysis and issue detection |
| [src/vectorStore.py](src/vectorStore.py) | OpenAI embeddings with local fallback |
| [src/feedbackSystem.py](src/feedbackSystem.py) | Feedback storage and analysis |

### Data Flow

```
User Input (CLI)
    ↓
ReviewAgent (orchestration)
    ├→ DiffAnalyzer (compare versions)
    ├→ CodeAnalyzer (static analysis)
    ├→ PythonParser/CodeParser (extract symbols)
    ├→ VectorStore (embeddings & search)
    └→ FeedbackSystem (store results)
    ↓
Structured Output (JSON/Console)
```

## Configuration

### Environment Variables

Add to `.env` file in the project root:

```bash
# OpenAI API key for embeddings and LLM features
OPENAI_API_KEY=sk-your_key_here

# Optional: Set logging level
LOG_LEVEL=INFO
```

### Directory Structure

Code Connoisseur creates and uses:

```
.code-connoisseur/
├── config.json              # Configuration metadata
├── feedback.json            # Stored review feedback
└── vectors/                 # Embedding data
    └── {filename}.json      # Per-file embeddings
```

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'openai'`

**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```

### Issue: OPENAI_API_KEY not recognized

**Solution**: Ensure `.env` file exists in the project root with proper formatting:
```bash
OPENAI_API_KEY=sk-...
```

Then verify it's loaded:
```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print(os.getenv('OPENAI_API_KEY'))"
```

### Issue: `Permission denied` on Windows PowerShell

**Solution**: Allow script execution:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then run:
```powershell
.\.venv\Scripts\Activate.ps1
```

### Issue: No `eslint` found for JavaScript analysis

**Solution**: Install ESLint globally or locally:
```bash
npm install -g eslint
# or locally
npm install --save-dev eslint
```

Code Connoisseur will auto-detect and use it if available.

## Limitations & Known Issues

- **JavaScript/TypeScript Parsing**: Uses regex-based heuristics, not a full AST parser. For production use, consider integrating tree-sitter or esprima
- **No Managed Vector DB**: Index files stored locally under `.code-connoisseur/vectors/`. For large codebases, consider FAISS or Pinecone integration
- **ESLint Optional**: Static analysis requires manual ESLint installation for JavaScript files
- **Python Only**: This port focuses on Python; the original Node.js version has broader stack support

## Development & Contributing

### Project Structure

```
code-connoisseur/
├── index.py              # CLI entry point
├── requirements.txt      # Python dependencies
├── .env.example          # Example configuration
├── README.md             # This file
└── src/
    ├── cli.py
    ├── agent.py
    ├── codeParser.py
    ├── pythonParser.py
    ├── tsParser.py
    ├── diffAnalyzer.py
    ├── codeAnalyzer.py
    ├── vectorStore.py
    └── feedbackSystem.py
```

### Adding New Features

To extend Code Connoisseur:

1. Add functionality to appropriate module in `src/`
2. Update `src/cli.py` to expose CLI commands
3. Test with sample Python and JavaScript files
4. Submit a PR with tests and documentation

### Running in Development

```bash
# Activate virtual environment
source .venv/bin/activate  # or .\.venv\Scripts\Activate.ps1 on Windows

# Run with debugging
python index.py review --help

# Run tests (if available)
python -m pytest tests/
```

## Roadmap & Next Steps

Potential improvements:

- ✅ Python AST-based parsing (complete)
- 🔄 LLM-driven natural language reviews (in progress)
- 🎯 Robust JS/TS AST parsing (tree-sitter integration)
- 🎯 Vector DB backends (FAISS, Pinecone, Weaviate)
- 🎯 GitHub integration for automated reviews
- 🎯 Review history and trends dashboard
- 🎯 Custom linting rules configuration
- 🎯 Test generation suggestions

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: Open a GitHub issue for bugs or feature requests
- **Questions**: Start a discussion in the repository
- **Contributions**: PRs welcome! Please include tests and documentation

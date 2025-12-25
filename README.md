<<<<<<< HEAD
# Code Connoisseur (Python Port)

Code Connoisseur is an AI-assisted code review agent designed for Python developers. This repository contains a Python port of the original Node.js project, providing intelligent code indexing, diff analysis, static analysis, optional AI embeddings, and a lightweight CLI for comprehensive code reviews.

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
=======
# Code Connoisseur

Code Connoisseur is an AI-powered code review agent built for multiple technology stacks, including MEAN/MERN, Java, and Python. It uses state-of-the-art language models (LLMs) to analyze your code changes and provide actionable, stack-specific feedback.

> **Want to know how Code Connoisseur compares to commercial tools?** See our [detailed comparison](COMPARISON.md) with leading code review tools like CodeRabbit, DeepCode, Codiga, and Bito.

## Features

- **Context-aware Reviews**: Understands your entire codebase, not just the changed files
- **Static Code Analysis**: Uses ESLint to catch syntax errors and potential bugs
- **Dependency Analysis**: Identifies files affected by changes
- **Test Coverage Estimation**: Suggests areas that need testing
- **Edge Case Detection**: Recommends edge cases to test based on code patterns
- **Multiple LLM Support**: Use OpenAI's GPT-4 or Anthropic's Claude models
- **Memory System**: Remembers past interactions to provide more consistent feedback
- **Advanced Feedback Loop**: Continuously improves through user feedback and analysis
- **Few-Shot Learning**: Uses examples of successful reviews to improve quality

## Installation

### Option 1: NPM Installation (Recommended)

Install Code Connoisseur globally via npm:

```bash
npm install -g code-connoisseur
```

If you encounter permission errors, you can either:

1. Use sudo (quick but not recommended for security):
   ```bash
   sudo npm install -g code-connoisseur
   ```

2. Configure npm to use a different directory (recommended):
   ```bash
   mkdir -p ~/.npm-global
   npm config set prefix '~/.npm-global'
   export PATH=~/.npm-global/bin:$PATH
   ```
   Add the export line to your .bashrc or .zshrc file to make it permanent.

After installation, the setup wizard will guide you through configuring your API keys. You'll need:
- OpenAI API key from [OpenAI](https://platform.openai.com/)
- Anthropic API key from [Anthropic](https://console.anthropic.com/)
- (Optional) Pinecone API key from [Pinecone](https://app.pinecone.io/)

You can reconfigure at any time by running:
```bash
code-connoisseur setup
```

### Option 2: Manual Installation

If you prefer to install from source:

1. Clone the repository:
   ```bash
   git clone https://github.com/Nilesh232001/code-connoisseur--AI-tool.git
   cd code-connoisseur
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create a `.env` file in the project directory:
   ```bash
   cp .env.example .env
   ```

4. Add your API keys to the `.env` file:
   ```
   OPENAI_API_KEY=your_openai_key_here
   ANTHROPIC_API_KEY=your_anthropic_key_here
   PINECONE_API_KEY=your_pinecone_key_here  # Optional
   ```

5. Make the CLI tool globally available:
   ```bash
   npm link
   ```

## Usage

### Indexing Your Codebase

Before you can use Code Connoisseur, you need to index your codebase:

```
code-connoisseur index
```

Options (all are optional):
- `--directory, -d <path>`: Path to your project (default: current directory)
- `--index-name, -i <name>`: Name for the vector database index (default: code-connoisseur)
- `--extensions, -e <list>`: File extensions to index as comma-separated list (default: js,ts,jsx,tsx,py)
- `--exclude, -x <list>`: Directories to exclude as comma-separated list (default: node_modules,dist,build,.git)
- `--js-only`: Only index JavaScript files (shortcut for -e js,jsx,ts,tsx)
- `--py-only`: Only index Python files (shortcut for -e py)
- `--java-only`: Only index Java files (shortcut for -e java)

All configuration and index data will be stored in a `.code-connoisseur` directory within your project:

```
.code-connoisseur/
  ├── config.json        # Configuration settings
  ├── feedback.json      # User feedback history
  ├── metadata/          # Additional metadata
  └── vectors/           # Vector embeddings for your codebase
```

### Reviewing Code Changes

To review changes in a file:

```
code-connoisseur review <path to file/directory>
```

Options:
- `--old, -o <path>`: Path to the previous version of the file (if not in git)
- `--llm, -l <provider>`: LLM provider to use (openai or anthropic)
- `--index-name, -i <name>`: Name of the index to use for review
- `--root, -r <dir>`: Project root directory for dependency analysis
- `--stack, -s <stack>`: Specify the technology stack (MEAN/MERN, Java, Python)
- `--directory, -d`: Review an entire directory of files
- `--extensions, -e <list>`: File extensions to include when reviewing directories
- `--markdown, -m <file>`: Save review to a markdown file (specify output path)
- `--max-files <number>`: Maximum number of files to review in a directory (default: 10)
- `--diff`: Only show changes in the review (compact mode)
- `--verbose, -v`: Show detailed output during the review process

### Analyzing Feedback

To view feedback statistics and analysis:

```
code-connoisseur feedback
```

This will show you statistics about past reviews, common issues, and suggested prompt improvements based on your feedback.

### Configuration

To configure Code Connoisseur:

```
code-connoisseur configure
```

This will launch an interactive prompt to set your preferences.

### Managing Indexed Codebases

To list all available indexed codebases:

```
code-connoisseur list
```

To clean up indexed files:

```
code-connoisseur clean [options]
```

Options:
- `--index-name, -i <name>`: Name of the index to remove
- `--all`: Remove all indexed data and configuration
- `--confirm`: Skip confirmation prompt (defaults to requiring confirmation)

### Global Options

These options can be used with any command:

```
code-connoisseur [command] [options]
```

- `--version`: Show the current version of Code Connoisseur
- `--verbose, -v`: Enable verbose output with detailed logging
- `--debug-env`: Display environment variable information for debugging

## How It Works

1. **Indexing**: Code Connoisseur parses your codebase, splits it into chunks, and stores embeddings in a vector database (Pinecone).
2. **Diff Analysis**: When reviewing, it analyzes the differences between old and new versions of a file.
3. **Static Analysis**: It checks for code quality issues using ESLint.
4. **Dependency Analysis**: It identifies which files depend on the changed file and which files it depends on.
5. **Test Coverage**: It estimates test coverage and identifies untested changes.
6. **Edge Case Detection**: It suggests edge cases to test based on the code patterns.
7. **Relevant Context**: It retrieves relevant context from the codebase based on the changes.
8. **Enhanced Prompt**: It builds a customized prompt based on feedback history and exemplars.
9. **AI Review**: It uses a language model to analyze all the information and generate comprehensive feedback.
10. **Feedback Collection**: User feedback is collected and analyzed to improve future reviews.
11. **Continuous Learning**: The system adapts to feedback by refining its prompts and approach.

### Implementation Details

Code Connoisseur is built with several components:

1. **Code Parser** (`src/codeParser.js`):
   - Uses `esprima` to parse JavaScript/TypeScript code into AST
   - Extracts functions, classes, and other structures
   - Handles error recovery for parsing issues

2. **Vector Store** (`src/vectorStore.js`):
   - Generates embeddings using OpenAI's text-embedding-ada-002 model
   - Stores embeddings in Pinecone for fast retrieval
   - Provides semantic search capabilities for finding relevant code

3. **Diff Analyzer** (`src/diffAnalyzer.js`):
   - Uses the `diff` library to compare code versions
   - Identifies added, removed, and modified lines
   - Provides detailed statistics about changes
   - Detects potential risks (e.g., commented code, console statements)

4. **Code Analyzer** (`src/codeAnalyzer.js`):
   - Performs static code analysis using ESLint
   - Analyzes dependencies using Madge
   - Estimates test coverage for changed code
   - Suggests edge cases based on code patterns

5. **Feedback System** (`src/feedbackSystem.js`):
   - Collects and stores user feedback on reviews
   - Analyzes feedback to identify common issues
   - Suggests prompt improvements based on patterns
   - Provides exemplars of good reviews for few-shot learning

6. **Code Review Agent** (`src/agent.js`):
   - Uses LangChain with OpenAI or Anthropic models
   - Integrates all analysis tools into a comprehensive review
   - Remembers past reviews through conversation memory
   - Adapts to feedback with improved prompts
   - Provides comprehensive, actionable feedback

7. **CLI Interface** (`src/cli.js`):
   - Provides a user-friendly interface with commands for indexing, reviewing, and analysis
   - Handles configuration management and API key validation
   - Facilitates the feedback loop for continuous improvement

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
#   c o d e - c o n n o i s s e u r - - A I - t o o l 
 

 

>>>>>>> e290d453a551ab34e23f0290698a5bc1bcb8a00c

# AutoCommit

AutoCommit is a local CLI tool that generates concise commit messages by analyzing `git diff` output using AI models like Ollama's Llama.

## Features

- **Local AI-Powered**: Generates commit messages locally without external dependencies.
- **Secure & Offline**: Operates entirely on your system, ensuring data privacy.
- **Easy Integration**: Simple command-line tool to streamline your commit process.

## Installation

1. **Clone the Repo**:
   ```bash
   git clone https://github.com/yourusername/AutoCommit.git
   cd AutoCommit
   ```
2. **Install Dependencies**:
   ```bash
   pip install ollama
   ```

## Usage

Run AutoCommit with:
```bash
python main.py
```
The tool will:
- Capture `git diff` output.
- Generate a commit message using the local AI model.

## Error Handling

- **Model Auto-Pull**: Pulls the model if not available.
- **Detailed Errors**: Provides clear messages for troubleshooting.

## License

Licensed under the MIT License.

---

# AutoCommit
AutoCommit is a CLI tool that locally creates concise commit messages by analyzing code changes with AI models such as Ollama's Llama.


## Features

- **Local AI-Powered**: Generates commit messages locally without external dependencies.
- **Editable Commit Messages**: Generated commit messages can be reviewed and edited as needed.
- **Secure & Offline**: Operates entirely on your system, ensuring data privacy.
- **Easy Integration**: Simple command-line tool to streamline your commit process.

## Status

This tool is currently under development. Stay tuned for updates!

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

Licensed under the Apache License 2.0. See the LICENSE file for more details.


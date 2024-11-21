![2](https://github.com/user-attachments/assets/d1a4c15e-8bdf-448b-adc0-4a0c39a3a023)

A lightweight CLI tool that automatically generates meaningful commit messages using small, efficient AI models locally. AutoCommitt leverages Ollama's Llama 3.2:3B model to create concise, context-aware commit messages while keeping resource usage minimal.

<div align="center">

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![PyPI version v0.1.6](https://badge.fury.io/py/autocommitt.svg)](https://badge.fury.io/py/autocommitt)

</div>

## ✨ Features

- **Local AI-Powered**: Generates commit messages using a small 3B parameter Llama 3.2 model
- **Flexible Editing**: Review and edit generated messages before committing
- **Privacy-First**: All operations performed locally, ensuring data privacy
- **Git Integration**: Seamlessly works with your existing Git workflow
- **Resource-Efficient**: Minimal computational overhead with lightweight AI model

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Git installed and configured
- Minimum 8GB RAM recommended

### Installation

```bash
pip install autocommitt
```
Get the latest updated llama 3.2 (3 billion) model
```bash
ollama pull llama3.2:3b
```

### Usage

1. Start the Ollama server:
   ```bash
   autocommitt start
   ```

2. Generate and edit commit message:
   ```bash
   autocommitt gen
   ```
   This will generate a commit message based on your changes using the Llama 3.2:3B model. Edit it if needed.

3. Press Enter to commit your changes.

   **Note:** When you're done generating commit messages, be sure to stop the Ollama server by running:
   ```bash
   autocommitt stop
   ```

That's it! 🎉

## 🔜 Roadmap

- **Git Hooks Integration**: Compatible with pre-commit hooks
- **Cross-Platform Support**: Enhanced compatibility for Windows, macOS, and Linux
- **Custom Templates**: Support for user-defined commit message templates
- **Interactive Mode**: Enhanced CLI interface for improved user experience
- **Multiple Language Model Support**: Option to choose different local AI models

## 🐛 Support

- Found a bug? [Open an issue](https://github.com/Spartan-71/AutoCommitt/issues)
- Have questions? [Start a discussion](https://github.com/Spartan-71/AutoCommitt/discussions)
- Want to contribute? Check out our [Contributing Guidelines](CONTRIBUTING.md)

## 📊 Project Status

- [x] Basic commit message generation
- [x] Local AI model integration (Llama 3.2:3B)
- [x] Python package release
- [ ] Cross-platform testing
- [ ] Interactive mode
- [ ] Custom template support
- [ ] Multi-model support

## 📄 License

Licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 👩‍💻 For Developers

Interested in contributing to AutoCommitt? We'd love your help! Check out our [Contributing Guidelines](CONTRIBUTING.md) for:

- Setting up the development environment
- Building from source
- Pull request process
- Development roadmap

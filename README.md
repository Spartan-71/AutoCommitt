![2](https://github.com/user-attachments/assets/d1a4c15e-8bdf-448b-adc0-4a0c39a3a023)

A lightweight CLI tool that automatically generates meaningful commit messages using small, efficient AI models locally. AutoCommitt leverages Ollama to create concise, context-aware commit messages while keeping resource usage minimal.

<div align="center">

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/autocommitt.svg)](https://badge.fury.io/py/autocommitt)

</div>

## Features

- **Local AI-Powered**: Generates commit messages using a small LLM models locally
- **Flexible Editing**: Review and edit generated messages before committing
- **Git Integration**: Seamlessly works with your existing Git workflow
- **Resource-Efficient**: Minimal computational overhead with lightweight LLM models
- **Multiple Language Model Support**: Option to choose different local AI models


### Prerequisites

- **Python 3.10** or higher
- **Git** installed and configured
- **RAM**:  
   - 8GB for smaller models (3B)  
   - 16GB for optimal performance
- **GPU** (Optional): Boosts performance, but not required
  
### Installation

> It is recommended to use virtual environment.
 
```bash
pip install autocommitt
```
OR
```bash
uv pip install autocommitt
```
### Upgrading
> If u already have autocommitt installed, then make sure to upgrade to latest version.

```bash
pip install -U autocommitt
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
   This will generate a commit message based on your changes using the Llama 3.2:3B model (default). Edit it if needed.

3. Press Enter to commit your changes.

   **Note:** When you're done generating commit messages, be sure to stop the Ollama server by running:
   ```bash
   autocommitt stop
   ```

That's it! :)

## Roadmap

- **Interactive Mode**: Enhanced CLI interface for improved user experience
- **Cross-Platform Support**: Enhanced compatibility for Windows and macOS.
- **Custom Templates**: Support for user-defined commit message templates
- **Git Hooks Integration**: Compatible with pre-commit hooks

## Project Status

- [x] Basic commit message generation
- [x] Local AI model integration
- [x] Python package release
- [x] Multi-model support
- [ ] Interactive mode
- [ ] Cross-platform testing
- [ ] Custom template support

## How It Works
It runs the `git diff --staged` command to gather all staged changes and processes them using a local LLM (default: `llama3.2:3b` provided by Ollama). The model analyzes the changes and generates a concise, context-aware commit message, ensuring privacy and avoiding external API dependencies.  


## Contributing
We welcome contributions to this project! Whether you'd like to report a bug, fix an existing issue, or implement a new feature, check out the [Issues](https://github.com/Spartan-71/AutoCommitt/issues) page to get started. Be sure to review our [Contribution Guide](CONTRIBUTING.md) for detailed instructions on how to set up, test, and contribute to the project.

For discussions, questions, or real-time collaboration, join our [Gitter community](https://matrix.to/#/#autocommitt:gitter.im) Your contributions and ideas are greatly appreciated! 🚀


![2](https://github.com/user-attachments/assets/7bc5a948-2477-4827-bae7-5af8dcf73769)

A lightweight CLI tool that automatically generates meaningful commit messages using small, efficient AI models locally. AutoCommitt leverages Ollama's Llama model (3B parameters) to create concise, context-aware commit messages while keeping resource usage minimal.

<div align="center">

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/autocommitt.svg)](https://badge.fury.io/py/autocommitt)

</div>

## ✨ Features

- **Local AI-Powered**: Generates commit messages using a small 3B parameter model
- **Flexible Editing**: Review and edit generated messages before committing
- **Privacy-First**: All operations performed locally, ensuring data privacy
- **Git Integration**: Seamlessly works with your existing Git workflow

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Git installed and configured
- Ollama installed locally
- Minimum 8GB RAM

### Installation
```bash
pip install autocommitt
```

### Usage
Just three simple steps:
1. Stage your files:
   ```bash
   git add your_file_name
   ```

2. Generate and edit commit message:
   ```bash
   ac
   ```
   This will generate a commit message based on your changes. Edit it if needed.

3. Press Enter to commit your changes.

That's it! 🎉

## 🔜 Coming Soon

- **Git hooks integration**: Compatible with all pre-commit hooks
- **Cross-Platform**: Enhanced support for Windows, macOS, and Linux
- **Custom Templates**: Support for user-defined commit message templates
- **Interactive Mode**: Enhanced CLI interface for better user experience

## 🐛 Need Help?

- Found a bug? [Open an issue](https://github.com/Spartan-71/AutoCommitt/issues)
- Have questions? [Check our discussions](https://github.com/Spartan-71/AutoCommitt/discussions)
- Want to contribute? Check out our [Contributing Guidelines](CONTRIBUTING.md)

## 📊 Project Status

- [x] Basic commit message generation
- [x] Local AI model integration (3B parameters)
- [x] Python package release
- [ ] Cross-platform testing
- [ ] Interactive mode
- [ ] Custom template support

## 📄 License

Licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

---
### 👩‍💻 For Developers

Interested in contributing to AutoCommitt? We'd love your help! Check out our [Contributing Guidelines](CONTRIBUTING.md) for:
- Setting up the development environment
- Building from source
- Pull request process
- Development roadmap
- Code style guidelines

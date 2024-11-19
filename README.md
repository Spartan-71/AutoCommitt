![2](https://github.com/user-attachments/assets/17718ea3-c71b-410f-bfa7-b6e219580baa)

AutoCommitt is a lightweight CLI tool that automatically generates meaningful commit messages using small, efficient AI models locally. It leverages Ollama's Llama model (3B parameters) to create concise, context-aware commit messages while keeping resource usage minimal.

<div align="center">

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)

</div>



## ✨ Features

- **Local AI-Powered**: Generates commit messages using a small 3B parameter model
- **Resource Efficient**: Minimal RAM and CPU usage with optimized model size
- **Privacy-First**: All operations performed locally, ensuring data privacy
- **Flexible Editing**: Review and edit generated messages before committing
- **Git Integration**: Seamlessly works with your existing Git workflow

## 🚀 Coming Soon

- **Git hooks integration**: Compatible with all pre-commit hooks
- **Cross-Platform**: Support for Windows, macOS, and Linux

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Git installed and configured
- Ollama installed locally
- Minimum 8GB RAM

### Steps

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/AutoCommit.git
   cd AutoCommit
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify Installation**
   ```bash
   python -m autocommitt --version
   ```

## 📖 Usage

```bash
python main.py
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please read our [Contributing Guidelines](CONTRIBUTING.md) for more details.

## 📊 Project Status

Current Version: 0.1.0 (Alpha)

- [x] Basic commit message generation
- [x] Local AI model integration (3B parameters)
- [x] Python package release
- [ ] Cross-platform testing
- [ ] Interactive mode
- [ ] Custom template support

## 📄 License

Licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

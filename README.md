![2](https://github.com/user-attachments/assets/d1a4c15e-8bdf-448b-adc0-4a0c39a3a023)

A lightweight CLI tool that automatically generates meaningful commit messages using small, efficient AI models locally. AutoCommitt leverages Ollama to create concise, context-aware commit messages while keeping resource usage minimal.

<div align="center">

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/autocommitt.svg)](https://badge.fury.io/py/autocommitt)
![PyPI Downloads](https://static.pepy.tech/badge/autocommitt)

</div>

## Features

- **Local AI-Powered**: Generates commit messages using a small LLM models locally
- **Flexible Editing**: Review and edit generated messages before committing
- **Git Integration**: Seamlessly works with your existing Git workflow
- **Multiple Language Model Support**: Option to choose different local AI models

## Setup
### Prerequisites

- **RAM** (minimum):  
   - 8GB for smaller models (<=3B parameters)  
   - 16GB for optimal performance
- **GPU** (Optional): Boosts performance, but not required
  
### Installation

It is recommended to use a virtual environment.

```bash
pip install autocommitt
```

### Upgrading
Check the installed version with:
```bash
pip list | grep autocommitt
```

If it's not [latest](https://github.com/Spartan-71/AutoCommitt/releases/), make sure to upgrade.

```bash
pip install -U autocommitt
```

## Basic Usage

**1. Start the Ollama server:**
   ```bash
   autocommitt start
   ```

**2. Stage the changes:**
   ```bash
   git add <files..>
   ```

**3. Generate and edit commit message:**
   ```bash
   autocommitt gen
   ```

**4. Stop the Ollama server** 
   ```bash
   autocommitt stop
   ```

## Additional Commands

By default, **AutoCommitt** uses the `llama3.2:3b` model to generate commit messages.

#### 1. Using a Custom Model

- To view the list of available models, run the following command:
   ```bash
   autocommitt list
   ```
- To select and set a model as active:
   ```bash
   autocommitt use <model_name>
   ```
   > **Note**: If the model is not already downloaded, this command will pull the model by running `ollama pull <model_name>` and set it as the default.

#### 2. Deleting a Model

```bash
autocommitt rm <model_name>
```
> **Note**: Since models require a significant amount of memory (minimum 2GB), it is recommended to use only one model and delete the rest to free up space.



## How It Works
It runs the `git diff --staged` command to gather all staged changes and processes them using a local LLM (default: `llama3.2:3b` provided by Ollama). The model analyzes the changes and generates a concise, context-aware commit message, ensuring privacy and avoiding external API dependencies.  

## Future Enhancements
- **Cross-Platform Support**: Compatibility for Windows.
- **Git Hooks Integration**: Compatible with pre-commit hooks
- **Custom Templates**: Support for user-defined commit message templates

## Contributing
We welcome contributions to this project! Whether you'd like to report a bug, fix an existing issue, or implement a new feature, check out the [Issues](https://github.com/Spartan-71/AutoCommitt/issues) page to get started. Be sure to review our [Contribution Guide](CONTRIBUTING.md) for detailed instructions on how to set up, test, and contribute to the project.

For discussions, questions, or real-time collaboration, join our [Gitter community](https://matrix.to/#/#autocommitt:gitter.im) Your contributions and ideas are greatly appreciated!

## Acknowledgments

We would like to express our gratitude to the following open-source projects that made AutoCommitt possible:

- [Ollama](https://ollama.ai/) - An impressive project that makes running large language models locally both possible and practical. Their API and model management system are integral to AutoCommitt's local AI capabilities.
- [Typer](https://typer.tiangolo.com/) - Created by [Sebastián Ramírez](https://github.com/tiangolo), the same author of FastAPI. Typer provides an elegant CLI builder that forms the backbone of our command-line interface.


Special thanks to the maintainers and contributors of these projects for their fantastic work in making developer tools more accessible and powerful.

---

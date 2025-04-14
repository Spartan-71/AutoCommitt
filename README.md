![new_banner](https://github.com/user-attachments/assets/4f867876-3651-4cc7-9cf1-a136c44b73ec)

<div align="center">

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![PyPI version](https://badge.fury.io/py/autocommitt.svg)](https://badge.fury.io/py/autocommitt)
![PyPI Downloads](https://static.pepy.tech/badge/autocommitt)

AutoCommit is a FOSS **AI-powered CLI tool** that generates context-aware commit messages locally.



</div>

## Features

- **Local AI-Powered**: Generates commit messages using a small LLM models locally
- **Flexible Editing**: Review and edit generated messages before committing
- **Git Integration**: Seamlessly works with your existing Git workflow
- **Multiple Language Model Support**: Option to choose different local AI models

## Setup
### Prerequisites

- **Ollama**: Download and install ollama from [offical website](https://ollama.com/download).
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

1. **Stage Your Changes**
   Stage the files you want to commit using Git:
   ```bash
   git add <files...>
   ```

2. **Generate and Edit Commit Messages**
   Generate a commit message based on your staged changes:
   ```bash
   act gen
   ```

   - The tool generates a message and allows you to review and edit it before committing.

   - To **automatically push** the commit to the remote repository, use the `-p` or `--push` flag:
     ```bash
     act gen -p
     ```

## Additional Commands

By default, **AutoCommitt** uses the `deepseek-r1:1.5b` model to generate commit messages.

#### 1. Using a Custom Model

- To view the list of available models, run the following command:
   ```bash
   act list
   ```
- To select and set a model as active:
   ```bash
   act use <model_name>
   ```
   > **Note**: If the model is not already downloaded, this command will pull the model by running `ollama pull <model_name>` and set it as the default.

#### 2. Deleting a Model

```bash
act rm <model_name>
```

#### 3. Viewing Commit History

Easily view recent commit messages using the `his` command:

```bash
act his -n 5
```
- **Flag Description**:`-n` or `--limit`: (Optional) Specify the number of recent commit messages to retrieve. If omitted, all commit messages will be displayed.

## Future Enhancements
- **Cross-Platform Support**: Compatibility for MacOS.
- **Git Hooks Integration**: Compatible with pre-commit hooks
- **Custom Templates**: Support for user-defined commit message templates

## Contributing

We welcome contributions! To report bugs, fix issues, or add features, visit the [Issues](https://github.com/Spartan-71/AutoCommitt/issues) page. Please review our [Contribution Guide](CONTRIBUTING.md) for setup and contribution instructions.


## Acknowledgments

We would like to express our gratitude to the following open-source projects that made AutoCommitt possible:


- [Ollama](https://ollama.ai/) - Enables local AI with large language models.
- [Typer](https://typer.tiangolo.com/) - A CLI builder by [Sebastián Ramírez](https://github.com/tiangolo), powering our command-line interface.

Special thanks to the maintainers and contributors for their outstanding work!

---

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

1. **Start the Ollama Server**  
Launch the Ollama server to activate model-based commit message generation.
   ```bash
   autocommitt start
   ```

2. **Stage Your Changes**  
   Stage the files you want to commit using Git:  
   ```bash
   git add <files...>
   ```

3. **Generate and Edit Commit Messages**  
   Generate a commit message based on your staged changes:  
   ```bash
   autocommitt gen
   ```  

   - The tool generates a message and allows you to review and edit it before committing.  

   - To **automatically push** the commit to the remote repository, use the `-p` or `--push` flag:  
     ```bash
     autocommitt gen -p
     ```  

   > **Pro Tip**: Save time by using the `--push` flag to combine committing and pushing into a single step.

4. **Stop the Ollama Server**  
   Once you're done, stop the Ollama server to free up resources:  
   ```bash
   autocommitt stop
   ```

>**Note**: You can use the `ac` alias for `autocommitt` throughout, making commands shorter and quicker to type!


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



#### 3. Viewing Commit History

Easily view recent commit messages using the `his` command:

```bash
autocommitt his -n 5
```
- **Flag Description**:`-n` or `--limit`: (Optional) Specify the number of recent commit messages to retrieve. If omitted, all commit messages will be displayed.

> **Pro Tip**: Use this command to quickly review your project's recent changes before generating new commit messages.

## How It Works
It runs the `git diff --staged` command to gather all staged changes and processes them using a local LLM (default: `llama3.2:3b` provided by Ollama). The model analyzes the changes and generates a concise, context-aware commit message, ensuring privacy and avoiding external API dependencies.  

## Future Enhancements
- **Cross-Platform Support**: Compatibility for Windows.
- **Git Hooks Integration**: Compatible with pre-commit hooks
- **Custom Templates**: Support for user-defined commit message templates

## Contributing

We welcome contributions! To report bugs, fix issues, or add features, visit the [Issues](https://github.com/Spartan-71/AutoCommitt/issues) page. Please review our [Contribution Guide](CONTRIBUTING.md) for setup and contribution instructions.

For discussions or real-time collaboration, join our [Gitter community](https://matrix.to/#/#autocommitt:gitter.im). Your contributions are appreciated!

## Acknowledgments

We would like to express our gratitude to the following open-source projects that made AutoCommitt possible:


- [Ollama](https://ollama.ai/) - Enables local AI with large language models.
- [Typer](https://typer.tiangolo.com/) - A CLI builder by [Sebastián Ramírez](https://github.com/tiangolo), powering our command-line interface.

Special thanks to the maintainers and contributors for their outstanding work!

---

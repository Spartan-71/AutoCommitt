# cli.py
import os
import json
import typer
import signal
import subprocess
from rich import box
from enum import Enum
from pathlib import Path
from rich.text import Text
from rich.theme import Theme
from rich.table import Table
from rich.panel import Panel
from rich.console import Console
from typing import Optional, Dict

from .main import ollama_ai

# ASCII art banner
BANNER = """
╭────────────────── AutoCommitt ───────────────────╮
│            ⚡ AI-Powered Git Commits ⚡          │
│         Generated Locally, Commit Globally       │
╰──────────────────────────────────────────────────╯
"""


app = typer.Typer()
console = Console()

# Constants
CONFIG_DIR = os.path.expanduser("~/.autocommitt")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
MODELS_FILE = os.path.join(CONFIG_DIR, "models.json")

DEFAULT_MODELS = {
    "llama-3.2:1b": {
        "description": "Lightweight model good for simple commits",
        "size":"1.3GB",
        "status":"disabled",
        "downloaded":"no"
    },
    "gemma2:2b": {
        "description":"Improved lightweight model", 
        "size":"1.6GB",
        "status": "disabled",
        "downloaded":"no"

    },
    "llama-3.2:3b": {
        "description":"Good quality for complex changes",
        "size":"2.0GB",
        "status":"disabled",
        "downloaded":"no"
 
    },
    "llama-3.1:8b": {
        "description":"Best quality for complex changes" ,
        "size":"4.7GB",
        "status": "disabled",
        "downloaded":"no"

    }
}

# class CommitType(str, Enum):
#     FEAT = "feat"
#     FIX = "fix"
#     DOCS = "docs"
#     STYLE = "style"
#     REFACTOR = "refactor"
#     TEST = "test"
#     CHORE = "chore"

def ensure_config():
    """Ensure config directory and files exist"""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    
    # Initialize config file if it doesn't exist
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w') as f:
            json.dump({"model": "llama3.2:3b"}, f)
    
    # Initialize models file if it doesn't exist
    if not os.path.exists(MODELS_FILE):
        with open(MODELS_FILE, 'w') as f:
            json.dump(DEFAULT_MODELS, f)

def get_config() -> Dict:
    """Get current configuration"""
    ensure_config()
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def get_models() -> Dict:
    """Get available models"""
    ensure_config()
    with open(MODELS_FILE, 'r') as f:
        return json.load(f)

def save_config(config: Dict):
    """Save configuration"""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)

def save_models(models: Dict):
    """Save models configuration"""
    with open(MODELS_FILE, 'w') as f:
        json.dump(models, f, indent=2)

@app.command()
def run():
    """Starts ollama app/server in the background"""
    console.print(Text(BANNER,justify="center"))
    try:
        process = subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
            # On Windows, you might want to use creationflags=subprocess.DETACHED_PROCESS
            # creationflags=subprocess.DETACHED_PROCESS if os.name == 'nt' else 0
        )
        with open(f"{CONFIG_DIR}/ollama_server.pid", "w") as pid_file:
            pid_file.write(str(process.pid))

        console.print("[green]Ollama server started successfully in the background![/green]")
        # console.print(f"[blue]Process ID (PID): {process.pid}[/blue]")
        return process    
    except FileNotFoundError:
        console.print("[red]Error: Ollama is not installed or not in PATH[/red]")
    except Exception as e:
        console.print(f"[red]Failed to start Ollama server: {e}[/red]")

@app.command()
def kill():
    """Stops the running ollama server."""
    try:
        # Read the PID from the file
        with open(f"{CONFIG_DIR}/ollama_server.pid", "r") as pid_file:
            pid = int(pid_file.read().strip())
        
        # Send the SIGTERM signal to terminate the process
        os.kill(pid, signal.SIGTERM)
        console.print("[green]Ollama server stopped successfully.[/green]")
        
        # Optionally, delete the PID file
        os.remove(f"{CONFIG_DIR}/ollama_server.pid")
    except FileNotFoundError:
        console.print("[red]No running Ollama server found (PID file missing).[/red]")
    except ProcessLookupError:
        console.print("[yellow]Process not found. It may have already stopped.[/yellow]")
    except Exception as e:
        console.print(f"[red]Failed to stop Ollama server: {e}[/red]")




@app.command()
def rm(
    model_name: str = typer.Argument(..., help="Name of the model to remove")
):
    """Remove a model from available models"""
    models = get_models()
    config = get_config()
    
    # Check if model exists
    if model_name not in models:
        console.print(f"[red]Error: Model '{model_name}' not found[/red]")
        raise typer.Exit(1)
    
    # Check if it's a default model
    if models[model_name].get('status')=="active":
        console.print(f"[red]Error: Cannot remove currently selected model[/red]")
        console.print("Please switch to another model first using 'use' command")
        raise typer.Exit(1)
    
    # Remove the model
    del models[model_name]
    save_models(models)
    console.print(f"[green]Successfully removed model: {model_name}[/green]")

@app.command()
def use(
    model_name: str = typer.Argument(..., help="Name of the model to use")
):
    """Select which model to use for generating commit messages"""
    models = get_models()
    
    if model_name not in models:
        console.print(f"[red]Error: Unknown model '{model_name}'[/red]")
        console.print("\nAvailable models:")
        list()
        raise typer.Exit(1)

    models = get_models()
    config = get_config()
    desc = models[model_name]
    desc["status"] ="active"
    config['model'] = model_name
    save_config(config)
    save_models(models)
    console.print(f"[green]Successfully switched to model: {model_name}[/green]")
    # console.print(f"Description: {models[model_name]['description']}")

@app.command()
def gen(
    type: CommitType = typer.Option(CommitType.FEAT, "--type", "-t", help="Type of commit"),
    edit: bool = typer.Option(False, "--edit", "-e", help="Edit commit message before committing"),
    push: bool = typer.Option(False, "--push", "-p", help="Push changes after commit"),
):
    """Generate and create a commit with an AI-generated message"""
    try:
        repo = Repo('.')
    except:
        console.print("[red]Error: Not a git repository[/red]")
        raise typer.Exit(1)

    # Get current changes
    # changed_files = []
    # for item in repo.index.diff(None):
    #     changed_files.append(item.a_path)
    # for item in repo.untracked_files:
    #     changed_files.append(item)

    changed_files = check_staged_changes()

    if not changed_files:
        console.print("[yellow]No stagged changes to commit[/yellow]")
        raise typer.Exit(1)

    # Get selected model
    config = get_config()
    models = get_models()
    model = config['model']
    
    console.print(f"Using model: [cyan]{model}[/cyan] ({models[model]['name']})")

    # Here you would integrate with your LLM to generate the message
    message = generate_commit_message(changed_files)
    edit = True

    if edit:
        message = typer.edit(message)
        if message is None:
            console.print("[yellow]Commit aborted[/yellow]")
            raise typer.Exit(1)

    
    # Create commit
    perform_git_commit(final_message)
    console.print(f"[green]Created commit: {message}[/green]")

    # if push:
    #     origin = repo.remote('origin')
    #     origin.push()
    #     console.print("[green]Successfully pushed changes[/green]")

# @app.command()
# def history(
#     limit: int = typer.Option(10, "--limit", "-n", help="Number of commits to show")
# ):
#     """View commit history"""
#     try:
#         repo = Repo('.')
#     except:
#         console.print("[red]Error: Not a git repository[/red]")
#         raise typer.Exit(1)

#     table = Table(title=f"Last {limit} Commits")
#     table.add_column("Hash", style="cyan")
#     table.add_column("Date", style="magenta")
#     table.add_column("Author", style="green")
#     table.add_column("Message", style="white")

#     for commit in list(repo.iter_commits('HEAD', max_count=limit)):
#         table.add_row(
#             commit.hexsha[:7],
#             commit.committed_datetime.strftime('%Y-%m-%d %H:%M'),
#             commit.author.name,
#             commit.message.split('\n')[0]
#         )

#     console.print(table)

if __name__ == "__main__":
    app()
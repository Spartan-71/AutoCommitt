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

from autocommitt.main import ollama_ai

# ASCII art banner
BANNER = """
╭────────────────── AutoCommitt ───────────────────╮
│            ⚡ AI-Powered Git Commits ⚡          │
│         Generated Locally, Commit Globally       │
╰──────────────────────────────────────────────────╯
"""

BANNER_1 = """
╭────────────────── AutoCommitt ──────────────────╮
│          Local AI Models Are Resting 😴         │
│                  See You Soon! 🚀               │
╰─────────────────────────────────────────────────╯
"""


app = typer.Typer()
console = Console()

# Constants
CONFIG_DIR = os.path.expanduser("~/.autocommitt")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
MODELS_FILE = os.path.join(CONFIG_DIR, "models.json")

DEFAULT_MODELS = {
    "llama3.2:1b": {
        "description": "Lightweight model good for simple commits",
        "size":"1.3GB",
        "status":"comming soon",
        "downloaded":"no"
    },
    "gemma2:2b": {
        "description":"Improved lightweight model", 
        "size":"1.6GB",
        "status": "comming soon",
        "downloaded":"no"

    },
    "llama3.2:3b": {
        "description":"Good quality for complex changes",
        "size":"2.0GB",
        "status":"active",
        "downloaded":"no"
 
    },
    "llama3.1:8b": {
        "description":"Best quality for complex changes" ,
        "size":"4.7GB",
        "status": "comming soon",
        "downloaded":"no"

    }
}

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
def start():
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
        ensure_config()
        with open(f"{CONFIG_DIR}/ollama_server.pid", "w") as pid_file:
            pid_file.write(str(process.pid))

        console.print("[green]Ollama server started successfully in the background![/green]")
        # console.print(f"[blue]Process ID (PID): {process.pid}[/blue]")
        return process   

    except FileNotFoundError:
        console.print("[red]Error: Ollama is not installed or not in PATH[/red]")

    except Exception as e:
        console.print("[red]Error: Ollama is not installed or not in PATH[/red]")
        console.print(f"[red]Failed to start Ollama server: {e}[/red]")

@app.command()
def stop():
    """Stops the running ollama server."""
    try:
        # Read the PID from the file
        with open(f"{CONFIG_DIR}/ollama_server.pid", "r") as pid_file:
            pid = int(pid_file.read().strip())
        
        # Send the SIGTERM signal to terminate the process
        os.kill(pid, signal.SIGTERM)
        console.print(Text(BANNER_1,justify="center"))
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
def gen():
    """Generate a commit msg, edit it and press ENTER to commit."""

    changed_files = ollama_ai.check_staged_changes()

    if not changed_files:
        console.print("[yellow]No stagged changes to commit[/yellow]")
        raise typer.Exit(1)

    # Get selected model
    # config = get_config()
    # models = get_models()
    # model = config['model']

    ollama_ai.model_name="llama3.2:3b"
    console.print(f"[cyan]Generating...[/cyan]")

    # Here you would integrate with your LLM to generate the message
    initial_message = ollama_ai.generate_commit_message(changed_files)
    final_message = ollama_ai.edit_commit_message(initial_message)

    if final_message is None:
        console.print("[yellow]Commit aborted[/yellow]")
        raise typer.Exit(1)

    
    # Create commit
    done :bool = ollama_ai.perform_git_commit(final_message)
    if done:
        console.print(f"[green]Commit Sucessfull![/green]")
    else:
        console.print(f"[red]Commit FAILED![/green]")


    # if push:
    #     origin = repo.remote('origin')
    #     origin.push()
    #     console.print("[green]Successfully pushed changes[/green]")

if __name__ == "__main__":
    app()
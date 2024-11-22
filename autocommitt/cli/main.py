# cli.py
import os
import time
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

from autocommitt.core.commit_manager import CommitManager
from autocommitt.core.ollama_manager import OllamaManager
from autocommitt.utils.config_manager import ConfigManager

app = typer.Typer()
console = Console()



@app.command()
def start() -> Optional[subprocess.Popen]:
    """
    Starts ollama server in the background and ensures the default model is available.
    
    Returns:
        Optional[subprocess.Popen]: Process object if server starts successfully, None otherwise
    """
    BANNER = """
    ╭────────────────── AutoCommitt ───────────────────╮
    │            ⚡ AI-Powered Git Commits ⚡          │
    │         Generated Locally, Commit Globally       │
    ╰──────────────────────────────────────────────────╯
    """
    console = Console()
    console.print(Text(BANNER, justify="center"))
    
    # Ensure configuration is set up
    ConfigManager.ensure_config()

    try:
        # First check if server is already running
        if OllamaManager.check_server_health():
            console.print("[yellow]Ollama server is already running![/yellow]")
            return None

        # Start the server
        process = subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
            creationflags=subprocess.DETACHED_PROCESS if os.name == 'nt' else 0
        )
        
        # Wait a bit for server to initialize
        time.sleep(1)
        
        # Save PID
        with open(f"{ConfigManager.CONFIG_DIR}/ollama_server.pid", "w") as pid_file:
            pid_file.write(str(process.pid))

        
        console.print("[green]Ollama server started successfully![/green]")

        # Check server health
        # max_retries = 3
        # retry_count = 0
        # while retry_count < max_retries:
        #     if ollama_cmd.check_server_health():
        #         break
        #     time.sleep(2)
        #     retry_count += 1
        
        # if retry_count == max_retries:
        #     console.print("[red]Warning: Server started but may not be responding correctly[/red]")
        #     return None

        # Check and pull default model
        model_name = "llama3.2:3b"  # Make sure this matches your default model name
        console.print(f"[blue]Checking for default model {model_name}...[/blue]")
        
        if not OllamaManager.is_model_present(model_name):
            console.print(f"[yellow]Default model {model_name} not found. Pulling...[/yellow]")
            if not OllamaManager.pull_model(model_name):
                console.print("[red]Failed to pull default model. Please check your internet connection[/red]")
                return process
        else:
            console.print(f"[green]Default model {model_name} is ready![/green]")

        return process

    except FileNotFoundError:
        console.print("[red]Error: Ollama is not installed or not in PATH[/red]")
        console.print("[yellow]Please install Ollama following the instructions at: https://ollama.ai[/yellow]")
        return None

    except Exception as e:
        console.print(f"[red]Failed to start Ollama server: {str(e)}[/red]")
        return None


@app.command()
def stop():
    """Stops the running ollama server."""

    BANNER = """
    ╭────────────────── AutoCommitt ──────────────────╮
    │          Local AI Models Are Resting 😴         │
    │                  See You Soon! 🚀               │
    ╰─────────────────────────────────────────────────╯
    """
    models = ConfigManager.get_models()
    config = ConfigManager.get_config()

    try:
        # Read the PID from the file
        with open(f"{ConfigManager.CONFIG_DIR}/ollama_server.pid", "r") as pid_file:
            pid = int(pid_file.read().strip())
        
        # Send the SIGTERM signal to terminate the process
        os.kill(pid, signal.SIGTERM)

        # update the table
        active_model = config["model_name"]
        models[active_model]["status"]="disabled"

        ConfigManager.save_config(config)
        ConfigManager.save_models(models)

        # Delete the config and PID file
        os.remove(ConfigManager.CONFIG_FILE)
        os.remove(f"{ConfigManager.CONFIG_DIR}/ollama_server.pid")

        console.print(Text(BANNER,justify="center"))
        console.print("[green]Ollama server stopped successfully.[/green]")
        
    except FileNotFoundError:
        console.print("[red]No running Ollama server found (PID file missing).[/red]")
    except ProcessLookupError:
        console.print("[yellow]Process not found. It may have already stopped.[/yellow]")
    except Exception as e:
        console.print(f"[red]Failed to stop Ollama server: {e}[/red]")

@app.command()
def gen():
    """Generate a commit msg, edit it and press ENTER to commit."""

    changed_files = CommitManager.check_staged_changes()

    if not changed_files:
        console.print("[yellow]No stagged changes to commit[/yellow]")
        raise typer.Exit(1)

    # Get selected model
    config = ConfigManager.get_config()
    models = ConfigManager.get_models()

    CommitManager.model_name = config['model_name']
    console.print(f"[cyan]Generating...[/cyan]")

    # Here you would integrate with your LLM to generate the message
    initial_message = CommitManager.generate_commit_message(changed_files)
    final_message = CommitManager.edit_commit_message(initial_message)

    if final_message is None:
        console.print("[yellow]Commit aborted[/yellow]")
        raise typer.Exit(1)

    
    # Create commit
    done :bool = CommitManager.perform_git_commit(final_message)
    if done:
        console.print(f"[green]Commit Sucessfull![/green]")
    else:
        console.print(f"[red]Commit FAILED![/green]")


    # if push:
    #     origin = repo.remote('origin')
    #     origin.push()
    #     console.print("[green]Successfully pushed changes[/green]")
    

@app.command()
def list():
    """List all available LLM models for commit message generation"""
    ConfigManager.ensure_config()   

    models = ConfigManager.get_models()
    config = ConfigManager.get_config()
    
    table = Table(title="Available Models")
    table.add_column("Name", style="cyan")
    table.add_column("Description", style="white")
    table.add_column("Size", style="yellow")
    table.add_column("Status", style="red")
    table.add_column("Downloaded",style="red")
    
    for model_name, details in models.items():
        # Enhanced status styling with icons and colors
        if OllamaManager.is_model_present(model_name) or details["downloaded"]=="yes":
            details["downloaded"]="yes"
            downloaded_style = "[bright_green]yes[/bright_green]"
        else:
            downloaded_style = "[red]no[/red]"
            
        if model_name == config['model_name']:
            status_style = "[bright_green]active[/bright_green]"
            model_name_style = f"[bold cyan]{model_name}[/bold cyan]"

        else:
            status_style = "[red]disabled[/red]"
            model_name_style = f"[cyan]{model_name}[/cyan]"
        
        table.add_row(
            model_name_style,
            details['description'],
            details['size'],
            status_style,
            downloaded_style
        )
    
    ConfigManager.save_models(models)
    console.print(table)


if __name__ == "__main__":
    app()
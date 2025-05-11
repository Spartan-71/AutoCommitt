import os
import time
import typer
import shutil
import subprocess
from rich.text import Text
from rich.table import Table
from rich.panel import Panel
from rich.console import Console
from typing import Optional

from autocommitt.core.commit_manager import CommitManager
from autocommitt.core.ollama_manager import OllamaManager
from autocommitt.utils.config_manager import ConfigManager

app = typer.Typer()
console = Console()


@app.command()
def start():
    """
    Starts ollama server and ensures the default LLM model is available.

    Returns:
        Optional[subprocess.Popen]: Process object if server starts successfully, None otherwise
    """
    BANNER = """
    ╭────────────────── AutoCommitt ───────────────────╮
    │            ⚡ AI-Powered Git Commits ⚡          │
    │         Generated Locally, Commit Globally       │
    ╰──────────────────────────────────────────────────╯
    """
    console.print(Text(BANNER, justify="center"))

    # Ensure configuration is set up
    ConfigManager.ensure_config()

    if shutil.which("ollama") is None:
        console.print("[red]Error: Ollama is not installed or not in PATH[/red]")
        console.print(
            "Please install Ollama following the instructions at: [cyan]https://ollama.ai/download[/cyan]"
        )
        raise typer.Exit(1)

    # First check if server is already running
    if not OllamaManager.is_server_running():
        started: bool = OllamaManager.start_ollama_service()

        if started:
            time.sleep(3)
            console.print("[green]Ollama server started successfully![/green]")
        else:
            return None

    else:
        console.print("[yellow]Warning: Ollama server is already running![/yellow]")

    # Check and pull default model
    model_name = "llama3.2:3b"

    # console.print(f"[blue]Checking for default model {model_name}...[/blue]")
    if not OllamaManager.is_model_present(model_name):
        console.print(f"[cyan]Default model {model_name} not found.[/cyan]")

        time.sleep(1)
        if not OllamaManager.pull_model(model_name):
            console.print(
                "[red]Failed to pull default model. Please check your internet connection[/red]"
            )
            return None
    else:
        console.print(f"[green]Default model {model_name} is ready![/green]")
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

    if OllamaManager.is_server_running():
        stopped: bool = OllamaManager.stop_ollama_service()
        if stopped:
            # Update model status
            active_model = config["model_name"]
            models[active_model]["status"] = "disabled"

            ConfigManager.save_config(config)
            ConfigManager.save_models(models)

            # Remove config files
            os.remove(ConfigManager.CONFIG_FILE)

            console.print(Text(BANNER, justify="center"))
            console.print("[green]Ollama server stopped successfully.[/green]")

    else:
        console.print("[yellow]Warning: No Ollama server running found![/yellow]")


@app.command()
def gen(
    push: bool = typer.Option(False, "--push", "-p", help="Enable auto-push"),
):
    """Generates a editable commit message."""
    if not OllamaManager.is_server_running():
        console.print("[red]Error: Ollama server is not running![/red]")
        console.print(
            "Start the ollama server by running [cyan]autocommitt start[/cyan] command."
        )
        raise typer.Exit(1)

    changed_files = CommitManager.check_staged_changes()

    if not changed_files:
        console.print("[yellow]Warning: No stagged changes to commit[/yellow]")
        raise typer.Exit(1)

    # Get selected model
    config = ConfigManager.get_config()
    ConfigManager.get_models()

    CommitManager.model_name = config["model_name"]
    console.print("[cyan]Generating...[/cyan]")

    # Here you would integrate with your LLM to generate the message
    initial_message = CommitManager.generate_commit_message(changed_files)
    final_message = CommitManager.edit_commit_message(initial_message)

    if final_message is None:
        console.print("[yellow]Commit aborted[/yellow]")
        raise typer.Exit(1)

    # Create commit
    done: bool = CommitManager.perform_git_commit(final_message)
    if done:
        console.print("[green]Commit Sucessfull![/green]")
    else:
        console.print("[red]Commit FAILED![/red]")

    if push:
        try:
            console.print("[blue]Pushing changes to the remote repository...[/blue]")
            result = subprocess.run(
                ["git", "push"],
                check=True,
                capture_output=True,
                text=True,
            )
            # Print the output
            if result.stdout:
                console.print(result.stdout.strip())

            console.print("[green]Push successful![/green]")
            return True

        except subprocess.CalledProcessError as e:
            console.print("[red]Error: Auto pushing FAILED![/red]")
            console.print(f"[red]{e.stderr}[/red]")
            return False

        except FileNotFoundError:
            console.print(
                "[red]Error: Git is not installed or not found in PATH.[/red]"
            )
            return False

        except Exception as e:
            console.print(f"[red]Unexpected error: {str(e)}[/red]")
            return False


@app.command()
def list():
    """Lists all available LLM models for commit message generation"""
    ConfigManager.ensure_config()

    models = ConfigManager.get_models()
    config = ConfigManager.get_config()

    table = Table(title="Available Models")
    table.add_column("Name", style="cyan")
    table.add_column("Description", style="white")
    table.add_column("Size", style="yellow")
    table.add_column("Status", style="red")
    table.add_column("Downloaded", style="red")

    for model_name, details in models.items():
        # Enhanced status styling with icons and colors
        if OllamaManager.is_model_present(model_name) or details["downloaded"] == "yes":
            details["downloaded"] = "yes"
            downloaded_style = "[bright_green]yes[/bright_green]"
        else:
            downloaded_style = "[red]no[/red]"

        if model_name == config["model_name"]:
            status_style = "[bright_green]active[/bright_green]"
            model_name_style = f"[bold cyan]{model_name}[/bold cyan]"

        else:
            status_style = "[red]disabled[/red]"
            model_name_style = f"[cyan]{model_name}[/cyan]"

        table.add_row(
            model_name_style,
            details["description"],
            details["size"],
            status_style,
            downloaded_style,
        )

    ConfigManager.save_models(models)
    console.print(table)


@app.command()
def rm(model_name: str = typer.Argument(..., help="Name of the model to delete")):
    """Delete a model from available models"""

    if not OllamaManager.is_server_running():
        console.print("[red]Error: Ollama server is not running![/red]")
        console.print(
            "Start the ollama server by running [cyan]autocommitt start[/cyan] command."
        )
        raise typer.Exit(1)

    models = ConfigManager.get_models()
    ConfigManager.get_config()

    # Check if model exists
    if not OllamaManager.is_model_present(model_name):
        console.print(
            f"[yellow]Model {model_name} doesn't exist, skipping deletion.[/yellow]"
        )
        raise typer.Exit(1)

    # Check if it's a default model
    if models[model_name].get("status") == "active":
        console.print("[red]Error: Cannot remove currently active model![/red]")
        console.print(
            "Please switch to a different model first using the 'use' command."
        )
        raise typer.Exit(1)

    if models[model_name].get("downloaded") == "no":
        console.print(
            f"[yellow]Warning: Model: '{model_name}' is not downloaded![/yellow]"
        )

    # Remove the model
    OllamaManager.delete_model(model_name)


@app.command()
def use(model_name: str = typer.Argument(..., help="Name of the model to use")):
    """Select which model to use for generating commit messages"""

    if not OllamaManager.is_server_running():
        console.print("[red]Error: Ollama server is not running![/red]")
        console.print(
            "Start the ollama server by running [cyan]autocommitt start[/cyan] command."
        )
        raise typer.Exit(1)

    models = ConfigManager.get_models()

    if model_name not in models:
        console.print(f"[red]Error: Unknown model '{model_name}'[/red]")
        list()
        raise typer.Exit(1)

    pulled: bool = True
    if models[model_name]["downloaded"] != "yes":
        pulled = OllamaManager.pull_model(model_name)

    if pulled:
        models = ConfigManager.get_models()
        config = ConfigManager.get_config()
        # deactivated old model
        models[config["model_name"]]["status"] = "disabled"

        models[model_name]["status"] = "active"
        config["model_name"] = model_name

        ConfigManager.save_config(config)
        ConfigManager.save_models(models)

        console.print(f"[green]Successfully switched to '{model_name}' model.[/green]")
    else:
        console.print("\n[red]Download cancelled![/red]")


@app.command()
def his(
    limit: Optional[int] = typer.Option(
        None, "--limit", "-n", help="Display only the latest n commit messages"
    ),
):
    """Display the git commit history, optionally limiting to n recent commits."""
    try:
        with console.status("[blue]Fetching commit history...[/blue]"):
            # Build the git command based on whether limit is provided
            git_cmd = ["git", "log", "--oneline"]
            if limit is not None:
                git_cmd.extend(["-n", str(limit)])

            result = subprocess.run(
                git_cmd,
                check=True,
                capture_output=True,
                text=True,
                creationflags=subprocess.DETACHED_PROCESS if os.name == "nt" else 0,
            )

            if result.stdout:
                # Create a title based on whether limit is used
                title = f"Latest {limit} Commits" if limit else "Commit History"
                console.print(
                    Panel(result.stdout.strip(), title=title, border_style="blue")
                )
                return True
            else:
                console.print("[yellow]No commit history found.[/yellow]")
                return True

    except subprocess.CalledProcessError as e:
        if "fatal: your current branch does not have any commits yet" in e.stderr:
            console.print("[yellow]No commits found in this repository yet.[/yellow]")
        else:
            console.print(
                Panel(
                    e.stderr.strip(), title="Error Fetching History", border_style="red"
                )
            )
        return False

    except FileNotFoundError:
        console.print("[red]Error: Git is not installed or not found in PATH.[/red]")
        return False

    except Exception as e:
        console.print(f"[red]Unexpected error: {str(e)}[/red]")
        return False


if __name__ == "__main__":
    app()

import os
import time
import sys
import subprocess
from pathlib import Path
from typing import Optional,Dict
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from autocommitt.utils.config_manager import ConfigManager

console = Console()

class OllamaManager:
    
    @staticmethod
    def is_server_running() -> bool:
        """Check if Ollama server is already running"""
        try:
            pid_path = Path(ConfigManager.CONFIG_DIR) / "ollama_server.pid"
            if pid_path.exists():
                pid = int(pid_path.read_text().strip())
                if os.name == "nt":  # Windows
                    import ctypes
                    kernel32 = ctypes.windll.kernel32
                    try:
                        # Try to open the process with minimal rights
                        handle = kernel32.OpenProcess(0x0400, False, pid)
                        if handle:
                            kernel32.CloseHandle(handle)
                            return True
                        return False
                    except Exception:
                        return False
                else:  # Unix-like systems
                    os.kill(pid, 0)  # This will raise an error if process doesn't exist
                    return True
        except (FileNotFoundError, ValueError, ProcessLookupError, PermissionError):
            return False
        return False

    @staticmethod
    def check_server_health() -> bool:
        """Check if the Ollama server is responding"""

        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                timeout=3,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
                text=True
                )
            
            models = ConfigManager.get_models()
            models["llama3.2:3b"]["downloaded"] = "yes"
            ConfigManager.save_models(models)
            return result.returncode == 0
        except Exception:
            return False

    @staticmethod
    def is_model_present(model_name: str) -> bool:
        """
        Checks if a specific model is present in the output of `ollama list`.

        Args:
            model_name (str): The name of the model to check.

        Returns:
            bool: True if the model is present, False otherwise.

        Raises:
            ValueError: If model_name is empty or not a string.
        """

        if not model_name.strip():
            raise ValueError("model_name cannot be empty")

        try:
            # Run the ollama list command with timeout
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                check=False,  # Don't raise CalledProcessError, handle manually
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
            )

            # Check if the command was successful
            if result.returncode != 0:
                # logger.error(f"ollama list command failed: {result.stderr.strip()}")
                return False

            # Parse the output and check for the model
            models_list = [
                line.strip() for line in result.stdout.split("\n") if line.strip()
            ]

            # Look for the model name in each line
            for model_line in models_list:
                # print(model_line.split()[0].strip())
                # Split on whitespace and take the first part (model name)
                if model_line.split()[0].strip() == model_name:
                    return True

            return False

        except FileNotFoundError:
            console.print(f"[yellow]ollama command not found. Please ensure Ollama is installed and in PATH.[/yellow]")
            return False

        except Exception as e:
            console.print(f"[red]Unexpected error checking for model '{model_name}': {str(e)}[/red]")
            return False

    @staticmethod
    def pull_model(model_name: str, timeout: float = 600.00) -> bool:
        """
        Pulls an Ollama model if it's not already present.

        Args:
            model_name (str): The name of the model to pull
            timeout (Optional[float]): Maximum time in seconds to wait for the pull.
            Defaults to 10 minutes.

        Returns:
            bool: True if model is available (pulled successfully or already present),
                False if pull failed
        """

        try:
            # Check if model is already pulled
            present: bool = OllamaManager.is_model_present(model_name)
            if present:
                console.print(f"[green]Model {model_name} is already pulled and ready to use.[/green]")
                return True

            # Model needs to be pulled
            console.print(f"[yellow]Pulling {model_name}...[/yellow]")
            console.print("[blue]NOTE: The download time varies based on your internet speed and the model size.\nIf the download doesn't complete within 10 minutes, please try running the command again.[/blue]")
            
            # Create a simple spinner with elapsed time
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                TimeElapsedColumn(),
                console=console,
            ) as progress:
                task = progress.add_task(f"Downloading {model_name}...", total=None)
                
                try:
                    # Run the pull command with timeout
                    result = subprocess.run(
                        ["ollama", "pull", model_name],
                        capture_output=True,
                        text=True,
                        timeout=timeout,
                        creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
                    )
                    
                    if result.returncode == 0:
                        # Update the table
                        models = ConfigManager.get_models()
                        models[model_name]["downloaded"] = "yes"
                        ConfigManager.save_models(models)

                        console.print(f"[green]Successfully pulled {model_name}![/green]")
                        return True
                    else:
                        error_message = result.stderr if result.stderr else "Unknown error"
                        console.print(f"[red]Error pulling model: {error_message.strip()}[/red]")
                        return False

                except subprocess.TimeoutExpired as e:
                    # Clean up the process when timeout occurs
                    if hasattr(e, 'process'):
                        e.process.kill()
                    console.print(f"[red]Error: Pull operation timed out after {timeout} seconds[/red]")
                    return False
                    
                except KeyboardInterrupt:
                    console.print("\n[yellow]Download cancelled![/yellow]")
                    return False

        except FileNotFoundError:
            console.print("[red]Error: ollama command not found. Please ensure Ollama is installed and in PATH[/red]")
            return False
        except Exception as e:
            console.print(f"[red]Unexpected error while pulling model: {str(e)}[/red]")
            return False
    
    @staticmethod
    def delete_model(model_name: str) -> bool:
        """
        Deletes an Ollama model if it's already present.

        Args:
            model_name (str): The name of the model to delete

        Returns:
            bool: True if model deleted successfully, False if model doesn't exist
        """
        try:
            # Delete the model
            # console.print(f"[yellow]Deleting {model_name}...[/yellow]")
            result = subprocess.run(
                ["ollama", "rm", model_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
            )

            if result.returncode == 0:
                # Update the models table
                models = ConfigManager.get_models()
                models[model_name]["downloaded"]="no"
                ConfigManager.save_models(models)
                console.print(f"[green]Successfully deleted {model_name}.[/green]")
                return True
            else:
                error = result.stderr.strip()
                console.print(f"[red]Error deleting {model_name}: {error}[/red]")
                return False

        except FileNotFoundError:
            console.print("[red]Error: ollama command not found. Please ensure Ollama is installed and in PATH.[/red]")
            return False
        except Exception as e:
            console.print(f"[red]Unexpected error while deleting model: {str(e)}[/red]")
            return False

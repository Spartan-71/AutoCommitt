import subprocess
import time
import sys
import os
from typing import Optional
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from autocommitt.utils.config_manager import ConfigManager


class OllamaManager:

    def is_server_running() -> bool:
        """Check if Ollama server is already running"""
        try:
            pid_path = Path(CONFIG_DIR) / "ollama_server.pid"
            if pid_path.exists():
                pid = int(pid_path.read_text().strip())
                # Check if process exists
                os.kill(pid, 0)  # This will raise an error if process doesn't exist
                return True
        except (FileNotFoundError, ValueError, ProcessLookupError, PermissionError):
            return False
        return False

    def check_server_health() -> bool:
        """Check if the Ollama server is responding"""

        try:
            result = subprocess.run(["ollama", "list"], capture_output=True, timeout=3)
            models = get_models()
            models["llama3.2:3b"]["downloaded"] = "yes"
            save_models(models)
            return result.returncode == 0
        except Exception:
            return False

    def is_model_present(model_name: str) -> bool:
        """
        Checks if a specific model is present in the output of `ollama list`.

        Args:
            model_name (str): The name of the model to check.
            timeout (Optional[float]): Maximum time in seconds to wait for the command to complete.
                Defaults to 30 seconds.

        Returns:
            bool: True if the model is present, False otherwise.

        Raises:
            ValueError: If model_name is empty or not a string.
            TimeoutExpired: If the command execution exceeds the timeout.
        """
        # # Input validation
        # if not isinstance(model_name, str):
        #     raise ValueError("model_name must be a string")
        if not model_name.strip():
            raise ValueError("model_name cannot be empty")

        # # Configure logging
        # logger = logging.getLogger(__name__)

        try:
            # Run the ollama list command with timeout
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                text=True,
                check=False,  # Don't raise CalledProcessError, handle manually
            )

            # Check if the command was successful
            if result.returncode != 0:
                # logger.error(f"ollama list command failed: {result.stderr.strip()}")
                return False

            # Parse the output and check for the model
            # Split output into lines and clean up whitespace
            models_list = [
                line.strip() for line in result.stdout.split("\n") if line.strip()
            ]

            # Look for the model name in each line
            # This is more robust than simple string containment
            for model_line in models_list:
                # print(model_line.split()[0].strip())
                # Split on whitespace and take the first part (model name)
                if model_line.split()[0].strip() == model_name:
                    return True

            # logger.debug(f"Model '{model_name}' not found in ollama list")
            return False

        except subprocess.TimeoutExpired as e:
            logger.error(f"Command timed out after {timeout} seconds")
            raise

        except FileNotFoundError:
            logger.error(
                "ollama command not found. Please ensure Ollama is installed and in PATH"
            )
            return False

        except Exception as e:
            logger.error(
                f"Unexpected error checking for model '{model_name}': {str(e)}"
            )
            return False

    def pull_model(model_name: str, timeout: Optional[float] = 600.0) -> bool:
        """
        Pulls an Ollama model if it's not already present.

        Args:
            model_name (str): The name of the model to pull
            timeout (Optional[float]): Maximum time in seconds to wait for the pull.
                Defaults to 600 seconds (10 minutes)

        Returns:
            bool: True if model is available (pulled successfully or already present),
                False if pull failed
        """
        console = Console()

        try:
            # Check if model is already pulled
            # present: bool = is_model_present(model_name)
            # if present:
            #     console.print(f"[green]Model {model_name} is already pulled and ready to use.[/green]")
            #     return True

            # Model needs to be pulled
            console.print(f"[yellow]Pulling {model_name}...[/yellow]")
            console.print(
                "[blue]NOTE: Download time depends on your internet speed and model size[/blue]"
            )

            # Create progress display
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                TimeElapsedColumn(),
                console=console,
            ) as progress:
                # Add a progress task
                task = progress.add_task(f"Downloading {model_name}...", total=None)

                # Start the pull process
                process = subprocess.Popen(
                    ["ollama", "pull", model_name],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    bufsize=1,
                    universal_newlines=True,
                )

                start_time = time.time()

                # Monitor the pull process
                while True:
                    if process.poll() is not None:
                        break

                    if timeout and (time.time() - start_time) > timeout:
                        process.kill()
                        console.print(
                            f"[red]Error: Pull operation timed out after {timeout} seconds[/red]"
                        )
                        return False

                    output = process.stdout.readline() if process.stdout else ""
                    if output:
                        # Update progress description with latest output
                        progress.update(task, description=output.strip())

                    time.sleep(0.1)

                # Check if pull was successful
                if process.returncode == 0:
                    # updaing the table
                    models = ConfigManager.get_models()
                    models[model_name]["downloaded"] = "yes"
                    ConfigManager.save_models(models)

                    console.print(f"[green]Successfully pulled {model_name}![/green]")
                    return True
                else:
                    error = process.stderr.read() if process.stderr else "Unknown error"
                    console.print(f"[red]Error pulling model: {error.strip()}[/red]")
                    return False

        except subprocess.TimeoutExpired:
            console.print(
                f"[red]Error: Command timed out while pulling {model_name}[/red]"
            )
            return False

        except FileNotFoundError:
            console.print(
                "[red]Error: ollama command not found. Please ensure Ollama is installed and in PATH[/red]"
            )
            return False

        except Exception as e:
            console.print(f"[red]Unexpected error while pulling model: {str(e)}[/red]")
            return False

    def delete_model(model_name: str) -> bool:
        """
        Deletes an Ollama model if it's already present.

        Args:
            model_name (str): The name of the model to delete

        Returns:
            bool: True if model deleted successfully, False if model doesn't exist
        """
        console = Console()

        try:
            # Delete the model
            console.print(f"[yellow]Deleting {model_name}...[/yellow]")
            result = subprocess.run(
                ["ollama", "rm", model_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
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



    # def main():
    #     """Main function to demonstrate model pulling functionality."""
    #     console = Console()
    #     model_name = "llama3.2:3b"

    #     # Pull the model
    #     success = pull_model(model_name)

    #     if success:
    #         console.print(f"[green]Model {model_name} is ready to use![/green]")
    #     else:
    #         console.print(f"[red]Failed to ensure model {model_name} is available.[/red]")
    #         sys.exit(1)


# if __name__ == "__main__":
#     main()

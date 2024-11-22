import ollama
import subprocess
import readline
from typing import Tuple, Optional, List
from rich.console import Console

class CommitManager:
    """
    Manages Git commit operations with AI-powered commit message generation.
    Handles git operations, message generation, and interactive editing.
    """
    
    def __init__(self, model_name: str = "llama3.2:3b", console: Optional[Console] = None):
        """
        Initialize CommitManager with specified model and console.
        
        Args:
            model_name (str): Name of the LLM model to use
            console (Optional[Console]): Rich console for output
        """
        self.model_name = model_name
        self.console = console or Console()

    @staticmethod
    def execute_git_command(command: List[str]) -> Tuple[Optional[str], Optional[str]]:
        """
        Executes a git command and returns its output.
        
        Args:
            command (List[str]): Git command to execute
            
        Returns:
            Tuple[Optional[str], Optional[str]]: Tuple of (stdout, stderr)
        """
        try:
            process = subprocess.run(
                command, 
                capture_output=True, 
                text=True, 
                check=True
            )
            return process.stdout, None
        except subprocess.CalledProcessError as e:
            return None, e.stderr

    def check_staged_changes(self) -> Optional[str]:
        """
        Checks for staged changes in git repository.
        
        Returns:
            Optional[str]: Git diff output if changes exist, None otherwise
        """
        output, error = self.execute_git_command(["git", "diff", "--staged"])

        if error:
            self.console.print("[red]Error in executing git diff command![/red]")
            self.console.print(f"[red]Error: {error}[/red]")
            return None

        if not output:
            self.console.print("[yellow]Warning: No changes staged![/yellow]")
            return None

        return output

    def generate_commit_message(self, diff_output: str) -> str:
        """
        Generates commit message using AI model based on git diff.
        
        Args:
            diff_output (str): Git diff content
            
        Returns:
            str: Generated commit message
        """
        system_prompt = """You are a Git expert specializing in concise and meaningful commit messages based on git diff. Follow this format strictly:
                        feat: add <new feature>, fix: resolve <bug>, docs: update <documentation>, test: add <tests>, refactor: <code improvements>
                        Generate only one commit message, no explanations."""

        message = ""
        stream = ollama.chat(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": diff_output}
            ],
            stream=True
        )

        for chunk in stream:
            content = chunk["message"]["content"]
            message += content

        return message.strip()

    @staticmethod
    def edit_commit_message(initial_message: str) -> str:
        """
        Provides interactive editing of the commit message.
        
        Args:
            initial_message (str): Initial AI-generated message
            
        Returns:
            str: Final edited message
        """
        def prefill_input(prompt: str) -> str:
            def hook():
                readline.insert_text(initial_message)
                readline.redisplay()
            readline.set_pre_input_hook(hook)
            user_input = input(prompt)
            readline.set_pre_input_hook()
            return user_input

        final_message = prefill_input("> ")
        return final_message.strip() or initial_message

    def perform_git_commit(self, message: str) -> bool:
        """
        Executes the git commit with the provided message.
        
        Args:
            message (str): Commit message to use
            
        Returns:
            bool: True if commit successful, False otherwise
        """
        try:
            subprocess.run(
                ['git', 'commit', '-m', message], 
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            self.console.print("[green]Commit successful![/green]")
            return True
        except subprocess.CalledProcessError as e:
            self.console.print(f"[red]Commit failed: {e.stderr}[/red]")
            return False

    def generate(self) -> bool:
        """
        Orchestrates the complete commit process from diff to commit.
        
        Returns:
            bool: True if commit process completed successfully, False otherwise
        """
        diff_output = self.check_staged_changes()
        if not diff_output:
            return False

        initial_message = self.generate_commit_message(diff_output)
        final_message = self.edit_commit_message(initial_message)
        return self.perform_git_commit(final_message)

def main():
    """CLI entry point for commit generation."""
    commit_manager = CommitManager()
    commit_manager.generate()

if __name__ == "__main__":
    main()
import os
import ollama
import subprocess
from typing import Tuple, Optional


class CommitManager:
    """Manages Git commit operations with AI-assisted commit message generation."""

    model_name: str = "llama3.2:3b"

    @staticmethod
    def execute_git_command(command: list[str]) -> Tuple[str, Optional[str]]:
        """
        Execute a Git command safely with cross-platform compatibility.

        Args:
            command (List[str]): The Git command to execute.

        Returns:
            Tuple[Optional[str], Optional[str]]: Stdout and stderr of the command.
        """

        try:
            process = subprocess.run(
                command,
                capture_output=True,
                text=True,
                check=True,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
                encoding="utf-8",
                errors="replace",
            )
            return process.stdout, None
        except subprocess.CalledProcessError as e:
            return None, e.stderr

    @staticmethod
    def check_staged_changes() -> Optional[str]:
        """
        Check for staged Git changes.

        Returns:
            Optional[str]: Staged changes diff, or None if no changes.
        """
        output, error = CommitManager.execute_git_command(["git", "diff", "--staged"])

        if error:
            print(f"Error in executing git diff command: {error}")
            return None

        if not output:
            # print("Warning: No changes staged!!")
            return None

        return output

    @staticmethod
    def generate_commit_message(diff_output: str, model: str = model_name) -> str:
        """
        Generate a commit message using an AI model.

        Args:
            diff_output (str): Git diff content.
            model (str, optional): Ollama model name.

        Returns:
            str: Generated commit message.
        """
        system_prompt = """You are a Git expert specializing in concise and meaningful commit messages based on output of git diff command.
                        Choose a type from below that best describes the git diff output :
                            fix: A bug fix,
                            docs: Documentation only changes,
                            style: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc),
                            refactor: A code change that neither fixes a bug nor adds a feature,
                            perf: A code change that improves performance,
                            test: Adding missing tests or correcting existing tests,
                            build: Changes that affect the build system or external dependencies,
                            ci: Changes to our CI configuration files and scripts,
                            chore: Other changes that don't modify src or test files,
                            revert: Reverts a previous commit',
                            feat: A new feature,
                        Now, generate a concise git commit message written in present tense in the format type: description for the output of git diff command which is provided by the user.
                        The git diff output can have changes in multiple files so analyze that properly and generate a commit message all taking all the changes into consideration.
                        Exclude anything unnecessary such as translation. Your entire response will be passed directly into git commit.
                        Generate only one commit message of maximum length 60 characters, no explanations.
                        """

        message = ""
        stream = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": diff_output},
            ],
            stream=True,
        )

        for chunk in stream:
            content = chunk["message"]["content"]
            message += content

        return message.strip()

    @staticmethod
    def edit_commit_message(initial_message: str) -> str:
        """
        Provide an interactive commit message editing experience.

        Args:
            initial_message (str): AI-generated commit message.

        Returns:
            str: Final commit message after potential user edits.
        """
        try:
            import readline  # Optional readline support
        except ImportError:
            try:
                import pyreadline3 as readline  # for windows
            except ImportError:
                readline = None

        # Prefill the readline buffer with the initial message
        def prefill_input(prompt):
            def hook():
                readline.insert_text(initial_message)
                readline.redisplay()

            readline.set_pre_input_hook(hook)
            user_input = input(prompt)
            readline.set_pre_input_hook(None)
            return user_input

        final_message = prefill_input("> ")

        return final_message.strip() or initial_message

    @staticmethod
    def perform_git_commit(message: str) -> bool:
        """
        Perform Git commit with the provided message.

        Args:
            message (str): Commit message.

        Returns:
            bool: True if commit was successful, False otherwise.
        """
        try:
            # Use shell=False for security and to avoid shell injection
            subprocess.run(
                ["git", "commit", "-m", message],
                check=True,  # Raise an exception if the command fails
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
                encoding="utf-8",
                errors="replace",
            )
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error: {e.stderr}")
            return False

    @staticmethod
    def generate():
        """
        Orchestrate the entire commit generation process.
        Checks staged changes, generates and edits commit message, then commits.
        """
        diff_output = CommitManager.check_staged_changes()
        if diff_output:
            initial_message = CommitManager.generate_commit_message(diff_output)
            final_message = CommitManager.edit_commit_message(initial_message)
            CommitManager.perform_git_commit(final_message)

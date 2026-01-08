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
        system_prompt = """You are a Git commit message generator.

            Rules (mandatory):
            - Output plain text only.
            - Line 1: concise title in imperative mood, max 72 characters.
            - Line 2: must be empty.
            - Remaining lines: bullet points describing individual changes.
            - Do not repeat the title in the body.
            - Do not include explanations, markdown, or quotes.

            Context:
            You are given the output of `git diff --staged`.
            Analyze all changes and generate a structured commit message.
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

        return CommitManager.normalize_commit_message(message.strip())

    @staticmethod
    def normalize_commit_message(message: str) -> str:
        lines = [l.strip() for l in message.splitlines() if l.strip()]

        if not lines:
            return "chore: update files"

        first = lines[0]

        # If the model did NOT give a real title, synthesize one
        if (
            first.startswith("-")
            or first.lower().startswith("here is")
            or len(first.split()) > 12
        ):
            title = "chore: update project files"
            body_lines = lines
        else:
            title = first[:72]
            body_lines = lines[1:]

        bullets = []
        for line in body_lines:
            line = line.lstrip("-*• ").strip()

            # Drop LLM meta commentary
            lowered = line.lower()
            if (
                lowered.startswith("here is")
                or lowered.startswith("note that")
                or "i've followed" in lowered
                or "rules specified" in lowered
                or "concise title" in lowered
                or "bullet points" in lowered
            ):
                continue
            if line:
                bullets.append(f"- {line}")
        if bullets:
            return f"{title}\n\n" + "\n".join(bullets)

        return title

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
        try:
            import tempfile

            with tempfile.NamedTemporaryFile(
                mode="w", delete=False, encoding="utf-8"
            ) as f:
                f.write(message)
                commit_file = f.name

            subprocess.run(
                ["git", "commit", "-F", commit_file],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0,
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

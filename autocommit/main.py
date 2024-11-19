import ollama
import subprocess
from typing import Tuple, Optional


def execute_git_command(command: list[str]) -> Tuple[str, str]:
    """
    Execute a git command and return its output and error.

    Args:
        command: List of command components
    Returns:
        Tuple of (output, error) strings
    """
    process = subprocess.Popen(
        command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    return process.communicate()


def check_staged_changes() -> Optional[str]:
    """
    Check for staged changes in git.

    Returns:
        The git diff output if there are changes, None otherwise
    """
    output, error = execute_git_command(["git", "diff", "--staged"])

    if error:
        print("Error in executing git diff command!!")
        print("Error:", error)
        return None

    if not output:
        print("Warning: No changes staged!!")
        return None

    return output


def generate_commit_message(diff_output: str, model: str = "llama3.2:3b") -> None:
    """
    Generate a commit message using the AI model based on git diff.

    Args:
        diff_output: The git diff content
        model: The AI model to use
    """
    print("--> Generating the commit msg...\n")

    system_prompt = """You are a Git expert specializing in concise and meaningful commit messages based on git diff.Follow this format strictly:
                    feat: add <new feature>, fix: resolve <bug>, docs: update <documentation>, test: add <tests>, refactor: <code improvements>
                    Generate only one commit message, no explanations."""

    stream = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": diff_output},
        ],
        stream=True,
    )

    print("\n-->Commit msg:")
    for chunk in stream:
        print(chunk["message"]["content"], end="", flush=True)


def run():
    """Main function to orchestrate the git diff analysis and commit message generation."""
    print("\n--> Executing the command...\n")
    print("--> git diff --staged")

    diff_output = check_staged_changes()
    if diff_output:
        print(f"--> Output: {diff_output}")
        generate_commit_message(diff_output)


if __name__ == "__main__":
    run()

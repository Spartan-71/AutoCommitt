import ollama
import subprocess
import readline  # Important for input editing
from typing import Tuple, Optional

def execute_git_command(command: list[str]) -> Tuple[str, Optional[str]]:
    """
    Execute a git command and return its output and error.
    
    Args:
        command: List of command components
    Returns:
        Tuple of (output, error) strings
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

def generate_commit_message(diff_output: str, model: str = "llama3.2:3b") -> str:
    """
    Generate a commit message using the AI model based on git diff.
    
    Args:
        diff_output: The git diff content
        model: The AI model to use
    Returns:
        Generated commit message
    """
    print("\n--> Generating the commit msg...\n")
    
    system_prompt = """You are a Git expert specializing in concise and meaningful commit messages based on git diff. Follow this format strictly:
                    feat: add <new feature>, fix: resolve <bug>, docs: update <documentation>, test: add <tests>, refactor: <code improvements>
                    Generate only one commit message, no explanations."""
    
    message = ""
    stream = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": diff_output}
        ],
        stream=True
    )
    
    for chunk in stream:
        content = chunk["message"]["content"]
        message += content
        # print(content, end="", flush=True)
    
    return message.strip()

def edit_commit_message(initial_message: str) -> str:
    """
    Provide an interactive editing experience for the commit message.
    
    Args:
        initial_message: The AI-generated commit message
    Returns:
        The edited commit message
    """
    # Prefill the readline buffer with the initial message
    def prefill_input(prompt):
        def hook():
            readline.insert_text(initial_message)
            readline.redisplay()
        readline.set_pre_input_hook(hook)
        user_input = input(prompt)
        readline.set_pre_input_hook()
        return user_input

    # print("\n--> Edit Commit Message (Edit in-line, then press Enter):")
    final_message = prefill_input("> ")
    
    return final_message.strip() or initial_message

def perform_git_commit(message: str) -> bool:
    """
    Perform git commit with the given message.
    
    Args:
        message: Commit message
    Returns:
        Boolean indicating success of commit
    """
    # try:
        # Use shell=False for security and to avoid shell injection
    subprocess.run(
        ['git', 'commit', '-m', message], 
        check=True,  # Raise an exception if the command fails
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    print("\n--> Commit successful!")
    return True
    # except subprocess.CalledProcessError as e:
    #     print("\n--> Commit failed:")
    #     print(e.stderr)
    #     return False

def main():
    """Main function to orchestrate the git diff analysis and commit message generation."""
    # print("\n--> Executing the command...\n")
    # print("--> git diff --staged")
    
    diff_output = check_staged_changes()
    if diff_output:
        # Generate the initial commit message
        initial_message = generate_commit_message(diff_output)
        
        # Allow user to edit the message interactively
        final_message = edit_commit_message(initial_message)
        
        # print("\nFinal commit message:")
        # print(final_message)
        
        # Perform the git commit
        perform_git_commit(final_message)

if __name__ == "__main__":
    main()
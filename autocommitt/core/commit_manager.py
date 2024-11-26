import ollama
import subprocess
import readline  # Important for input editing
from typing import Tuple, Optional


class CommitManager:
    model_name: str = "llama3.2:3b"

    def execute_git_command(command: list[str]) -> Tuple[str, Optional[str]]:
        try:
            process = subprocess.run(
                command, capture_output=True, text=True, check=True
            )
            return process.stdout, None
        except subprocess.CalledProcessError as e:
            return None, e.stderr

    def check_staged_changes() -> Optional[str]:
        output, error = CommitManager.execute_git_command(["git", "diff", "--staged"])

        if error:
            print("Error in executing git diff command!!")
            print("Error:", error)
            return None

        if not output:
            print("Warning: No changes staged!!")
            return None

        return output

    def generate_commit_message(diff_output: str, model: str = model_name) -> str:
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
                        Now, generate a concise git commit message written in present tense in the format "type": "description" for the output of git diff command which is provided by the user.
                        Exclude anything unnecessary such as translation. Your entire response will be passed directly into git commit.
                        Generate only one commit message of maximum length 40 characters, no explanations.
                        """

        message = ""
        stream = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": diff_output}
            ],
            stream=True,
        )

        for chunk in stream:
            content = chunk["message"]["content"]
            message += content
            # print(content, end="", flush=True)

        return message.strip()

    def edit_commit_message(initial_message: str) -> str:
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
        try:
            # Use shell=False for security and to avoid shell injection
            subprocess.run(
                ["git", "commit", "-m", message],
                check=True,  # Raise an exception if the command fails
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            # print("\n--> Commit successful!")
            return True
        except subprocess.CalledProcessError as e:
            # print("\n--> Commit failed:")
            print(e.stderr)
            return False

    def generate():
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


# if __name__ == "__main__":
#     generate()

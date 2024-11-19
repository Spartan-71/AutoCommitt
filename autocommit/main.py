import ollama
import subprocess

# defing different git diff commands
gd_command = ["git", "diff"]
gds_commands = ["git", "diff", "--staged"]

# Execute the command
print("\n--> Executing the command...\n")
print("--> git diff")
process = subprocess.Popen(
    gd_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
)

# capture the output and error
output, error = process.communicate()

# display the command output
print("\n--> Output:\n")
print("Output:", output)
if error:
    print("Error:", error)
    print("Error in executing git diff command!!")

if not error:
    print("\n--> Generating the commit msg...\n")

    # streaming response
    stream = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "system",
                "content": "You are a Git expert specializing in generating concise and meaningful commit messages by analyzing the output of the git diff command. Your task is to create commit messages based on the provided input. Ensure that these messages are short, informative, and adhere to standard best practices for commit message formatting, including a clear description of changes made, the purpose of the changes, and any relevant issue references. Remember not to give description in response , generate just the commit msg.",
            },
            {"role": "user", "content": output},
        ],
        stream=True,
    )

    print(f"\n-->Commit msg:")
    for chunk in stream:
        print(chunk["message"]["content"], end="", flush=True)

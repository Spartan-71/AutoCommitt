import ollama
import subprocess

# defing different git diff commands
gd_command = ["git", "diff"]
gds_command = ["git", "diff", "--staged"]

# Execute the command
print("\n--> Executing the command...\n")
print("--> git diff --staged")
process = subprocess.Popen(
    gds_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
)

# capture the output and error
output, error = process.communicate()

# display the command output
print("\n--> Output:\n")
print(output)
if error:
    print("Error:", error)
    print("Error in executing git diff command!!")

if not error:
    print("\n--> Generating the commit msg...\n")

    # streaming response
    stream = ollama.chat(
        # best -> llama3.2:3b (2.0Gb)
        # okish -> gemma2:2b  (1.6Gb)
        model="llama3.2:3b",
        messages=[
            {
                "role": "system",
                "content": """You are a Git expert specializing in concise and meaningful commit messages based on git diff.Follow this format strictly:
                            feat: add <new feature>, fix: resolve <bug>, docs: update <documentation>, test: add <tests>, refactor: <code improvements>
                            Generate only one commit message, no explanations. If the input is empty i.e no changes are stagged then output appropriate warning.""",
            },
            {"role": "user", "content": output},
        ],
        stream=True,
    )

    print(f"\n-->Commit msg:")
    for chunk in stream:
        print(chunk["message"]["content"], end="", flush=True)

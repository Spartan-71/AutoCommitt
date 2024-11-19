from setuptools import setup, find_packages

# Parse the tabular requirements.txt file
# def parse_requirements(file_path):
#     requirements = []
#     with open(file_path) as f:
#         for line in f:
#             # Skip the header, separator, and empty lines
#             if (
#                 line.strip()
#                 and not line.startswith("Package")
#                 and not line.startswith("-")
#             ):
#                 parts = line.split()
#                 if len(parts) >= 2:
#                     package, version = parts[0], parts[1]
#                     requirements.append(f"{package}=={version}")
#     return requirements


# # Load the specific requirements
# requirements = parse_requirements("requirements.txt")

setup(
    name="autocommit",
    version="0.0.1",
    author="Spartan (Anish Dabhane)",
    author_email="<anishdabhane@gmail.com>",
    description="A CLI tool for generating editable commit messages with local AI models",
    packages=find_packages(),
    # install_requires=requirements,
    install_requires=['ollama'],
    keywords=["autocommit","aicommit","git diff","git automation","CLI tool","local AI"],
    entry_points={
        "console_scripts": [
            "autocommit = autocommit:hello",
            "ac = autocommit:run"
        ]
    },
)

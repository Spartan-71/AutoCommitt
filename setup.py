from setuptools import setup, find_packages

# Parse the tabular requirements.txt file
def parse_requirements(file_path):
    requirements = []
    with open(file_path) as f:
        for line in f:
            # Skip the header, separator, and empty lines
            if (
                line.strip()
                and not line.startswith("Package")
                and not line.startswith("-")
            ):
                parts = line.split()
                if len(parts) >= 2:
                    package, version = parts[0], parts[1]
                    requirements.append(f"{package}=={version}")
    return requirements


# Load the specific requirements
requirements = parse_requirements("requirements.txt")

setup(
    name="autocommit",
    version="0.0.3",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "ac = autocommit:hello",
        ]
    },
)

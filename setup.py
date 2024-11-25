from setuptools import setup, find_packages

# Read the contents of your README file
with open('README.md', 'r', encoding='utf-8') as f:
    long_des = f.read()

setup(
    name="autocommitt",
    version="v0.1.9",
    author="Anish Dabhane",
    author_email="anishdabhane@gmail.com",
    description="A CLI tool for generating editable commit messages with local AI models",
    long_description=long_des,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=["ollama","typer"],
    keywords=[
        "autocommit",
        "aicommit",
        "git diff",
        "git automation",
        "CLI tool",
        "local AI",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
    ],
    entry_points={
        "console_scripts": ["autocommitt = autocommitt.cli.main:app","ac = autocommitt.cli.main:app"]
    },
    url="https://github.com/Spartan-71/autocommitt",  # Update with your actual URL
    license="Apache-2.0",  # Specify your license type
    python_requires='>=3.8',  # Specify the minimum Python version required
)
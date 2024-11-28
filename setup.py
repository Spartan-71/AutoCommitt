from setuptools import setup, find_packages
import sys

# Read the contents of your README file
with open('README.md', 'r', encoding='utf-8') as f:
    long_des = f.read()

# Conditional dependencies for platform-specific requirements
platform_specific_requires = []
if sys.platform == "win32":
    platform_specific_requires.append("pyreadline3")

setup(
    name="autocommitt",
    version="v0.1.10",
    author="Anish Dabhane",
    author_email="anishdabhane@gmail.com",
    description="A CLI tool for generating editable commit messages locally using Ollama.",
    long_description=long_des,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        "ollama",
        "typer",
        "requests",
        "platformdirs",
        "psutil",
    ] + platform_specific_requires,
    keywords=[
        "autocommit",
        "aicommit",
        "git automation",
        "CLI tool",
        "local AI",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Operating System :: Microsoft :: Windows :: Windows 11",
        "Operating System :: MacOS"
    ],
    entry_points={
        "console_scripts": [
            "autocommitt = autocommitt.cli.main:app",
            "act = autocommitt.cli.main:app"
        ]
    },
    url="https://github.com/Spartan-71/autocommitt",  # Update with your actual URL
    license="Apache-2.0",  # Specify your license type
    python_requires='>=3.10',  # Specify the minimum Python version required
)

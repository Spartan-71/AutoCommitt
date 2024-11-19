from setuptools import setup, find_packages

# Read the contents of your README file
with open('README.md', 'r', encoding='utf-8') as f:
    long_des = f.read()

setup(
    name="autocommitt",
    version="0.1.1",
    author="Spartan (Anish Dabhane)",
    author_email="<anishdabhane@gmail.com>",
    description="A CLI tool for generating editable commit messages with local AI models",
    long_description=long_des,
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=["ollama"],
    keywords=[
        "autocommit",
        "aicommit",
        "git diff",
        "git automation",
        "CLI tool",
        "local AI",
    ],
    classifiers=[
        "Development Status :: Alpha version",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Linux",
    ],
    entry_points={
        "console_scripts": ["autocommitt = autocommitt:hello", "ac = autocommitt:run"]
    },

)

from setuptools import setup, find_packages

setup(
    name="autocommitt",
    version="0.1.1",
    author="Spartan (Anish Dabhane)",
    author_email="<anishdabhane@gmail.com>",
    description="A CLI tool for generating editable commit messages with local AI models",
    packages=find_packages(),
    # install_requires=requirements,
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

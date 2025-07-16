from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fs-analyzer",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A modular tool for analyzing file systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/fs-analyzer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: System :: Filesystems",
        "Topic :: Utilities",
    ],
    python_requires=">=3.8",
    install_requires=[
        # No external dependencies required
    ],
    entry_points={
        "console_scripts": [
            "fs-analyzer=fs_analyzer.main:main",
        ],
    },
)

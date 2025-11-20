from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="tonl-converter",
    version="0.1.0",
    description="A Python library for converting to and from TONL (Token-Optimized Notation Language)",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author="erdalbektas",
    author_email="erdalbektas@gmail.com",
    url="https://github.com/erdalbektas/tonl_converter",
    packages=find_packages(),
    install_requires=[
        "pyyaml",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup",
    ],
    keywords="tonl, converter, json, yaml, markdown, token-optimization",
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "tonl=tonl_converter.cli:main",
        ],
    },
)

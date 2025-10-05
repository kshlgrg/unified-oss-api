from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gh_maintainer_dashboard",
    version="0.1.0",
    author="Kushal Garg",
    author_email="kushalgarg71106@outlook.com",
    description="A comprehensive dashboard for GitHub repository maintainers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kshlgrg/gh-maintainer-dashboard",
    packages=find_packages(include=["gh_maintainer_dashboard", "gh_maintainer_dashboard.*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.9",
    install_requires=[
        "requests>=2.31.0",
        "gql[all]>=3.5.0",
        "pydantic>=2.5.0",
        "python-dotenv>=1.0.0",
        "redis>=5.0.0",
        "textblob>=0.17.1",
        "nltk>=3.8.1",
        "aiohttp>=3.9.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
)

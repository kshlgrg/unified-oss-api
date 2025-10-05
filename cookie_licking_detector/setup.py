from setuptools import setup, find_packages

setup(
    name="cookie-licking-detector",
    version="0.1.0",
    author="Kushal Garg",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
    ],
)

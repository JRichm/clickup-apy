from setuptools import setup, find_packeges

setup(
    name="clickup-apy",
    version="0.1.0",
    packages=find_packeges(),
    install_requires=[
        "requests",
        "python-dotenv"
    ],
    python_requires=">=3.8"
)
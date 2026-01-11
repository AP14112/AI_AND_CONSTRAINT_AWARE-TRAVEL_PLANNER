from setuptools import setup, find_packages

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="ai-travel-planner",
    version="0.1",
    description="An AI-powered travel planning application",
    author="Aryaman Prasad",
    packages=find_packages(),
    install_requires=requirements,
)
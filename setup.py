from setuptools import find_packages, setup


setup(
    name="mcnp-auto-scripting",
    version="0.1.0",
    description="Tools for automatically generating MCNP input scripts.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.9",
    author="Jose A. Cortes",
    packages=find_packages(include=["MCNPAutoScripting*"]),
    install_requires=["matplotlib", "numpy"],
)
from setuptools import setup, find_packages

setup(
    name="appchecker",
    version="0.2.1",
    packages=find_packages(),
    install_requires=[
        "halo>=0.0.31",
    ],
    description="Adds healthcheck for PythonApp",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/so89bur/AppChecker",
    author="Sov Bur",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)

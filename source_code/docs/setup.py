import setuptools

with open("README.md", "r") as rm:
    description = rm.read()

setuptools.setup(
    name="idl",
    version="0.0.1",
    author="Joseph Barsness",
    description="collection from the command line",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/jgbarsness/idl",
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: MIT License",
        "Operating System :: MacOS",
    ]
)
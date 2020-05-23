import setuptools

with open("README.md", "r") as rm:
    description = rm.read()

setuptools.setup(
    name="journal_mngr",
    version="0.0.1",
    author="Joseph Barsness",
    description="journal from the command line",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/jgbarsness/journal_mngr",
    packages=setuptools.find_packages(),
    python_requires='>=3.7',
    classifiers=["License :: OSI Approved :: MIT License"]
)
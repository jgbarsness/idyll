from setuptools import setup, find_packages
import pathlib
from io import open
from peck.info_and_paths import VERSION


# directory containing this file
FOLDER = pathlib.Path(__file__).parent
README = (FOLDER / "README.md").read_text()

setup(
    name = 'peck',
    description = 'simple notes on the command line',
    version = VERSION,
    packages = find_packages(),
    python_requires = '>=2.7',
    entry_points = '''
        [console_scripts]
        peck=peck.peck:driver
    ''',
    author = 'Joseph Barsness',
    long_description = README,
    long_description_content_type = 'text/markdown',
    license='MIT',
    url = 'https://github.com/jgbarsness/peck',
)
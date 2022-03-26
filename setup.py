# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='xenoponics',  # Required

    # Versions should comply with PEP 440
    # https://www.python.org/dev/peps/pep-0440/
    version='0.0.2',  # Required

    description='Tools and scripts to run hydroponics systems in a smarter way.',
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://github.com/nubly/Xenoponics',

    author='Alex Denofre',
    author_email='alex@51aliens.space',

    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Supported Python version metadata
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Programming Language :: Python :: 3.10",
        'Programming Language :: Python :: 3 :: Only',
    ],

    keywords='hydroponics, IoT, chemistry, botany, plants',  # Optional

    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['tests']),

    # Supported Python versions
    python_requires='>=3.8, <4',

    # Pip dependencies
    install_requires=[
        'requests',
        'smbus2',
        'typer'
        'w1thermsensor',
    ],

    # To provide executable scripts, use entry points
    entry_points={
        'console_scripts': [
            'xenoponics=control:main',
        ],
    },
)


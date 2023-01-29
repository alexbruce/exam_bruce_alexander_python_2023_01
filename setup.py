from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'ATM Project for Data Academy'
LONG_DESCRIPTION = 'Full project package for Data Academy first assignment.'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name='atm',
    version=VERSION,
    author='Alexander Bruce',
    author_email='alexbrucedev@gmail.com',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas'
    ],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'

    keywords=['python', 'atm'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
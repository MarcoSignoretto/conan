import os

from setuptools import setup
from setuptools import find_packages


def generate_console_scripts(path: str) -> [str]:
    console_script_definitions = [path + f for f in os.listdir(path)]
    print(console_script_definitions)
    return console_script_definitions


def main():
    setup(
        name='conan',
        version='0.0.1',
        packages=find_packages('src/'),
        package_dir={'': 'src'},
        url='https://https://github.com/MarcoSignoretto/conan',
        author='Marco Signoretto',
        author_email='marco.signoretto.dev@gmail.com',
        description='Tool collection for analysing data',
        install_requires=[
            "notebook",
            "jupyterlab",
            "pandas",
            "numpy",
            "matplotlib",
            "tabulate",
            "scipy"
        ],
        classifiers=[
            'Intended Audience :: Developers',
            'Operating System :: OS Independent',
            'Programming Language :: Python',
            'Topic :: Software Development :: Libraries :: Python Modules',
        ],
        scripts=generate_console_scripts("scripts/")
    )


main()

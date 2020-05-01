"""Setup nem command."""

from setuptools import setup


requirements = [line for line in open("requirements.txt").readlines()]

setup(
    name="nem",
    version="1.0.0",
    description="Nem Programming Language",
    author="Nemanja Mirić",
    author_email="nemanjamiric@outlook.com",
    maintainer="Nemanja Mirić",
    maintainer_email="nemanjamiric@outlook.com",
    license="MIT",
    install_requires=requirements,
    packages=["nem"],
    entry_points={
        "console_scripts": [
            'nemrun = nem.nemrun:script'
        ]
    }
)

from setuptools import setup, find_packages

setup(
    name="rochinko",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "rochinko": ["assets/*"],
    },
    install_requires=[
        "pymunk",
        "dataclass-wizard",
        "arcade @ https://github.com/pythonarcade/arcade/archive/refs/heads/development.zip",
    ],
    entry_points={
        "console_scripts": [
            "rochinko=rochinko.__main__:main",
        ],
    },
)

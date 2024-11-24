from setuptools import setup, find_packages

setup(
    name="mp3_manager",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "eyed3>=0.9.7",
    ],
    entry_points={
        "console_scripts": [
            "mp3=mp3_manager.main:cli"
        ]
    }
)
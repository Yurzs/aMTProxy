import os

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

os.chdir('./amtproxy/')
packages = setuptools.find_packages()
os.chdir('../')

setuptools.setup(
    name="aMTProxy",
    version="0.2",
    author="Yury (Yurzs)",
    author_email="dev@best-service.online",
    description="Async python MTProxy server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Yurzs/pyMTProxy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pyaes',
    ]
)

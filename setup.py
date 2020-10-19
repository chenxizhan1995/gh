'''
Created on 2020年10月19日

@author: chenx
'''
import setuptools
with open("Readme.md", "r", encoding='UTF-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="chx-gh", 
    version="0.0.2",
    author="Xizhan Chen",
    author_email="chenxizhan1995@163.com",
    description="Github 命令行工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/chenxizhan1995/gh.git",
    packages=setuptools.find_namespace_packages(include=['chx.*']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

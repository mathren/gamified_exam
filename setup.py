from setuptools import setup, find_packages

with open("README.org", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gamified_exam",
    version="0.1.0",
    author="Mathieu Renzo",
    author_email="mrenzo@arizona.edu",
    description="A Duolingo-style exam system for stellar evolution",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mathren/gamified_exam",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPLv3.0",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.11",
    install_requires=[
        "difflib",
    ],
    extras_require={
        "dev": [
            "jupyter",
            "notebook",
            "ipywidgets",
            "matplotlib",
            "pandas",
            "pytest",
        ],
    },
    package_data={
        "stellar_exam": ["../data/*.txt"],
    },
    include_package_data=True,
)

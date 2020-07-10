from setuptools import setup, find_packages


"""
Instructions for creating a release of the blackstone library.
1. Make sure your working directory is clean.
2. Make sure that you have changed the versions in "blackstone/version.py".
3. Create the distribution by running "python setup.py sdist" in the root of the repository.
4. Check you can install the new distribution in a clean environment.
5. Upload the distribution to pypi by running
   "twine upload <path to the distribution> -u <username> -p <password>".
   This step will ask you for a username and password - the username is "iclr-d" you can
   get the password from ICLR&D
"""

VERSION = {}
# version.py defines VERSION and VERSION_SHORT variables.
with open("blackstone/version.py", "r") as version_file:
    exec(version_file.read(), VERSION)

setup(
    name="blackstone",
    version=VERSION["VERSION"],
    url="https://research.iclr.co.uk/blackstone",
    author="ICLR&D (Incorporated Council of Law Reporting Research Lab)",
    author_email="research@iclr.co.uk",
    description="A SpaCy pipeline and models for NLP on unstructured legal text.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    keywords=["law caselaw lawtech legaltech nlp spacy SpaCy"],
    classifiers=[
        "Intended Audience :: Science/Research",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.6",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    license="Apache",
    install_requires=[
        "spacy>=2.3.0,<3.0.0",
        "requests", # required for the legislation linker.
        "conllu",
        "numpy",
        "pandas"
        ],
    tests_require=["pytest", "pytest-cov"],
    python_requires=">=3.6.0",
)

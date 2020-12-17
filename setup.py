import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bsu_irds_file_timestamper",
    version="0.0.1",
    author="Alex Kluber",
    author_email="ajkluber@bsu.edu",
    description="Tools for parsing timestamps in filenames",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ajkluber/file_timestamper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)

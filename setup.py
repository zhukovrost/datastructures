import setuptools

# Load the long_description from README.md
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Algorithms and Data Structures",
    version="0.0.1",
    author="zhukovrost",
    author_email="rosf.zhukov@gmail.com",
    description="Python Algorithms and Data Structures",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zhukovrost/algorithms",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

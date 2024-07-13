import setuptools

VERSION = "0.1.1"

NAME = "slav-eeik-datastructures"

INSTALL_REQUIRES = []

EXTRAS_REQUIRE = {
    "dev": [
        "sphinx",
        "sphinx-rtd-theme",
        "pytest",
    ]
}

setuptools.setup(
    name=NAME,
    version=VERSION,
    description="Simple datastructures library with documentation.",
    url="https://github.com/zhukovrost/datastructures",
    project_urls={
        "Source Code": "https://github.com/zhukovrost/datastructures",
        "Documentation": "https://zhukovrost.github.io/datastructures/",
    },
    author="Zhukov Rostislav",
    author_email="2rosf.zhukov@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
    ],

    python_requires=">=3.10",

    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    packages=["datastructures"],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)

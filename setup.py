from setuptools import setup, find_packages

setup(
    name="bbfetcher",
    version="0.1.0",
    description="BitBake-compatible Git fetcher for use in Python projects",
    author="Kadir Guzel",
    author_email="kguzel@voxel.at",
    url="https://github.com/velopera/bbfetcher",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL-2.0-only",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)

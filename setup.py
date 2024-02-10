import setuptools

setuptools.setup(
    name="compreader",
    version="0.1",
    author="Benjamin Fankhauser",
    author_email="benjamin.fankhauser@hotmail.ch",
    description="PDF Comp Reader",
    url="https://github.com/regio-beo/comp-reader",
    packages=setuptools.find_packages(exclude=['test', 'files']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
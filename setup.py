import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="VibrationAnalysisAE",
    version="0.0.1",
    author="Alex de Ruijter",
    author_email="alex.deruijter@hotmail.com",
    description="A package for simple analysis of a spring-mass-dashpot system.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AlexdeRuijter/VibrationAnalysisAE",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

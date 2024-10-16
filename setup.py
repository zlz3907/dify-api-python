from setuptools import setup, find_packages

setup(
    name="dify-api-python",
    version="0.1.5",
    author="zlz3907",
    author_email="zlz3907@gmail.com",
    description="A Python client for the Dify API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/zlz3907/dify-api-python",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    license="Apache License 2.0",
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "sseclient-py>=1.7.2",
    ],
)

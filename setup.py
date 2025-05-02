
from setuptools import setup, find_packages

setup(
    name="aurora-iam-db",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "boto3",
        "aiomysql",
        "SQLAlchemy"
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="Secure Aurora MySQL IAM auth connector with async and pooling support",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/YOUR_USERNAME/aurora-iam-db",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)

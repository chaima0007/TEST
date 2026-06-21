from setuptools import setup, find_packages

setup(
    name="caelum-kb-api",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "connexion[flask,swagger-ui]>=3.1.0",
        "python-dotenv>=1.0.0",
        "faiss-cpu>=1.7.4",
        "sentence-transformers>=2.7.0",
        "numpy>=1.24.0",
    ],
)

from setuptools import setup, find_packages

setup(
    name="assistant",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'click',
        'python-dotenv',
        'google-generativeai',
        'langchain',
        'langchain-google-genai',
        'chromadb',
        'tqdm'
    ],
    entry_points={
        'console_scripts': [
            'purwa-cli = assistant.cli:main',
        ],
    },
)
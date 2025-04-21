from setuptools import setup, find_packages

setup(
    name='quackbox',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        "charset-normalizer",
        "certifi",
        "requests",
        "urllib3",
    ],
    author="Sean O'Donnell",
    author_email='saoski88@gmail.com',
    description='A library for game developers to easily communicate with the QuackBox.',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
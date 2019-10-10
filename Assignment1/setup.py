"""
contactbook processor
"""

from setuptools import setup, find_packages

setup(
    name='contactbook',
    version='0.0.1',
    author='Minh Phan',
    description='Assignment 1',
    license=None,
    long_description='',
    packages=find_packages(),
    zip_safe=True,
    python_requires='>3.4, <4.0.0',
    install_requires=[
        'PyYAML==5.1.2',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Data Processing',
        'Topic :: Software Development'
    ]
)
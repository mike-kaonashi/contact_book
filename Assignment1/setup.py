"""
contactbook processor
"""

from setuptools import setup, find_packages

setup(
    name='contactbook',
    version='0.0.1',
    author='Minh Phan',
    author_email="minhpq.contact@gmail.com",
    description='Assignment 1',
    license='MIT',
    long_description='',
    packages=find_packages(),
    zip_safe=True,
    python_requires='>3.4, <4.0.0',
    install_requires=[
        'PyYAML==5.1.2',
    ],
    include_package_data=True,
    data_files=[
        # ('utils', [
        #     ('config', ['contactbook/utils/config/app-config.yml'])]
        # ),
        ('config', ['contactbook/utils/config/app-config.yml']),
        ('schema', ['contactbook/schema/contact.schema']),
        ('storages', ['contactbook/storages/contacts.json'])
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
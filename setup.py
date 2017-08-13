# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

project = 'hello'

setup(
    name=project,
    version='0.0.1',
    url='https://github.com/yuikns/hello-fabric',
    description='',
    author='Yu Jing',
    author_email='yu@argcv.com',
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
                         'fabric3',
                         'setuptools',
                         # 'pymongo', # for mongo io
                         'jieba',
                         'bs4',
                         'rq',
                         'numpy',
                         'scikit-learn',
                         'scipy',
                         'gensim',
                         'pandas',
                         'argparse'
                     ],
    test_suite='tests',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)

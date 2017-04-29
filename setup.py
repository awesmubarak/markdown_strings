from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as file:
    long_description = file.read()

setup(
     name='markdown_strings',
     version='1.0.0',
     description='Create markdown-formatted text',
     long_description=long_description,
     url='https://github.com/abactel/markdown_strings',
     author='abactel',
     author_email='abactel@protonmail.com',
     license='MIT',
     classifiers=[
         'Development Status :: 5 - Production/Stable',
         'Intended Audience :: Developers',
         'Operating System :: OS Independent'
         'Topic :: Text Processing :: Markup'
         'License :: OSI Approved :: MIT License',
         # check which of these it acually works on:
         'Programming Language :: Python'
         'Programming Language :: Python :: 2'
         'Programming Language :: Python :: 2.3'
         'Programming Language :: Python :: 2.4'
         'Programming Language :: Python :: 2.5'
         'Programming Language :: Python :: 2.6'
         'Programming Language :: Python :: 2.7'
         'Programming Language :: Python :: 3'
         'Programming Language :: Python :: 3.0'
         'Programming Language :: Python :: 3.1'
         'Programming Language :: Python :: 3.2'
         'Programming Language :: Python :: 3.3'
         'Programming Language :: Python :: 3.4'
         'Programming Language :: Python :: 3.5'
         'Programming Language :: Python :: 3.6'
     ],
     keywords='markdown md',
     packages=['markdown_strings']
)

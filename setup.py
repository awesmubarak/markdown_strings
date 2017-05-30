from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as file:
    long_description = file.read()

setup(
     name='markdown_strings',
     version='2.1.0',
     description='Create markdown-formatted text',
     long_description=long_description,
     url='https://github.com/abactel/markdown_strings',
     author='abactel',
     author_email='abactel@protonmail.com',
     license='MIT',
     classifiers=[
         'Development Status :: 5 - Production/Stable',
         'Intended Audience :: Developers',
         'Operating System :: OS Independent',
         'Topic :: Text Processing :: Markup',
         'License :: OSI Approved :: MIT License',
         'Programming Language :: Python'
     ],
     keywords='markdown md',
     packages=['markdown_strings']
)

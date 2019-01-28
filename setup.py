from setuptools import setup

with open("README", 'r') as f:
    long_description = f.read()

setup(
   name='dictator',
   version='1.0',
   description='A game to improve you typing',
   license="MIT",
   long_description=long_description,
   author='Aaron Goshine',
   author_email='greenlig@gmail.com',
   url="http://www.goshine-dev.co.uk/",
   packages=['dictator'],
   install_requires=[],
   scripts=['scripts/main']
)

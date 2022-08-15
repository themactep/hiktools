from setuptools import setup, find_packages

setup(
  name="boseapi",
  version="1.0.03",
  description="Hiktools",
  url="https://github.com/MatrixEditor/hiktools",
  author="MatrixEditor",
  author_email="not@supported.com",
  license="MIT License",

  packages=find_packages(
    where='.',
    include=['hiktools*']
  ),

  requires=[],

  classifiers= [
    'Development Status :: 1 - Planning',
    'Intended Audience :: Science/Research',
    'License :: MIT License',  
    'Operating System :: Windows :: Linux',        
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8'
  ]
)


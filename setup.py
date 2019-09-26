from setuptools import setup, find_packages

with open('README.md') as f:
    readme = f.read()

setup(
  name='multimedia-retrieval',
  description='content-based retrieval system for 3d shapes',
  long_description=readme,
  author='Ruben Schenkhuizen, Thomas Kok',
  author_email='r.schenkhuizen@students.uu.nl, t.t.kok@students.uu.nl',
  packages=find_packages(exclude=['data', 'docs'])
)

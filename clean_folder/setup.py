from setuptools import setup, find_namespace_packages
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
  name='clean_folder_ib',
  version='1.0.1',
  description='Utility tool for organizing and structuring files in selected folder',
  author='Ievgen Bardadym',
  author_email='ievgen.bardadym@gmail.coim',
  license='MIT',
  long_description=long_description,
  long_description_content_type='text/markdown',
  packages=find_namespace_packages(),
  classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
  ],
  entry_points={'console_scripts': ['clean_folder=clean_folder.clean:clean']}
)

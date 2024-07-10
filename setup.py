from os import path

from setuptools import setup


def main():
    # read the contents of README file
    this_directory = path.abspath(path.dirname(__file__))
    with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()

    # Run setup script
    setup(name='pyxtf',
          version='1.4.2',
          description='eXtended Triton Format (XTF) file interface',
          long_description=long_description,
          long_description_content_type='text/markdown',
          author='Oystein Sture',
          author_email='oysstu@gmail.com',
          url='https://github.com/oysstu/pyxtf',
          project_urls={
            "Bug Tracker": "https://github.com/oysstu/pyxtf/issues",
          },
          license='MIT',
          setup_requires=['numpy>=1.11'],
          install_requires=['numpy>=1.11'],
          extras_require={'Plotting': ['matplotlib>=1.5.1']},
          packages=['pyxtf', 'pyxtf.vendors'],
          package_data={'': ['*.pyi']},
          include_package_data=True,
          use_2to3=False,
          classifiers=[
              'License :: OSI Approved :: MIT License',
              'Intended Audience :: Developers',
              'Intended Audience :: Other Audience',
              'Intended Audience :: Science/Research',
              'Natural Language :: English',
              'Topic :: Scientific/Engineering',
              'Programming Language :: Python :: 3 :: Only'
          ])


if __name__ == '__main__':
    main()

from setuptools import setup
from tools.generate_pyi import generate_pyi

def main():
    # Generate .pyi files
    import pyxtf.xtf_ctypes
    generate_pyi(pyxtf.xtf_ctypes)
    import pyxtf.vendors.kongsberg
    generate_pyi(pyxtf.vendors.kongsberg)

    # Run setup script
    setup(name='pyxtf',
          version='0.1',
          description='eXtended Triton Format (XTF) file interface',
          author='Oystein Sture',
          author_email='oysstu@gmail.com',
          url='https://github.com/oysstu/pyxtf',
          license='MIT',
          setup_requires=['numpy>=1.11'],
          install_requires=['numpy>=1.11'],
          packages=['pyxtf', 'pyxtf.vendors'],
          package_data={'':['*.pyi']},
          use_2to3=False,
          classifiers=[
              'License :: OSI Approved :: MIT License',
              'Intended Audience :: Developers',
              'Intended Audience :: Other Audience',
              'Intended Audience :: Science/Research',
              'Natural Language :: English',
              'Topic :: Scientific/Engineering',
              'Programming Language:: Python:: 3:: Only'
          ])

if __name__ == '__main__':
    main()
from setuptools import setup

def read(fname):
    with open(fname, 'r') as f:
        return f.read()

setup(name             = 'python-numa',
      description      = 'Python libnuma ctypes wrapper',
      long_description = read('README.md'),
      py_modules       = ['numa'],
      version          = '0.5',
      author           = 'Alex Revetchi',
      author_email     = 'alex.revetchi@gmail.com',
      url              = 'https://github.com/zakalibit/python-numa',
      license          = 'License :: OSI Approved :: MIT License',
      platforms        = 'Linux',
      classifiers      = [
          'Development Status :: 2 - Pre-Alpha',
          'Intended Audience :: Developers',
          'Intended Audience :: Information Technology',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: MIT License',
          'Operating System :: POSIX',
          'Operating System :: POSIX :: Linux',
          'Programming Language :: Python'
          ],
      )

from setuptools import setup

setup(name='cs3020_support',
      version='0.9',
      description='Support code for CS 3020: compiler construction',
      url='http://github.com/jnear/cs3020-assignments',
      author='Joe Near',
      author_email='jnear@uvm.edu',
      license='GPLv3',
      package_data={'cs3020_support': ['py.typed']},
      packages=['cs3020_support'],
      install_requires=[
            'lark-parser',
            'pandas'
      ],
      zip_safe=False)

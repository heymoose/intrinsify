from setuptools import setup, find_packages

setup(name='intrinsify',
      version='0.1',
      description="""Python package that pulls stock information and calculates a 
                     rough intrinsic value based on the Ben Graham formula""",
      url='https://github.com/heymoose/intrinsify',
      author='Marc Novak',
      license='MIT',
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
          'Click',
      ],
      entry_points='''
          [console_scripts]
          intrinsify=intrinsify.stockdata:intrinsify
      ''',
      zip_safe=False)

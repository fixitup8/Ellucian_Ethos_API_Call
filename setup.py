from setuptools import find_packages, setup

# Dependency lists maintained here and in tox.ini
sp_install_requires = [
  'requests==2.33.0',
  'pytz==2019.3',
  'python-dateutil==2.8.1',
  'PythonAPIClientBase==0.0.15'
]
sp_tests_require = [
  'pytest'
]

all_require = sp_install_requires + sp_tests_require

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='EthosClient',
      version='0.0.0',
      description='Python package which provides Ellucian Ethos Client',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/dchang/EthosClient',
      author='DChang',
      author_email='chang818@gmail.com',
      license='MIT',
      python_requires='>=3.10',
      packages=find_packages(include=['EthosClient', 'EthosClient.*']),
      zip_safe=False,
      install_requires=sp_install_requires,
      include_package_data=True)

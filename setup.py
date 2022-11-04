from setuptools import find_packages, setup 

setup(
    name='cabinet',
    packages=find_packages(include=['cabinet_lib']),
    version='0.1.0',
    description='blob cataloger',
    author='paper_dragonfly',
    license='MIT',
    # install_requires=[],
    # tests_require = ['pytest'],
    # test_suite= 'tests',
)
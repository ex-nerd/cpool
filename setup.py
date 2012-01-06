from distutils.core import setup

setup(
    name='cpool',
    version='0.2.0',
    author='Chris Petersen',
    author_email='geek@ex-nerd.com',
    py_modules=['cpool'],
    url='https://github.com/ex-nerd/cpool',
    license='LICENSE.txt',
    description='Simple Connection Pool handler',
    long_description=open('README.txt').read(),
    install_requires=[
        "threading",
    ],
)

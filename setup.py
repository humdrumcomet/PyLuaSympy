from setuptools import setup

setup(
    name='pyLuaSympy',
    packages = ['pyLuaSympy'],
    version='0.1.0',
    description='perform computation and then seamlessly pull them into latex',
    author='Aaron English',
    install_requires=['sympy',
                      'numpy'],
)

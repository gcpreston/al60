from distutils.core import setup

# TODO: Remove external heapdict requirement
setup(name='al60',
      version='0.0',
      description='Various algorithm and data structure implementations',
      author='Graham Preston',
      packages=['al60'], requires=['heapdict'])

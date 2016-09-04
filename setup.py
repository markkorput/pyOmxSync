from setuptools import setup

setup(name='omxsync',
      version='0.1.1',
      description='Master/slave syncing of omxplayer instances over network',
      url='http://github.com/markkorput/pyOmxSync',
      author='Mark van de Korput',
      author_email='dr.theman@gmail.com',
      license='MIT',
      packages=['omxsync'],
      install_requires=['omxplayer-wrapper'],
      # dependency_links=['https://github.com/willprice/python-omxplayer-wrapper'],
      zip_safe=True)

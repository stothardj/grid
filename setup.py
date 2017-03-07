from setuptools import setup

setup(
  name='grid',
  packages=['grid'],
  include_package_data=True,
  install_requires=[
    'eventlet',
    'flask',
    'flask-socketio',
  ],
)

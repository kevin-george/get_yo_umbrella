from setuptools import setup

setup(
    name='grab_yo_umbrella',
    version='0.1',
    py_modules=['alert_me'],
    install_requires=[
        'click',
        'requests',
        'pyyaml',
    ],
    entry_points='''
        [console_scripts]
        grab_yo_umbrella=alert_me:check_weather
    ''',
)
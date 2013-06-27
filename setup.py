from setuptools import setup

setup(
    name='dumplr',
    description='A tumblr downloader.',
    version='0.0.1',
    author='TLed',
    author_email='tled@ledderboge.de',
    url='',
    license="GPLv3",
    platforms=['POSIX'],
    keywords=['tumblr'],
    scripts=['dumplr'],
    packages=['Scrapelr'],
    install_requires=['beautifulsoup']
    )

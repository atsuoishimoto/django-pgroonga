import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="django-pgroonga",
    version="0.0.1",
    author="Atsuo Ishimoto",
    author_email="ishimoto@gembook.org",
    description="PGroonga utility for Django.",
    license="MIT",
    keywords="django groonga pgroonga",
    url="https://github.com/atsuoishimoto/django-pgroonga",
    long_description=read('README.rst'),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 3 - Alpha",
        "Framework :: Django",
    ],
    packages=['django_pgroonga'],
)

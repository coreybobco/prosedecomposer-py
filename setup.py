from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

requirements = [
    'Gutenberg==0.7.0',
    'inflect==2.1.0',
    'internetarchive==1.8.5',
    'markovify==0.7.1',
    'nltk==3.4.5',
    'rdflib==4.2.2',
    'spacy==2.1.8',
    'unittest2==1.1.0',
    'wordfreq>=2.2.1'
]

setup(
    name='prosedecomposer',
    version='0.1.1',
    description='Decompose, transform, and recombine prose into mutated forms.',
    long_description=readme,
    author="Corey Bobco",
    author_email='corey.bobco@gmail.com',
    url='https://github.com/coreybobco/prosedecomposer-py',
    dependency_links=['https://github.com/coreybobco/gutenberg_cleaner@master#egg=gutenberg_cleaner'],
    packages=[
        'prosedecomposer',
    ],
    package_dir={'prosedecomposer':
                 'prosedecomposer'},
    install_requires=requirements,
    license="MIT",
    zip_safe=True,
    keywords='poetry',
    classifiers=[
        "Development Status :: 3 - Alpha",
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Topic :: Artistic Software",
    ],
    test_suite='tests',
)

from setuptools import setup
import sct_dbtool


install_requirements = [
        'setuptools>=0.6c11',
        'docopt>=0.6.2',
        'requests>=2.19.1',
        'tqdm>=4.23.0',
        'jinja2>=2.10',
        'nibabel>=2.3.0',
        'sphinx>=1.7.2',
]

setup(
    name='sct_dbtool',
    version=sct_dbtool.__version__,
    url='https://github.com/neuropoly',
    license='Apache License 2.0',
    author=sct_dbtool.__author__,
    author_email='christian.perone@gmail.com',
    description='A MRI database management tools.',
    long_description='A MRI database management tools.',
    packages=['sct_dbtool'],
    keywords='MRI, database, tool, management',
    platforms='Any',
    package_data={
      'sct_dbtool': ['static/*.*', 'templates/*.*'],
    },
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requirements,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    entry_points={
        'console_scripts': [
            'sct_dbtool = sct_dbtool.main:run_main',
        ],
    },
)

from distutils.core import setup
setup(
    name='adalitix',         # How you named your package folder (MyLib)
    packages=['adalitix'],
    version='0.1',
    license='MIT',
    description='Python package to interact with adalitix',
    author='Andrea Zanin',
    author_email='azanin@fbk.eu',
    url='https://github.com/Adalitix/adalitix.py',
    download_url='https://github.com/Adalitix/adalitix.py/archive/v0.1.tar.gz',
    keywords=['adalitix'],
    install_requires=[
        'numpy',
        'requests',
        'Pillow'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)

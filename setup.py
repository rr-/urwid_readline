from setuptools import setup, find_packages

setup(
    author='Marcin Kurczewski',
    author_email='rr-@sakuya.pl',
    name='urwid_readline',
    description=(
        'A textbox edit widget for urwid that supports readline shortcuts'),
    version='0.6',
    url='https://github.com/rr-/urwid_readline',
    packages=find_packages(),

    install_requires=[
        'urwid',
    ],

    classifiers=[
        'Environment :: Console',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Desktop Environment',
        'Topic :: Software Development',
        'Topic :: Software Development :: Widget Sets',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ])

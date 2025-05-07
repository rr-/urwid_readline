from setuptools import find_packages, setup

setup(
    author="Marcin Kurczewski",
    author_email="rr-@sakuya.pl",
    name="urwid_readline",
    description=(
        "A textbox edit widget for urwid that supports readline shortcuts"
    ),
    version="0.15.1",
    url="https://github.com/rr-/urwid_readline",
    license="MIT",
    packages=find_packages(),
    install_requires=["urwid"],
    classifiers=[
        "Environment :: Console",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Desktop Environment",
        "Topic :: Software Development",
        "Topic :: Software Development :: Widget Sets",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    extras_require={
        "dev": ["black", "pytest"],
    },
)

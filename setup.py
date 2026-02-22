from setuptools import setup, find_packages

setup(
    name="linux-monster",
    version="1.4.6",
    description="A bruteforce tool, built and packaged for resilience. Purpose: strictly for penetration testing only",
    author="Shade",
    author_email="adesolasherifdeen3@gmail.com",
    packages=find_packages(),
    install_requires=[
        'requests',
        'selenium==4.9.1',
        'beautifulsoup4',
        'flask'
    ],
    entry_points={
        "console_scripts": [
            "linux-monster=linux_monster.main:main",
            "linux-monster-server=linux_monster.server:start",
            "linux-monster-migrate=linux_monster.migrate:migrator",
            "linux-monster-log=linux_monster.main:readlog"
        ]
    },
    include_package_data=True,
    package_data={
        "linux_monster": ["password/*", "data/*", "cache/*"],
    },
    python_requires='>=3.11',
    license="GPL-3.0",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "GitHub": "https://github.com/harkerbyte",
        "Facebook": "https://facebook.com/harkerbyte",
        "Whatsapp" : "https://whatsapp.com/channel/0029Vb5f98Z90x2p6S1rhT0S",
        "Youtube" : "https://youtube.com/@harkerbyte",
        "Instagram": "https://instagram.com/harkerbyte"
    },
    long_description=open("pypi.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
)
from setuptools import setup, find_packages

from aiomarzban import __version__


def readme():
    with open('README.md', 'r') as f:
        return f.read()


setup(
    name='aiomarzban',
    version=__version__,
    author='P1nk_L0rd',
    author_email='mestepanik@gmail.com',
    description='User-friendly async SDK for the Marzban API.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    url='https://github.com/P1nk-L0rD/aiomarzban',
    packages=find_packages(),
    install_requires=[
        'requests>=2.5.0',
        'aiohttp>=3.7.3',
        'pydantic>=2.0',
        'datetime>=4.0',
    ],
    classifiers=[
    'Programming Language :: Python :: 3.10',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent'
    ],
    keywords=["aiomarzban", "marzban", "marzban API", "marzban SDK", "Gozargah", "marzpy", "marz"],
    project_urls={
        "Homepage": "https://github.com/P1nk-L0rD/aiomarzban",
        "Source": "https://github.com/P1nk-L0rD/aiomarzban",
        "Developer": "https://t.me/IMC_tech",
    },
    python_requires='>=3.9'
)
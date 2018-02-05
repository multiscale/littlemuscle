from setuptools import setup
setup(
        name = 'littlemuscle',
        packages = ['littlemuscle'],
        version = 'develop',
        description = 'A very simple multiscale coupler for prototyping and education',
        author = 'Lourens Veen',
        author_email = 'l.veen@esciencecenter.nl',
        url = 'https://github.com/multiscale/littlemuscle',
        download_url = 'https://github.com/multiscale/littlemuscle/archive/develop.tar.gz',
        license = 'Apache License 2.0',
        python_requires='>=3.5, <4',
        install_requires=[
                'overrides'
            ],
        keywords = ['multiscale', 'coupling', 'MUSCLE'],
        classifiers = [
            'Development Status :: 3 - Alpha',
            'License :: OSI Approved :: Apache Software License',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6'],
        )

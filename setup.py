from setuptools import setup, find_packages
setup(
    name="Django-TeamHub",
    version="0.1",
    packages=find_packages(exclude=['project_settings']),

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=[
                       " Django==1.4.1",
                        "docutils==0.9.1",
                        ],

    # metadata for upload to PyPI
    author="Veronika Gross, Tim Jagodzinski, Dennis Lipps, Ruslan Mousarov",
    author_email="tim.jagodzinski@gmail.com",
    description="Slimmed down task management application for Django framework",
    license="None",
    keywords="task management project",
    url="https://github.com/neonsamurai/swp2-teamhub", # project home page, if any
    include_package_data=True,

    # could also include long_description, download_url, classifiers, etc.
)

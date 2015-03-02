from distutils.core import setup

setup(
    name='herringbone-toolbox',
    version='0.1.0',
    packages=['herringbone-toolbox'],
    package_dir={'herringbone-toolbox': 'herringbone-toolbox'},
    package_data={'herringbone-toolbox': ['esri/toolboxes/*.*']},
    license='Apache v2.0',
    author='Florenz A. P. Hollebrandse',
    author_email='fhollebrandse@envirocentre.co.uk',
    description='ArcGIS toolbox to create a herringbone pattern'
)

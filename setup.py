from setuptools import setup, find_packages


the_file = open("requirements.txt", "r")
packages_alt = the_file.readlines()

packages = []
for package in packages_alt:
    package = package.strip()
    packages.append(package)
    
# More infos: https://docs.python.org/3/distutils/setupscript.html


setup(
    name="School-Project",
    version="0.0.1",
    packages=['school'],
    author='Tim&Franck',
    author_email='example@gmail.com',
    maintainer='Tim&Franck',
    maintainer_email='...',
    description='School Manager Project; Able to manage Students/Grades/Subjects/Teachers',
    #long_description=''
    install_requires=packages,
    license='...',
    classifiers=[],  #https://pypi.org/classifiers/

    include_package_data=True,
)

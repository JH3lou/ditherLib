# setup.py
from setuptools import setup, find_packages

setup(
    name="ditherlib",
    version="0.1.0",
    author="JH3lou",
    description="A modern Python library and GUI for image dithering algorithms including adaptive and classic diffusion.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/JH3lou/ditherLib",
    project_urls={
        "Bug Tracker": "https://github.com/JH3lou/ditherLib/issues",
        "Documentation": "https://github.com/JH3lou/ditherLib#readme",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "customtkinter==5.2.2",
        "darkdetect==0.8.0",
        "exceptiongroup==1.2.2",
        "iniconfig==2.1.0",
        "numpy==2.2.4",
        "packaging==24.2",
        "pillow==11.1.0",
        "pluggy==1.5.0",
        "pytest==8.3.5",
        "tomli==2.2.1",
    ],
    python_requires=">=3.8",
)

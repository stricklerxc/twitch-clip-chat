from setuptools import setup

packages = [
    "twitch_clip_chat"
]

install_requires = [
    "requests>=2.23.0,<3.0.0",
    "yaml>=5.3.1,<6.0.0"
]

entry_points = {
    "console_scripts": ["clip_chat = twitch_clip_chat.cli:main"]
}

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="twitch_clip_chat",
    version="0.0.2",
    author="Stricklerxc",
    author_email=None,
    description="Python package for scrapping chat from Twitch clips",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/stricklerxc/twitch-clip-chat",
    packages=packages,
    install_requires=install_requires,
    entry_points=entry_points,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.7,<4.0"
)

from setuptools import setup

setup(
    name="c4_sign",
    version="0.0.1",
    description="funny sign go brrrrrrrr",
    url="https://github.com/CornellCollegeComputingClub/c4-sign",
    author="Mark Smith",
    author_email="totallynotmark6@gmail.com",
    license="none",
    packages=["c4_sign"],
    install_requires=["requests", "arrow", "segno", "numpy", "bdfparser", "srt", "Pillow", "gdown", "ffmpeg-downloader"],
    extras_require={
        "physical": ["rpi_ws281x", "adafruit-circuitpython-neopixel", "smbus"],
        "simulator": ["flask", "flask-socketio"],
        "misc": ["black", "autoflake", "isort", "pyinstrument"],
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
    ],
)

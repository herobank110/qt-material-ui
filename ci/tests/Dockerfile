FROM python:3.10
ENV QT_QPA_PLATFORM=offscreen
RUN apt-get update
RUN apt-get install libegl1 libgl1 libxkbcommon0 -y
RUN python -m pip install --upgrade pip

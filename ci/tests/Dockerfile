FROM python:3.10-slim
ENV QT_QPA_PLATFORM=offscreen
RUN apt-get update
RUN apt-get install -y libegl1 libgl1 libxkbcommon0 libdbus-1-3
RUN python -m pip install --upgrade pip

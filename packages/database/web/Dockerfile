# syntax=docker/dockerfile:1
FROM ubuntu
WORKDIR /code
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
# RUN apk add --no-cache gcc musl-dev linux-headers
RUN apt-get update
RUN apt-get install -y python3-pip
RUN apt-get install ffmpeg libsm6 libxext6 -y
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . .
# RUN pip install https://download.pytorch.org/whl/cu101/torch-1.14.0-cp37-cp37-win_amd64.whl
# RUN pip install https://download.pytorch.org/whl/cu101/torchvision-0.14.0-cp38-cp38-win_amd64.whl
RUN pip3 install torch torchvision --extra-index-url https://download.pytorch.org/whl/cpu
# RUN cd CNN && pip3 install -r requirements.txt
CMD ["flask", "run"]

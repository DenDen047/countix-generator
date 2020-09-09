FROM python:3.8.5

RUN apt-get update -y
RUN apt-get install -y libgl1-mesa-glx

# pip
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# clean
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*
FROM balenalib/fincm3-alpine-python
CMD ["cat", "/etc/os-release"]

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt

RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

ENV UDEV=1

CMD ["python3","-u","src/main.py"]
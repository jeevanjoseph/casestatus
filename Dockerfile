FROM python:3
COPY ["casestatus","requirements.txt", "/app/"]
WORKDIR /app/
ENV PATH=$PATH:/app/
RUN pip3 install -r requirements.txt
CMD ["casestatus"]

FROM python:3.8

ADD src /src

RUN pip install prometheus_client
RUN pip install plotly
RUN pip install polyline
RUN pip install python-dateutil
RUN pip install python-dotenv
RUN pip install requests
RUN pip install geopy

WORKDIR /src


ENV PYTHONPATH '/src/'
ENV RIVIAN_PASSWORD 'secret'
ENV RIVIAN_USERNAME 'k8s'

CMD ["python" , "/src/rivian_exporter.py"]
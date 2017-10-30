FROM joommf/oommf

RUN apt-get -y update 
RUN apt-get install -y git python3 python3-pip
RUN pip3 install matplotlib pytest scipy ipywidgets numpy pandas

RUN ln -s /usr/bin/python3 /usr/bin/python

# Headless Matplotlib:
ENV MPLBACKEND=Agg

ENV OMP_NUM_THREADS=2
WORKDIR /io

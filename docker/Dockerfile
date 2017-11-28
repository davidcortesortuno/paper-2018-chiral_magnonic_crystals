FROM ubuntu:16.04

RUN apt-get -y update 
RUN apt-get install -y git tk-dev tcl-dev wget

# Compile oommf 1.2b1 and create OOMMFTCL environment variable
WORKDIR /usr/local
RUN wget http://math.nist.gov/oommf/dist/oommf12b1_20170927.tar.gz
RUN tar xvzf oommf12b1_20170927.tar.gz && rm oommf12b1_20170927.tar.gz
WORKDIR /usr/local/oommf
RUN ./oommf.tcl pimake
ENV OOMMFTCL /usr/local/oommf/oommf.tcl

# Create executable oommf script
WORKDIR /usr/local/bin
RUN echo "#! /bin/bash" > oommf
RUN echo "tclsh /usr/local/oommf/oommf.tcl \"\$@\"" >> oommf
RUN chmod a+x oommf

# Tools for the simulations
RUN apt-get install -y git python3 python3-pip fonts-lato
RUN pip3 install matplotlib pytest scipy ipywidgets numpy pandas

# Set Python 3 as default
RUN ln -s /usr/bin/python3 /usr/bin/python

# Headless Matplotlib:
ENV MPLBACKEND=Agg

ENV OMP_NUM_THREADS=2
WORKDIR /io

FROM python:3.6.4-stretch

# install base packages
RUN apt-get clean \
 && apt-get update --fix-missing \
 && apt-get install -y \
    git \
    curl \
    gcc \
    g++ \
    build-essential \
    wget \
    awscli

WORKDIR /work

# install python packages
COPY dev-requirements.txt dev-requirements.txt

# add the code as the final step so that when we modify the code
# we don't bust the cached layers holding the dependencies and
# system packages.
COPY blackstone/ blackstone/
COPY setup.py setup.py
COPY README.md README.md
COPY scripts/ scripts/
COPY tests/ tests/
COPY examples/ examples/
COPY .flake8 .flake8

RUN pip install -r dev-requirements.txt
RUN pip install -e .
RUN pip install https://blackstone-model.s3-eu-west-1.amazonaws.com/en_blackstone_proto-0.0.1.tar.gz

CMD [ "/bin/bash" ]

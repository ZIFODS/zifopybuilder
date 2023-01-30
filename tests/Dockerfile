FROM python:3
LABEL name="test-zifopybuilder"
LABEL version="0.2.0"

# Install git
RUN apt update
RUN apt install git
# Needed to install Numpy
RUN apt install -y build-essential python3-dev
RUN apt install git

RUN git config --global user.email "test@zifornd.com"
RUN git config --global user.name "test"

# Install hatch and zifopybuilder
COPY /dist /dist
RUN pip install poetry
RUN pip install /dist/zifopybuilder-0.2.0-py3-none-any.whl

# Copy test script over and run tests on start
COPY tests/tests.sh /tests.sh
RUN chmod +x /tests.sh
ENTRYPOINT [ "/tests.sh" ]

FROM python:3
# Arguments
ARG WHEEL

# Install git
RUN apt update
RUN apt install git
# Needed to install Numpy
RUN apt install -y build-essential python3-dev

# Install hatch and zifopybuilder
COPY $WHEEL $WHEEL
RUN pip install hatch
RUN pip install pre-commit
RUN pip install ${WHEEL}

# Copy test script over and run tests on start
COPY tests/tests.sh /tests.sh
ENTRYPOINT [ "/tests.sh" ]

FROM python:3
# Arguments
ARG WHEEL

# Install hatch and zifopybuilder
COPY $WHEEL $WHEEL
RUN pip install hatch
RUN pip install ${WHEEL}

# Copy test script over and run tests on start
COPY tests/tests.sh /tests.sh
ENTRYPOINT [ "/tests.sh" ]

FROM python:3.7

# Install dependecies
COPY Pipfile* /tmp/
RUN pip install --quiet --no-cache --upgrade pipenv
RUN cd /tmp && pipenv lock --requirements > requirements.txt
RUN pip install --quiet --no-cache  -r /tmp/requirements.txt

# Adding user
RUN useradd --create-home appuser
USER appuser

# Set up environment
WORKDIR /home/appuser
ENV DEBUG=True
ENV FLASK_ENV=development

# Copy source
COPY ./src/ ./src
COPY ./models/ ./models

# Execute
EXPOSE 5000
CMD ./src/app.py
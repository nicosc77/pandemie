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
ENV DEBUG=False
ENV FLASK_ENV=production
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy source
COPY ./src .

# Lint
RUN flake8 .

# Execute
EXPOSE 5000
CMD gunicorn --timeout 1000 --workers 4 --threads 4 --preload --log-level error --bind 0.0.0.0:5000 app:app
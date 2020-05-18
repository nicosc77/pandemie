FROM python:3.7

# Install dependecies
COPY requirements.txt .
RUN pip install -r ./requirements.txt

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
CMD python3 ./src/app.py
FROM python:3.6-slim

WORKDIR /app

# Install git (needed for pip install from git)
RUN apt-get update && \
    apt-get install -y git gcc python3-dev build-essential && \
    rm -rf /var/lib/apt/lists/*

COPY . /app

RUN pip install --upgrade pip

RUN pip install cltk
RUN mkdir -p $HOME/cltk_data/greek/model
RUN mkdir -p $HOME/cltk_data/latin/model 
RUN git clone https://github.com/cltk/greek_models_cltk $HOME/cltk_data/greek/model/greek_models_cltk
RUN git clone https://github.com/cltk/latin_models_cltk $HOME/cltk_data/latin/model/latin_models_cltk

RUN pip install -r requirements.txt

RUN pip install gunicorn

# Expose Flask port
# EXPOSE 8000
EXPOSE 5000

CMD ["python", "-m", "example.example_launcher"]
# CMD ["gunicorn", "--bind", "0.0.0.0", "apitess:app"]
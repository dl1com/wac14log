# Dockerfile
FROM python:3.10.4-slim-buster
RUN pip install --upgrade pip

RUN useradd -m myuser
USER myuser
WORKDIR /home/myuser

ENV PATH="/home/myuser/.local/bin:${PATH}"

COPY --chown=myuser:myuser contestlib.py contestlib.py
COPY --chown=myuser:myuser dbhandler.py dbhandler.py
COPY --chown=myuser:myuser home.py home.py
COPY --chown=myuser:myuser jsonhandler.py jsonhandler.py
COPY --chown=myuser:myuser requirements.txt requirements.txt
RUN pip install --user -r requirements.txt

CMD ["streamlit", "run", "home.py"]
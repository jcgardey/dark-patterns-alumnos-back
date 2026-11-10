FROM python:3.12.11-slim

ENV USER=api
ENV HOME=/usr/src/app
ENV PYTHONUNBUFFERED=1

WORKDIR ${HOME}

# Crear usuario del sistema no-root
RUN addgroup --system ${USER} --gid 1000 \
    && adduser --system --uid 1000 --gid 1000 ${USER}

# Instalar dependencias y descargar el modelo spaCy
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && python -m spacy download es_core_news_lg

# Copiar el proyecto
COPY . ${HOME}
RUN chown -R ${USER}:${USER} ${HOME}

USER ${USER}

EXPOSE 5000

# Servidor de producción WSGI optimizado para concurrencia
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--threads", "4", "--timeout", "120", "app:app"]

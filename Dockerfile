FROM python:3.12.11-slim

ENV USER=api
ENV HOME=/usr/src/app
ENV PYTHONUNBUFFERED=1

WORKDIR ${HOME}

# Crear usuario
RUN addgroup --system ${USER} --gid 1000 \
    && adduser --system --uid 1000 --gid 1000 ${USER}

# Instalar dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# El código se monta mediante docker-compose
RUN chown -R ${USER}:${USER} ${HOME}

USER ${USER}

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000", "--debug"]
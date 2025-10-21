FROM python:3.12.11-slim

ENV USER=api
ENV HOME=/usr/src/app
WORKDIR ${HOME}
COPY . .

# Create a group and user
RUN addgroup --system ${USER} --gid 1000 && adduser -u 1000 --gid 1000 ${USER} 
RUN usermod -aG sudo ${USER}

RUN pip install -r requirements.txt
RUN chown -R ${USER}:${USER} /usr/src/app
USER ${USER} 

EXPOSE 5000
CMD ["flask", "run", "--host=0.0.0.0"] 
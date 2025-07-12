FROM n8nio/n8n

USER root

WORKDIR /data

COPY package.json ./
RUN npm install && chown -R node:node /data/node_modules

USER node

WORKDIR /home/node/.n8n
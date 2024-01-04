FROM node:lts-alpine

WORKDIR /app

COPY package.json /app
COPY package-lock.json /app

RUN npm install

EXPOSE 3000

CMD ["npm", "start"]

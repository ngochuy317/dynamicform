FROM node:14
RUN npm cache clean --f
WORKDIR /code
COPY package*.json ./
RUN npm install
EXPOSE 3000
CMD ["npm", "run", "dev"]
FROM node:20-alpine

WORKDIR /app

COPY package.json ./
RUN yarn install

COPY . .
RUN yarn build
RUN npm install -g serve

EXPOSE 3000
CMD ["serve", "-s", "dist"]
FROM node:10.20.1-buster as build

WORKDIR /app
COPY ./package* ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:1.17.10

WORKDIR /app
COPY ./nginx.conf /etc/nginx
COPY --from=build /app/dist /app/dist
# RUN service nginx restart;
CMD  ["nginx", "-g", "daemon off;"]

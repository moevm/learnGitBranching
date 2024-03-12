FROM node:20-alpine

# Create app directory
WORKDIR /app

# Create front directory
RUN mkdir -p /app/front
# Create server directory
RUN mkdir -p /app/server
RUN mkdir -p /app/server/src/dist

# Install front dependencies and build front app
WORKDIR /app/front
COPY ./front ./
RUN npm install
RUN yarn gulp fastBuild

# Install server dependencies and run server app
WORKDIR /app/server
COPY ./server ./
COPY ./.env ./

# Copy front build to server
RUN ["mv", "/app/front/index.html", "/app/server/src/dist/index.html"]
RUN ["mv", "/app/front/build", "/app/server/src/dist/build"]
RUN ["mv", "/app/front/assets", "/app/server/src/dist/assets"]
EXPOSE 3000/tcp
RUN ["npm", "install"]
#RUN ["npm", "run", "start:dev"]

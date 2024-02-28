FROM node:20-alpine

# Create app directory
WORKDIR /app

# Create front directory
RUN mkdir -p /app/front
# Create server directory
RUN mkdir -p /app/server
RUN mkdir -p /app/server/dist

# Install front dependencies and build front app
WORKDIR /app/front
COPY ./front ./
RUN ["npm", "install"]
CMD ["yarn", "gulp", "fastBuild"]

# Copy front build to server
CMD ["mv", "/app/front/index.html", "/app/server/dist/src/index.html"]
CMD ["mv", "/app/front/build", "/app/server/src/dist/build"]
CMD ["mv", "/app/front/assets", "/app/server/src/dist/assets"]

# Delete front source code
WORKDIR /app
CMD ["rm", "-rf", "./front"]

# Install server dependencies and run server app
WORKDIR /app/server
COPY ./server ./
EXPOSE 3000
RUN ["npm", "install"]
RUN ["cat", "/app/server/src/dist/index.html"]
CMD ["npm", "run", "start:dev"]

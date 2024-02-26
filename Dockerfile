FROM node:20-alpine

# Create app directory
WORKDIR /app

# Create front directory
RUN mkdir -p /app/front
# Create server directory
RUN mkdir -p /app/server
RUN mkdir -p /app/server/dist

# Install front dependencies
WORKDIR /app/front

COPY ./front ./
#WORKDIR /app
#RUN ls -a
#WORKDIR /app/front
#RUN ls -a
CMD ["npm", "install"]
CMD ["yarn", "gulp", "fastBuild"]
RUN ls -a
#RUN cat ./index.html

# Copy front build to server
RUN ["mv", "/app/front/index.html", "/app/server/dist/index.html"]
RUN ["mv", "/app/front/build", "/app/server/dist/build"]
RUN ["mv", "/app/front/assets", "/app/server/dist/assets"]

# Install server dependencies
WORKDIR /app/server
COPY /server/package*.json ./
CMD ["npm", "install"]
CMD ["npm", "cache", "clean", "--force"]

# Build app source
WORKDIR /app/server
COPY ./server ./
EXPOSE 3000
CMD ["npm", "run", "start:dev"]

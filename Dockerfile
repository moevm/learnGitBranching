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
RUN ["npm", "install"]
CMD ["yarn", "gulp", "fastBuild"]
CMD ["ls", "-a"]
#RUN cat ./index.html

# Copy front build to server
CMD ["mv", "/app/front/index.html", "/app/server/dist/index.html"]
CMD ["mv", "/app/front/build", "/app/server/dist/build"]
CMD ["mv", "/app/front/assets", "/app/server/dist/assets"]
RUN ["ls", "-a"]

# Install server dependencies
WORKDIR /app/server
COPY /server/package*.json ./
RUN ["cat", "package.json"]
RUN ["npm", "install"]
CMD ["npm", "cache", "clean", "--force"]

# Build app source
WORKDIR /app/server
COPY ./server ./
EXPOSE 3000
RUN ["ls", "-a"]
#RUN ["npm", "list"]
RUN ["npm", "install"]
CMD ["npm", "run", "start:dev"]

FROM node:20-alpine

# Create app directory
WORKDIR /app


# Install app dependencies
COPY package*.json ./
RUN npm install


# Build app source
COPY . .
EXPOSE 3000
CMD ["npm", "run", "start:dev"]

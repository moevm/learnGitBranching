# syntax=docker/dockerfile:1.7
FROM node:20-alpine

WORKDIR /app

# Install and cache front-end dependencies separately from the source code.
# The retry loop is intentional: npm registry connections were unstable in the
# target environment, while BuildKit's cache avoids downloading successful
# packages again on the next attempt/build.
WORKDIR /app/front
COPY ./front/package.json ./front/package-lock.json ./
RUN --mount=type=cache,target=/root/.npm \
    set -eu; \
    for attempt in 1 2 3 4 5; do \
        echo "front npm ci: attempt ${attempt}/5"; \
        rm -rf /app/front/node_modules; \
        if npm ci --include=dev \
            --prefer-offline \
            --no-audit \
            --no-fund \
            --maxsockets=1 \
            --fetch-retries=10 \
            --fetch-retry-factor=2 \
            --fetch-retry-mintimeout=10000 \
            --fetch-retry-maxtimeout=120000 \
            --fetch-timeout=600000; then \
            break; \
        fi; \
        if [ "$attempt" -eq 5 ]; then \
            exit 1; \
        fi; \
        echo "Connection failed; retrying in 10 seconds..."; \
        sleep 10; \
    done; \
    test -x ./node_modules/.bin/gulp

COPY ./front ./
RUN ./node_modules/.bin/gulp fastBuild

# Install server dependencies. Development dependencies are required at
# runtime because docker-compose starts the server through nodemon/Babel.
WORKDIR /app/server
COPY ./server/package.json ./server/package-lock.json ./
RUN --mount=type=cache,target=/root/.npm \
    set -eu; \
    for attempt in 1 2 3 4 5 6 7 8 9 10; do \
        echo "server npm ci: attempt ${attempt}/10"; \
        rm -rf /app/server/node_modules; \
        if npm ci --include=dev \
            --prefer-offline \
            --no-audit \
            --no-fund \
            --maxsockets=1 \
            --fetch-retries=10 \
            --fetch-retry-factor=2 \
            --fetch-retry-mintimeout=10000 \
            --fetch-retry-maxtimeout=120000 \
            --fetch-timeout=600000 \
            --loglevel=http; then \
            break; \
        fi; \
        if [ "$attempt" -eq 10 ]; then \
            exit 1; \
        fi; \
        echo "Connection failed; retrying in 30 seconds..."; \
        sleep 30; \
    done; \
    test -x ./node_modules/.bin/nodemon

COPY ./server ./

# Copy the browser build into the directory served by NestJS.
RUN mkdir -p /app/server/src/dist \
    && mv /app/front/index.html /app/server/src/dist/index.html \
    && mv /app/front/build /app/server/src/dist/build \
    && mv /app/front/assets /app/server/src/dist/assets

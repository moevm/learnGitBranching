import * as dotenv from 'dotenv'

// Docker Compose injects values from the root .env through env_file.
// dotenv.config() still supports launching the server directly from the
// server directory, but the application no longer requires .env to be copied
// into the Docker image during build.
dotenv.config()
export const env = process.env

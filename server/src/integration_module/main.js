import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import cors from 'cors';
const cookieParser = require('cookie-parser')


async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.use(cors({
    credentials: true,
    origin: true,
  }))
  app.use(cookieParser());
  await app.listen(80);
}

bootstrap();

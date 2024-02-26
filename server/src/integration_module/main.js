import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import cors from 'cors'


async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.use(cors({
    credentials: true,
    origin: true,
  }))
  await app.listen(3000);
}
bootstrap();


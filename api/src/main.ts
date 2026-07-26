import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { ConfigService } from '@nestjs/config';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  // ── Read port from .env ──
  const configService = app.get(ConfigService);
  const port = configService.get<number>('PORT', 3000);

  // ── Swagger docs at /docs ──
  const swaggerConfig = new DocumentBuilder()
    .setTitle('NestJS Learning API')
    .setDescription('Learning NestJS routing concepts')
    .setVersion('1.0')
    .build();
  const document = SwaggerModule.createDocument(app, swaggerConfig);
  SwaggerModule.setup('docs', app, document);

  await app.listen(port);
  console.log(`Server: http://localhost:${port}`);
  console.log(`Docs: http://localhost:${port}/docs`);
}

bootstrap().catch((err) => {
  console.error('Startup failed:', err);
  process.exit(1);
});

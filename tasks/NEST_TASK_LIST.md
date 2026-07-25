# NestJS Learning Lab — Task Checklist (Production-Grade Edition)

> **How to use:** Work through each group in order. Each task tells you **what to create**,
> **what code to write**, and **how to test it** with curl or the browser.
> Mark `[x]` as you complete each task.
>
> **Philosophy:** From day one, we use a real-world folder structure, repository pattern,
> standardized responses, environment validation, Swagger documentation, and database
> migrations. This isn't a toy — it's how production NestJS apps are built.

---

## Target Folder Structure (This is what we're building toward)

```
nest-learn/
├── docker-compose.yml
├── .env                          # NEVER committed
├── .env.example                  # Committed template
├── .gitignore
├── package.json
├── tsconfig.json
├── tsconfig.build.json
├── nest-cli.json
├── .eslintrc.js
├── .prettierrc
│
└── src/
    ├── main.ts                   # App bootstrap
    ├── app.module.ts             # Root module
    │
    ├── config/                   # ── Configuration ──
    │   ├── app.config.ts         # App-level settings
    │   ├── database.config.ts    # Database settings
    │   ├── config.module.ts      # Config module (validates env vars)
    │   ├── env.validation.ts     # Env var validation schema
    │   └── index.ts
    │
    ├── database/                 # ── Database ──
    │   ├── typeorm.config.ts     # TypeORM data source (for migrations)
    │   ├── migrations/           # Generated migration files
    │   └── seeds/                # Seed data
    │
    ├── common/                   # ── Shared Across All Modules ──
    │   ├── constants/
    │   │   ├── error-codes.ts
    │   │   └── index.ts
    │   ├── decorators/
    │   │   ├── current-user.decorator.ts
    │   │   ├── public.decorator.ts
    │   │   └── index.ts
    │   ├── dto/                  # Shared DTOs
    │   │   ├── pagination.dto.ts
    │   │   ├── paginated-response.dto.ts
    │   │   ├── api-response.dto.ts
    │   │   └── index.ts
    │   ├── entities/
    │   │   └── base.entity.ts    # Base entity (id, timestamps, soft-delete)
    │   ├── enums/
    │   │   └── index.ts
    │   ├── exceptions/
    │   │   └── index.ts
    │   ├── filters/
    │   │   ├── http-exception.filter.ts
    │   │   └── index.ts
    │   ├── guards/
    │   │   ├── api-key.guard.ts
    │   │   ├── admin.guard.ts
    │   │   └── index.ts
    │   ├── interceptors/
    │   │   ├── response-wrapper.interceptor.ts
    │   │   ├── request-id.interceptor.ts
    │   │   ├── logging.interceptor.ts
    │   │   └── index.ts
    │   ├── interfaces/
    │   │   └── index.ts
    │   ├── middleware/
    │   │   ├── request-timer.middleware.ts
    │   │   └── index.ts
    │   ├── pipes/
    │   │   ├── parse-object-id.pipe.ts
    │   │   └── index.ts
    │   └── types/
    │       └── index.ts
    │
    ├── modules/                  # ── Feature Modules ──
    │   ├── items/
    │   │   ├── dto/
    │   │   │   ├── create-item.dto.ts
    │   │   │   ├── update-item.dto.ts
    │   │   │   ├── item-response.dto.ts
    │   │   │   ├── filter-item.dto.ts
    │   │   │   └── index.ts
    │   │   ├── entities/
    │   │   │   └── item.entity.ts
    │   │   ├── repositories/
    │   │   │   └── item.repository.ts
    │   │   ├── services/
    │   │   │   └── item.service.ts
    │   │   ├── controllers/
    │   │   │   └── item.controller.ts
    │   │   ├── items.module.ts
    │   │   └── index.ts
    │   │
    │   ├── users/
    │   │   ├── dto/
    │   │   ├── entities/
    │   │   ├── repositories/
    │   │   ├── services/
    │   │   ├── controllers/
    │   │   ├── users.module.ts
    │   │   └── index.ts
    │   │
    │   ├── auth/          # (for Group 10+)
    │   ├── admin/         # (for Group 15)
    │   └── websocket/     # (for Group 14)
    │
    └── health/                  # ── Health Check ──
        ├── health.controller.ts
        ├── health.module.ts
        └── index.ts
```

---

## Group 0 — Project Setup, Docker, Database & Production Foundation

### Task 0.1: Install NestJS CLI globally
```bash
npm install -g @nestjs/cli
```

### Task 0.2: Create the NestJS project with strict TypeScript
```bash
nest new nest-learn --strict
cd nest-learn
# Choose npm as the package manager
```

### Task 0.3: Install ALL production foundation dependencies
```bash
# Database
npm install --save @nestjs/typeorm typeorm pg

# Configuration & validation
npm install --save @nestjs/config class-validator class-transformer

# Security
npm install --save helmet @nestjs/throttler

# API documentation
npm install --save @nestjs/swagger

# Utility
npm install --save cookie-parser
npm install --save-dev @types/cookie-parser @types/multer
```

### Task 0.4: Set up TypeScript path aliases
In `tsconfig.json`, add path aliases (so you can write `@common/`, `@modules/`, `@config/`):
```json
{
  "compilerOptions": {
    "paths": {
      "@common/*": ["./src/common/*"],
      "@modules/*": ["./src/modules/*"],
      "@config/*": ["./src/config/*"],
      "@database/*": ["./src/database/*"]
    }
  }
}
```

Also update `tsconfig.build.json` and `nest-cli.json` to support path aliases during builds
(install `tsconfig-paths` for jest if needed).

### Task 0.5: Create docker-compose.yml (at project root)
```yaml
services:
  postgres:
    image: postgres:16-alpine
    container_name: nest-postgres
    restart: unless-stopped
    environment:
      POSTGRES_USER: nest
      POSTGRES_PASSWORD: nest
      POSTGRES_DB: nest_learn
    ports:
      - "5400:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U nest -d nest_learn"]
      interval: 5s
      timeout: 5s
      retries: 5

  pgadmin:
    image: dpage/pgadmin4:latest
    container_name: nest-pgadmin
    restart: unless-stopped
    environment:
      PGADMIN_DEFAULT_EMAIL: admin@admin.com
      PGADMIN_DEFAULT_PASSWORD: admin
    ports:
      - "5050:80"
    volumes:
      - pgadmin-data:/var/lib/pgadmin
    depends_on:
      postgres:
        condition: service_healthy

volumes:
  pgdata:
  pgadmin-data:
```

### Task 0.6: Start the containers
```bash
docker compose up -d
docker compose ps
# Should see postgres (healthy) and pgadmin running
```

### Task 0.7: Verify pgAdmin
Open [http://localhost:5050](http://localhost:5050)
- Login: `admin@admin.com` / `admin`
- Add server: host=`postgres`, port=`5432`, user=`nest`, password=`nest`, db=`nest_learn`

### Task 0.8: Create `.env` (NEVER commit)
```
# ── App ──
NODE_ENV=development
PORT=3000
API_PREFIX=api

# ── Database ──
DATABASE_HOST=localhost
DATABASE_PORT=5400
DATABASE_USER=nest
DATABASE_PASSWORD=nest
DATABASE_NAME=nest_learn

# ── Auth ──
API_KEY=dev-api-key-change-in-production
ADMIN_API_KEY=dev-admin-key-change-in-production

# ── Throttle ──
THROTTLE_TTL=60
THROTTLE_LIMIT=100
```

### Task 0.9: Create `.env.example` (committed to git)
```
NODE_ENV=development
PORT=3000
API_PREFIX=api
DATABASE_HOST=localhost
DATABASE_PORT=5400
DATABASE_USER=nest
DATABASE_PASSWORD=changeme
DATABASE_NAME=nest_learn
API_KEY=your-api-key-here
ADMIN_API_KEY=your-admin-api-key-here
THROTTLE_TTL=60
THROTTLE_LIMIT=100
```

### Task 0.10: Verify/update `.gitignore`
```
node_modules/
dist/
.env
.env.local
.env.*.local
uploads/
*.log
coverage/
```

### Task 0.11: Create `src/common/entities/base.entity.ts`
Every entity in the project extends this:
```typescript
import {
  PrimaryGeneratedColumn,
  CreateDateColumn,
  UpdateDateColumn,
  DeleteDateColumn,
} from 'typeorm';

export abstract class BaseEntity {
  @PrimaryGeneratedColumn()
  id: number;

  @CreateDateColumn({ type: 'timestamptz' })
  createdAt: Date;

  @UpdateDateColumn({ type: 'timestamptz' })
  updatedAt: Date;

  @DeleteDateColumn({ type: 'timestamptz', nullable: true })
  deletedAt: Date | null;  // soft delete
}
```

### Task 0.12: Create `src/config/env.validation.ts` — env var validation
Validate environment variables at startup so you fail fast, not at query time:
```typescript
import { IsString, IsNumber, IsEnum, validateSync } from 'class-validator';
import { plainToInstance, Transform } from 'class-transformer';

enum Environment {
  Development = 'development',
  Production = 'production',
  Test = 'test',
}

export class EnvironmentVariables {
  @IsEnum(Environment)
  NODE_ENV: Environment;

  @IsNumber()
  @Transform(({ value }) => parseInt(value, 10))
  PORT: number;

  @IsString()
  API_PREFIX: string;

  @IsString()
  DATABASE_HOST: string;

  @IsNumber()
  @Transform(({ value }) => parseInt(value, 10))
  DATABASE_PORT: number;

  @IsString()
  DATABASE_USER: string;

  @IsString()
  DATABASE_PASSWORD: string;

  @IsString()
  DATABASE_NAME: string;

  @IsString()
  API_KEY: string;

  @IsString()
  ADMIN_API_KEY: string;

  @IsNumber()
  @Transform(({ value }) => parseInt(value, 10))
  THROTTLE_TTL: number;

  @IsNumber()
  @Transform(({ value }) => parseInt(value, 10))
  THROTTLE_LIMIT: number;
}

export function validate(config: Record<string, unknown>) {
  const validatedConfig = plainToInstance(EnvironmentVariables, config, {
    enableImplicitConversion: true,
  });

  const errors = validateSync(validatedConfig, {
    skipMissingProperties: false,
  });

  if (errors.length > 0) {
    throw new Error(`Environment validation failed: ${errors.toString()}`);
  }

  return validatedConfig;
}
```

### Task 0.13: Create `src/config/app.config.ts`
```typescript
import { registerAs } from '@nestjs/config';

export const appConfig = registerAs('app', () => ({
  nodeEnv: process.env.NODE_ENV,
  port: parseInt(process.env.PORT!, 10),
  apiPrefix: process.env.API_PREFIX,
}));
```

### Task 0.14: Create `src/config/database.config.ts`
```typescript
import { registerAs } from '@nestjs/config';

export const databaseConfig = registerAs('database', () => ({
  host: process.env.DATABASE_HOST,
  port: parseInt(process.env.DATABASE_PORT!, 10),
  username: process.env.DATABASE_USER,
  password: process.env.DATABASE_PASSWORD,
  database: process.env.DATABASE_NAME,
}));
```

### Task 0.15: Create `src/config/config.module.ts`
```typescript
import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { validate } from './env.validation';
import { appConfig } from './app.config';
import { databaseConfig } from './database.config';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      cache: true,
      validate,
      load: [appConfig, databaseConfig],
      envFilePath: ['.env'],
      expandVariables: true,
    }),
  ],
})
export class AppConfigModule {}
```

### Task 0.16: Create `src/database/typeorm.config.ts` — for migrations CLI
```typescript
import { DataSource } from 'typeorm';
import * as dotenv from 'dotenv';

dotenv.config();

export default new DataSource({
  type: 'postgres',
  host: process.env.DATABASE_HOST,
  port: parseInt(process.env.DATABASE_PORT!, 10),
  username: process.env.DATABASE_USER,
  password: process.env.DATABASE_PASSWORD,
  database: process.env.DATABASE_NAME,
  entities: ['dist/**/*.entity.js'],
  migrations: ['dist/database/migrations/*.js'],
  migrationsTableName: 'typeorm_migrations',
  // synchronize: false,  // MIGRATIONS ONLY in prod pattern
  // For learning: we'll use synchronize:true in dev mode only
});
```

### Task 0.17: Create `src/common/dto/api-response.dto.ts`
Standardized API response — EVERY endpoint wraps its data in this:
```typescript
export class ApiResponse<T = any> {
  success: boolean;
  data: T;
  message?: string;
  meta?: PaginationMeta;

  static ok<T>(data: T, meta?: PaginationMeta, message?: string): ApiResponse<T> {
    return { success: true, data, meta, message };
  }

  static fail(message: string): ApiResponse<null> {
    return { success: false, data: null, message };
  }
}

export interface PaginationMeta {
  page: number;
  pageSize: number;
  total: number;
  totalPages: number;
}
```

### Task 0.18: Create `src/common/dto/pagination.dto.ts`
Reusable pagination DTO — use in any controller:
```typescript
import { IsOptional, IsInt, Min, Max } from 'class-validator';
import { ApiPropertyOptional } from '@nestjs/swagger';
import { Type } from 'class-transformer';

export class PaginationDto {
  @ApiPropertyOptional({ default: 1, minimum: 1 })
  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @Min(1)
  page?: number = 1;

  @ApiPropertyOptional({ default: 20, minimum: 1, maximum: 100 })
  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @Min(1)
  @Max(100)
  pageSize?: number = 20;

  get skip(): number {
    return ((this.page ?? 1) - 1) * (this.pageSize ?? 20);
  }

  get take(): number {
    return this.pageSize ?? 20;
  }
}
```

### Task 0.19: Create the folder structure
```bash
# Create all directories at once
mkdir -p src/config
mkdir -p src/database/migrations
mkdir -p src/database/seeds
mkdir -p src/common/{constants,decorators,dto,entities,enums,exceptions,filters,guards,interceptors,interfaces,middleware,pipes,types}
mkdir -p src/modules/items/{dto,entities,repositories,services,controllers}
mkdir -p src/modules/users/{dto,entities,repositories,services,controllers}
mkdir -p src/health
```

### Task 0.20: Build `src/main.ts` — production-grade bootstrap
```typescript
import { NestFactory } from '@nestjs/core';
import { ValidationPipe, Logger, VersioningType } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import helmet from 'helmet';
import * as cookieParser from 'cookie-parser';
import { AppModule } from './app.module';
import { AllExceptionsFilter } from '@common/filters';
import { ResponseWrapperInterceptor } from '@common/interceptors';
import { RequestIdInterceptor } from '@common/interceptors';
import { setupSwagger } from './swagger';  // We'll create this in a later task

async function bootstrap() {
  const app = await NestFactory.create(AppModule, {
    bufferLogs: true,
  });

  const configService = app.get(ConfigService);
  const logger = new Logger('Bootstrap');

  // ── Security ──
  app.use(helmet());
  app.use(cookieParser());

  // ── CORS ──
  app.enableCors({
    origin: configService.get<string>('CORS_ORIGIN', '*'),
    methods: 'GET,HEAD,PUT,PATCH,POST,DELETE',
    credentials: true,
  });

  // ── Global prefix ──
  app.setGlobalPrefix(configService.get<string>('API_PREFIX', 'api'));

  // ── API Versioning ──
  app.enableVersioning({
    type: VersioningType.URI,
    defaultVersion: '1',
  });

  // ── Global pipes, filters, interceptors ──
  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true,
      forbidNonWhitelisted: true,
      transform: true,
      transformOptions: { enableImplicitConversion: true },
    }),
  );
  app.useGlobalFilters(new AllExceptionsFilter());
  app.useGlobalInterceptors(
    new RequestIdInterceptor(),
    new ResponseWrapperInterceptor(),
  );

  // ── Start ──
  const port = configService.get<number>('app.port', 3000);
  await app.listen(port);

  logger.log(`🚀 Application running on http://localhost:${port}`);
  logger.log(`📖 Swagger docs at http://localhost:${port}/api/docs`);
  logger.log(`🌍 Environment: ${configService.get('app.nodeEnv')}`);
}
bootstrap();
```

> ⚠️ Some imports above reference files we haven't created yet.
> The app won't start until Group 1 — that's fine. We're scaffolding the target first.

### Task 0.21: Build `src/app.module.ts`
```typescript
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { ConfigService } from '@nestjs/config';
import { ThrottlerModule, ThrottlerGuard } from '@nestjs/throttler';
import { APP_GUARD } from '@nestjs/core';
import { AppConfigModule } from '@config/config.module';

@Module({
  imports: [
    // ── Config (validates env vars) ──
    AppConfigModule,

    // ── Database ──
    TypeOrmModule.forRootAsync({
      imports: [AppConfigModule],
      inject: [ConfigService],
      useFactory: (config: ConfigService) => ({
        type: 'postgres',
        host: config.get<string>('database.host'),
        port: config.get<number>('database.port'),
        username: config.get<string>('database.username'),
        password: config.get<string>('database.password'),
        database: config.get<string>('database.database'),
        autoLoadEntities: true,
        // synchronize: true in DEV, migrations in PROD
        synchronize: config.get('app.nodeEnv') === 'development',
        logging: config.get('app.nodeEnv') === 'development' ? ['query', 'error'] : ['error'],
      }),
    }),

    // ── Rate limiting ──
    ThrottlerModule.forRootAsync({
      imports: [AppConfigModule],
      inject: [ConfigService],
      useFactory: (config: ConfigService) => ({
        throttlers: [{
          ttl: config.get<number>('THROTTLE_TTL', 60) * 1000,
          limit: config.get<number>('THROTTLE_LIMIT', 100),
        }],
      }),
    }),

    // Feature modules will be added here as we build them
  ],
  providers: [
    // Apply rate limiting globally
    { provide: APP_GUARD, useClass: ThrottlerGuard },
  ],
})
export class AppModule {}
```

### Task 0.22: Test the foundation
```bash
npm run start:dev
```
Expect: app starts, connects to PostgreSQL, no errors.
Open `http://localhost:3000/api` — you should get a JSON response.

> Note: if imports for not-yet-created files cause errors, stub them or comment them out.
> The point is to verify the DB connection and config loading works.

### Task 0.23: Set up TypeORM migration scripts in `package.json`
```json
{
  "scripts": {
    "typeorm": "npx ts-node -r tsconfig-paths/register ./node_modules/typeorm/cli.js",
    "migration:generate": "npm run typeorm -- migration:generate src/database/migrations/migration -d src/database/typeorm.config.ts",
    "migration:run": "npm run typeorm -- migration:run -d src/database/typeorm.config.ts",
    "migration:revert": "npm run typeorm -- migration:revert -d src/database/typeorm.config.ts"
  }
}
```

---

## Group 1 — Hello World (The Right Way)

### Task 1.1: Understand the structure
The NestJS CLI generates a basic `AppController` + `AppService`. We'll keep these but
move domain logic into `modules/`.

### Task 1.2: Create `src/common/interceptors/response-wrapper.interceptor.ts`
Every response is wrapped in `{ success: true, data: ... }` automatically:
```typescript
import {
  Injectable, NestInterceptor, ExecutionContext, CallHandler,
} from '@nestjs/common';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { ApiResponse, PaginationMeta } from '@common/dto';

@Injectable()
export class ResponseWrapperInterceptor<T> implements NestInterceptor<T, ApiResponse<T>> {
  intercept(context: ExecutionContext, next: CallHandler): Observable<ApiResponse<T>> {
    return next.handle().pipe(
      map((data) => {
        // Don't double-wrap if already an ApiResponse or if it's a raw response (e.g. file download)
        if (data?.success !== undefined) return data;
        return ApiResponse.ok(data);
      }),
    );
  }
}
```

### Task 1.3: Create `src/common/interceptors/request-id.interceptor.ts`
```typescript
import { Injectable, NestInterceptor, ExecutionContext, CallHandler } from '@nestjs/common';
import { Observable } from 'rxjs';
import { v4 as uuidv4 } from 'uuid'; // npm install uuid @types/uuid

@Injectable()
export class RequestIdInterceptor implements NestInterceptor {
  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const request = context.switchToHttp().getRequest();
    request.requestId = request.headers['x-request-id'] || uuidv4();
    return next.handle();
  }
}
```

### Task 1.4: Create `src/common/interceptors/index.ts`
```typescript
export * from './response-wrapper.interceptor';
export * from './request-id.interceptor';
```

### Task 1.5: Create `src/common/filters/http-exception.filter.ts`
Standardized error responses:
```typescript
import {
  ExceptionFilter, Catch, ArgumentsHost, HttpException, HttpStatus, Logger,
} from '@nestjs/common';
import { Request, Response } from 'express';

interface ErrorResponse {
  success: false;
  data: null;
  message: string;
  errorCode?: string;
  statusCode: number;
  timestamp: string;
  path: string;
  requestId?: string;
}

@Catch()
export class AllExceptionsFilter implements ExceptionFilter {
  private readonly logger = new Logger(AllExceptionsFilter.name);

  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const request = ctx.getRequest<Request>();

    let status: number;
    let message: string | object;

    if (exception instanceof HttpException) {
      status = exception.getStatus();
      message = exception.getResponse();
    } else {
      status = HttpStatus.INTERNAL_SERVER_ERROR;
      message = 'Internal server error';

      // Log unexpected errors with full stack trace
      this.logger.error(
        `Unhandled exception: ${exception instanceof Error ? exception.message : 'Unknown error'}`,
        exception instanceof Error ? exception.stack : undefined,
      );
    }

    const errorBody: ErrorResponse = {
      success: false,
      data: null,
      message: typeof message === 'string' ? message : (message as any).message || 'Error',
      statusCode: status,
      timestamp: new Date().toISOString(),
      path: request.url,
      requestId: (request as any).requestId,
    };

    response.status(status).json(errorBody);
  }
}
```

### Task 1.6: Create `src/common/filters/index.ts`
```typescript
export * from './http-exception.filter';
```

### Task 1.7: Create the Swagger setup file `src/swagger.ts`
```typescript
import { INestApplication } from '@nestjs/common';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';

export function setupSwagger(app: INestApplication): void {
  const config = new DocumentBuilder()
    .setTitle('NestJS Learning API')
    .setDescription('Production-grade NestJS API with PostgreSQL')
    .setVersion('1.0')
    .addApiKey({ type: 'apiKey', name: 'X-API-Key', in: 'header' }, 'api-key')
    .addTag('Items', 'Item CRUD operations')
    .addTag('Users', 'User management')
    .build();

  const document = SwaggerModule.createDocument(app, config);
  SwaggerModule.setup('api/docs', app, document);
}
```

Call `setupSwagger(app)` in `main.ts` (uncomment the import).

### Task 1.8: Verify the Hello route
Start the server:
```bash
npm run start:dev
```

Test:
```bash
curl http://127.0.0.1:3000/
curl http://127.0.0.1:3000/api            # with global prefix
curl http://127.0.0.1:3000/api/docs        # Swagger UI
```

### Task 1.9: Create a `src/common/dto/index.ts`
```typescript
export * from './api-response.dto';
export * from './pagination.dto';
```

---

## Group 2 — CRUD with Repository Pattern (Items)

### Task 2.1: Create `src/modules/items/entities/item.entity.ts`
Extend `BaseEntity` for free timestamps + soft delete:
```typescript
import { Entity, Column, Index } from 'typeorm';
import { BaseEntity } from '@common/entities/base.entity';

@Entity('items')
export class Item extends BaseEntity {
  @Column({ length: 255 })
  @Index()
  name: string;

  @Column({ type: 'decimal', precision: 10, scale: 2 })
  price: number;

  @Column({ nullable: true, length: 1000 })
  description: string | null;

  @Column({ name: 'in_stock', default: true })
  inStock: boolean;
}
```

### Task 2.2: Create DTOs for Items
**`src/modules/items/dto/create-item.dto.ts`:**
```typescript
import { IsString, IsNumber, IsOptional, IsBoolean, Min, MaxLength } from 'class-validator';
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';

export class CreateItemDto {
  @ApiProperty({ example: 'Laptop', description: 'Item name' })
  @IsString()
  @MaxLength(255)
  name: string;

  @ApiProperty({ example: 999.99, description: 'Price in USD' })
  @IsNumber()
  @Min(0)
  price: number;

  @ApiPropertyOptional({ example: 'A powerful laptop', description: 'Optional description' })
  @IsOptional()
  @IsString()
  @MaxLength(1000)
  description?: string;

  @ApiPropertyOptional({ default: true })
  @IsOptional()
  @IsBoolean()
  inStock?: boolean;
}
```

**`src/modules/items/dto/update-item.dto.ts`:**
```typescript
import { PartialType } from '@nestjs/swagger'; // Swagger-aware PartialType
import { CreateItemDto } from './create-item.dto';

export class UpdateItemDto extends PartialType(CreateItemDto) {}
```

**`src/modules/items/dto/item-response.dto.ts`:**
```typescript
import { Expose, Exclude } from 'class-transformer';
import { ApiProperty } from '@nestjs/swagger';

@Exclude()
export class ItemResponseDto {
  @ApiProperty()
  @Expose()
  id: number;

  @ApiProperty()
  @Expose()
  name: string;

  @ApiProperty()
  @Expose()
  price: number;

  @ApiProperty({ nullable: true })
  @Expose()
  description: string | null;

  @ApiProperty()
  @Expose()
  inStock: boolean;

  @ApiProperty()
  @Expose()
  createdAt: Date;

  @ApiProperty()
  @Expose()
  updatedAt: Date;

  constructor(partial: Partial<ItemResponseDto>) {
    Object.assign(this, partial);
  }
}
```

**`src/modules/items/dto/filter-item.dto.ts`:**
```typescript
import { IsOptional, IsString, IsNumber, IsBoolean } from 'class-validator';
import { Type, Transform } from 'class-transformer';
import { ApiPropertyOptional } from '@nestjs/swagger';
import { PaginationDto } from '@common/dto';

export class FilterItemDto extends PaginationDto {
  @ApiPropertyOptional({ description: 'Filter by name (ILIKE search)' })
  @IsOptional()
  @IsString()
  name?: string;

  @ApiPropertyOptional({ description: 'Max price filter' })
  @IsOptional()
  @Type(() => Number)
  @IsNumber()
  maxPrice?: number;

  @ApiPropertyOptional({ description: 'Filter by stock status' })
  @IsOptional()
  @Transform(({ value }) => value === 'true' || value === true)
  @IsBoolean()
  inStock?: boolean;
}
```

**`src/modules/items/dto/index.ts`:**
```typescript
export * from './create-item.dto';
export * from './update-item.dto';
export * from './item-response.dto';
export * from './filter-item.dto';
```

### Task 2.3: Create the Repository (Repository Pattern)
**`src/modules/items/repositories/item.repository.ts`:**
```typescript
import { Injectable } from '@nestjs/common';
import { DataSource, Repository, ILike, FindOptionsWhere } from 'typeorm';
import { Item } from '../entities/item.entity';
import { FilterItemDto } from '../dto';

@Injectable()
export class ItemRepository extends Repository<Item> {
  constructor(private dataSource: DataSource) {
    super(Item, dataSource.createEntityManager());
  }

  /**
   * Find items with filters and pagination.
   * Returns [items, totalCount].
   */
  async findFiltered(filters: FilterItemDto): Promise<[Item[], number]> {
    const where: FindOptionsWhere<Item> = {};

    if (filters.inStock !== undefined) {
      where.inStock = filters.inStock;
    }

    const queryBuilder = this.createQueryBuilder('item');

    if (filters.name) {
      queryBuilder.andWhere('item.name ILIKE :name', { name: `%${filters.name}%` });
    }

    if (filters.maxPrice !== undefined) {
      queryBuilder.andWhere('item.price <= :maxPrice', { maxPrice: filters.maxPrice });
    }

    if (filters.inStock !== undefined) {
      queryBuilder.andWhere('item.inStock = :inStock', { inStock: filters.inStock });
    }

    queryBuilder
      .skip(filters.skip)
      .take(filters.take)
      .orderBy('item.createdAt', 'DESC');

    return queryBuilder.getManyAndCount();
  }
}
```

> **Why Repository Pattern?** It encapsulates query logic. Services never write raw SQL or
> QueryBuilder. If you switch from TypeORM to Prisma later, you only change the repository.

### Task 2.4: Create the Service
**`src/modules/items/services/item.service.ts`:**
```typescript
import { Injectable, NotFoundException } from '@nestjs/common';
import { ItemRepository } from '../repositories/item.repository';
import { CreateItemDto, UpdateItemDto, FilterItemDto, ItemResponseDto } from '../dto';
import { PaginationMeta } from '@common/dto';

@Injectable()
export class ItemService {
  constructor(private readonly itemRepository: ItemRepository) {}

  async create(dto: CreateItemDto): Promise<ItemResponseDto> {
    const item = this.itemRepository.create(dto);
    const saved = await this.itemRepository.save(item);
    return new ItemResponseDto(saved);
  }

  async findAll(filters: FilterItemDto): Promise<{ items: ItemResponseDto[]; meta: PaginationMeta }> {
    const [items, total] = await this.itemRepository.findFiltered(filters);

    return {
      items: items.map(i => new ItemResponseDto(i)),
      meta: {
        page: filters.page ?? 1,
        pageSize: filters.pageSize ?? 20,
        total,
        totalPages: Math.ceil(total / (filters.pageSize ?? 20)),
      },
    };
  }

  async findOne(id: number): Promise<ItemResponseDto> {
    const item = await this.itemRepository.findOneBy({ id });
    if (!item) {
      throw new NotFoundException(`Item with ID ${id} not found`);
    }
    return new ItemResponseDto(item);
  }

  async update(id: number, dto: UpdateItemDto): Promise<ItemResponseDto> {
    const item = await this.itemRepository.findOneBy({ id });
    if (!item) {
      throw new NotFoundException(`Item with ID ${id} not found`);
    }
    Object.assign(item, dto);
    const updated = await this.itemRepository.save(item);
    return new ItemResponseDto(updated);
  }

  async remove(id: number): Promise<void> {
    const item = await this.itemRepository.findOneBy({ id });
    if (!item) {
      throw new NotFoundException(`Item with ID ${id} not found`);
    }
    await this.itemRepository.softRemove(item); // soft delete!
  }
}
```

### Task 2.5: Create the Controller
**`src/modules/items/controllers/item.controller.ts`:**
```typescript
import {
  Controller, Get, Post, Body, Patch, Param, Delete,
  HttpCode, HttpStatus, ParseIntPipe, Query,
} from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse as SwaggerResponse, ApiSecurity } from '@nestjs/swagger';
import { ItemService } from '../services/item.service';
import { CreateItemDto, UpdateItemDto, ItemResponseDto, FilterItemDto } from '../dto';

@ApiTags('Items')
@Controller('items')
export class ItemController {
  constructor(private readonly itemService: ItemService) {}

  @Post()
  @HttpCode(HttpStatus.CREATED)
  @ApiOperation({ summary: 'Create an item' })
  @SwaggerResponse({ status: 201, description: 'Item created', type: ItemResponseDto })
  @SwaggerResponse({ status: 400, description: 'Validation failed' })
  create(@Body() dto: CreateItemDto): Promise<ItemResponseDto> {
    return this.itemService.create(dto);
  }

  @Get()
  @ApiOperation({ summary: 'List items with pagination & filtering' })
  findAll(@Query() filters: FilterItemDto) {
    return this.itemService.findAll(filters);
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get a single item' })
  @SwaggerResponse({ status: 404, description: 'Item not found' })
  findOne(@Param('id', ParseIntPipe) id: number): Promise<ItemResponseDto> {
    return this.itemService.findOne(id);
  }

  @Patch(':id')
  @ApiOperation({ summary: 'Partial update of an item' })
  update(
    @Param('id', ParseIntPipe) id: number,
    @Body() dto: UpdateItemDto,
  ): Promise<ItemResponseDto> {
    return this.itemService.update(id, dto);
  }

  @Delete(':id')
  @HttpCode(HttpStatus.NO_CONTENT)
  @ApiOperation({ summary: 'Soft-delete an item' })
  remove(@Param('id', ParseIntPipe) id: number): Promise<void> {
    return this.itemService.remove(id);
  }
}
```

### Task 2.6: Create the Module + barrel export
**`src/modules/items/items.module.ts`:**
```typescript
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { Item } from './entities/item.entity';
import { ItemRepository } from './repositories/item.repository';
import { ItemService } from './services/item.service';
import { ItemController } from './controllers/item.controller';

@Module({
  imports: [TypeOrmModule.forFeature([Item])],
  controllers: [ItemController],
  providers: [ItemRepository, ItemService],
  exports: [ItemService], // export if other modules need it
})
export class ItemsModule {}
```

**`src/modules/items/index.ts`:**
```typescript
export * from './items.module';
export * from './dto';
export * from './entities/item.entity';
```

### Task 2.7: Register in AppModule
```typescript
// In src/app.module.ts, add:
import { ItemsModule } from '@modules/items';

@Module({
  imports: [
    // ... existing imports ...
    ItemsModule,
  ],
})
export class AppModule {}
```

### Task 2.8: Test full CRUD
```bash
# Create
curl -X POST http://127.0.0.1:3000/api/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "price": 999.0}'

curl -X POST http://127.0.0.1:3000/api/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Phone", "price": 699.0, "inStock": true}'

# List (paginated)
curl "http://127.0.0.1:3000/api/items?page=1&pageSize=10"

# List with filter
curl "http://127.0.0.1:3000/api/items?name=lap&maxPrice=1000"

# Get one
curl http://127.0.0.1:3000/api/items/1

# Partial update
curl -X PATCH http://127.0.0.1:3000/api/items/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Gaming Laptop"}'

# Delete (soft delete)
curl -X DELETE http://127.0.0.1:3000/api/items/1

# Open Swagger: http://localhost:3000/api/docs
```

---

## Group 3 — Path Parameters + Pipes

### Task 3.1: Create `src/modules/path-params/` module folder
```bash
mkdir -p src/modules/path-params/{controllers,services,pipes}
```

### Task 3.2: Create `src/modules/path-params/pipes/category.pipe.ts`
```typescript
import { PipeTransform, Injectable, BadRequestException } from '@nestjs/common';

const VALID_CATEGORIES = ['books', 'movies', 'music'] as const;
type Category = (typeof VALID_CATEGORIES)[number];

@Injectable()
export class CategoryValidationPipe implements PipeTransform<string, Category> {
  transform(value: string): Category {
    if (!VALID_CATEGORIES.includes(value as Category)) {
      throw new BadRequestException(
        `Invalid category "${value}". Allowed: ${VALID_CATEGORIES.join(', ')}`,
      );
    }
    return value as Category;
  }
}
```

### Task 3.3: Create `src/modules/path-params/controllers/path-params.controller.ts`
```typescript
import { Controller, Get, Param, ParseIntPipe } from '@nestjs/common';
import { ApiTags, ApiOperation } from '@nestjs/swagger';
import { CategoryValidationPipe } from '../pipes/category.pipe';

@ApiTags('Path Parameters')
@Controller('path-params')
export class PathParamsController {
  @Get('users/:userId')
  @ApiOperation({ summary: 'Int path param with ParseIntPipe' })
  getUser(@Param('userId', ParseIntPipe) userId: number) {
    return { userId, type: typeof userId };
  }

  @Get('users/:username/profile')
  @ApiOperation({ summary: 'String path param' })
  getProfile(@Param('username') username: string) {
    return { username, profile: { bio: 'Hello', joined: '2024' } };
  }

  @Get('orgs/:org/repos/:repo')
  @ApiOperation({ summary: 'Multiple path params' })
  getRepo(@Param('org') org: string, @Param('repo') repo: string) {
    return { org, repo, url: `https://github.com/${org}/${repo}` };
  }

  @Get('catalog/:category')
  @ApiOperation({ summary: 'Path param with custom validation pipe (Enum)' })
  getCatalog(@Param('category', CategoryValidationPipe) category: string) {
    return { category, items: [] };
  }
}
```

### Task 3.4: Create `src/modules/path-params/path-params.module.ts`
```typescript
import { Module } from '@nestjs/common';
import { PathParamsController } from './controllers/path-params.controller';

@Module({
  controllers: [PathParamsController],
})
export class PathParamsModule {}
```

### Task 3.5: Register in AppModule and test
```bash
curl http://127.0.0.1:3000/api/path-params/users/42
curl http://127.0.0.1:3000/api/path-params/users/abc           # 400
curl http://127.0.0.1:3000/api/path-params/users/alice/profile
curl http://127.0.0.1:3000/api/path-params/orgs/microsoft/repos/vscode
curl http://127.0.0.1:3000/api/path-params/catalog/books        # works
curl http://127.0.0.1:3000/api/path-params/catalog/games        # 400
```

---

## Group 4 — Query Parameters & DB-Backed Filtering

### Task 4.1: Extend the ItemsController
Add these endpoints to the existing items controller:

```typescript
// In items controller, add:

@Get('filter')
@ApiOperation({ summary: 'Filter items with dynamic query building' })
filterItems(@Query() filters: FilterItemDto) {
  // This already exists from Group 2! The findAll method does exactly this.
  return this.itemService.findAll(filters);
}

@Get('available')
@ApiOperation({ summary: 'Filter items by stock availability' })
findAvailable(
  @Query('inStock', new DefaultValuePipe(true), ParseBoolPipe) inStock: boolean,
) {
  return this.itemService.findAll({ inStock } as FilterItemDto);
}

@Get('by-ids')
@ApiOperation({ summary: 'Get items by comma-separated IDs' })
findByIds(@Query('ids', new ParseArrayPipe({ items: Number, separator: ',' })) ids: number[]) {
  return this.itemRepository.findByIds(ids);
  // Note: you may want to add a service method for this
}
```

### Task 4.2: Test
```bash
curl "http://127.0.0.1:3000/api/items?page=1&pageSize=2"
curl "http://127.0.0.1:3000/api/items/filter?name=phone"
curl "http://127.0.0.1:3000/api/items/filter?maxPrice=500&inStock=true"
curl "http://127.0.0.1:3000/api/items/available?inStock=false"
curl "http://127.0.0.1:3000/api/items/by-ids?ids=1,2,3"
```

---

## Group 5 — Request Body, Nested DTOs & User Entity

### Task 5.1: Create the User entity
`src/modules/users/entities/user.entity.ts`:
```typescript
import { Entity, Column, Index } from 'typeorm';
import { BaseEntity } from '@common/entities/base.entity';

@Entity('users')
export class User extends BaseEntity {
  @Column({ length: 100, unique: true })
  @Index()
  username: string;

  @Column({ length: 255, unique: true })
  email: string;

  @Column({ name: 'hashed_password', length: 255 })
  hashedPassword: string;  // Never return this in API responses

  @Column({ name: 'is_admin', default: false })
  isAdmin: boolean;
}
```

### Task 5.2: Create User DTOs
`src/modules/users/dto/create-user.dto.ts`:
```typescript
import { IsString, IsEmail, IsOptional, IsBoolean, MinLength, MaxLength } from 'class-validator';
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';

export class CreateUserDto {
  @ApiProperty({ example: 'alice' })
  @IsString()
  @MinLength(3)
  @MaxLength(100)
  username: string;

  @ApiProperty({ example: 'alice@example.com' })
  @IsEmail()
  email: string;

  @ApiProperty({ example: 'Str0ngP@ss!', minLength: 8 })
  @IsString()
  @MinLength(8)
  password: string;  // DTO uses 'password'; entity stores 'hashedPassword'

  @ApiPropertyOptional({ default: false })
  @IsOptional()
  @IsBoolean()
  isAdmin?: boolean;
}
```

### Task 5.3: Create nested DTOs (Address example)
`src/modules/users/dto/register-user.dto.ts`:
```typescript
import { IsString, IsEmail, IsArray, ValidateNested, IsPostalCode, ArrayMinSize } from 'class-validator';
import { Type } from 'class-transformer';
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';

export class AddressDto {
  @ApiProperty({ example: '123 Main St' })
  @IsString()
  street: string;

  @ApiProperty({ example: 'Springfield' })
  @IsString()
  city: string;

  @ApiProperty({ example: '62701' })
  @IsString()
  @IsPostalCode('US')
  zipCode: string;
}

export class RegisterUserDto {
  @ApiProperty({ example: 'Alice Johnson' })
  @IsString()
  name: string;

  @ApiProperty({ example: 'alice@example.com' })
  @IsEmail()
  email: string;

  @ApiProperty({ description: 'Nested address object' })
  @ValidateNested()
  @Type(() => AddressDto)
  address: AddressDto;

  @ApiPropertyOptional({ example: ['admin', 'beta-tester'] })
  @IsArray()
  @IsString({ each: true })
  @ArrayMinSize(1)
  tags: string[];
}
```

### Task 5.4: Create UserResponseDto — exclude sensitive fields
```typescript
import { Exclude, Expose } from 'class-transformer';
import { ApiProperty } from '@nestjs/swagger';

@Exclude()
export class UserResponseDto {
  @ApiProperty()
  @Expose()
  id: number;

  @ApiProperty()
  @Expose()
  username: string;

  @ApiProperty()
  @Expose()
  email: string;

  // hashedPassword is NOT @Expose'd → never leaks to client

  @ApiProperty()
  @Expose()
  isAdmin: boolean;

  @ApiProperty()
  @Expose()
  createdAt: Date;

  @ApiProperty()
  @Expose()
  updatedAt: Date;

  constructor(partial: Partial<UserResponseDto>) {
    Object.assign(this, partial);
  }
}
```

### Task 5.5: Create the UsersController (register endpoint)
```typescript
@Controller('users')
export class UsersController {
  @Post('register')
  @ApiOperation({ summary: 'Register a user with nested address' })
  register(@Body() dto: RegisterUserDto) {
    return { message: 'User registered', data: dto };
  }
}
```

### Task 5.6: Register UsersModule in AppModule and test
```bash
# Valid nested JSON
curl -X POST http://127.0.0.1:3000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice",
    "email": "alice@example.com",
    "address": {"street": "123 Main St", "city": "Springfield", "zipCode": "62701"},
    "tags": ["admin", "beta"]
  }'

# Validation failures
curl -X POST http://127.0.0.1:3000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{"name": "Bob"}'  # Missing fields → 400

curl -X POST http://127.0.0.1:3000/api/users/register \
  -H "Content-Type: application/json" \
  -d '{"name":"Bob","email":"bob@test.com","address":{"street":"1","city":"NYC","zipCode":"bad"},"tags":[]}'  # 400
```

---

## Group 6 — Response Serialization

### Task 6.1: Understand the pattern
We already use `@Exclude()` + `@Expose()` on our response DTOs. The `ClassSerializerInterceptor`
projects entity → DTO, stripping internal fields. In a production app, you ALWAYS have
response DTOs — never return raw entities.

### Task 6.2: Create a serialization test endpoint
Add to ItemsController:
```typescript
@Get(':id/raw')
@ApiOperation({ summary: 'Get raw entity (no serialization) — for comparison' })
async findOneRaw(@Param('id', ParseIntPipe) id: number) {
  // Bypass the response DTO to show the raw entity
  const item = await this.itemRepository.findOneByOrFail({ id });
  return item; // raw entity — has all columns including internal ones
}
```

### Task 6.3: Test serialization
```bash
curl http://127.0.0.1:3000/api/items/1        # filtered through ItemResponseDto
curl http://127.0.0.1:3000/api/items/1/raw    # raw entity (no filtering)
```

### Task 6.4: Add response_model_exclude_none equivalent
```typescript
// The ResponseWrapperInterceptor can be configured to strip nulls
// Or you can use @Transform(({ value }) => value ?? undefined) on specific fields
```

---

## Group 7 — Headers & Cookies

### Task 7.1: Create `src/modules/headers-cookies/` module
```bash
mkdir -p src/modules/headers-cookies/controllers
```

### Task 7.2: Create the controller
```typescript
import { Controller, Get, Headers, Res, Req } from '@nestjs/common';
import { ApiTags, ApiOperation, ApiHeader } from '@nestjs/swagger';
import { Request, Response } from 'express';

@ApiTags('Headers & Cookies')
@Controller('headers-cookies')
export class HeadersCookiesController {
  @Get('whoami')
  @ApiOperation({ summary: 'Read the User-Agent header' })
  whoami(@Headers('user-agent') userAgent: string) {
    return { userAgent };
  }

  @Get('custom')
  @ApiOperation({ summary: 'Read X-Request-Id header' })
  @ApiHeader({ name: 'X-Request-Id', description: 'Custom request ID' })
  customHeader(@Headers('x-request-id') requestId: string) {
    return { requestId };
  }

  @Get('read-cookie')
  @ApiOperation({ summary: 'Read a cookie named session_id' })
  readCookie(@Req() req: Request) {
    return { sessionId: req.cookies?.session_id ?? 'no cookie found' };
  }

  @Get('set-cookie')
  @ApiOperation({ summary: 'Set a response cookie' })
  setCookie(@Res({ passthrough: true }) res: Response) {
    res.cookie('session_id', 'uuid-' + Date.now(), {
      httpOnly: true,
      maxAge: 3600 * 1000,
      sameSite: 'lax',
    });
    return { message: 'Cookie set!' };
  }

  @Get('set-headers')
  @ApiOperation({ summary: 'Set custom response headers' })
  setHeaders(@Res({ passthrough: true }) res: Response) {
    res.set('X-Custom-Header', 'hello-from-nest');
    res.set('X-App-Version', '1.0.0');
    return { message: 'Custom headers set!' };
  }
}
```

### Task 7.3: Test
```bash
curl -H "User-Agent: MyApp/1.0" http://127.0.0.1:3000/api/headers-cookies/whoami
curl -H "X-Request-Id: abc-123" http://127.0.0.1:3000/api/headers-cookies/custom
curl -b "session_id=hello123" http://127.0.0.1:3000/api/headers-cookies/read-cookie
curl -v http://127.0.0.1:3000/api/headers-cookies/set-cookie
curl -v http://127.0.0.1:3000/api/headers-cookies/set-headers
```

---

## Group 8 — Status Codes

### Task 8.1: Create `src/modules/status-codes/` module
```bash
mkdir -p src/modules/status-codes/controllers
```

### Task 8.2: Create the controller
```typescript
import { Controller, Post, Delete, Get, Param, Body, HttpCode, HttpStatus, Res } from '@nestjs/common';
import { ApiTags, ApiOperation } from '@nestjs/swagger';
import { Response } from 'express';

@ApiTags('Status Codes')
@Controller('status-codes')
export class StatusCodesController {
  @Post('products')
  @HttpCode(HttpStatus.CREATED)
  @ApiOperation({ summary: 'Create → 201 Created' })
  createProduct(@Body() body: any) {
    return { id: 1, ...body };
  }

  @Post('products/upsert')
  @ApiOperation({ summary: 'Upsert → 200 or 201 dynamically' })
  async upsert(@Body() body: any, @Res() res: Response) {
    const existed = false; // pretend check
    return res.status(existed ? 200 : 201).json({ id: 1, ...body });
  }

  @Delete('products/:id')
  @HttpCode(HttpStatus.NO_CONTENT)
  @ApiOperation({ summary: 'Delete → 204 No Content' })
  remove(@Param('id') id: string) {
    return; // nothing returned → 204
  }

  @Get('old-resource')
  @ApiOperation({ summary: '301 Permanent Redirect' })
  redirectOld(@Res() res: Response) {
    return res.redirect(301, '/api/status-codes/products');
  }
}
```

### Task 8.3: Test
```bash
curl -v -X POST http://127.0.0.1:3000/api/status-codes/products \
  -H "Content-Type: application/json" -d '{"name":"Test"}'  # 201

curl -v -X DELETE http://127.0.0.1:3000/api/status-codes/products/1  # 204

curl -v http://127.0.0.1:3000/api/status-codes/old-resource  # 301
```

---

## Group 9 — Form Data & File Uploads

### Task 9.1: Create `src/modules/form-files/` module
```bash
mkdir -p src/modules/form-files/controllers
```

### Task 9.2: Install multer types (already done in Group 0)

### Task 9.3: Create the controller
```typescript
import {
  Controller, Post, Body, UseInterceptors, UploadedFile, UploadedFiles,
  HttpCode, HttpStatus,
} from '@nestjs/common';
import { FileInterceptor, FilesInterceptor } from '@nestjs/platform-express';
import { ApiTags, ApiOperation, ApiConsumes, ApiBody } from '@nestjs/swagger';
import { diskStorage } from 'multer';
import { extname } from 'path';

const storage = diskStorage({
  destination: './uploads',
  filename: (_req, file, cb) => {
    const uniqueSuffix = Date.now() + '-' + Math.round(Math.random() * 1e9);
    cb(null, `${uniqueSuffix}${extname(file.originalname)}`);
  },
});

@ApiTags('Form Data & Files')
@Controller('form-files')
export class FormFilesController {
  @Post('login')
  @HttpCode(HttpStatus.OK)
  @ApiOperation({ summary: 'Login via URL-encoded form data' })
  @ApiConsumes('application/x-www-form-urlencoded')
  login(
    @Body('username') username: string,
    @Body('password') password: string,
  ) {
    return { username, message: 'Login successful (demo)' };
  }

  @Post('upload')
  @UseInterceptors(FileInterceptor('file', { storage }))
  @ApiOperation({ summary: 'Upload a single file' })
  @ApiConsumes('multipart/form-data')
  uploadSingle(@UploadedFile() file: Express.Multer.File) {
    return {
      filename: file.originalname,
      size: file.size,
      mimetype: file.mimetype,
      storedPath: file.path,
    };
  }

  @Post('upload-multiple')
  @UseInterceptors(FilesInterceptor('files', 10, { storage }))
  @ApiOperation({ summary: 'Upload multiple files (max 10)' })
  @ApiConsumes('multipart/form-data')
  uploadMultiple(@UploadedFiles() files: Express.Multer.File[]) {
    return files.map(f => ({
      filename: f.originalname,
      size: f.size,
      mimetype: f.mimetype,
    }));
  }

  @Post('profile')
  @UseInterceptors(FileInterceptor('avatar', { storage }))
  @ApiOperation({ summary: 'Upload profile: form fields + avatar file' })
  @ApiConsumes('multipart/form-data')
  createProfile(
    @Body('name') name: string,
    @UploadedFile() avatar: Express.Multer.File,
  ) {
    return {
      name,
      avatarFilename: avatar?.originalname ?? 'none',
      avatarUrl: avatar?.path ?? null,
    };
  }
}
```

### Task 9.4: Test
```bash
# Form login
curl -X POST http://127.0.0.1:3000/api/form-files/login \
  -d "username=alice&password=secret"

# Single file upload
echo "test content" > /tmp/test.txt
curl -X POST http://127.0.0.1:3000/api/form-files/upload \
  -F "file=@/tmp/test.txt"

# Multiple file upload
echo "file 1" > /tmp/a.txt && echo "file 2" > /tmp/b.txt
curl -X POST http://127.0.0.1:3000/api/form-files/upload-multiple \
  -F "files=@/tmp/a.txt" -F "files=@/tmp/b.txt"

# Form + file
curl -X POST http://127.0.0.1:3000/api/form-files/profile \
  -F "name=Alice" -F "avatar=@/tmp/test.txt"
```

---

## Group 10 — Guards & Auth (API Key + Role-Based)

### Task 10.1: Create `src/common/guards/api-key.guard.ts`
```typescript
import { Injectable, CanActivate, ExecutionContext, UnauthorizedException } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { Reflector } from '@nestjs/core';
import { IS_PUBLIC_KEY } from '@common/decorators/public.decorator';

@Injectable()
export class ApiKeyGuard implements CanActivate {
  constructor(
    private readonly configService: ConfigService,
    private readonly reflector: Reflector,
  ) {}

  canActivate(context: ExecutionContext): boolean {
    // Skip if route is marked @Public()
    const isPublic = this.reflector.getAllAndOverride<boolean>(IS_PUBLIC_KEY, [
      context.getHandler(),
      context.getClass(),
    ]);
    if (isPublic) return true;

    const request = context.switchToHttp().getRequest();
    const apiKey = request.headers['x-api-key'];

    if (!apiKey) {
      throw new UnauthorizedException('Missing X-API-Key header');
    }

    const validKey = this.configService.get<string>('API_KEY');
    const adminKey = this.configService.get<string>('ADMIN_API_KEY');

    if (apiKey === validKey || apiKey === adminKey) {
      request.apiKey = apiKey;
      request.isAdmin = apiKey === adminKey;
      return true;
    }

    throw new UnauthorizedException('Invalid API key');
  }
}
```

### Task 10.2: Create `@Public()` decorator
`src/common/decorators/public.decorator.ts`:
```typescript
import { SetMetadata } from '@nestjs/common';

export const IS_PUBLIC_KEY = 'isPublic';
export const Public = () => SetMetadata(IS_PUBLIC_KEY, true);
```

### Task 10.3: Create Admin guard
`src/common/guards/admin.guard.ts`:
```typescript
import { Injectable, CanActivate, ExecutionContext, ForbiddenException } from '@nestjs/common';

@Injectable()
export class AdminGuard implements CanActivate {
  canActivate(context: ExecutionContext): boolean {
    const request = context.switchToHttp().getRequest();
    if (!request.isAdmin) {
      throw new ForbiddenException('Admin access required');
    }
    return true;
  }
}
```

### Task 10.4: Register guards globally in AppModule
```typescript
import { APP_GUARD } from '@nestjs/core';
import { ApiKeyGuard } from '@common/guards';

providers: [
  { provide: APP_GUARD, useClass: ThrottlerGuard },
  { provide: APP_GUARD, useClass: ApiKeyGuard }, // All routes require API key by default
],
```

### Task 10.5: Create a protected admin endpoint
```typescript
@ApiTags('Admin')
@Controller('admin')
@UseGuards(AdminGuard)
export class AdminController {
  @Get('dashboard')
  @ApiSecurity('api-key')
  dashboard(@Req() req: Request) {
    return {
      message: 'Welcome admin!',
      apiKey: (req as any).apiKey,
      timestamp: new Date().toISOString(),
    };
  }

  @Get('stats')
  @ApiSecurity('api-key')
  stats() {
    return { users: 42, items: 128, uptime: process.uptime() };
  }
}
```

### Task 10.6: Mark public routes
```typescript
// In the HelloController or ItemsController:
@Public()
@Get('ping')
ping() {
  return { status: 'ok' };
}
```

### Task 10.7: Test guards
```bash
# Without API key → 401
curl http://127.0.0.1:3000/api/items

# With valid key → works
curl -H "X-API-Key: dev-api-key-change-in-production" http://127.0.0.1:3000/api/items

# Admin endpoint with non-admin key → 403
curl -H "X-API-Key: dev-api-key-change-in-production" http://127.0.0.1:3000/api/admin/dashboard

# Admin endpoint with admin key → works
curl -H "X-API-Key: dev-admin-key-change-in-production" http://127.0.0.1:3000/api/admin/dashboard

# Public route → no key needed
curl http://127.0.0.1:3000/api/ping
```

---

## Group 11 — Error Handling (Custom Exceptions)

### Task 11.1: Create `src/common/exceptions/item-not-found.exception.ts`
```typescript
import { NotFoundException } from '@nestjs/common';
import { ERROR_CODES } from '@common/constants';

export class ItemNotFoundException extends NotFoundException {
  constructor(id: number) {
    super({
      message: `Item with ID ${id} not found`,
      errorCode: ERROR_CODES.ITEM_NOT_FOUND,
    });
  }
}
```

### Task 11.2: Create `src/common/constants/error-codes.ts`
```typescript
export const ERROR_CODES = {
  ITEM_NOT_FOUND: 'ITEM_NOT_FOUND',
  USER_NOT_FOUND: 'USER_NOT_FOUND',
  VALIDATION_FAILED: 'VALIDATION_FAILED',
  UNAUTHORIZED: 'UNAUTHORIZED',
  FORBIDDEN: 'FORBIDDEN',
  INTERNAL_ERROR: 'INTERNAL_ERROR',
} as const;
```

### Task 11.3: Use the custom exception in ItemService
Replace `throw new NotFoundException(...)` with `throw new ItemNotFoundException(id)`.

### Task 11.4: Test error responses
```bash
curl http://127.0.0.1:3000/api/items/99999  # 404 with errorCode
curl -X POST http://127.0.0.1:3000/api/items \
  -H "Content-Type: application/json" \
  -d '{"bad": "data"}'                       # 400 validation error
```

---

## Group 12 — Middleware (Request Timer + Logging)

### Task 12.1: Create `src/common/middleware/request-timer.middleware.ts`
```typescript
import { Injectable, NestMiddleware, Logger } from '@nestjs/common';
import { Request, Response, NextFunction } from 'express';

@Injectable()
export class RequestTimerMiddleware implements NestMiddleware {
  private readonly logger = new Logger('HTTP');

  use(req: Request, res: Response, next: NextFunction) {
    const start = Date.now();
    const { method, originalUrl } = req;

    res.on('finish', () => {
      const duration = Date.now() - start;
      const { statusCode } = res;
      res.setHeader('X-Response-Time-ms', duration.toString());

      if (statusCode >= 400) {
        this.logger.warn(`${method} ${originalUrl} → ${statusCode} (${duration}ms)`);
      } else {
        this.logger.log(`${method} ${originalUrl} → ${statusCode} (${duration}ms)`);
      }
    });

    next();
  }
}
```

### Task 12.2: Register in AppModule
```typescript
import { MiddlewareConsumer, Module, NestModule } from '@nestjs/common';
import { RequestTimerMiddleware } from '@common/middleware';

export class AppModule implements NestModule {
  configure(consumer: MiddlewareConsumer) {
    consumer.apply(RequestTimerMiddleware).forRoutes('*');
  }
}
```

### Task 12.3: Create a logging interceptor
`src/common/interceptors/logging.interceptor.ts`:
```typescript
import { Injectable, NestInterceptor, ExecutionContext, CallHandler, Logger } from '@nestjs/common';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

@Injectable()
export class LoggingInterceptor implements NestInterceptor {
  private readonly logger = new Logger(LoggingInterceptor.name);

  intercept(context: ExecutionContext, next: CallHandler): Observable<any> {
    const request = context.switchToHttp().getRequest();
    const { method, url, body, requestId } = request;

    this.logger.log(`→ ${method} ${url}`, requestId ? `[${requestId}]` : '');

    if (Object.keys(body || {}).length > 0) {
      this.logger.debug(`  Body: ${JSON.stringify(body)}`);
    }

    return next.handle().pipe(
      tap(() => this.logger.log(`← ${method} ${url}`, requestId ? `[${requestId}]` : '')),
    );
  }
}
```

### Task 12.4: Test
```bash
curl -v http://127.0.0.1:3000/api/items
# Look for X-Response-Time-ms header
# Check server console for structured logs
```

---

## Group 13 — Background Tasks (Event Emitter + Scheduling)

### Task 13.1: Install event emitter
```bash
npm install --save @nestjs/event-emitter @nestjs/schedule
```

### Task 13.2: Register in AppModule
```typescript
import { EventEmitterModule } from '@nestjs/event-emitter';
import { ScheduleModule } from '@nestjs/schedule';

@Module({
  imports: [
    // ...
    EventEmitterModule.forRoot(),
    ScheduleModule.forRoot(),
  ],
})
export class AppModule {}
```

### Task 13.3: Create `src/modules/items/events/item-created.event.ts`
```typescript
export class ItemCreatedEvent {
  constructor(
    public readonly itemId: number,
    public readonly itemName: string,
  ) {}
}
```

### Task 13.4: Emit event in ItemService.create()
```typescript
import { EventEmitter2 } from '@nestjs/event-emitter';
import { ItemCreatedEvent } from '../events/item-created.event';

// In constructor: add `private eventEmitter: EventEmitter2`

async create(dto: CreateItemDto): Promise<ItemResponseDto> {
  const item = this.itemRepository.create(dto);
  const saved = await this.itemRepository.save(item);

  this.eventEmitter.emit('item.created', new ItemCreatedEvent(saved.id, saved.name));

  return new ItemResponseDto(saved);
}
```

### Task 13.5: Create `src/modules/items/listeners/item-created.listener.ts`
```typescript
import { Injectable, Logger } from '@nestjs/common';
import { OnEvent } from '@nestjs/event-emitter';
import { ItemCreatedEvent } from '../events/item-created.event';

@Injectable()
export class ItemCreatedListener {
  private readonly logger = new Logger(ItemCreatedListener.name);

  @OnEvent('item.created', { async: true })
  handleItemCreated(event: ItemCreatedEvent) {
    // Simulate async work (email, search indexing, etc.)
    this.logger.log(`[BACKGROUND] Processing item #${event.itemId} "${event.itemName}"...`);

    // Simulated delay
    setTimeout(() => {
      this.logger.log(`[BACKGROUND] Done: item #${event.itemId} processed`);
    }, 1000);
  }
}
```

### Task 13.6: Create a scheduled task (cleanup)
`src/common/services/scheduled-tasks.service.ts`:
```typescript
import { Injectable, Logger } from '@nestjs/common';
import { Cron, CronExpression } from '@nestjs/schedule';

@Injectable()
export class ScheduledTasksService {
  private readonly logger = new Logger(ScheduledTasksService.name);

  @Cron(CronExpression.EVERY_DAY_AT_MIDNIGHT)
  handleNightlyCleanup() {
    this.logger.log('Running nightly cleanup...');
  }

  @Cron(CronExpression.EVERY_30_SECONDS)
  handleHeartbeat() {
    this.logger.debug('System heartbeat');
  }
}
```

### Task 13.7: Test — create an item and watch logs
```bash
curl -X POST http://127.0.0.1:3000/api/items \
  -H "X-API-Key: dev-api-key-change-in-production" \
  -H "Content-Type: application/json" \
  -d '{"name": "Monitor", "price": 299.99}'
# Check server console: response is instant, then background log appears
```

---

## Group 14 — WebSockets (Gateways)

### Task 14.1: Install WebSocket packages (already done if installed platform-socket.io)
```bash
npm install --save @nestjs/websockets @nestjs/platform-socket.io socket.io
```

### Task 14.2: Create `src/modules/websocket/events.gateway.ts`
```typescript
import {
  WebSocketGateway, WebSocketServer, SubscribeMessage,
  OnGatewayConnection, OnGatewayDisconnect, MessageBody, ConnectedSocket,
} from '@nestjs/websockets';
import { Server, Socket } from 'socket.io';
import { Logger } from '@nestjs/common';

@WebSocketGateway({
  namespace: '/events',
  cors: { origin: '*', credentials: true },
})
export class EventsGateway implements OnGatewayConnection, OnGatewayDisconnect {
  @WebSocketServer()
  server: Server;

  private readonly logger = new Logger(EventsGateway.name);
  private connectedClients = new Map<string, Socket>();

  handleConnection(client: Socket) {
    this.logger.log(`Client connected: ${client.id}`);
    this.connectedClients.set(client.id, client);
  }

  handleDisconnect(client: Socket) {
    this.logger.log(`Client disconnected: ${client.id}`);
    this.connectedClients.delete(client.id);
  }

  @SubscribeMessage('message')
  handleMessage(@ConnectedSocket() client: Socket, @MessageBody() payload: any) {
    this.logger.log(`Message from ${client.id}: ${JSON.stringify(payload)}`);

    // Echo to ALL connected clients
    this.server.emit('message', {
      from: client.id,
      text: payload,
      timestamp: new Date().toISOString(),
    });
  }

  @SubscribeMessage('joinRoom')
  handleJoinRoom(@ConnectedSocket() client: Socket, @MessageBody() room: string) {
    client.join(room);
    this.server.to(room).emit('message', {
      from: 'system',
      text: `${client.id} joined room "${room}"`,
    });
  }

  @SubscribeMessage('roomMessage')
  handleRoomMessage(
    @ConnectedSocket() client: Socket,
    @MessageBody() payload: { room: string; text: string },
  ) {
    this.server.to(payload.room).emit('message', {
      from: client.id,
      text: payload.text,
      timestamp: new Date().toISOString(),
    });
  }

  // Broadcast to all: `this.server.emit('event', data)`
  // Send to specific room: `this.server.to('roomName').emit('event', data)`
}
```

### Task 14.3: Create `src/modules/websocket/websocket.module.ts`
```typescript
import { Module } from '@nestjs/common';
import { EventsGateway } from './events.gateway';

@Module({
  providers: [EventsGateway],
})
export class WebsocketModule {}
```

### Task 14.4: Test with browser console
Create a file `ws-test.html` (anywhere, open in browser):
```html
<!DOCTYPE html>
<html>
<body>
<h1>WebSocket Test</h1>
<pre id="log"></pre>
<script src="https://cdn.socket.io/4.7.2/socket.io.min.js"></script>
<script>
const log = (msg) => document.getElementById('log').textContent += msg + '\n';
const socket = io('http://localhost:3000/events');
socket.on('connect', () => log('Connected: ' + socket.id));
socket.on('message', (data) => log('Received: ' + JSON.stringify(data)));
socket.emit('message', { text: 'Hello from browser!' });
</script>
</body>
</html>
```

---

## Group 15 — API Versioning, Admin Module & Router Nesting

### Task 15.1: Verify versioned routes work
Routes are already at `/v1/` due to the URI versioning in `main.ts`.
Also accessible at `/` (default version).

Test:
```bash
curl http://127.0.0.1:3000/api/v1/items
curl http://127.0.0.1:3000/api/items     # same (default version)
```

### Task 15.2: Create a v2 controller
```typescript
@ApiTags('Items V2')
@Controller({ path: 'items', version: '2' })
export class ItemsControllerV2 {
  @Get()
  findAllV2() {
    return {
      version: '2.0',
      items: [],
      _links: {
        self: '/api/v2/items',
        filter: '/api/v2/items?name=:name',
      },
    };
  }
}
```

### Task 15.3: Test versioning
```bash
curl http://127.0.0.1:3000/api/v1/items  # v1 (your full CRUD)
curl http://127.0.0.1:3000/api/v2/items  # v2 placeholder
```

### Task 15.4: Create AdminModule with router-level guards
```typescript
@Module({
  imports: [ItemsModule], // reuse items service
  controllers: [AdminController],
  providers: [],
})
export class AdminModule {}
```
All routes in AdminModule already require API key (global guard) + AdminGuard (per-controller).

### Task 15.5: Add a health endpoint
`src/health/health.controller.ts`:
```typescript
import { Controller, Get } from '@nestjs/common';
import { ApiTags, ApiOperation } from '@nestjs/swagger';
import { Public } from '@common/decorators/public.decorator';

@ApiTags('Health')
@Controller('health')
export class HealthController {
  @Get()
  @Public()  // No API key needed
  @ApiOperation({ summary: 'Health check' })
  check() {
    return {
      status: 'ok',
      uptime: process.uptime(),
      timestamp: new Date().toISOString(),
      memory: process.memoryUsage(),
    };
  }
}
```

---

## Group 16 — Build Your Own (Production-Style)

Now combine everything. Each option follows the same architecture:
`modules/<domain>/{entities, dto, repositories, services, controllers, events, listeners}`

### Option A: Todo API
- **Entity** `Todo`: extends `BaseEntity` → title, done (default false), dueDate (nullable)
- **Repository**: `TodoRepository` with `findByDone(done: boolean)` using query builder
- **Service**: `TodoService` with CRUD + `markComplete(id)` that emits `todo.completed`
- **Controller**: full CRUD + `GET ?done=true&page=1&pageSize=20`
- **Listener**: `TodoCompletedListener` that logs/sends notification
- **Swagger**: `@ApiTags('Todos')` with all response DTOs

### Option B: Blog API
- **Entity** `Post`: extends `BaseEntity` → title, body, author, publishedAt (nullable), tags (simple JSON array or separate entity)
- **Entity** `Comment`: extends `BaseEntity` → body, author, `@ManyToOne(() => Post, p => p.comments)`
- **Relationship**: `Post.comments` with `@OneToMany`
- **Repository**: `PostRepository.findWithComments()`, `CommentRepository`
- **Service**: `PostService` + `CommentService`
- **Controller**: CRUD for both, `GET /posts?tag=typescript&page=1`
- **File upload**: cover image for posts using `FileInterceptor`
- **Guard**: Admin-only for create/update/delete posts

### Option C: E-Commerce Product Catalog
- **Entity** `Product`: extends `BaseEntity` → name, price, description, imageUrl
- **Entity** `Category`: extends `BaseEntity` → name, slug, `@OneToMany(() => Product)`
- **Entity** `Review`: extends `BaseEntity` → rating (1-5), comment, author, `@ManyToOne(() => Product)`
- **Relationships**: Product ↔ Category (ManyToOne), Product ↔ Reviews (OneToMany)
- **Repository**: `ProductRepository.findByCategory()` with JOINs
- **Service**: filter by category slug, price range, min rating
- **Controller**: `GET /products?category=electronics&minPrice=100&maxPrice=1000&minRating=4`
- **Response DTOs**: `ProductWithReviewsDto`, `CategoryWithProductCountDto`

---

## Cheat Sheet — Commands

### NestJS CLI
```bash
nest g mo modules/<name>              # Module
nest g co modules/<name>/controllers  # Controller
nest g s  modules/<name>/services     # Service
nest g gu common/guards/<name>        # Guard
nest g in common/interceptors/<name>  # Interceptor
nest g mi common/middleware/<name>    # Middleware
nest g pi common/pipes/<name>         # Pipe
nest g f  common/filters/<name>       # Exception filter
nest g ga modules/websocket/<name>    # Gateway
```

### Testing
```bash
# Query parameters
curl "http://127.0.0.1:3000/api/items?page=1&pageSize=5&name=laptop"

# Path parameters
curl http://127.0.0.1:3000/api/items/1

# JSON body
curl -X POST http://127.0.0.1:3000/api/items \
  -H "Content-Type: application/json" \
  -H "X-API-Key: dev-api-key-change-in-production" \
  -d '{"name": "Laptop", "price": 999.0}'

# Form data
curl -X POST http://127.0.0.1:3000/api/form-files/login \
  -d "username=alice&password=pass"

# File upload
curl -X POST http://127.0.0.1:3000/api/form-files/upload \
  -F "file=@myfile.txt"

# Show response headers
curl -v http://127.0.0.1:3000/api/items

# Versioned API
curl http://127.0.0.1:3000/api/v2/items
```

### Docker
```bash
docker compose up -d                # Start
docker compose down                 # Stop
docker compose down -v              # Stop + wipe data
docker compose ps                   # Status
docker compose logs -f postgres     # Live DB logs
```

### PostgreSQL in Docker
```bash
docker exec -it nest-postgres psql -U nest -d nest_learn
# Inside psql:
\dt              # list tables
\d items         # describe table
SELECT * FROM items;
\q               # quit
```

### TypeORM Migrations (for when you're ready to go full production)
```bash
# After changing entities:
npm run migration:generate -- -n AddNewColumn

# Apply pending migrations:
npm run migration:run

# Revert last migration:
npm run migration:revert
```

---

## The Golden Pattern (Repository Pattern Edition)

```typescript
// ── Entity (extends BaseEntity for free id/timestamps/soft-delete) ──
@Entity('items')
export class Item extends BaseEntity {
  @Column() name: string;
  @Column({ type: 'decimal', precision: 10, scale: 2 }) price: number;
}

// ── DTOs (per operation, with Swagger decorators) ──
export class CreateItemDto {
  @ApiProperty()
  @IsString()
  name: string;

  @ApiProperty()
  @IsNumber() @Min(0)
  price: number;
}

export class UpdateItemDto extends PartialType(CreateItemDto) {}

@Exclude()
export class ItemResponseDto {
  @ApiProperty() @Expose() id: number;
  @ApiProperty() @Expose() name: string;
  @ApiProperty() @Expose() price: number;

  constructor(partial: Partial<ItemResponseDto>) {
    Object.assign(this, partial);
  }
}

// ── Repository (encapsulates ALL query logic) ──
@Injectable()
export class ItemRepository extends Repository<Item> {
  constructor(private dataSource: DataSource) {
    super(Item, dataSource.createEntityManager());
  }

  async findFiltered(filters: FilterItemDto): Promise<[Item[], number]> {
    const qb = this.createQueryBuilder('item');
    if (filters.name) qb.andWhere('item.name ILIKE :name', { name: `%${filters.name}%` });
    return qb.skip(filters.skip).take(filters.take).getManyAndCount();
  }
}

// ── Service (orchestrates business logic) ──
@Injectable()
export class ItemService {
  constructor(private readonly itemRepo: ItemRepository) {}

  async findAll(filters: FilterItemDto) {
    const [items, total] = await this.itemRepo.findFiltered(filters);
    return { items: items.map(i => new ItemResponseDto(i)), meta: { /* pagination */ } };
  }

  async create(dto: CreateItemDto) {
    const saved = await this.itemRepo.save(this.itemRepo.create(dto));
    return new ItemResponseDto(saved);
  }
}

// ── Controller (thin — delegates to service) ──
@ApiTags('Items')
@Controller('items')
export class ItemController {
  constructor(private readonly itemService: ItemService) {}

  @Get()
  findAll(@Query() filters: FilterItemDto) { return this.itemService.findAll(filters); }

  @Post()
  @HttpCode(HttpStatus.CREATED)
  create(@Body() dto: CreateItemDto) { return this.itemService.create(dto); }
}

// ── Module ──
@Module({
  imports: [TypeOrmModule.forFeature([Item])],
  controllers: [ItemController],
  providers: [ItemRepository, ItemService],
  exports: [ItemService],
})
export class ItemsModule {}
```

---

## FastAPI → NestJS Concept Map (Production)

| Concept | FastAPI | NestJS (Production) |
|---|---|---|
| **Framework** | FastAPI (Starlette) | NestJS (Express/Fastify) |
| **Language** | Python | TypeScript (strict) |
| **ORM** | SQLAlchemy | TypeORM (Repository pattern) |
| **Validation** | Pydantic v2 | class-validator + class-transformer |
| **API Docs** | Auto /openapi.json | `@nestjs/swagger` decorators |
| **Routing** | `APIRouter(prefix=)` | `@Controller('path')` |
| **DI** | `Depends(callable)` | Constructor injection (`@Injectable()`) |
| **Path params** | `{param}: type` | `@Param('param', Pipe)` |
| **Query params** | `param: type = default` | `@Query('param', Pipe)` |
| **Request body** | `body: PydanticModel` | `@Body() dto: ClassDto` |
| **Response model** | `response_model=Schema` | `ClassSerializerInterceptor` + `@Expose()` DTO |
| **Middleware** | `@app.middleware("http")` | `NestMiddleware` |
| **Error handling** | `HTTPException` | `HttpException` + `ExceptionFilter` |
| **Background tasks** | `BackgroundTasks.add_task()` | `EventEmitter2` + `@nestjs/schedule` |
| **WebSockets** | `WebSocket` endpoint | `@WebSocketGateway()` + Socket.IO |
| **Auth guard** | `Depends(verify_key)` | `@UseGuards(ApiKeyGuard)` + `CanActivate` |
| **Rate limiting** | `slowapi` or middleware | `@nestjs/throttler` |
| **Security headers** | `secure_headers` middleware | `helmet` |
| **Env validation** | `pydantic-settings` | `class-validator` + `validate()` in ConfigModule |
| **DB migrations** | Alembic | TypeORM CLI migrations |
| **Module system** | Not built-in | `@Module()` (core architectural unit) |

---

**Done!** This task list teaches NestJS the way it's used in production: modular architecture,
repository pattern, standardized API responses, Swagger docs, env validation, soft deletes,
guards, interceptors, event-driven background jobs, and a clean separation of concerns from
day one.

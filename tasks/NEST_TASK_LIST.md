# NestJS Learning Lab — Step-by-Step Task Checklist

> **How to use:** Each step creates ONE file (or a small, related group). Work top to bottom.
> After every step, run `pnpm run start:dev` and test with curl or browser.

---

## Phase 0 — Project on Its Feet (Scaffold + First Route)

### Step 0.1: Scaffold the NestJS project
```bash
nest new api --strict
cd api
pnpm install   # only if pnpm failed during scaffold
```
**What you get:** `main.ts`, `app.module.ts`, `app.controller.ts`, `app.service.ts` — a working "Hello World" app out of the box.

### Step 0.2: Verify it runs
```bash
pnpm run start:dev
```
Open [http://localhost:3000](http://localhost:3000). You should see `{"message": "Hello World!"}`.

### Step 0.3: Understand the 4 generated files

| File | What it does |
|------|-------------|
| `src/main.ts` | Entry point — creates the app, calls `app.listen(3000)` |
| `src/app.module.ts` | Root module — the registry of everything the app uses |
| `src/app.controller.ts` | A route — `@Get()` on `/` returns a message |
| `src/app.service.ts` | Business logic — the controller calls `this.appService.getHello()` |

**Request flow:** Browser → `main.ts` → `AppModule` → `AppController` → `AppService.getHello()` → "Hello World!"

### Step 0.4: Install ALL packages you'll need
```bash
pnpm add @nestjs/typeorm typeorm pg @nestjs/config class-validator class-transformer helmet @nestjs/throttler @nestjs/swagger cookie-parser
pnpm add -D @types/cookie-parser @types/multer
```
**Why now:** One install, never stop mid-build again.

### Step 0.5: Create `.env`
```
PORT=3000
```
**Where:** `api/.env` (project root)
**Why:** We'll wire config next.

### Step 0.6: Update `src/main.ts` — port from .env + Swagger docs
```typescript
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
```
**Why each block:**
- `ConfigService` — reads `.env` so you never hardcode the port
- `SwaggerModule` — gives you interactive API docs like FastAPI's `/docs`

### Step 0.7: Update `src/app.module.ts` — register ConfigModule
```typescript
import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { AppController } from './app.controller';
import { AppService } from './app.service';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      envFilePath: '.env',
    }),
  ],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
```
**Why:** `ConfigModule.forRoot()` reads `.env` at startup. Without it, `ConfigService` has nothing to serve. `isGlobal: true` means every module gets access without re-importing.

### Step 0.8: Test
```bash
pnpm run start:dev
```
- [http://localhost:3000](http://localhost:3000) → `{"message": "Hello World!"}`
- [http://localhost:3000/docs](http://localhost:3000/docs) → Swagger UI (mostly empty, one default route)

---

## Phase 1 — Docker + Database Connection

### Step 1.1: Create `docker-compose.yml`
**Where:** `api/docker-compose.yml`
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
    depends_on:
      postgres:
        condition: service_healthy

volumes:
  pgdata:
```
**Why:** Same setup as your FastAPI project, just different credentials (`nest`/`nest`/`nest_learn`).

### Step 1.2: Start the database
```bash
docker compose up -d
docker compose ps   # verify both containers are running
```

### Step 1.3: Update `.env` — add database credentials
```
PORT=3000
DATABASE_HOST=localhost
DATABASE_PORT=5400
DATABASE_USER=nest
DATABASE_PASSWORD=nest
DATABASE_NAME=nest_learn
```
**Why port 5400:** Your docker-compose maps host `5400` to container `5432` (so it doesn't conflict with your FastAPI postgres on 5400 as well — actually change to `5500` if the FastAPI DB is already on 5400).

### Step 1.4: Update `src/app.module.ts` — connect TypeORM to Postgres
```typescript
import { Module } from '@nestjs/common';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { TypeOrmModule } from '@nestjs/typeorm';
import { AppController } from './app.controller';
import { AppService } from './app.service';

@Module({
  imports: [
    ConfigModule.forRoot({
      isGlobal: true,
      envFilePath: '.env',
    }),

    // ── Database connection ──
    TypeOrmModule.forRootAsync({
      inject: [ConfigService],
      useFactory: (config: ConfigService) => ({
        type: 'postgres',
        host: config.get<string>('DATABASE_HOST'),
        port: config.get<number>('DATABASE_PORT'),
        username: config.get<string>('DATABASE_USER'),
        password: config.get<string>('DATABASE_PASSWORD'),
        database: config.get<string>('DATABASE_NAME'),
        autoLoadEntities: true,          // auto-discover @Entity() classes
        synchronize: true,               // auto-create tables (DEV ONLY)
      }),
    }),
  ],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
```
**Why `forRootAsync`:**
- `forRoot` = config is hardcoded
- `forRootAsync` = config comes from a service (ConfigService). You need this because your DB credentials live in `.env`, not in code.
- `synchronize: true` = TypeORM reads your entity classes and creates/alters tables automatically. Use only in development. In production you use migrations.

### Step 1.5: Test database connection
```bash
pnpm run start:dev
```
If there's no error about database connection, Phase 1 is done.

---

## Phase 2 — Your First CRUD (Items)

### Step 2.1: Create `src/common/entities/base.entity.ts`
**Why:** Every table gets `id`, `createdAt`, `updatedAt`, `deletedAt` for free. Write once, reuse forever.
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
  deletedAt: Date | null;
}
```

### Step 2.2: Create the Item entity — `src/modules/items/entities/item.entity.ts`
```bash
mkdir -p src/modules/items/{dto,entities,services,controllers}
```
**File:** `src/modules/items/entities/item.entity.ts`
```typescript
import { Entity, Column, Index } from 'typeorm';
import { BaseEntity } from '../../common/entities/base.entity';

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
**Why this structure:**
- `@Entity('items')` — maps this class to the `items` table in Postgres
- `extends BaseEntity` — inherits `id`, `createdAt`, `updatedAt`, `deletedAt` for free
- `@Column()` — each property becomes a database column
- `name: 'in_stock'` — in the DB it's `in_stock` (snake_case), in TypeScript it's `inStock` (camelCase)

### Step 2.3: Create the DTO — `src/modules/items/dto/create-item.dto.ts`
**Why:** A DTO (Data Transfer Object) is what the client sends. You validate it with decorators.
```typescript
import { IsString, IsNumber, IsOptional, IsBoolean, Min, MaxLength } from 'class-validator';
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';

export class CreateItemDto {
  @ApiProperty({ example: 'Laptop', description: 'Item name' })
  @IsString()
  @MaxLength(255)
  name: string;

  @ApiProperty({ example: 999.99 })
  @IsNumber()
  @Min(0)
  price: number;

  @ApiPropertyOptional({ example: 'A powerful laptop' })
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
**Why each decorator:**
- `@ApiProperty()` — shows this field in Swagger docs with an example
- `@IsString()` — rejects numbers, booleans, nulls
- `@Min(0)` — rejects negative prices
- `@IsOptional()` — field can be omitted entirely

### Step 2.4: Create the Update DTO — `src/modules/items/dto/update-item.dto.ts`
```typescript
import { PartialType } from '@nestjs/swagger';
import { CreateItemDto } from './create-item.dto';

export class UpdateItemDto extends PartialType(CreateItemDto) {}
```
**Why so short:** `PartialType()` makes every field from `CreateItemDto` optional. One line. PATCH only updates what the client sends, so this is exactly what you need.

### Step 2.5: Create the Service — `src/modules/items/services/item.service.ts`
**Why:** Services hold business logic. Controllers only handle HTTP — they call services.
```typescript
import { Injectable, NotFoundException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { Item } from './item.entity';
import { CreateItemDto } from './create-item.dto';
import { UpdateItemDto } from './update-item.dto';

@Injectable()
export class ItemService {
  constructor(
    @InjectRepository(Item)
    private itemRepo: Repository<Item>,
  ) {}

  async create(dto: CreateItemDto): Promise<Item> {
    const item = this.itemRepo.create(dto);
    return this.itemRepo.save(item);
  }

  async findAll(): Promise<Item[]> {
    return this.itemRepo.find({ order: { createdAt: 'DESC' } });
  }

  async findOne(id: number): Promise<Item> {
    const item = await this.itemRepo.findOneBy({ id });
    if (!item) throw new NotFoundException(`Item ${id} not found`);
    return item;
  }

  async update(id: number, dto: UpdateItemDto): Promise<Item> {
    const item = await this.findOne(id);   // reuses findOne (which throws 404)
    Object.assign(item, dto);              // merges dto fields into item
    return this.itemRepo.save(item);
  }

  async remove(id: number): Promise<void> {
    const item = await this.findOne(id);
    await this.itemRepo.softRemove(item);  // soft delete — sets deletedAt, doesn't actually delete
  }
}
```
**Key patterns:**
- `@InjectRepository(Item)` — NestJS creates a TypeORM repository for the Item entity and injects it
- `softRemove` — marks the row as deleted instead of actually removing it (BaseEntity's `deletedAt` column)
- `findOne` reuses itself — the `update` and `remove` methods call `this.findOne(id)` so 404 logic lives in one place

### Step 2.6: Create the Controller — `src/modules/items/controllers/item.controller.ts`
**Why:** The controller translates HTTP requests into service calls.
```typescript
import {
  Controller, Get, Post, Body, Patch, Param, Delete,
  HttpCode, HttpStatus, ParseIntPipe,
} from '@nestjs/common';
import { ApiTags, ApiOperation, ApiResponse } from '@nestjs/swagger';
import { ItemService } from './item.service';
import { CreateItemDto } from './create-item.dto';
import { UpdateItemDto } from './update-item.dto';
import { Item } from './item.entity';

@ApiTags('Items')
@Controller('items')
export class ItemController {
  constructor(private readonly itemService: ItemService) {}

  @Post()
  @HttpCode(HttpStatus.CREATED)
  @ApiOperation({ summary: 'Create an item' })
  @ApiResponse({ status: 201, description: 'Item created' })
  create(@Body() dto: CreateItemDto): Promise<Item> {
    return this.itemService.create(dto);
  }

  @Get()
  @ApiOperation({ summary: 'List all items' })
  findAll(): Promise<Item[]> {
    return this.itemService.findAll();
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get one item' })
  @ApiResponse({ status: 404, description: 'Not found' })
  findOne(@Param('id', ParseIntPipe) id: number): Promise<Item> {
    return this.itemService.findOne(id);
  }

  @Patch(':id')
  @ApiOperation({ summary: 'Partial update' })
  update(
    @Param('id', ParseIntPipe) id: number,
    @Body() dto: UpdateItemDto,
  ): Promise<Item> {
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
**Key patterns:**
- `@Controller('items')` — every route in this class starts with `/items`
- `@Param('id', ParseIntPipe)` — extracts `id` from the URL AND validates it's an integer
- `@HttpCode(HttpStatus.CREATED)` — POST returns 201 instead of default 200
- `@HttpCode(HttpStatus.NO_CONTENT)` — DELETE returns 204 with no body

### Step 2.7: Create the Module — `src/modules/items/items.module.ts`
**Why:** Every feature needs a module. It tells NestJS: "these are the pieces of the Items feature."
```typescript
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { Item } from './item.entity';
import { ItemService } from './item.service';
import { ItemController } from './item.controller';

@Module({
  imports: [TypeOrmModule.forFeature([Item])],
  controllers: [ItemController],
  providers: [ItemService],
  exports: [ItemService],
})
export class ItemsModule {}
```

### Step 2.8: Register ItemsModule in AppModule
In `src/app.module.ts`, add:
```typescript
import { ItemsModule } from './modules/items/items.module';

// In the @Module() imports array, add:
ItemsModule,
```

### Step 2.9: Test full CRUD
```bash
# Create
curl -X POST http://localhost:3000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Laptop", "price": 999.99}'

curl -X POST http://localhost:3000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Phone", "price": 699.00}'

# List
curl http://localhost:3000/items

# Get one
curl http://localhost:3000/items/1

# Update
curl -X PATCH http://localhost:3000/items/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Gaming Laptop"}'

# Delete
curl -X DELETE http://localhost:3000/items/1

# List again — item 1 is gone
curl http://localhost:3000/items

# Open Swagger: http://localhost:3000/docs — you'll see all routes documented
```

### Step 2.10: Check the database
```bash
docker exec nest-postgres psql -U nest -d nest_learn -c "SELECT * FROM items;"
```
Notice the soft-deleted item still exists — it just has a `deletedAt` timestamp.

---

## Phase 3 — Query Parameters & Pagination

### Step 3.1: Create `src/modules/items/dto/filter-item.dto.ts`
**Why:** Separate DTO for GET query parameters. Extends pagination with filter fields.
```typescript
import { IsOptional, IsString, IsNumber, IsBoolean, IsInt, Min, Max } from 'class-validator';
import { Type, Transform } from 'class-transformer';
import { ApiPropertyOptional } from '@nestjs/swagger';

export class FilterItemDto {
  @ApiPropertyOptional({ default: 1 })
  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @Min(1)
  page?: number = 1;

  @ApiPropertyOptional({ default: 10 })
  @IsOptional()
  @Type(() => Number)
  @IsInt()
  @Min(1)
  @Max(100)
  pageSize?: number = 10;

  @ApiPropertyOptional({ description: 'Search by name (case-insensitive)' })
  @IsOptional()
  @IsString()
  name?: string;

  @ApiPropertyOptional({ description: 'Max price filter' })
  @IsOptional()
  @Type(() => Number)
  @IsNumber()
  @Min(0)
  maxPrice?: number;

  @ApiPropertyOptional({ description: 'Filter by stock status' })
  @IsOptional()
  @Transform(({ value }) => value === 'true' || value === true)
  @IsBoolean()
  inStock?: boolean;

  get skip(): number {
    return (this.page - 1) * this.pageSize;
  }

  get take(): number {
    return this.pageSize;
  }
}
```
**Why `@Type(() => Number)`:** Query parameters arrive as strings (`?page=2`). class-validator needs `@Type(() => Number)` to convert `"2"` to `2` before validation.

### Step 3.2: Update `item.service.ts` — add filter + pagination method
Add this method:
```typescript
async findFiltered(filters: FilterItemDto): Promise<{ items: Item[]; total: number }> {
  const qb = this.itemRepo.createQueryBuilder('item');

  if (filters.name) {
    qb.andWhere('item.name ILIKE :name', { name: `%${filters.name}%` });
  }
  if (filters.maxPrice !== undefined) {
    qb.andWhere('item.price <= :maxPrice', { maxPrice: filters.maxPrice });
  }
  if (filters.inStock !== undefined) {
    qb.andWhere('item.inStock = :inStock', { inStock: filters.inStock });
  }

  qb.skip(filters.skip).take(filters.take).orderBy('item.createdAt', 'DESC');

  const [items, total] = await qb.getManyAndCount();
  return { items, total };
}
```
Add the import: `import { FilterItemDto } from './filter-item.dto';`

### Step 3.3: Update `item.controller.ts` — replace findAll with filtered version
```typescript
import { FilterItemDto } from './filter-item.dto';

@Get()
@ApiOperation({ summary: 'List items with pagination & filters' })
findAll(@Query() filters: FilterItemDto) {
  return this.itemService.findFiltered(filters);
}
```

### Step 3.4: Test pagination and filtering
```bash
curl "http://localhost:3000/items?page=1&pageSize=2"
curl "http://localhost:3000/items?name=phone"
curl "http://localhost:3000/items?maxPrice=500&inStock=true"
curl "http://localhost:3000/items?pageSize=200"   # 400 — validation error
```

---

## Phase 4 — Validation Pipes & Error Handling

### Step 4.1: Update `src/main.ts` — add global ValidationPipe
Add to bootstrap, before `await app.listen()`:
```typescript
import { ValidationPipe } from '@nestjs/common';

app.useGlobalPipes(
  new ValidationPipe({
    whitelist: true,              // strip unknown properties
    forbidNonWhitelisted: true,   // throw error on unknown properties
    transform: true,              // auto-transform types (string → number)
  }),
);
```
**Why:**
- Without `transform: true`, `@Type(() => Number)` in FilterItemDto doesn't work
- Without `whitelist`, a client can send `{"hacked": true}` and it silently passes through
- Without `forbidNonWhitelisted`, you never know the client sent garbage

### Step 4.2: Test validation
```bash
curl -X POST http://localhost:3000/items \
  -H "Content-Type: application/json" \
  -d '{"name": ""}'     # 400 — name too short, price missing

curl -X POST http://localhost:3000/items \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","price":10,"hacked":true}'   # 400 — unknown property
```

---

## Phase 5 — Users Module (Password Hashing)

### Step 5.1: Create `src/modules/users/entities/user.entity.ts`
```bash
mkdir -p src/modules/users/{dto,entities,services,controllers}
```
```typescript
import { Entity, Column, Index } from 'typeorm';
import { BaseEntity } from '../../common/entities/base.entity';

@Entity('users')
export class User extends BaseEntity {
  @Column({ length: 100, unique: true })
  @Index()
  username: string;

  @Column({ length: 255, unique: true })
  email: string;

  @Column({ name: 'hashed_password', length: 255 })
  hashedPassword: string;

  @Column({ name: 'is_admin', default: false })
  isAdmin: boolean;
}
```

### Step 5.2: Create `src/modules/users/dto/create-user.dto.ts`
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

  @ApiProperty({ example: 'password123', minLength: 8 })
  @IsString()
  @MinLength(8)
  password: string;  // plain text from client → hashed before DB

  @ApiPropertyOptional({ default: false })
  @IsOptional()
  @IsBoolean()
  isAdmin?: boolean;
}
```

### Step 5.3: Create `src/modules/users/dto/update-user.dto.ts`
```typescript
import { PartialType } from '@nestjs/swagger';
import { CreateUserDto } from './create-user.dto';

export class UpdateUserDto extends PartialType(CreateUserDto) {}
```

### Step 5.4: Install bcrypt and create password helper
```bash
pnpm add bcrypt
pnpm add -D @types/bcrypt
```

Create `src/common/utils/password.util.ts`:
```bash
mkdir -p src/common/utils
```
```typescript
import * as bcrypt from 'bcrypt';

export async function hashPassword(password: string): Promise<string> {
  return bcrypt.hash(password, 10);
}

export async function verifyPassword(password: string, hash: string): Promise<boolean> {
  return bcrypt.compare(password, hash);
}
```

### Step 5.5: Create `src/modules/users/services/user.service.ts`
```typescript
import { Injectable, NotFoundException, ConflictException } from '@nestjs/common';
import { InjectRepository } from '@nestjs/typeorm';
import { Repository } from 'typeorm';
import { User } from './user.entity';
import { CreateUserDto } from './create-user.dto';
import { UpdateUserDto } from './update-user.dto';
import { hashPassword } from '../../common/utils/password.util';

@Injectable()
export class UserService {
  constructor(
    @InjectRepository(User)
    private userRepo: Repository<User>,
  ) {}

  async create(dto: CreateUserDto): Promise<User> {
    const existing = await this.userRepo.findOneBy({ email: dto.email });
    if (existing) throw new ConflictException('Email already registered');

    const user = this.userRepo.create({
      ...dto,
      hashedPassword: await hashPassword(dto.password),
    });
    return this.userRepo.save(user);
  }

  async findAll(): Promise<User[]> {
    return this.userRepo.find();
  }

  async findOne(id: number): Promise<User> {
    const user = await this.userRepo.findOneBy({ id });
    if (!user) throw new NotFoundException(`User ${id} not found`);
    return user;
  }

  async update(id: number, dto: UpdateUserDto): Promise<User> {
    const user = await this.findOne(id);
    if (dto.password) {
      dto.hashedPassword = await hashPassword(dto.password);
      delete dto.password;
    }
    Object.assign(user, dto);
    return this.userRepo.save(user);
  }

  async remove(id: number): Promise<void> {
    const user = await this.findOne(id);
    await this.userRepo.softRemove(user);
  }
}
```
**Why the password dance:** Client sends `password` (plain text). DB stores `hashedPassword`. The service hashes it between receiving and saving.

### Step 5.6: Create `src/modules/users/controllers/user.controller.ts`
```typescript
import {
  Controller, Get, Post, Body, Patch, Param, Delete,
  HttpCode, HttpStatus, ParseIntPipe,
} from '@nestjs/common';
import { ApiTags, ApiOperation } from '@nestjs/swagger';
import { UserService } from './user.service';
import { CreateUserDto } from './create-user.dto';
import { UpdateUserDto } from './update-user.dto';
import { User } from './user.entity';

@ApiTags('Users')
@Controller('users')
export class UserController {
  constructor(private readonly userService: UserService) {}

  @Post()
  @HttpCode(HttpStatus.CREATED)
  @ApiOperation({ summary: 'Create user' })
  create(@Body() dto: CreateUserDto): Promise<User> {
    return this.userService.create(dto);
  }

  @Get()
  @ApiOperation({ summary: 'List users' })
  findAll(): Promise<User[]> {
    return this.userService.findAll();
  }

  @Get(':id')
  @ApiOperation({ summary: 'Get user' })
  findOne(@Param('id', ParseIntPipe) id: number): Promise<User> {
    return this.userService.findOne(id);
  }

  @Patch(':id')
  @ApiOperation({ summary: 'Update user' })
  update(
    @Param('id', ParseIntPipe) id: number,
    @Body() dto: UpdateUserDto,
  ): Promise<User> {
    return this.userService.update(id, dto);
  }

  @Delete(':id')
  @HttpCode(HttpStatus.NO_CONTENT)
  @ApiOperation({ summary: 'Delete user' })
  remove(@Param('id', ParseIntPipe) id: number): Promise<void> {
    return this.userService.remove(id);
  }
}
```

### Step 5.7: Create `src/modules/users/users.module.ts`
```typescript
import { Module } from '@nestjs/common';
import { TypeOrmModule } from '@nestjs/typeorm';
import { User } from './user.entity';
import { UserService } from './user.service';
import { UserController } from './user.controller';

@Module({
  imports: [TypeOrmModule.forFeature([User])],
  controllers: [UserController],
  providers: [UserService],
  exports: [UserService],
})
export class UsersModule {}
```

### Step 5.8: Register UsersModule in AppModule
```typescript
import { UsersModule } from './modules/users/users.module';
// Add to imports array
```

### Step 5.9: Test
```bash
curl -X POST http://localhost:3000/users \
  -H "Content-Type: application/json" \
  -d '{"username":"alice","email":"alice@example.com","password":"password123"}'

curl http://localhost:3000/users
```

---

## Phase 6 — API Key Guards (Auth)

### Step 6.1: Update `.env` — add API keys
```
PORT=3000
DATABASE_HOST=localhost
DATABASE_PORT=5400
DATABASE_USER=nest
DATABASE_PASSWORD=nest
DATABASE_NAME=nest_learn
API_KEY=dev-api-key
ADMIN_API_KEY=dev-admin-key
```

### Step 6.2: Create `src/common/guards/api-key.guard.ts`
```bash
mkdir -p src/common/guards
```
```typescript
import { Injectable, CanActivate, ExecutionContext, UnauthorizedException } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';

@Injectable()
export class ApiKeyGuard implements CanActivate {
  constructor(private readonly configService: ConfigService) {}

  canActivate(context: ExecutionContext): boolean {
    const request = context.switchToHttp().getRequest();
    const apiKey = request.headers['x-api-key'];

    if (!apiKey) {
      throw new UnauthorizedException('Missing X-API-Key header');
    }

    const validKey = this.configService.get<string>('API_KEY');
    const adminKey = this.configService.get<string>('ADMIN_API_KEY');

    if (apiKey === validKey || apiKey === adminKey) {
      request.isAdmin = apiKey === adminKey;
      return true;
    }

    throw new UnauthorizedException('Invalid API key');
  }
}
```

### Step 6.3: Apply guard globally in AppModule
In `src/app.module.ts`:
```typescript
import { APP_GUARD } from '@nestjs/core';
import { ApiKeyGuard } from './common/guards/api-key.guard';

// In providers array:
providers: [
  AppService,
  { provide: APP_GUARD, useClass: ApiKeyGuard },
],
```
**Why `APP_GUARD`:** This applies the guard to EVERY route automatically. No `@UseGuards()` needed on every controller.

### Step 6.4: Test auth
```bash
curl http://localhost:3000/items                    # 401 — no key
curl -H "X-API-Key: wrong" http://localhost:3000/items  # 401 — wrong key
curl -H "X-API-Key: dev-api-key" http://localhost:3000/items  # 200
curl -H "X-API-Key: dev-admin-key" http://localhost:3000/items # 200 (admin key also works)
```

---

## Phase 7 — Headers, Cookies, Status Codes, Form/Files

These are small, self-contained modules. Each follows the same pattern: `mkdir`, create controller, create module, register in AppModule.

### Step 7.1: Headers & Cookies — `src/modules/headers-cookies/`
```bash
mkdir -p src/modules/headers-cookies
```

`headers-cookies.controller.ts`:
```typescript
import { Controller, Get, Headers, Req, Res } from '@nestjs/common';
import { ApiTags, ApiOperation } from '@nestjs/swagger';
import { Request, Response } from 'express';

@ApiTags('Headers & Cookies')
@Controller('demo')
export class HeadersCookiesController {
  @Get('whoami')
  @ApiOperation({ summary: 'Read User-Agent header' })
  whoami(@Headers('user-agent') ua: string) {
    return { userAgent: ua };
  }

  @Get('read-cookie')
  @ApiOperation({ summary: 'Read session_id cookie' })
  readCookie(@Req() req: Request) {
    return { sessionId: req.cookies?.session_id ?? 'none' };
  }

  @Get('set-cookie')
  @ApiOperation({ summary: 'Set a cookie' })
  setCookie(@Res({ passthrough: true }) res: Response) {
    res.cookie('session_id', 'abc-123', { httpOnly: true, maxAge: 3600000 });
    return { message: 'Cookie set!' };
  }

  @Get('set-headers')
  @ApiOperation({ summary: 'Set custom response headers' })
  setHeaders(@Res({ passthrough: true }) res: Response) {
    res.set('X-Custom', 'hello');
    return { message: 'Headers set!' };
  }
}
```

`headers-cookies.module.ts`:
```typescript
import { Module } from '@nestjs/common';
import { HeadersCookiesController } from './headers-cookies.controller';

@Module({
  controllers: [HeadersCookiesController],
})
export class HeadersCookiesModule {}
```

Register in AppModule, then test:
```bash
curl -H "X-API-Key: dev-api-key" -H "User-Agent: MyApp" http://localhost:3000/demo/whoami
curl -H "X-API-Key: dev-api-key" -b "session_id=test123" http://localhost:3000/demo/read-cookie
curl -H "X-API-Key: dev-api-key" -v http://localhost:3000/demo/set-cookie
```

### Step 7.2: Status Codes — `src/modules/status-codes/`
```bash
mkdir -p src/modules/status-codes
```
```typescript
@ApiTags('Status Codes')
@Controller('demo-status')
export class StatusCodesController {
  @Post('created')
  @HttpCode(HttpStatus.CREATED)
  create() { return { id: 1 }; }

  @Delete('removed')
  @HttpCode(HttpStatus.NO_CONTENT)
  remove() { return; }

  @Get('redirect')
  redirect(@Res() res: Response) {
    return res.redirect(301, '/items');
  }
}
```
Test: `curl -v -H "X-API-Key: dev-api-key" http://localhost:3000/demo-status/redirect`

### Step 7.3: Form Data & File Uploads — `src/modules/form-files/`
```bash
mkdir -p src/modules/form-files
mkdir uploads
```
```typescript
@Post('login')
@ApiConsumes('application/x-www-form-urlencoded')
login(@Body('username') username: string, @Body('password') password: string) {
  return { username };
}

@Post('upload')
@UseInterceptors(FileInterceptor('file', { dest: './uploads' }))
upload(@UploadedFile() file: Express.Multer.File) {
  return { filename: file.originalname, size: file.size };
}
```
Test:
```bash
curl -X POST http://localhost:3000/form-files/login -H "X-API-Key: dev-api-key" -d "username=alice&password=pass"
curl -X POST http://localhost:3000/form-files/upload -H "X-API-Key: dev-api-key" -F "file=@test.txt"
```

---

## Phase 8 — Response Wrapper (Standardized API Responses)

### Step 8.1: Create an interceptor to wrap all responses
`src/common/interceptors/response-wrapper.interceptor.ts`:
```bash
mkdir -p src/common/interceptors
```
```typescript
import { Injectable, NestInterceptor, ExecutionContext, CallHandler } from '@nestjs/common';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';

export interface WrappedResponse<T> {
  success: boolean;
  data: T;
  timestamp: string;
}

@Injectable()
export class ResponseWrapperInterceptor<T> implements NestInterceptor<T, WrappedResponse<T>> {
  intercept(context: ExecutionContext, next: CallHandler): Observable<WrappedResponse<T>> {
    return next.handle().pipe(
      map((data) => ({
        success: true,
        data,
        timestamp: new Date().toISOString(),
      })),
    );
  }
}
```

### Step 8.2: Register globally in main.ts
```typescript
import { ResponseWrapperInterceptor } from './common/interceptors/response-wrapper.interceptor';
app.useGlobalInterceptors(new ResponseWrapperInterceptor());
```

Now every response is automatically wrapped:
```json
{
  "success": true,
  "data": { "id": 1, "name": "Laptop", ... },
  "timestamp": "2026-07-25T..."
}
```

---

## Phase 9 — WebSockets

### Step 9.1: Install
```bash
pnpm add @nestjs/websockets @nestjs/platform-socket.io socket.io
```

### Step 9.2: Create `src/modules/websocket/events.gateway.ts`
```bash
mkdir -p src/modules/websocket
```
```typescript
import {
  WebSocketGateway, WebSocketServer, SubscribeMessage,
  OnGatewayConnection, OnGatewayDisconnect,
  MessageBody, ConnectedSocket,
} from '@nestjs/websockets';
import { Server, Socket } from 'socket.io';

@WebSocketGateway({ cors: { origin: '*' } })
export class EventsGateway implements OnGatewayConnection, OnGatewayDisconnect {
  @WebSocketServer()
  server: Server;

  handleConnection(client: Socket) {
    console.log(`WS connected: ${client.id}`);
  }

  handleDisconnect(client: Socket) {
    console.log(`WS disconnected: ${client.id}`);
  }

  @SubscribeMessage('message')
  handleMessage(@ConnectedSocket() client: Socket, @MessageBody() payload: string) {
    this.server.emit('message', {
      from: client.id,
      text: payload,
      timestamp: new Date().toISOString(),
    });
  }
}
```

### Step 9.3: Test in browser console
```js
const socket = io('http://localhost:3000');
socket.on('message', data => console.log('Received:', data));
socket.emit('message', 'Hello from browser!');
```

---

## Where You Are Now

```
api/
├── docker-compose.yml
├── .env
├── package.json
├── tsconfig.json
├── uploads/
│
└── src/
    ├── main.ts                     ← Entry: ConfigService, Swagger, ValidationPipe, ResponseWrapper
    ├── app.module.ts               ← Root: ConfigModule, TypeORM, ItemsModule, UsersModule, Guards
    │
    ├── common/
    │   ├── entities/
    │   │   └── base.entity.ts      ← id, createdAt, updatedAt, deletedAt
    │   ├── guards/
    │   │   └── api-key.guard.ts    ← Global auth via X-API-Key header
    │   ├── interceptors/
    │   │   └── response-wrapper.interceptor.ts
    │   └── utils/
    │       └── password.util.ts    ← bcrypt hash/verify
    │
    └── modules/
        ├── items/
        │   ├── item.entity.ts      ← @Entity — DB table
        │   ├── create-item.dto.ts  ← Validation — POST body
        │   ├── update-item.dto.ts  ← PartialType — PATCH body
        │   ├── filter-item.dto.ts  ← Query params + pagination
        │   ├── item.service.ts     ← Business logic
        │   ├── item.controller.ts  ← HTTP routes
        │   └── items.module.ts     ← Feature module
        │
        ├── users/
        │   ├── user.entity.ts
        │   ├── create-user.dto.ts
        │   ├── update-user.dto.ts
        │   ├── user.service.ts
        │   ├── user.controller.ts
        │   └── users.module.ts
        │
        ├── headers-cookies/
        ├── status-codes/
        ├── form-files/
        └── websocket/
```

---

## NestJS → FastAPI Parallel (What You Already Know)

| Concept | FastAPI | NestJS |
|---------|---------|--------|
| Route | `@router.get("/items")` | `@Get()` in a `@Controller('items')` |
| Path param | `item_id: UUID` | `@Param('id', ParseIntPipe) id: number` |
| Query param | `q: str = None` | `@Query('q') q?: string` |
| Body validation | Pydantic `BaseModel` | class-validator DTO |
| DI | `Depends(get_db)` | `constructor(private service: ItemService)` |
| ORM model | `class Item(Base)` | `class Item extends BaseEntity` |
| Create table | `Base.metadata.create_all()` | `synchronize: true` or migrations |
| Swagger | Automatic | `@ApiProperty()` decorators |
| Exception | `HTTPException(404)` | `NotFoundException()` |
| Middleware | `@app.middleware("http")` | `NestMiddleware` or interceptor |
| Background | `BackgroundTasks.add_task()` | `@nestjs/event-emitter` or `@nestjs/schedule` |
| WebSocket | `@router.websocket("/ws")` | `@WebSocketGateway()` |
| Auth guard | `Depends(verify_key)` | `CanActivate` guard |
| Settings | `pydantic-settings` | `@nestjs/config` + class-validator |
| Env file | `.env` (same) | `.env` (same) |

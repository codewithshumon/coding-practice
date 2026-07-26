# Learning Notes — Backend Development Concepts

---

## NestJS: Module vs Service vs Controller

### One request, start to finish

```
Client:  POST /items  { "name": "Laptop", "price": 999 }
                │
                ▼
┌─────────────────────────────────────────────────────┐
│  CONTROLLER                                         │
│  Job: "I handle HTTP."                              │
│                                                      │
│  - Receives the request                              │
│  - Extracts the JSON body → CreateItemDto            │
│  - Validates it (via ValidationPipe)                 │
│  - Calls: this.itemService.create(dto)               │
│  - Returns the result as JSON + 201 status           │
│                                                      │
│  Knows: HTTP, JSON, status codes, URLs               │
│  Does NOT know: the database, business rules         │
└──────────────────────┬──────────────────────────────┘
                       │ calls
                       ▼
┌─────────────────────────────────────────────────────┐
│  SERVICE                                            │
│  Job: "I handle business logic."                     │
│                                                      │
│  - Takes the DTO                                     │
│  - Decides: "is this valid? any rules to check?"     │
│  - Calls: this.itemRepo.save(item)                   │
│  - Returns the saved item                            │
│                                                      │
│  Knows: business rules, the repository/ORM           │
│  Does NOT know: HTTP, URLs, request/response         │
└──────────────────────┬──────────────────────────────┘
                       │ uses
                       ▼
              ┌────────────────────┐
              │   TypeORM          │
              │   Repository       │
              │   → PostgreSQL     │
              └────────────────────┘
```

### Summary Table

| | Controller | Service | Module |
|---|-----------|---------|--------|
| **One-line job** | Translates HTTP into function calls | Contains the actual business logic | Registers everything as a unit |
| **Analogy** | Waiter — takes orders, brings food | Chef — cooks the food | The restaurant's org chart |
| **Decorator** | `@Controller('items')` | `@Injectable()` | `@Module({...})` |
| **Knows about** | `@Get()`, `@Post()`, `@Body()`, `@Param()` | Business rules, validation logic, calling the DB | Which controllers/services belong together |
| **Does NOT know** | Database queries, business logic | HTTP, URLs, status codes | Business logic (just wiring) |
| **Side that talks to** | Client (browser/curl) | Repository/ORM (database) | NestJS framework |

### Why three separate pieces?

| If you combined them... | Problem |
|------------------------|---------|
| Controller + Service in one class | Can't test business logic without HTTP. Can't reuse logic in WebSocket gateway or cron job. |
| Service + Module in one | Can't swap implementations. Can't mock for tests. |
| Everything in one file | 5000-line file. 50 imports. Nightmare. |

### Code comparison

**Controller** — only HTTP concerns:
```typescript
@Controller('items')
export class ItemController {
  constructor(private itemService: ItemService) {}  // injects the service

  @Get()
  findAll(@Query() filters: FilterItemDto) {         // reads query params
    return this.itemService.findAll(filters);         // delegates to service
  }

  @Post()
  @HttpCode(201)                                     // sets HTTP status
  create(@Body() dto: CreateItemDto) {               // reads JSON body
    return this.itemService.create(dto);              // delegates to service
  }
}
```

**Service** — only business logic:
```typescript
@Injectable()
export class ItemService {
  constructor(@InjectRepository(Item) private repo: Repository<Item>) {}

  async create(dto: CreateItemDto): Promise<Item> {
    const item = this.repo.create(dto);
    return this.repo.save(item);
  }

  async findAll(filters: FilterItemDto) {
    const qb = this.repo.createQueryBuilder('item');
    if (filters.name) qb.andWhere('item.name ILIKE :name', { name: `%${filters.name}%` });
    return qb.getManyAndCount();
  }
}
```

**Module** — only wiring:
```typescript
@Module({
  imports: [TypeOrmModule.forFeature([Item])],   // what DB entities this module uses
  controllers: [ItemController],                  // which controllers belong here
  providers: [ItemService],                       // which services belong here
  exports: [ItemService],                         // what other modules can use
})
export class ItemsModule {}
```

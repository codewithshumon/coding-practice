import { 
  IsString, 
  IsNumber, 
  IsOptional, 
  IsBoolean, 
  Min,
  MaxLength
} from 'class-validator';
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';

export class CreateItemDto {
  @ApiProperty({ example: 'Laptop', description: 'Item name' })
  @IsString()
  @MaxLength(255)
  name!: string;

  @ApiProperty({ example: 999.99 })
  @IsNumber()
  @Min(0)
  price!: number;

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

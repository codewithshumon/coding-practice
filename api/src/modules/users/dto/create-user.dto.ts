import {
  IsString,
  IsNumber,
  IsOptional,
  IsBoolean,
  Min,
  MaxLength,
} from 'class-validator';
import { ApiProperty, ApiPropertyOptional } from '@nestjs/swagger';

export class CreateUserDto {
  @ApiProperty({ example: 'Shumon Khan', description: 'User name' })
  @IsString()
  @MaxLength(255)
  name!: string;

  @ApiProperty({ example: 25 })
  @IsNumber()
  @Min(0)
  age!: number;

  @ApiPropertyOptional({ default: true })
  @IsOptional()
  @IsBoolean()
  status!: boolean;

  @ApiPropertyOptional({ example: 'I am a software engineer' })
  @IsOptional()
  @IsString()
  @MaxLength(1000)
  bio?: string;
}

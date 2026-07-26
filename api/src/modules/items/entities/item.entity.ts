import { Entity, Column, Index } from 'typeorm';
import { BaseEntity } from '@common/entities/base.entity';

@Entity('items')
export class Item extends BaseEntity {
  @Column({ length: 255 })
  @Index()
  name!: string;

  @Column({ type: 'decimal', precision: 10, scale: 2 })
  price!: number;

  @Column({ type: 'text', nullable: true })
  description!: string | null;

  @Column({ name: 'in_stock', default: true })
  inStock!: boolean;
}

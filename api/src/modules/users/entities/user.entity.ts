import { Entity, Column, Index } from 'typeorm';
import { BaseEntity } from '@common/entities/base.entity';

@Entity('users')
export class User extends BaseEntity {
  @Column({ length: 255 })
  @Index()
  name!: string;

  @Column({ type: 'int' })
  age!: number;

  @Column({ default: true })
  status!: boolean;

  @Column({ type: 'text', nullable: true })
  bio!: string | null;
}

export enum TableStatus {
  AVAILABLE = 'available',
  OCCUPIED = 'occupied',
  RESERVED = 'reserved',
  CLEANING = 'cleaning'
}

export interface Table {
  id: number;
  number: string;
  capacity: number;
  status: TableStatus;
  location?: string;
  created_at: string;
  updated_at?: string;
}

export interface TableCreate {
  number: string;
  capacity: number;
  location?: string;
}


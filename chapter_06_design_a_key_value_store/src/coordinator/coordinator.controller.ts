import { Body, Controller, Get, Param, Post } from '@nestjs/common';
import { CoordinatorService } from './coordinator.service';

@Controller('coordinator')
export class CoordinatorController {
  constructor(private readonly coordinatorService: CoordinatorService) {}

  @Get(':key')
  getValue(@Param('key') key: string): string {
    return this.coordinatorService.get(key);
  }

  @Post(':key')
  putValue(@Param('key') key: string, @Body() value: string): void {
    this.coordinatorService.put(key, value);
  }
}

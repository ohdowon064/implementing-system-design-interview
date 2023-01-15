import { Body, Controller, Delete, Get, Param, Post } from '@nestjs/common';
import { CoordinatorService } from './coordinator.service';
import { PutValueDto } from './put-value.dto';

@Controller('coordinator')
export class CoordinatorController {
  constructor(private readonly coordinatorService: CoordinatorService) {}

  @Get(':key')
  getValue(@Param('key') key: string): string {
    return this.coordinatorService.get(key);
  }

  @Post(':key')
  putValue(@Param('key') key: string, @Body() body: PutValueDto): void {
    this.coordinatorService.put(key, body.value);
  }

  @Delete(':id')
  removeNode(@Param('id') id: string): void {
    this.coordinatorService.removeNode(+id);
  }

  @Post('node')
  addNode(): void {
    this.coordinatorService.addNode();
  }
}

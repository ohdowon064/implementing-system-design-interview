import { Body, Controller, Get, Param, Post } from '@nestjs/common';
import { ClientService } from './client.service';
import { PutValueDto } from 'src/coordinator/put-value.dto';

@Controller('client')
export class ClientController {
  constructor(private readonly clientService: ClientService) {}

  @Post('put/:key')
  async putValue(@Param('key') key: string, @Body() body: PutValueDto) {
    console.log('client put 호출됨');
    console.log(body.value);
    await this.clientService.put(key, body.value);
  }

  @Get('get/:key')
  async getValue(@Param('key') key: string) {
    return await this.clientService.get(key);
  }
}

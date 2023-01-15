import { HttpService } from '@nestjs/axios';
import { Injectable, NotFoundException } from '@nestjs/common';

@Injectable()
export class ClientService {
  constructor(private readonly httpService: HttpService) {}

  async put(key: string, value: string): Promise<void> {
    const body = { value: value };
    console.log(body);
    await this.httpService
      .post(`http://localhost:3000/coordinator/${key}`, body)
      .toPromise();
  }

  async get(key: string): Promise<string> {
    const response = await this.httpService
      .get(`http://localhost:3000/coordinator/${key}`)
      .toPromise();
    if (response.data === '') {
      throw new NotFoundException();
    }
    return response.data;
  }
}

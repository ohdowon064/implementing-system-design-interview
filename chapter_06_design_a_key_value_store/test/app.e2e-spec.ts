import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication } from '@nestjs/common';
import * as request from 'supertest';
import { AppModule } from './../src/app.module';

describe('AppController (e2e)', () => {
  let app: INestApplication;

  beforeAll(async () => {
    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleFixture.createNestApplication();
    await app.init();
  });

  it('/ (GET)', () => {
    return request(app.getHttpServer())
      .get('/')
      .expect(200)
      .expect('Hello World!');
  });

  describe('/client', () => {
    it('/put/:key (POST)', () => {
      return request(app.getHttpServer())
        .post('/client/put/key1')
        .send({ value: 'test' })
        .expect(201);
    });
    it('/get/:key (GET)', () => {
      return request(app.getHttpServer())
        .get('/client/get/key1')
        .expect(200)
        .expect('test');
    });
  });

  describe('removeNode', () => {
    it('/:id (DELETE)', () => {
      return request(app.getHttpServer()).delete('/coordinator/1').expect(200);
    });
    it('/get/:key (GET 404)', () => {
      return request(app.getHttpServer()).get('/client/get/key1').expect(404);
    });
  });

  describe('addNode', () => {
    it('/node (POST)', () => {
      return request(app.getHttpServer()).post('/coordinator/node').expect(201);
    });
  });
});

import { Module } from '@nestjs/common';
import { AppController } from './app.controller';
import { AppService } from './app.service';
import { CoordinatorModule } from './coordinator/coordinator.module';
import { ClientModule } from './client/client.module';

@Module({
  imports: [CoordinatorModule, ClientModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}

# chapter_7_design_a_unique_id_generator_in_distributed_system
## Tech Specs
### Goal
분산 시스템을 위한 유일 ID 생성기 설계

### Requirements
- ID는 유일해야 한다
- ID는 숫자로만 구성되어야 한다
- ID는 64비트로 표현될 수 있는 값이어야 한다
- ID는 발급 날짜에 따라 정렬할 수 있어야 한다
- 초당 10,000개의 ID를 만들 수 있어야 한다 (Optional)
- 생성기는 라이브러리 형태이든, 웹 API 형태이든 상관없습니다.
- 시계 동기화를 고려할 수 있다면, 고려해주세요.

## Installation

```bash
$ npm install
```

## System Design
- 타임스탬프: Unix 에포크 이후 초 단위로 측정된 ObjectId 생성을 나타내는 4바이트 타임스탬프입니다.
- 랜덤: 프로세스당 한 번 생성되는 5바이트임의 값입니다. 이 무작위 값은 기계와 프로세스에 고유합니다.
- 카운터: 임의의 값으로 초기화되는 3바이트 증분 카운터입니다.

## Code Structure
```bash
$ tree . tree -I node_modules 

tree .
├── README.md
├── mutex.ts
├── objectid.only.number.ts
├── objectid.ts
├── package-lock.json
└── package.json
tree
[1]    58753 segmentation fault  tree . tree -I node_modules

```

## Test

```bash
# unit tests
$ ts-node objectid.only.number.ts
```


# Reference
- random bytes: https://dirask.com/posts/TypeScript-random-bytes-139LYp
- thread locking: https://www.npmjs.com/package/async-lock
- mongodb objectid: https://www.mongodb.com/docs/manual/reference/method/ObjectId/
- js-mutex: https://velog.io/@johnsuhr4542/JS-Mutex-%EC%82%AC%EC%9A%A9
- multiprocessing: https://yogae.tistory.com/34
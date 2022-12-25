## 아키텍처
```mermaid
graph LR
    subgraph Cloud Network
        im[Infra Manager]
    
        subgraph External
            c[Client]
            fs[Forward Server]
        end
        
        subgraph Cache Load Balancer
            ch[Consistent Hashing]
            subgraph Thread
                ro[Redis Observer]
                cm[Config Manager]
            end
        end
        
        subgraph File System
            cy["Config File (.yaml)"]
        end
    
        subgraph Cache Server
            r1[Redis Server 1]
            r2[Redis Server 2]
            ri[Redis Server i]
            ...
            rn[Redis Server n]
        end
    end

    im -- "1. Scale In/Out" --> ri
    cm -- "2. Read periodically" --> cy
    ro -- "3. Observe periodically" --> ri
    c -- "4. Request" --> fs
    fs -- "5. Request(Read/Write) Redis Data" --> ch
    ch -- "6. Get Config" --> cm -. "7. Return Config" .-> ch
    ch -- "8. Get Redis Nodes Count" --> ro -. "9. Return Redis Nodes Count" .-> ch
    ch -- "10. Read or Write" --> ri -. "11. Return Result" .-> ch  
    ch -. "12. Response(Read/Write) Redis Data" .-> fs
    fs -. "13. Successful Response with Headers" .-> c
```

## 테스트 실행 방법

## 참고
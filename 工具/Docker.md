# Docker

> 容器是指运行实例，镜像是模板

---

## 核心概念

- **镜像（Image）**：只读的模板，用于创建容器，类似于类
- **容器（Container）**：镜像的运行实例，类似于对象
- **仓库（Registry）**：存放镜像的地方，默认是 `docker.io`（Docker Hub）
- **卷（Volume）**：用于持久化容器数据，不随容器删除而消失

---

## 镜像管理

### pull — 拉取镜像

```bash
docker pull docker.io/library/nginx:latest
```

- `docker.io` 是官方仓库地址
- `library` 是作者名（官方镜像作者名为 library）
- `nginx:latest` 是镜像名加版本号，不写版本号默认 `latest`

### images — 查看本地镜像

```bash
docker images
```

| 字段 | 说明 |
|---|---|
| REPOSITORY | 镜像名 |
| TAG | 版本标签 |
| IMAGE ID | 镜像唯一 ID |
| SIZE | 镜像大小 |

### rmi — 删除镜像

```bash
docker rmi 镜像名称
docker rmi 镜像ID
```

- 如果有容器正在使用该镜像，需要先删除容器

### search — 搜索镜像

```bash
docker search nginx
```

---

## 容器管理

### run — 创建并启动容器

```bash
docker run 镜像名字
docker run -d 镜像名字
docker run -p 80:80 镜像名字
docker run -d -p 80:80 -v "宿主机目录":"容器目录" nginx
```

| 参数 | 说明 |
|---|---|
| `-d` | 后台运行，不阻塞当前终端 |
| `-p 外:内` | 端口映射，宿主机端口:容器端口 |
| `-v 外:内` | 目录挂载（绑定挂载），宿主机目录:容器目录 |
| `-e KEY=VALUE` | 传递环境变量 |
| `-it` | 交互式终端，可以进入容器内部操作 |
| `--rm` | 容器停止后自动删除容器 |
| `--name 名字` | 给容器指定名字，不指定则随机生成 |
| `--restart` | 重启策略（`no` / `always` / `on-failure` / `unless-stopped`） |
| `--network` | 指定容器所在的网络 |

```bash
# 示例：运行一个 nginx，后台运行，端口映射，挂载目录，自动重启
docker run -d -p 80:80 -v "/data/html":"/usr/share/nginx/html" --restart always --name my-nginx nginx
```

- 容器和宿主机的网络是隔离的，`-p` 做端口关联，顺序是**先外后内**
- `-v` 绑定挂载：两者修改文件会相互影响，但删除容器不会影响宿主机文件

### ps — 查看容器

```bash
docker ps         # 查看正在运行的容器
docker ps -a      # 查看所有容器（包括已停止的）
```

- `ps` 是 `process status` 的缩写

### start / stop / restart — 启停容器

```bash
docker start 容器名字
docker stop 容器名字
docker restart 容器名字
```

### rm — 删除容器

```bash
docker rm 容器名字
docker rm -f 容器名字    # 强制删除正在运行的容器
```

### exec — 进入容器

```bash
docker exec -it 容器名字 /bin/bash
docker exec -it 容器名字 /bin/sh    # 部分镜像没有 bash，用 sh
```

- `-it`：交互式终端
- 进入容器后可以执行容器内的命令，`exit` 退出不会停止容器

### logs — 查看日志

```bash
docker logs 容器名字
docker logs -f 容器名字       # 实时滚动查看日志
docker logs --tail 100 容器名字   # 查看最后 100 行日志
```

### inspect — 查看容器详情

```bash
docker inspect 容器名字
```

- 返回 JSON 格式的容器详细信息，包括网络、挂载、环境变量等

### stats — 查看资源占用

```bash
docker stats              # 实时查看所有容器的资源使用
docker stats 容器名字     # 查看指定容器的资源使用
```

---

## 数据卷（Volume）

数据卷用于持久化数据，生命周期独立于容器，容器删除后数据仍然保留。

```bash
docker volume create 名字        # 创建数据卷
docker volume ls                 # 查看所有数据卷
docker volume inspect 名字       # 查看数据卷详情
docker volume rm 名字            # 删除数据卷
docker volume prune              # 删除所有未被使用的数据卷
```

使用数据卷挂载（替代绑定挂载）：

```bash
docker run -d -v 卷名字:/容器内目录 nginx
```

- 绑定挂载（`-v 宿主机路径:容器路径`）：路径由自己控制
- 数据卷挂载（`-v 卷名:容器路径`）：Docker 管理存储位置，更推荐用于数据持久化

---

## 网络（Network）

### 网络模式

Docker 有几种内置网络模式，通过 `--network` 参数指定：

| 模式 | 说明 |
|---|---|
| `bridge` | 默认模式，容器通过虚拟网桥与宿主机通信，容器间隔离 |
| `host` | 容器直接使用宿主机网络，不做隔离，性能最好但无端口隔离 |
| `none` | 不配置任何网络，完全隔离 |
| `container:容器名` | 共享另一个容器的网络命名空间 |

```bash
docker run --network host nginx        # 使用 host 模式
docker run --network none nginx        # 使用 none 模式
```

---

### Host 网络模式

Host 模式下容器**不再拥有独立的网络命名空间**，而是直接共享宿主机的网络栈，容器的网卡、IP、端口和宿主机完全一致。

```
bridge 模式：                        host 模式：
┌─────────────────────┐              ┌─────────────────────┐
│       宿主机         │              │       宿主机         │
│  eth0: 192.168.1.10 │              │  eth0: 192.168.1.10 │
│  docker0: 172.17.0.1│              │                     │
│    └── 容器(172.17.0.2)│           │  容器（无独立 IP，   │
│         -p 80:80    │              │  直接用宿主机网络）  │
└─────────────────────┘              └─────────────────────┘
外部访问：宿主机IP:80                外部访问：宿主机IP:80（容器监听的端口直接暴露）
```

#### 使用方式

```bash
docker run --network host nginx
```

- **不需要 `-p` 做端口映射**，容器内监听什么端口，宿主机上就直接开放什么端口
- 如果加了 `-p` 参数，在 host 模式下会被**忽略**

#### 特点与适用场景

| 对比项 | bridge 模式 | host 模式 |
|---|---|---|
| 网络隔离 | ✅ 有隔离 | ❌ 无隔离 |
| 端口映射 | 需要 `-p` | 不需要，直接暴露 |
| 性能 | 有一层 NAT 转发开销 | 直接通信，性能最好 |
| 端口冲突 | 容器间不冲突 | 容器与宿主机可能冲突 |
| 适用场景 | 通用场景 | 对网络性能要求高、监控类工具 |

#### 注意事项

- **只在 Linux 上有效**，macOS / Windows 上的 Docker 是跑在虚拟机里的，host 模式共享的是虚拟机的网络，而不是真正的宿主机网络
- 容器内的端口会直接占用宿主机端口，如果多个容器都用 host 模式且监听同一端口，会发生**端口冲突**
- 安全性较低，容器可以直接访问宿主机上的所有网络资源

---

### 桥接模式（Bridge）

桥接模式是 Docker 的**默认网络模式**，Docker 会在宿主机上创建一个名为 `docker0` 的虚拟网桥，所有容器都挂在这个网桥上。

```
宿主机
├── docker0（虚拟网桥，默认网段 172.17.0.0/16）
│   ├── 容器 A（172.17.0.2）
│   ├── 容器 B（172.17.0.3）
│   └── 容器 C（172.17.0.4）
└── eth0（宿主机网卡，连接外网）
```

- 容器通过 `docker0` 网桥互相通信，也能访问外网
- 容器对外不可见，需要通过 `-p` 端口映射才能被外部访问
- **默认 bridge 网络的容器之间只能通过 IP 访问，不能用容器名**

---

### 创建自定义网络（子网）

使用自定义网络可以指定网段，并且容器之间可以**直接用容器名通信**（Docker 内置 DNS 解析）。

```bash
# 创建默认桥接网络
docker network create 网络名

# 创建时指定子网和网关
docker network create \
  --driver bridge \
  --subnet 192.168.10.0/24 \
  --gateway 192.168.10.1 \
  网络名
```

- `--driver bridge`：指定网络驱动为桥接模式（默认可省略）
- `--subnet`：指定网段，格式为 CIDR（如 `192.168.10.0/24` 表示 192.168.10.1 ~ 192.168.10.254）
- `--gateway`：指定网关 IP，通常是子网的第一个地址

```bash
# 示例：创建一个名为 mynet 的网络，网段 10.0.0.0/24
docker network create --subnet 10.0.0.0/24 --gateway 10.0.0.1 mynet
```

---

### 网络管理命令

```bash
docker network ls                           # 查看所有网络
docker network inspect 网络名              # 查看网络详情（含已连接的容器和 IP）
docker network create 网络名               # 创建网络
docker network rm 网络名                   # 删除网络
docker network connect 网络名 容器名       # 将运行中的容器加入网络
docker network disconnect 网络名 容器名    # 将容器从网络移除
docker network prune                       # 删除所有未被使用的网络
```

---

### 容器通信

#### 同一自定义网络下的容器通信

自定义网络内的容器，Docker 会自动做 DNS 解析，**可以直接用容器名当域名访问**：

```bash
# 创建网络
docker network create mynet

# 启动两个容器，都加入同一网络
docker run -d --name app --network mynet my-app
docker run -d --name db  --network mynet mysql:8.0

# 此时 app 容器内可以直接用容器名访问 db
# 比如连接数据库时 host 填 db 即可，不需要填 IP
```

#### 运行时指定容器 IP

在自定义网络中可以给容器分配固定 IP：

```bash
docker run -d --name app --network mynet --ip 192.168.10.10 my-app
```

- 固定 IP 必须在该网络的子网范围内
- 只有自定义网络才能指定固定 IP，默认 bridge 网络不支持

#### 默认 bridge 网络下的容器通信

默认 bridge 网络中的容器**不能用容器名互访**，只能通过 IP：

```bash
# 查看容器 IP
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' 容器名

# 或者通过 --link 参数（旧方式，不推荐）
docker run --link 目标容器名:别名 镜像名
```

> 推荐使用自定义网络替代 `--link`，更灵活安全

#### 容器访问宿主机

在容器内访问宿主机上的服务（如宿主机跑了一个数据库），可以用 Docker 提供的特殊地址：

```bash
host.docker.internal    # Windows / Mac 下可用
172.17.0.1              # Linux 下 docker0 网桥的 IP，即宿主机在容器网络中的地址
```

---

### 多容器通信完整示例

```bash
# 1. 创建自定义网络
docker network create --subnet 172.20.0.0/24 --gateway 172.20.0.1 backend

# 2. 启动数据库容器，加入网络
docker run -d \
  --name mysql \
  --network backend \
  -e MYSQL_ROOT_PASSWORD=123456 \
  -e MYSQL_DATABASE=mydb \
  mysql:8.0

# 3. 启动应用容器，加入同一网络
docker run -d \
  --name app \
  --network backend \
  -p 3000:3000 \
  -e DB_HOST=mysql \
  my-app:1.0

# 4. app 容器内通过容器名 mysql 即可访问数据库，无需关心 IP
```

---

## Dockerfile

用于自定义构建镜像的脚本文件。

```dockerfile
# 基础镜像
FROM node:18-alpine

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY package*.json ./

# 安装依赖
RUN npm install

# 复制项目文件
COPY . .

# 暴露端口
EXPOSE 3000

# 启动命令
CMD ["node", "app.js"]
```

| 指令 | 说明 |
|---|---|
| `FROM` | 指定基础镜像 |
| `WORKDIR` | 设置工作目录，后续命令都在此目录下执行 |
| `COPY` | 从宿主机复制文件到镜像 |
| `ADD` | 类似 COPY，但支持 URL 和自动解压 tar |
| `RUN` | 构建时执行命令（每条 RUN 会新增一层） |
| `CMD` | 容器启动时执行的默认命令，可被 `docker run` 覆盖 |
| `ENTRYPOINT` | 容器启动时执行的命令，不会被覆盖 |
| `ENV` | 设置环境变量 |
| `EXPOSE` | 声明容器监听的端口（仅说明，不自动映射） |
| `VOLUME` | 声明挂载点 |
| `ARG` | 构建时的变量（仅构建阶段有效） |

### build — 构建镜像

```bash
docker build -t 镜像名:版本号 .
docker build -t my-app:1.0 .    # 在当前目录构建，. 表示 Dockerfile 所在位置
```

- `-t`：给镜像打标签（tag）
- `.`：构建上下文路径，Docker 会把这个目录下的文件发送给构建引擎

---

## Docker Compose

用于定义和运行多容器应用，通过 `docker-compose.yml` 文件配置。

```yaml
# docker-compose.yml 示例
services:
  web:
    image: nginx
    ports:
      - "80:80"
    volumes:
      - ./html:/usr/share/nginx/html
    depends_on:
      - app

  app:
    build: .
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=production
    restart: always

  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: 123456
      MYSQL_DATABASE: mydb
    volumes:
      - db_data:/var/lib/mysql

volumes:
  db_data:
```

```bash
docker compose up -d          # 后台启动所有服务
docker compose down           # 停止并删除容器
docker compose down -v        # 停止并删除容器和数据卷
docker compose ps             # 查看服务状态
docker compose logs -f        # 查看日志
docker compose build          # 重新构建镜像
docker compose restart        # 重启服务
```

---

## 推送镜像

将本地构建好的镜像推送到远程仓库，供他人拉取或在服务器上部署使用。

### 推送到 Docker Hub

#### 1. 登录

```bash
docker login
# 或指定仓库地址
docker login docker.io
```

- 输入 Docker Hub 的用户名和密码
- 登录信息会保存在本地，下次无需重复登录
- 退出登录：`docker logout`

#### 2. 给镜像打标签（tag）

推送前必须将镜像名改为 `用户名/镜像名:版本号` 的格式：

```bash
docker tag 本地镜像名:版本号 用户名/镜像名:版本号

# 示例
docker tag my-app:1.0 myusername/my-app:1.0
docker tag my-app:1.0 myusername/my-app:latest
```

- 同一个镜像可以打多个 tag（如同时打 `1.0` 和 `latest`）
- `docker tag` 不会复制镜像，只是给同一个镜像增加一个新名字（别名）

#### 3. 推送

```bash
docker push 用户名/镜像名:版本号

# 示例
docker push myusername/my-app:1.0
docker push myusername/my-app:latest
```

---

### 推送到私有仓库（Registry）

私有仓库常用于公司内网或自建服务器，不走 Docker Hub。

#### 1. 登录私有仓库

```bash
docker login 私有仓库地址

# 示例
docker login registry.example.com
```

#### 2. 打标签

```bash
docker tag 本地镜像名:版本号 私有仓库地址/命名空间/镜像名:版本号

# 示例
docker tag my-app:1.0 registry.example.com/myproject/my-app:1.0
```

#### 3. 推送

```bash
docker push registry.example.com/myproject/my-app:1.0
```

#### 4. 拉取

```bash
docker pull registry.example.com/myproject/my-app:1.0
```

---

### 推送到阿里云容器镜像服务（ACR）

阿里云提供免费的私有镜像仓库，国内网络速度快。

```bash
# 1. 登录
docker login --username=阿里云账号 registry.cn-hangzhou.aliyuncs.com

# 2. 打标签
docker tag 本地镜像名:版本号 registry.cn-hangzhou.aliyuncs.com/命名空间/镜像名:版本号

# 3. 推送
docker push registry.cn-hangzhou.aliyuncs.com/命名空间/镜像名:版本号

# 4. 拉取
docker pull registry.cn-hangzhou.aliyuncs.com/命名空间/镜像名:版本号
```

- 地域不同地址不同，如 `cn-hangzhou`、`cn-shanghai`、`cn-beijing` 等
- 命名空间在阿里云控制台创建

---

### 完整推送流程示意

```bash
# 1. 构建镜像
docker build -t my-app:1.0 .

# 2. 打 tag（以 Docker Hub 为例）
docker tag my-app:1.0 myusername/my-app:1.0
docker tag my-app:1.0 myusername/my-app:latest

# 3. 登录
docker login

# 4. 推送
docker push myusername/my-app:1.0
docker push myusername/my-app:latest
```

---

## 常用清理命令

```bash
docker system prune           # 清理所有未使用的资源（容器、镜像、网络）
docker system prune -a        # 包括未被任何容器使用的镜像一起清理
docker container prune        # 清理所有停止的容器
docker image prune            # 清理所有悬空镜像（没有 tag 的镜像）
```

---

## 常见场景速查

```bash
# 进入正在运行的容器
docker exec -it 容器名 /bin/bash

# 从容器复制文件到宿主机
docker cp 容器名:/容器内路径 宿主机路径

# 从宿主机复制文件到容器
docker cp 宿主机路径 容器名:/容器内路径

# 查看容器 IP
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' 容器名

# 导出镜像为文件
docker save -o 文件名.tar 镜像名

# 从文件加载镜像
docker load -i 文件名.tar
```

---

# 实战案例：前端 + 后端 + 数据库全栈部署

> 以 Vue 前端 + Spring Boot 后端 + MySQL 数据库为例，使用 Docker Compose 一键部署整个项目

## 项目结构

```
my-project/
├── docker-compose.yml
├── frontend/
│   ├── Dockerfile
│   ├── nginx.conf
│   └── dist/                  # Vue 打包后的静态文件
├── backend/
│   ├── Dockerfile
│   └── target/
│       └── app.jar            # Spring Boot 打包后的 jar
└── db/
    └── init.sql               # 数据库初始化脚本
```

---

## 数据库初始化脚本

MySQL 容器首次启动时会自动执行 `/docker-entrypoint-initdb.d/` 目录下的 `.sql` 文件。

```sql
-- db/init.sql
CREATE DATABASE IF NOT EXISTS mydb CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE mydb;

CREATE TABLE user (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO user (username, email) VALUES
('admin', 'admin@example.com'),
('test', 'test@example.com');
```

---

## 后端 Dockerfile

```dockerfile
# backend/Dockerfile
FROM openjdk:17-jdk-slim

WORKDIR /app

COPY target/app.jar app.jar

EXPOSE 8080

# 等待数据库就绪后再启动，避免连接失败
CMD ["java", "-jar", "app.jar"]
```

- 后端连接数据库时，`application.yml` 中 host 填容器名 `mysql`，不填 IP

```yaml
# Spring Boot 的 application.yml 示例
spring:
  datasource:
    url: jdbc:mysql://mysql:3306/mydb?useSSL=false&serverTimezone=Asia/Shanghai
    username: root
    password: 123456
```

---

## 前端 Dockerfile + Nginx 配置

```dockerfile
# frontend/Dockerfile
FROM nginx:alpine

# 删除默认配置
RUN rm /etc/nginx/conf.d/default.conf

# 复制自定义 nginx 配置
COPY nginx.conf /etc/nginx/conf.d/

# 复制打包好的前端文件
COPY dist/ /usr/share/nginx/html/

EXPOSE 80
```

```nginx
# frontend/nginx.conf
server {
    listen 80;
    server_name localhost;

    # 前端静态文件
    location / {
        root /usr/share/nginx/html;
        index index.html;
        try_files $uri $uri/ /index.html;    # Vue Router history 模式
    }

    # 后端 API 反向代理
    location /api/ {
        proxy_pass http://backend:8080/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

- `proxy_pass http://backend:8080`：`backend` 是后端容器名，Docker 自动做 DNS 解析
- 前端请求 `/api/xxx` 会被 Nginx 转发到后端容器的 8080 端口

---

## Docker Compose 配置

```yaml
# docker-compose.yml
services:

  # ---------- 数据库 ----------
  mysql:
    image: mysql:8.0
    container_name: mysql
    environment:
      MYSQL_ROOT_PASSWORD: 123456
      MYSQL_DATABASE: mydb
      TZ: Asia/Shanghai
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql         # 数据持久化
      - ./db/init.sql:/docker-entrypoint-initdb.d/init.sql   # 初始化脚本
    networks:
      - app-network
    restart: always
    command: --character-set-server=utf8mb4 --collation-server=utf8mb4_general_ci
    healthcheck:
      test: ["CMD", "mysqladmin", "ping", "-h", "localhost"]
      interval: 10s
      timeout: 5s
      retries: 5

  # ---------- 后端 ----------
  backend:
    build: ./backend
    container_name: backend
    environment:
      - SPRING_DATASOURCE_URL=jdbc:mysql://mysql:3306/mydb?useSSL=false&serverTimezone=Asia/Shanghai
      - SPRING_DATASOURCE_USERNAME=root
      - SPRING_DATASOURCE_PASSWORD=123456
    ports:
      - "8080:8080"
    networks:
      - app-network
    restart: always
    depends_on:
      mysql:
        condition: service_healthy         # 等 MySQL 健康检查通过后再启动

  # ---------- 前端 ----------
  frontend:
    build: ./frontend
    container_name: frontend
    ports:
      - "80:80"
    networks:
      - app-network
    restart: always
    depends_on:
      - backend

# 自定义网络，三个容器互通，可通过容器名访问
networks:
  app-network:
    driver: bridge

# 数据卷，MySQL 数据持久化
volumes:
  mysql_data:
```

---

## 关键配置说明

| 配置 | 说明 |
|---|---|
| `depends_on` + `healthcheck` | 控制启动顺序：MySQL 先启动且健康 → 后端启动 → 前端启动 |
| `networks: app-network` | 三个容器加入同一网络，互相用容器名访问 |
| `volumes: mysql_data` | MySQL 数据持久化，容器删除后数据不丢失 |
| `proxy_pass http://backend:8080` | 前端 Nginx 反代后端，`backend` 是容器名 |
| `jdbc:mysql://mysql:3306` | 后端连接数据库，`mysql` 是容器名 |

---

## 启动与常用操作

```bash
# 1. 一键启动（首次会自动构建镜像）
docker compose up -d

# 2. 查看运行状态
docker compose ps

# 3. 查看某个服务的日志
docker compose logs -f backend
docker compose logs -f mysql

# 4. 重新构建并启动（代码改了之后）
docker compose up -d --build

# 5. 只重启某一个服务
docker compose restart backend

# 6. 停止所有服务
docker compose down

# 7. 停止并删除数据卷（清空数据库数据）
docker compose down -v
```

---

## 容器间通信流程

```
用户浏览器
    │
    ▼ 访问 http://localhost
┌──────────────┐
│   frontend   │ ── Nginx 托管前端静态文件
│   (80端口)   │ ── /api/* 反向代理到后端
└──────┬───────┘
       │ proxy_pass http://backend:8080
       ▼
┌──────────────┐
│   backend    │ ── Spring Boot 处理业务逻辑
│  (8080端口)  │ ── 连接数据库读写数据
└──────┬───────┘
       │ jdbc:mysql://mysql:3306
       ▼
┌──────────────┐
│    mysql     │ ── 存储数据
│  (3306端口)  │ ── 数据持久化到 volume
└──────────────┘
```

- 三个容器在同一个 `app-network` 网络中
- 容器之间通过**容器名**通信，Docker 自动 DNS 解析
- 只有 frontend 的 80 端口对外暴露，用户所有请求都经过 Nginx 转发

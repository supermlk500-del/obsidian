# Docker 部署第二个网站笔记目录

## 1. 部署背景

### 1.1 服务器环境说明
 `-h` 参数，它一般表示 **human-readable**，也就是“人类可读格式”。
在服务器中执行
```powershell
hostnamectl ## 查看系统信息
nproc ## 查看处理器核数
free -h ## 查看内存
df -h ## 查看磁盘
nginx -v ## 查看nginx版本
docker version ## 查看docker版本
docker compose version ## 查看docker compose版本
```
![[服务器信息.png]]

### 1.2 已有第一个网站的部署情况
```powershell
systemctl status 服务名 --no-pager -l ## 查看已有服务状态
ps -ef | grep '[j]ava' ## 查看java进程
nginx -T | grep -n "mlksuper.top\|服务名\|端口\|root" -C 5 ## 查看宿主机 Nginx 配置
```

### 1.3 第二个网站的部署目标
```text
第二个网站名称：Zhihuitong / 织慧通
部署目录：/opt/saas
访问域名：zhihuitong.mlksuper.top
部署方式：Docker Compose
前端：Nginx 容器
后端：Spring Boot jar 容器
数据库：连接宿主机 MySQL
模型文件：best.onnx
```

### 1.4 为什么选择 Docker 部署第二个网站

---

## 2. 整体部署架构

### 2.1 最终访问链路
curl是用命令行发送http请求
`-k` 表示忽略 HTTPS 证书校验，也叫 `--insecure`。因为你访问的是 HTTPS，如果证书不完整、证书域名不匹配、使用自签证书，curl 默认会拒绝请求。加 `-k` 后，curl 会继续请求。这个参数只适合测试排查，正式环境不代表证书已经没问题。

`-i` 表示把响应头也打印出来，也叫 `--include`。不加 `-i` 时，通常只看到响应体；
```powershell
curl -k -i '页面中能勾请求到好端的请求' ## 需要返回成功和业务json
curl -i 'http://127.0.0.1:18080/prod-api/api/batches?pageNum=1&pageSize=1' ## 这里是测试宿主机到docker前端容器的链路
```

```text
浏览器
 ↓
域名
 ↓
宿主机nginx
 ↓
本地如127.0.0.1:18080
 ↓
容器:nginx:端口
 ↓
/prod-api/转发
 ↓
后端容器:端口
 ↓
宿主机mysql
```

### 2.2 宿主机 Nginx、前端容器、后端容器的职责划分
```bash
nginx -T | grep -n "域名\|端口" -C 8 ## 查看宿主机nginx
```
![[查看宿主机nginx.png]]
- 宿主机nginx主要职责
	- 接收公网请求
	- 处理域名和https
	- 把域名的所有请求转发
```bash
cat 前端nginx配置文件 ## 查看前端nginx
```
![[前端nginx.png]]
- 前端容器的职责
	- 提供前端静态页面
	- 处理前端路由
	- 把 /prod-api/请求转发给 后端:端口
```bash
docker logs --tail=80 服务名 ## 查看后端容器日志
```
- 主要职责
	- 运行springboot后端服务
	- 监听容器内部8081端口
	- 链接mysql
	- 处理业务api
常用参数说明：

- `curl -k`：忽略 HTTPS 证书校验，适合临时测试自签名证书或证书未完全配置好的站点。
- `curl -i`：显示 HTTP 响应头，方便查看状态码、server、content-type 等信息。
- `nginx -t`：检查 Nginx 配置语法是否正确，不输出完整配置。
- `nginx -T`：检查 Nginx 配置语法，并打印 Nginx 实际加载的完整配置。
- `grep -n`：显示匹配行的行号。
- `grep -C 5`：显示匹配行上下各 5 行上下文。
- `grep -E`：启用扩展正则表达式，便于使用 `|` 表示“或”。
- `-h`：在 `df -h`、`free -h` 中表示 human-readable，即用更易读的 GB、MB 等单位显示。
### 2.3 宿主机端口与容器端口的区别
```bash
docker ps ## 
```
![[Pasted image 20260619014808.png]]
```bash
ss -lntp | grep -E ':80|:443|:18080|:8081|:3306' ## 查看宿主机端口
```
| 项目 | 容器内部端口 | 宿主机端口 | 是否公网直接访问 |
|---|---:|---:|---|
| saas-frontend | 80 | 127.0.0.1:18080 | 否，只允许宿主机 Nginx 访问 |
| saas-backend | 8081 | 无直接映射 | 否，只允许 Docker 内部访问 |
| 宿主机 Nginx | 80 / 443 | 80 / 443 | 是 |
| LinguaLearn 后端 | 无容器 | 8081 | 否，通过 Nginx 转发 |
### 2.4 为什么 Docker 后端不直接暴露到公网
1. 后端接口不应该直接暴露公网,避免绕过前端代理和安全控制
2. 宿主机8081已经被占用
3. docker后端只需要被前端容器访问,不需要外部访问
4. 使用docker内部网络可以通过服务名访问后端
5. 后端不映射宿主机端口,可以减少端口冲突

### 2.5 第二个网站与第一个网站的端口隔离方案

---

## 3. 服务器目录规划

### 3.1 `/opt/saas` 项目根目录
/opt/saas 是第二个网站 Zhihuitong 的部署根目录，里面包含前端文件、后端 jar、Dockerfile、docker-compose.yml、模型文件和数据目录。

### 3.2 后端目录：`/opt/saas/backend`
/opt/saas/backend 用来存放后端 Spring Boot jar 包和后端 Dockerfile。Docker 构建时会把该目录下的 jar 文件复制到容器内的 /app/app.jar，然后通过 java -jar 启动。
重新上传后端时，需要把新的 jar 放到 /opt/saas/backend，然后重新构建后端容器。
```bash
docker compose up -d --build saas-backend
```

### 3.3 前端目录：`/opt/saas/frontend`
/opt/saas/frontend 用来存放前端打包产物、前端容器 Dockerfile 和前端容器内部的 nginx.conf。前端容器启动后，Nginx 从 /usr/share/nginx/html 提供静态页面，并把 /prod-api/ 请求转发给后端容器。
```bash
docker compose up -d --build saas-frontend
```
### 3.4 模型文件目录：`/opt/saas/docs`
宿主机上的模型文件路径是 /opt/saas/docs/best.onnx。
容器内后端读取的路径不是这个，而是 /app/docs/best.onnx。
两者通过 docker-compose.yml 的 volumes 映射关联。
```bash
volumes:
  - /opt/saas/docs:/app/docs:ro ## 这里的 `:ro` 表示只读挂载。容器只能读取模型文件，不能修改宿主机模型文件。
```
/opt/saas/docs 用来存放 YOLO ONNX 模型文件 best.onnx。后端代码在 Docker 容器内读取 /app/docs/best.onnx，因此必须通过 volumes 将宿主机的 /opt/saas/docs 挂载到容器内的 /app/docs。

### 3.5 数据持久化目录：`/opt/saas/data`
/opt/saas/data 用来保存业务运行时产生的数据，例如上传文件和检测结果。该目录通过 volumes 挂载到容器内 /app/data，避免容器删除或重建时数据丢失。

### 3.6 宿主机路径与容器内路径的映射关系
| 用途         | 宿主机路径                          | 容器内路径                   | 说明                  |
| ---------- | ------------------------------ | ----------------------- | ------------------- |
| 后端 jar     | `/opt/saas/backend/*.jar`      | `/app/app.jar`          | 构建镜像时复制进去           |
| 前端静态文件     | `/opt/saas/frontend`           | `/usr/share/nginx/html` | 构建前端镜像时复制进去         |
| YOLO 模型文件  | `/opt/saas/docs/best.onnx`     | `/app/docs/best.onnx`   | volumes 只读挂载        |
| 上传文件       | `/opt/saas/data/upload`        | `/app/data/upload`      | volumes 持久化挂载       |
| 检测结果       | `/opt/saas/data/results`       | `/app/data/results`     | volumes 持久化挂载       |
| Compose 配置 | `/opt/saas/docker-compose.yml` | 不进入容器                   | Docker Compose 编排文件 |
本次部署将第二个网站的所有文件统一放在 `/opt/saas` 下。需要区分“宿主机路径”和“容器内路径”：后端程序运行在容器中，因此代码中配置的路径必须是容器内路径，例如 `/app/docs/best.onnx`，而不是宿主机路径 `/opt/saas/docs/best.onnx`。宿主机路径通过 Docker volumes 映射到容器内部。

---

## 4. 后端 Docker 容器配置

### 4.1 后端 jar 文件准备
本次部署将第二个网站的所有文件统一放在 `/opt/saas` 下。需要区分“宿主机路径”和“容器内路径”：后端程序运行在容器中，因此代码中配置的路径必须是容器内路径，例如 `/app/docs/best.onnx`，而不是宿主机路径 `/opt/saas/docs/best.onnx`。宿主机路径通过 Docker volumes 映射到容器内部。

### 4.2 后端 Dockerfile 编写
```dockerfile
FROM eclipse-temurin:21-jre ## 使用java21运行环境作为基础镜像

WORKDIR /app ## 设置容器内工作目录为/app

COPY *.jar /app/app.jar ## 将 backend 目录下的 jar 复制到容器内，并命名为 app.jar

EXPOSE 8081 ## 声明后端容器内部服务端口号

CMD ["java", "-Xms128m", "-Xmx512m", "-XX:MaxMetaspaceSize=128m", "-jar", "/app/app.jar"] ## 启动时执行的命令,可以限制资源

```

### 4.3 Java 运行参数说明
```bash
java -Xms128m -Xmx512m -XX:MaxMetaspaceSize=128m -jar /app/app.jar
```
| 参数 | 作用 |
|---|---|
| `java` | 启动 Java 运行时 |
| `-Xms128m` | 设置 JVM 初始堆内存为 128MB |
| `-Xmx512m` | 设置 JVM 最大堆内存为 512MB |
| `-XX:MaxMetaspaceSize=128m` | 限制 Metaspace 最大为 128MB |
| `-jar /app/app.jar` | 运行容器内的 Spring Boot jar |

### 4.4 JVM 内存限制：`-Xms`、`-Xmx`、`MaxMetaspaceSize`
Java 应用如果不限制 JVM 内存，在流量增加、对象创建较多或出现内存泄漏时，可能持续占用系统内存。为了避免单个服务拖垮整台服务器，本次后端容器同时使用 JVM 限制和 Docker 容器限制。
```markdown
- `-Xmx512m`：限制 Java 堆内存最大 512MB。
- `-Xms128m`：降低启动时预占用内存。
- `-XX:MaxMetaspaceSize=128m`：限制类元数据区域，避免 Metaspace 过度增长。
```

### 4.5 `EXPOSE 8081` 的含义
`EXPOSE 8081` 只是声明容器内部应用监听 8081 端口，方便其他容器或运维人员理解该镜像的服务端口。它不会自动占用宿主机的 8081 端口，也不会让公网访问到该端口。

### 4.6 为什么后端只使用 `expose` 而不是 `ports`
后端接口不需要直接暴露到宿主机或公网。外部用户访问网站时，先进入宿主机 Nginx，再进入前端容器。只有当前端请求 `/prod-api/` 接口时，前端容器中的 Nginx 才会把请求转发到 `saas-backend:8081`。
```
浏览器
  ↓
宿主机 Nginx
  ↓
127.0.0.1:18080
  ↓
saas-frontend 容器
  ↓
http://saas-backend:8081
  ↓
saas-backend 容器
```

---

## 5. 前端 Docker 容器配置

### 5.1 前端打包文件准备
前端项目已经在本地完成打包，并上传到服务器 `/opt/saas/frontend` 目录。该目录中包含前端静态资源、前端容器的 `Dockerfile`，以及前端容器内部使用的 `nginx.conf`。

### 5.2 前端 Dockerfile 编写
```dockerfile
FROM nginx:alpine ## 使用轻量级nginx镜像作为前端运行环境

COPY . /usr/share/nginx/html ## 将前端打包文件复制到 Nginx 默认静态资源目录
COPY nginx.conf /etc/nginx/conf.d/default.conf ## 使用自定义nginx配置覆盖容器默认站点配置

EXPOSE 80 ## 声明前端容器使用80端口提供http服务

```
这里使用 `COPY . /usr/share/nginx/html`，说明 `/opt/saas/frontend` 下的内容会被整体复制进容器。更新前端时，需要替换 `/opt/saas/frontend` 下的打包文件，然后重新构建 `saas-frontend` 容器。

### 5.3 使用 `nginx:alpine` 托管前端静态资源
前端项目打包后本质上是一组静态文件，例如 `index.html`、`assets/*.js`、`assets/*.css`。这些文件不需要 Node.js 运行环境，使用 Nginx 直接托管即可。`nginx:alpine` 镜像体积较小，适合用于生产环境提供静态资源。

### 5.4 前端容器端口映射：`127.0.0.1:18080:80`
```docker-compose
services:
  saas-backend:
    build:
      context: ./backend
    container_name: saas-backend
    restart: always
    extra_hosts:
      - "host.docker.internal:host-gateway"
    environment:
      - TZ=Asia/Shanghai
      - SERVER_PORT=8081
      - MYSQL_HOST=host.docker.internal
      - MYSQL_PORT=3306
      - MYSQL_DATABASE=zhihuitong
      - MYSQL_USERNAME=zhihuitong
      - MYSQL_PASSWORD=<DB_PASSWORD>
    volumes:
      - /opt/saas/docs:/app/docs:ro
      - /opt/saas/data:/app/data
    expose:
      - "8081"
    mem_limit: 800m
    cpus: 1.0

  saas-frontend:
    build:
      context: ./frontend
    container_name: saas-frontend
    restart: always
    ports:
      - "127.0.0.1:18080:80"
    depends_on:
      - saas-backend
    mem_limit: 128m
    cpus: 0.5

```
`127.0.0.1:18080:80` 表示将容器内部的 80 端口映射到宿主机本地地址 `127.0.0.1` 的 `18080` 端口。
### 5.5 前端容器中的 Nginx 配置
```nginx.conf
server {
    listen 80; ## 监听端口
    server_name _;

    root /usr/share/nginx/html; ## 静态文件根目录
    index index.html;## 默认首页文件

    location / {
        try_files $uri $uri/ /index.html; ## 处理前端页面和spa路由.当访问的路径对应真实文件时，Nginx 直接返回该文件；如果找不到对应文件，就回退到 `index.html`。这对 Vue / React 单页应用很重要，否则刷新 `/dashboard` 这类前端路由时会出现 404。
    }

    location /prod-api/ { ## 处理前端生产环境api请求
        proxy_pass http://saas-backend:8081/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /api/ {
        proxy_pass http://saas-backend:8081/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```
- `/usr/share/nginx/html` 是 Nginx 官方镜像默认的静态资源目录。本项目使用 `nginx:alpine` 作为前端基础镜像，因此将前端打包文件复制到该目录，并在 `nginx.conf` 中通过 `root /usr/share/nginx/html;` 指定 Nginx 从该目录读取 `index.html` 和 `assets` 等静态资源。

需要注意的是，`/opt/saas/frontend` 是宿主机上的目录，`/usr/share/nginx/html` 是容器内部的目录。构建镜像时，Dockerfile 中的 `COPY . /usr/share/nginx/html` 会把宿主机前端目录中的文件复制进容器内部。

### 5.6 `/prod-api/` 代理到后端容器的配置

---

## 6. Docker Compose 编排

### 6.1 `docker-compose.yml` 的整体结构

`docker-compose.yml` 是本次 Docker 部署的核心编排文件，用来同时管理前端容器和后端容器。通过 Docker Compose，可以用一个配置文件定义多个服务的构建方式、容器名称、端口映射、环境变量、目录挂载、资源限制和启动顺序。

```docker-compose.yml
services:
  saas-backend:
    build:
      context: ./backend
    container_name: saas-backend
    restart: always
    extra_hosts:
      - "host.docker.internal:host-gateway"
    environment:
      - TZ=Asia/Shanghai
      - SERVER_PORT=8081
      - MYSQL_HOST=host.docker.internal
      - MYSQL_PORT=3306
      - MYSQL_DATABASE=zhihuitong
      - MYSQL_USERNAME=zhihuitong
      - MYSQL_PASSWORD=<DB_PASSWORD>
    volumes:
      - /opt/saas/docs:/app/docs:ro
      - /opt/saas/data:/app/data
    expose:
      - "8081"
    mem_limit: 800m
    cpus: 1.0

  saas-frontend:
    build:
      context: ./frontend
    container_name: saas-frontend
    restart: always
    ports:
      - "127.0.0.1:18080:80"
    depends_on:
      - saas-backend
    mem_limit: 128m
    cpus: 0.5
```
-  `services`下的每一个二级配置都代表要给容器服务.上面的代码定义了两个服务
### 6.2 `saas-backend` 服务配置
```docker-compose.yml
saas-backend:
  build:
    context: ./backend ## 这里表示使用什么目录来构建镜像
  container_name: saas-backend ## 指定容器名字
  restart: always ## 服务器重启或者容器异常退出后自动重启
  extra_hosts:
    - "host.docker.internal:host-gateway" ## 让容器可以通过`host.docker.internal` 访问宿主机
  environment: ## 给后端传入运行环境配置
    - TZ=Asia/Shanghai
    - SERVER_PORT=8081
    - MYSQL_HOST=host.docker.internal
    - MYSQL_PORT=3306
    - MYSQL_DATABASE=zhihuitong
    - MYSQL_USERNAME=zhihuitong
    - MYSQL_PASSWORD=<DB_PASSWORD>
    - AI_YOLO_MODEL_PATH=/app/docs/best.onnx
    - INSPECTION_STORAGE_UPLOAD_ROOT=/app/data/upload
    - INSPECTION_STORAGE_RESULT_ROOT=/app/data/results
  volumes: ## 把宿主机模型文件和数据目录挂载进容器
    - /opt/saas/docs:/app/docs:ro
    - /opt/saas/data:/app/data
  expose: ## 只在内部暴露8081,不映射宿主机
    - "8081"
  mem_limit: 800m ## 限制后端容器使用的内存
  cpus: 1.0 ## 限制后端容器最多使用1核cpu
```

### 6.3 `saas-frontend` 服务配置
```docker.compose.yml
saas-frontend:
  build:
    context: ./frontend
  container_name: saas-frontend
  restart: always
  ports:
    - "127.0.0.1:18080:80" ## 将内部容器80端口映射到宿主机本地18080端口
  depends_on:
    - saas-backend
  mem_limit: 128m
  cpus: 0.5
```
- 前端容器没有直接占用宿主机 80 端口，而是映射到 `127.0.0.1:18080`。公网请求先进入宿主机 Nginx，再由宿主机 Nginx 转发到这个本地端口。
### 6.4 容器启动策略：`restart: always`
```bash
docker ps -a ## 查看所有容器，包括已经退出的
```

### 6.5 容器资源限制：`mem_limit` 与 `cpus`
```bash
docker stats ## 查看容器资源使用
```

### 6.6 容器间通信：通过服务名访问 `saas-backend`
```nginx
proxy_pass http://saas-backend:8081/; ## saas-backend 是 Docker Compose 服务名
```
- Docker Compose 会为同一个 `docker-compose.yml` 中的服务创建默认内部网络。在这个网络中，容器之间可以直接通过服务名互相访问。因此，前端容器可以通过 `http://saas-backend:8081` 访问后端容器。
### 6.7 重新构建与启动容器
- 首次构建并启动
```bash
docker compose up -d --build
```
- 只构建后端
```bash
docker compose up -d --build saas-backend
```
- 只构建前端
```bash
docker compose up -d --build saas-frontend
```
- 停止并删除当前compose管理的容器
```bash
docker compose down
```
- 前后端否更新重新部署
```bash
docker compose down
docker compose up -d --build
```
- 无缓存重新构建
```bash
docker compose build --no-cache
docker compose up -d
```
- 查看后端服务
```bash
docker logs -f saas-backend
```
- 退出实时日志
```test
ctrl+c
```

---

## 7. 模型文件与数据目录挂载

### 7.1 YOLO ONNX 模型文件的部署位置
后端项目需要读取 YOLO ONNX 模型文件 `best.onnx`。该文件没有打包进后端 jar，而是单独放在宿主机目录 `/opt/saas/docs` 下。

宿主机上的实际模型文件路径为：/opt/saas/docs/best.onnx

### 7.2 `best.onnx` 文件找不到的问题
部署过程中后端容器启动失败，日志提示找不到 YOLO ONNX 模型文件。错误路径为 Windows 本地开发环境路径：D:\lhr\Desktop\saas\docs\best.onnx

### 7.3 Windows 路径与 Linux 容器路径的差异
本地开发环境和服务器 Docker 环境的文件路径不同：

| 环境             | 示例路径                                 | 是否适合 Docker 部署 |
| -------------- | ------------------------------------ | -------------- |
| Windows 本地开发环境 | `D:\lhr\Desktop\saas\docs\best.onnx` | 不适合            |
| Linux 宿主机路径    | `/opt/saas/docs/best.onnx`           | 宿主机可访问         |
| Docker 容器内路径   | `/app/docs/best.onnx`                | 后端程序应使用        |
后端 Spring Boot 程序运行在 `saas-backend` 容器中，因此配置文件里应该写容器内路径：/app/docs/best.onnx
### 7.4 使用 volumes 挂载 `/opt/saas/docs:/app/docs:ro`
```yml
volumes:
  - /opt/saas/docs:/app/docs:ro
```
- 含义是把宿主机上的目录挂载到容器中的目录并且设置为只读
- 通过 Docker Compose 的 `volumes` 配置，将宿主机模型目录 `/opt/saas/docs` 挂载到后端容器内的 `/app/docs`。因此后端程序应该读取 `/app/docs/best.onnx`。

这里使用 `:ro` 表示只读挂载，后端容器只能读取模型文件，不能修改宿主机上的模型文件，安全性更高。
### 7.5 上传目录和结果目录挂载：`/opt/saas/data:/app/data`
`/opt/saas/data` 用来保存后端运行过程中产生的数据，例如上传图片和检测结果。该目录通过 volumes 挂载到容器内 `/app/data`，这样即使后端容器删除或重新构建，业务数据仍然保留在宿主机上。

### 7.6 使用环境变量覆盖后端路径配置
这一节写最终解决办法。

因为后端 jar 里可能还保留 Windows 路径，所以我们在 `docker-compose.yml` 里用环境变量覆盖。

在 `saas-backend` 的 `environment` 下添加或确认有：

```yaml
environment:
  - AI_YOLO_MODEL_PATH=/app/docs/best.onnx
  - INSPECTION_STORAGE_UPLOAD_ROOT=/app/data/upload
  - INSPECTION_STORAGE_RESULT_ROOT=/app/data/results
```

这几行对应后端配置：

```yaml
ai:
  yolo:
    model-path: /app/docs/best.onnx
inspection:
  storage:
    upload-root: /app/data/upload
    result-root: /app/data/results
```

笔记里可以这样写：

```
为了避免 jar 包中的配置仍然使用本地 Windows 路径，本次部署在 `docker-compose.yml` 中通过环境变量覆盖后端配置。Spring Boot 支持宽松绑定，环境变量 `AI_YOLO_MODEL_PATH` 可以覆盖配置项 `ai.yolo.model-path`，`INSPECTION_STORAGE_UPLOAD_ROOT` 可以覆盖 `inspection.storage.upload-root`，`INSPECTION_STORAGE_RESULT_ROOT` 可以覆盖 `inspection.storage.result-root`。
```

修改后需要重新启动后端容器：

```bash
cd /opt/saas
docker compose up -d --build saas-backend
```

如果想完整重启：

```bash
cd /opt/saas
docker compose down
docker compose up -d --build
```

然后查看日志：

```
docker logs -f saas-backend
```

正常情况下，不应该再出现：

```
D:\lhr\Desktop\saas\docs\best.onnx
```

而应该使用：

```
/app/docs/best.onnx
```

---

这一章你需要收集的命令主要是：

```bash
ls -lh /opt/saas/docs
ls -lh /opt/saas/docs/best.onnx
find /opt/saas/data -maxdepth 2 -type d | sort
cat /opt/saas/docker-compose.yml
docker exec -it saas-backend ls -lh /app/docs
docker exec -it saas-backend ls -lh /app/docs/best.onnx
docker exec -it saas-backend ls -lh /app/data
docker logs --tail=100 saas-backend
```

第七章最后可以这样总结：

```
本次部署中，模型文件和业务数据目录没有直接打包进后端 jar，而是通过 Docker volumes 从宿主机挂载到容器内。宿主机上的 `/opt/saas/docs/best.onnx` 在容器内对应 `/app/docs/best.onnx`，后端程序必须使用容器内路径读取模型文件。上传文件和检测结果统一挂载到 `/app/data`，保证容器重建后数据不会丢失。
```

这一章的核心是：**Docker 容器里的程序只能使用容器内路径。宿主机路径必须通过 volumes 映射后，才能在容器中访问。**

---

## 8. 后端配置文件适配 Docker 环境

### 8.1 `server.port` 修改为容器内部端口
后端原始配置中 `server.port` 可能是 `8080`，但在 Docker 部署中，后端容器内部统一使用 `8081` 端口。为了避免修改 jar 内部配置，本次通过 Docker Compose 环境变量 `SERVER_PORT=8081` 覆盖 Spring Boot 的 `server.port` 配置。

前端容器中的 Nginx 通过 `http://saas-backend:8081` 访问后端，因此后端实际监听端口必须与代理配置保持一致。
### 8.2 `ai.yolo.model-path` 的路径修改
本地开发时，YOLO 模型路径使用的是 Windows 路径，例如 `D:\lhr\Desktop\saas\docs\best.onnx`。部署到 Docker 后，后端程序运行在 Linux 容器中，不能访问 Windows 路径。

本次部署将宿主机目录 `/opt/saas/docs` 挂载到容器内 `/app/docs`，因此后端程序应读取容器内路径 `/app/docs/best.onnx`。

通过 Docker Compose 环境变量 `AI_YOLO_MODEL_PATH=/app/docs/best.onnx` 覆盖后端配置项 `ai.yolo.model-path`。
### 8.3 `inspection.storage.upload-root` 的路径修改
后端上传文件目录不能继续使用本地 Windows 路径。Docker 容器内使用 `/app/data/upload` 作为上传文件目录，并通过 Docker volumes 将宿主机 `/opt/saas/data` 挂载到容器内 `/app/data`。

这样上传文件实际保存在宿主机 `/opt/saas/data/upload` 中，即使容器被删除或重建，上传文件也不会丢失。

### 8.4 `inspection.storage.result-root` 的路径修改
检测结果目录也需要从 Windows 本地路径改为 Docker 容器内路径。本次使用 `/app/data/results` 保存检测结果，对应宿主机目录 `/opt/saas/data/results`。

该目录通过 volumes 挂载实现持久化，避免容器重新构建后结果文件丢失。

### 8.5 `application.yml` 与 `application-dev.yml` 的覆盖关系
后端项目启用了 `dev` profile，因此 Spring Boot 启动时不仅会读取 `application.yml`，还会读取 `application-dev.yml`。如果 `application-dev.yml` 中仍然配置了 Windows 本地路径，即使 `application.yml` 已经修改，也可能导致部署后继续读取错误路径。

因此排查配置问题时，需要同时检查 `application.yml` 和 `application-dev.yml`。

### 8.6 重新上传 jar 后路径配置回退的问题
重新上传后端 jar 后，原本已经解决的模型路径问题再次出现。原因是新打包的 jar 中仍然保留了本地 Windows 路径，导致容器启动时继续读取 `D:\lhr\Desktop\saas\docs\best.onnx`。

为避免每次打包都因为环境路径不同导致问题，本次最终选择在 `docker-compose.yml` 中使用环境变量统一覆盖部署环境配置。

---

## 9. Docker 容器连接宿主机 MySQL

### 9.1 Docker 容器中的 `localhost` 含义
```text
localhost = 当前容器自己
```
Docker 容器有独立的网络命名空间。后端程序运行在 `saas-backend` 容器中，因此容器内的 `localhost` 指向的是容器自身，而不是宿主机。如果后端在容器中使用 `localhost:3306` 连接 MySQL，就会尝试连接容器自己的 3306 端口，导致连接失败。
### 9.2 为什么容器不能直接使用 `localhost:3306`
部署初期，后端容器连接数据库失败，日志中出现 `Communications link failure` 和 `Connection refused`。原因是后端容器中配置的数据库地址默认为 `localhost`，但容器内的 `localhost` 并不是宿主机，因此无法连接宿主机上的 MySQL。

### 9.3 使用 `host.docker.internal` 访问宿主机
为了让 Docker 容器访问宿主机 MySQL，本次部署使用 `host.docker.internal` 作为宿主机地址。后端容器通过 `host.docker.internal:3306` 连接宿主机上的 MySQL 服务。

### 9.4 `extra_hosts: host.docker.internal:host-gateway` 的作用
在 Linux 服务器中，Docker 容器默认不一定能识别 `host.docker.internal`。因此需要在 `docker-compose.yml` 中通过 `extra_hosts` 手动添加映射：

```yaml
extra_hosts:
  - "host.docker.internal:host-gateway"
```
这行配置的作用是：让容器内的 `host.docker.internal` 指向 Docker 提供的宿主机网关地址，从而使容器能够访问宿主机上的 MySQL。

### 9.5 MySQL 环境变量配置
```yml
environment:
  - MYSQL_HOST=host.docker.internal
  - MYSQL_PORT=3306
  - MYSQL_DATABASE=zhihuitong
  - MYSQL_USERNAME=zhihuitong
  - MYSQL_PASSWORD=<DB_PASSWORD>
```
后端项目的数据库连接信息通过 Docker Compose 环境变量传入。这样可以避免把服务器数据库地址、用户名和密码写死在 jar 包中，也便于不同环境使用不同配置。
| 环境变量 | 作用 |
|---|---|
| `MYSQL_HOST` | MySQL 主机地址，这里为 `host.docker.internal` |
| `MYSQL_PORT` | MySQL 端口，默认为 `3306` |
| `MYSQL_DATABASE` | 业务数据库名 |
| `MYSQL_USERNAME` | 数据库用户名 |
| `MYSQL_PASSWORD` | 数据库密码 |
### 9.6 MySQL 用户授权问题
```text
Host '172.18.0.2' is not allowed to connect to this MySQL server
```
- 这是说明容器已经能够访问到mysql,但是mysql不允许这个来源ip的用户连接
- 当后端日志出现 `Host '172.18.0.2' is not allowed to connect to this MySQL server` 时，说明网络已经打通，但 MySQL 用户权限不足。MySQL 用户不仅包含用户名，还包含允许连接的来源主机。例如 `'root'@'localhost'` 只允许本机连接，不允许 Docker 容器 IP 连接。
### 9.7 创建业务专用数据库用户
- 最终不使用root,而是创建业务专用用户
```bash
mysql -uroot -p ##登录mysql
```

为了让 Docker 后端容器可以连接数据库，本次没有继续使用 root 用户，而是创建了业务专用数据库用户：
```mysql
CREATE USER IF NOT EXISTS 'zhihuitong'@'%' IDENTIFIED BY '<DB_PASSWORD>';
GRANT ALL PRIVILEGES ON zhihuitong.* TO 'zhihuitong'@'%';
FLUSH PRIVILEGES;
```
### 9.8 `Host '172.18.0.2' is not allowed` 的原因与解决
错误：

```
Host '172.18.0.2' is not allowed to connect to this MySQL server
```

原因：

```
MySQL 用户没有允许 Docker 容器 IP 连接。
```

解决：

```
创建 'zhihuitong'@'%' 用户，并授权 zhihuitong 数据库。
```

验证方式：

```bash
cd /opt/saas
docker compose up -d --build saas-backend
docker logs -f saas-backend
```

正常日志里应该看到类似：

```text
HikariPool-1 - Start completed
Tomcat started on port 8081
Started ZhihuitongApplication
```

笔记可以写：

```
该错误不是密码错误，也不是数据库不存在，而是 MySQL 用户的来源主机限制导致。创建 `'zhihuitong'@'%'` 并授予 `zhihuitong.*` 权限
```

### 9.9 MySQL `bind-address` 配置注意事项
MySQL 默认可能只监听：

```
127.0.0.1
```

如果只监听 `127.0.0.1`，Docker 容器可能无法从宿主机网关地址连接进来。

配置文件通常在：

```
/etc/mysql/mysql.conf.d/mysqld.cnf
```

查看配置：

```
grep -R "bind-address" /etc/mysql/ -n
```

正确写法：

```
bind-address = 0.0.0.0
```

错误写法包括：

```text
bind-address: 0.0.0.0
bind-address = host.docker.internal
bind-address = 一个服务器不存在的 IP
```

我们曾经遇到 MySQL 启动失败：

```
Error: 99 Cannot assign requested address
```

这通常说明 `bind-address` 写成了一个本机没有的地址，导致 MySQL 无法绑定该地址。

修改后重启 MySQL：

```bash
systemctl restart mysql
systemctl status mysql --no-pager -l
```

检查端口监听：

```
ss -lntp | grep 3306
```

笔记里可以写：

MySQL 的 `bind-address` 用来控制 MySQL 监听哪个网络地址。如果只监听 `127.0.0.1`，可能只允许本机回环访问；如果需要 Docker 容器通过宿主机网关访问 MySQL，可以将其设置为 `0.0.0.0`。`bind-address` 必须写在 MySQL 配置文件的 `[mysqld]` 段下：

```ini
bind-address = 0.0.0.0
```

不要写成 `host.docker.internal`，也不要写成服务器不存在的 IP，否则 MySQL 可能启动失败并报 `Cannot assign requested address`。

第九章需要收集的命令主要是：

```bash
cat /opt/saas/docker-compose.yml
docker exec -it saas-backend printenv | grep -E "MYSQL_HOST|MYSQL_PORT|MYSQL_DATABASE|MYSQL_USERNAME"
docker exec -it saas-backend getent hosts host.docker.internal
grep -R "bind-address" /etc/mysql/ -n
ss -lntp | grep 3306
mysql -uroot -p
```

进入 MySQL 后可查：

```sql
SELECT user, host FROM mysql.user WHERE user = 'zhihuitong';
SHOW GRANTS FOR 'zhihuitong'@'%';
```

第九章最后可以这样总结：

```
Docker 容器中的 `localhost` 指向容器自身，不是宿主机。因此后端容器不能使用 `localhost:3306` 连接宿主机 MySQL。本次部署通过 `extra_hosts` 添加 `host.docker.internal:host-gateway` 映射，并在后端环境变量中配置 `MYSQL_HOST=host.docker.internal`，让后端容器访问宿主机 MySQL。同时，为避免 MySQL 用户来源限制问题，创建了业务专用用户 `'zhihuitong'@'%'` 并授权 `zhihuitong` 数据库。
```

这一章的核心结论是：

```
容器访问宿主机服务，不能直接用 localhost。MySQL 连接不仅要网络通，还要 MySQL 用户权限允许。
```

---

## 10. 宿主机 Nginx 反向代理配置

### 10.1 为什么需要子域名独立 server 块
- 服务器上有多个网站的时候
- nginx必须通过不同的`server_name`判断请求属于哪一个网站
```bash
nginx -T | grep -n "server_name" -C 3
```
宿主机 Nginx 负责接收公网 80/443 请求。由于同一台服务器上部署了多个网站，Nginx 必须通过 `server_name` 区分不同域名应该转发到哪个项目。

第一个网站使用 `mlksuper.top` 和 `www.mlksuper.top`，第二个网站使用 `zhihuitong.mlksuper.top`。因此第二个网站需要单独配置一个 Nginx `server` 块。
### 10.2 `zhihuitong.mlksuper.top` 的 Nginx 配置
`zhihuitong.mlksuper.top` 使用独立的 Nginx server 块。HTTPS 请求进入宿主机 Nginx 后，会被转发到宿主机本地端口 `127.0.0.1:18080`，也就是 Docker 前端容器映射出来的端口。

HTTP 的 80 端口请求不直接提供服务，而是通过 `return 301` 重定向到 HTTPS。


### 10.3 宿主机 Nginx 只代理到 `127.0.0.1:18080`
- 宿主机nginx对第二个网站只做一个事 
```text
zhihuitong.mlksuper.top -> 127.0.0.1:18080
```
宿主机 Nginx 不直接访问后端容器，而是统一把 `zhihuitong.mlksuper.top` 的请求转发到 `127.0.0.1:18080`。这个端口对应 `saas-frontend` 容器内部的 Nginx 服务。

这样可以让前端页面请求和 API 请求都先进入前端容器，再由前端容器内部的 Nginx 决定是返回静态文件，还是把 `/prod-api/` 转发给后端。
### 10.4 为什么宿主机 Nginx 不直接处理 `/prod-api/`
- 宿主机 Nginx 不应该直接处理第二个网站的 `/prod-api/` 请求。因为第二个网站的后端运行在 Docker 内部网络中，宿主机没有直接暴露该后端端口。

- 如果宿主机 Nginx 将 `/prod-api/` 转发到 `127.0.0.1:8081`，实际会转发到第一个网站的后端，导致接口返回异常。因此本项目将 `/prod-api/` 的处理放在前端容器 Nginx 中，由它转发到 Docker 内部服务名 `saas-backend:8081`。

### 10.5 默认 server 块导致请求被转发到错误后端的问题
部署过程中曾经出现接口返回 `401 Unauthorized`。通过对比测试发现，直接访问 `127.0.0.1:18080` 时接口正常返回 200，但通过公网域名访问时返回 401。

这说明 Docker 内部链路正常，问题出在宿主机 Nginx。最终排查发现，宿主机 Nginx 没有为 `zhihuitong.mlksuper.top` 配置独立的 `server_name`，导致请求被默认 server 块接收，并转发到了第一个网站的后端。

解决方式是为 `zhihuitong.mlksuper.top` 新增独立的 Nginx server 块，并统一代理到 `127.0.0.1:18080`。

### 10.6 HTTPS 配置与证书复用问题
本次配置中，`zhihuitong.mlksuper.top` 暂时复用了主域名证书路径。需要注意，HTTPS 证书必须覆盖当前访问的子域名，否则浏览器可能提示证书不匹配。

排查阶段使用 `curl -k` 可以忽略证书校验，用来先验证反向代理链路是否正确。但正式访问时仍应确保证书包含对应子域名。

### 10.7 Nginx 配置检查与重载
修改 Nginx 配置后，应先使用 `nginx -t` 检查语法。只有配置测试通过后，才执行 `systemctl reload nginx` 重新加载配置。相比直接重启，reload 不会中断正在运行的连接，更适合线上服务更新配置。

---

## 11. 部署过程中遇到的问题与解决方案

本章按照“现象 → 原因 → 解决方案 → 验证方式 → 经验总结”的结构复盘部署故障。

### 11.1 Docker 拉取基础镜像超时

**现象：**

执行 `docker compose up -d --build` 时，Docker 无法拉取 `eclipse-temurin:21-jre`：

```text
failed to resolve source metadata for docker.io/library/eclipse-temurin:21-jre
i/o timeout
```

**原因：**

服务器访问 Docker Hub 不稳定，导致基础镜像拉取超时。

**解决方案：**

配置可用的 Docker 镜像加速地址：

```bash
cat > /etc/docker/daemon.json <<'EOF'
{
  "registry-mirrors": [
    "https://mirror.ccs.tencentyun.com"
  ]
}
EOF

systemctl daemon-reload
systemctl restart docker
```

**验证方式：**

```bash
docker pull eclipse-temurin:21-jre
cd /opt/saas
docker compose up -d --build
```

**经验总结：**

镜像拉取失败时，应先检查网络、DNS 和镜像源，不要反复执行相同的构建命令。

### 11.2 后端容器启动失败：找不到 `best.onnx`

**现象：**

```text
YOLO ONNX model file does not exist:
D:\lhr\Desktop\saas\docs\best.onnx
```

**原因：**

jar 中仍保留 Windows 开发环境路径，而后端实际运行在 Linux 容器中。

**解决方案：**

```yaml
environment:
  - AI_YOLO_MODEL_PATH=/app/docs/best.onnx

volumes:
  - /opt/saas/docs:/app/docs:ro
```

**验证方式：**

```bash
ls -lh /opt/saas/docs/best.onnx
docker exec -it saas-backend ls -lh /app/docs/best.onnx
docker logs --tail=200 saas-backend
```

**经验总结：**

容器中的程序必须使用容器内路径；宿主机文件需要通过 `volumes` 挂载后才能访问。

### 11.3 后端容器连接 MySQL 失败：`Connection refused`

**现象：**

```text
Communications link failure
Connection refused
```

**原因：**

后端使用 `localhost:3306`，但容器中的 `localhost` 指向容器自身，不是宿主机。

**解决方案：**

```yaml
extra_hosts:
  - "host.docker.internal:host-gateway"

environment:
  - MYSQL_HOST=host.docker.internal
  - MYSQL_PORT=3306
```

**验证方式：**

```bash
docker exec -it saas-backend getent hosts host.docker.internal
ss -lntp | grep 3306
docker logs --tail=200 saas-backend
```

**经验总结：**

容器访问宿主机服务时，应使用宿主机网关地址，而不是 `localhost`。

### 11.4 MySQL 启动失败：`Cannot assign requested address`

**现象：**

```text
Error: 99 Cannot assign requested address
```

**原因：**

`bind-address` 被设置成服务器不存在的 IP，或错误地写成 `host.docker.internal`。

**解决方案：**

在 MySQL 配置文件的 `[mysqld]` 段使用：

```ini
bind-address = 0.0.0.0
```

以下写法是错误的：

```text
bind-address: 0.0.0.0
bind-address = host.docker.internal
bind-address = 一个本机不存在的 IP
```

**验证方式：**

```bash
grep -R "bind-address" /etc/mysql/ -n
systemctl restart mysql
systemctl status mysql --no-pager -l
journalctl -u mysql --no-pager -n 100
ss -lntp | grep 3306
```

**经验总结：**

`bind-address` 是 MySQL 服务端监听地址，必须是本机能够绑定的地址。

### 11.5 MySQL 拒绝 Docker 容器连接

**现象：**

```text
Host '172.18.0.2' is not allowed to connect to this MySQL server
```

**原因：**

MySQL 用户由“用户名 + 来源主机”共同确定。`'root'@'localhost'` 不允许 Docker 容器 IP 连接。

**解决方案：**

```sql
CREATE USER IF NOT EXISTS 'zhihuitong'@'%' IDENTIFIED BY '<DB_PASSWORD>';
GRANT ALL PRIVILEGES ON zhihuitong.* TO 'zhihuitong'@'%';
FLUSH PRIVILEGES;
```

> 笔记和公开配置中不要保存真实数据库密码。

**验证方式：**

```sql
SELECT user, host FROM mysql.user WHERE user = 'zhihuitong';
SHOW GRANTS FOR 'zhihuitong'@'%';
```

```bash
docker logs --tail=100 saas-backend
```

正常日志中应出现：

```text
HikariPool-1 - Start completed
Tomcat started on port 8081
Started ZhihuitongApplication
```

**经验总结：**

数据库连接不仅要求网络可达，还要求用户授权允许当前来源主机连接。

### 11.6 接口返回 401 的误判过程

**现象：**

公网域名访问接口返回 `401 Unauthorized`，最初被误判为 token 或后端鉴权问题。

**原因：**

请求实际上被宿主机 Nginx 转发到了错误的网站后端。

**解决方案与验证方式：**

对比本地端口和公网域名：

```bash
curl -i 'http://127.0.0.1:18080/prod-api/api/batches?pageNum=1&pageSize=1'
curl -k -i 'https://zhihuitong.mlksuper.top/prod-api/api/batches?pageNum=1&pageSize=1'
```

如果本地返回 200、公网返回 401，说明 Docker 内部链路正常，应检查宿主机 Nginx。

**经验总结：**

401 不一定是当前项目的鉴权问题，也可能是请求进入了错误后端。

### 11.7 通过 curl 对比定位宿主机 Nginx 转发错误

**现象：**

```text
127.0.0.1:18080 返回 200
公网域名返回 401
```

**原因：**

宿主机 Nginx 没有为 `zhihuitong.mlksuper.top` 配置独立的 `server_name`，请求被默认 `server` 块处理。

**解决方案：**

为子域名配置独立 `server` 块，并统一代理到 `127.0.0.1:18080`。

**验证方式：**

```bash
nginx -T | grep -n "zhihuitong.mlksuper.top\|prod-api\|18080\|8081\|server_name" -C 5
nginx -t
systemctl reload nginx
```

**经验总结：**

本地端口正常而公网域名异常时，优先检查宿主机 Nginx 的 `server_name`、证书和 `proxy_pass`。

### 11.8 `/prod-api/` 代理路径配置错误

**现象：**

前端请求 `/prod-api/api/...`，但前端容器 Nginx 最初只配置了 `/api/`。

**原因：**

前端生产环境接口前缀与 Nginx `location` 规则不一致。

**解决方案：**

```nginx
location /prod-api/ {
    proxy_pass http://saas-backend:8081/;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

由于 `proxy_pass` 末尾有 `/`，请求路径会发生如下转换：

```text
/prod-api/api/batches
→ /api/batches
```

重新构建并验证：

```bash
cd /opt/saas
docker compose up -d --build saas-frontend
curl -i 'http://127.0.0.1:18080/prod-api/api/batches?pageNum=1&pageSize=1'
```

**经验总结：**

前端接口前缀必须与 Nginx 代理规则一致，可通过浏览器 Network 面板确认真实请求路径。

### 11.9 重新上传 jar 后配置回退的问题

**现象：**

上传新 jar 并重新部署后，已经解决的 Windows 模型路径问题再次出现。

**原因：**

新 jar 的 `application.yml` 或 `application-dev.yml` 仍保留本地路径。

**解决方案：**

```yaml
environment:
  - SERVER_PORT=8081
  - AI_YOLO_MODEL_PATH=/app/docs/best.onnx
  - INSPECTION_STORAGE_UPLOAD_ROOT=/app/data/upload
  - INSPECTION_STORAGE_RESULT_ROOT=/app/data/results
```

**验证方式：**

```bash
docker exec -it saas-backend printenv | grep -E "SERVER_PORT|AI_YOLO|INSPECTION"

cd /opt/saas/backend
unzip -p *.jar BOOT-INF/classes/application.yml | grep -n "best.onnx" -C 5
unzip -p *.jar BOOT-INF/classes/application-dev.yml | grep -n "best.onnx" -C 5
```

**经验总结：**

部署环境配置不应写死在 jar 中，应通过环境变量注入。

### 11.10 本章总结

排查部署故障时应按访问链路逐层验证：

```text
容器状态
  ↓
后端日志
  ↓
宿主机本地端口
  ↓
公网域名
```

不要只根据表面错误判断原因：401 不一定是鉴权问题，`Connection refused` 不一定是 MySQL 宕机，文件不存在也不一定是文件没有上传。

---

## 12. 验证部署是否成功

部署完成后，应沿访问链路逐层验证。前一层通过后再测试后一层，可以快速确定故障范围。

### 12.1 查看容器运行状态

```bash
cd /opt/saas
docker ps
docker compose ps
```

正常情况下：

```text
saas-backend    Up
saas-frontend   Up
```

| 检查项 | 正常表现 |
|---|---|
| 后端状态 | `saas-backend` 为 `Up` |
| 前端状态 | `saas-frontend` 为 `Up` |
| 前端端口 | `127.0.0.1:18080->80/tcp` |
| 后端端口 | 只显示 `8081/tcp` |

### 12.2 查看后端启动日志

```bash
docker logs --tail=100 saas-backend
docker logs -f saas-backend
```

按 `Ctrl + C` 退出实时日志。

正常日志：

```text
Tomcat started on port 8081
Started ZhihuitongApplication
HikariPool-1 - Start completed
```

| 日志关键词 | 可能原因 |
|---|---|
| `YOLO ONNX model file does not exist` | 模型路径错误或挂载失败 |
| `Communications link failure` | 后端连接 MySQL 失败 |
| `Connection refused` | MySQL 地址或端口不可访问 |
| `Host ... is not allowed` | MySQL 用户权限不足 |

> 容器显示 `Up` 不代表业务程序一定正常，必须结合应用日志判断。

### 12.3 测试前端容器是否正常

```bash
curl -I http://127.0.0.1:18080
curl http://127.0.0.1:18080 | head
```

正常应返回 `HTTP/1.1 200 OK`，并能看到 HTML 内容。这一步只验证宿主机到前端容器的链路。

### 12.4 测试 Docker 内部 API 代理

```bash
curl -i 'http://127.0.0.1:18080/prod-api/api/batches?pageNum=1&pageSize=1'
```

如果返回 HTTP 200 和业务 JSON，说明以下链路基本正常：

```text
宿主机 127.0.0.1:18080
  ↓
saas-frontend 容器 Nginx
  ↓
/prod-api/ 代理
  ↓
saas-backend:8081
  ↓
MySQL
```

如果失败，优先检查前端 `nginx.conf`、后端日志、数据库连接和 Docker 服务名。

### 12.5 测试公网域名接口

```bash
curl -k -i 'https://zhihuitong.mlksuper.top/prod-api/api/batches?pageNum=1&pageSize=1'
```

正常应返回 HTTP 200 和业务 JSON。`-k` 只用于排查时忽略证书校验，正式环境仍需确保证书覆盖当前子域名。

本地正常而公网异常时，检查宿主机 Nginx：

```bash
nginx -T | grep -n "zhihuitong.mlksuper.top\|18080\|prod-api\|8081\|server_name" -C 5
```

### 12.6 浏览器强制刷新与缓存问题

命令行正常但浏览器仍显示旧页面时：

1. 确认前端容器已经重新构建。
2. 使用 `Ctrl + F5` 强制刷新。
3. 使用无痕窗口访问。
4. 清理浏览器缓存。
5. 必要时无缓存重建镜像。

```bash
cd /opt/saas
docker compose build --no-cache saas-frontend
docker compose up -d saas-frontend
```

### 12.7 部署验证清单

- [ ] 前后端容器均为 `Up`
- [ ] 后端日志没有模型、数据库或启动异常
- [ ] 前端本地端口返回成功
- [ ] 本地 `/prod-api/` 接口返回业务 JSON
- [ ] 公网域名接口返回业务 JSON
- [ ] HTTPS 证书与子域名匹配
- [ ] 浏览器页面和核心业务功能正常

核心判断：

```text
先测容器，再测本地端口，最后测公网域名。
本地正常、公网异常：优先检查宿主机 Nginx。
本地 API 异常：优先检查前端代理、后端日志和数据库连接。
```

---

## 13. 常用维护命令

本章以速查表为主。Compose 命令建议先进入 `/opt/saas` 目录执行。

### 13.1 查看容器

```bash
docker ps
docker ps -a

cd /opt/saas
docker compose ps
```

### 13.2 查看后端日志

```bash
docker logs --tail=100 saas-backend
docker logs -f saas-backend
```

### 13.3 查看前端日志

```bash
docker logs --tail=100 saas-frontend
docker logs -f saas-frontend

docker exec -it saas-frontend sh
ls -lh /usr/share/nginx/html
exit
```

### 13.4 重建前端容器

适用于更新前端文件、`nginx.conf` 或前端 Dockerfile：

```bash
cd /opt/saas
docker compose up -d --build saas-frontend
curl -I http://127.0.0.1:18080
```

### 13.5 重建后端容器

适用于更新 jar、后端 Dockerfile 或后端环境变量：

```bash
cd /opt/saas
docker compose up -d --build saas-backend
docker logs -f saas-backend
```

重新上传 jar 后必须重建镜像，否则运行的仍是旧镜像中的 `/app/app.jar`。

### 13.6 前后端同时重新部署

```bash
cd /opt/saas
docker compose down
docker compose up -d --build
docker compose ps
```

该操作不会删除宿主机 `/opt/saas/docs` 和 `/opt/saas/data` 中的数据。

> 不要随意为 `docker compose down` 添加 `-v`，否则可能删除 Compose 管理的命名卷。

### 13.7 无缓存重新构建

```bash
# 前端
cd /opt/saas
docker compose build --no-cache saas-frontend
docker compose up -d saas-frontend

# 后端
docker compose build --no-cache saas-backend
docker compose up -d saas-backend

# 全部服务
docker compose build --no-cache
docker compose up -d
```

### 13.8 查看 Docker 资源占用

```bash
docker stats
free -h
df -h
```

| 字段 | 含义 |
|---|---|
| `CPU %` | 容器 CPU 使用率 |
| `MEM USAGE / LIMIT` | 当前内存使用量和限制 |
| `MEM %` | 容器内存使用比例 |
| `NET I/O` | 网络输入输出 |
| `BLOCK I/O` | 磁盘读写 |

### 13.9 检查宿主机 Nginx 配置

```bash
nginx -t
nginx -T
nginx -T | grep -n "zhihuitong.mlksuper.top\|18080\|prod-api\|8081\|server_name" -C 5
cat /etc/nginx/sites-enabled/zhihuitong.conf
```

### 13.10 重载宿主机 Nginx

```bash
nginx -t
systemctl reload nginx
systemctl status nginx --no-pager -l
```

`reload` 会平滑加载新配置，通常比直接重启更适合线上配置更新。

### 13.11 常用验证命令速查

```bash
cd /opt/saas

docker compose ps
docker logs --tail=100 saas-backend
docker logs --tail=100 saas-frontend

curl -I http://127.0.0.1:18080
curl -i 'http://127.0.0.1:18080/prod-api/api/batches?pageNum=1&pageSize=1'
curl -k -i 'https://zhihuitong.mlksuper.top/prod-api/api/batches?pageNum=1&pageSize=1'

nginx -t
systemctl status nginx --no-pager -l
systemctl status mysql --no-pager -l
```

### 13.12 维护操作原则

1. 先查看状态和日志，再决定是否重建。
2. 只更新一个服务时，只重建对应服务。
3. 修改 Nginx 后先执行 `nginx -t`。
4. 重新上传文件后必须重建镜像。
5. 无缓存构建只在普通构建仍使用旧文件时使用。
6. 不在笔记、Compose 文件或命令历史中保存真实密码。

---

## 14. 更新前端和后端的流程

本章说明以后修改前端页面、重新打包后端 jar，或同时更新前后端时，文件应该上传到哪里、执行哪些命令，以及如何确认更新成功。

### 14.1 只更新前端文件

前端打包产物位于：

```text
/opt/saas/frontend
```

先检查 Dockerfile：

```bash
cat /opt/saas/frontend/Dockerfile
```

如果配置是：

```dockerfile
COPY . /usr/share/nginx/html
```

应将打包产物直接上传到 `/opt/saas/frontend`，目录中通常包括：

```text
index.html
assets/
Dockerfile
nginx.conf
```

如果配置是：

```dockerfile
COPY dist /usr/share/nginx/html
```

则应上传到：

```text
/opt/saas/frontend/dist
```

上传后重新构建前端容器：

```bash
cd /opt/saas
docker compose up -d --build saas-frontend
```

验证：

```bash
docker compose ps
curl -I http://127.0.0.1:18080
```

> 前端文件会在构建镜像时复制到容器中，只替换宿主机文件不会自动更新正在运行的容器。

### 14.2 只更新后端 jar

后端 jar 位于：

```text
/opt/saas/backend
```

更新前先检查当前文件：

```bash
ls -lh /opt/saas/backend
ls -lh /opt/saas/backend/*.jar
```

为避免 `COPY *.jar /app/app.jar` 匹配到多个文件，后端目录中只保留一个待部署 jar。建议先备份旧版本：

```bash
cd /opt/saas/backend
cp 当前版本.jar 当前版本.jar.bak
```

确认备份无误后，再移除旧 jar 并上传新 jar：

```bash
rm -f /opt/saas/backend/*.jar
ls -lh /opt/saas/backend/*.jar
```

重新构建后端容器：

```bash
cd /opt/saas
docker compose up -d --build saas-backend
docker logs -f saas-backend
```

正常日志应包含：

```text
Tomcat started on port 8081
Started ZhihuitongApplication
HikariPool-1 - Start completed
```

重新上传 jar 后，要防止 jar 内配置重新带回 Windows 本地路径。部署环境中的模型路径、上传路径和结果路径应继续由 Compose 环境变量覆盖。

```bash
docker exec -it saas-backend printenv | grep -E "SERVER_PORT|AI_YOLO|INSPECTION|MYSQL_HOST"
```

### 14.3 前后端同时更新

前后端文件均上传完成后，可以完整重新部署：

```bash
cd /opt/saas
docker compose down
docker compose up -d --build
docker compose ps
```

适用场景：

- 前端打包文件更新
- 后端 jar 更新
- Dockerfile 更新
- `docker-compose.yml` 更新
- 前端 `nginx.conf` 更新

该操作会删除并重建容器和默认网络，但不会删除宿主机上的 `/opt/saas/docs` 与 `/opt/saas/data`。

> 不要随意给 `docker compose down` 添加 `-v`，否则可能删除 Compose 管理的命名卷。

如果怀疑构建缓存导致新文件没有生效：

```bash
cd /opt/saas
docker compose build --no-cache
docker compose up -d
```

### 14.4 更新后检查容器和接口

更新完成后按访问链路逐层检查。

第一步，查看容器：

```bash
docker compose ps
```

正常应看到：

```text
saas-backend    Up
saas-frontend   Up
```

第二步，查看后端日志：

```bash
docker logs --tail=100 saas-backend
```

重点确认没有：

```text
YOLO ONNX model file does not exist
Connection refused
Communications link failure
Host ... is not allowed
```

第三步，测试前端容器：

```bash
curl -I http://127.0.0.1:18080
```

第四步，测试本地 API 代理：

```bash
curl -i 'http://127.0.0.1:18080/prod-api/api/batches?pageNum=1&pageSize=1'
```

第五步，测试公网域名：

```bash
curl -k -i 'https://zhihuitong.mlksuper.top/prod-api/api/batches?pageNum=1&pageSize=1'
```

如果本地 `18080` 正常而公网异常，优先检查宿主机 Nginx：

```bash
nginx -T | grep -n "zhihuitong.mlksuper.top\|18080\|prod-api\|8081\|server_name" -C 5
```

`-k` 仅用于临时排查证书问题；正式验证还应去掉 `-k`，确认证书链与子域名匹配。

### 14.5 常见缓存问题处理

前端文件已经更新，但浏览器仍显示旧页面时：

1. 确认前端容器已经重新构建。
2. 使用 `Ctrl + F5` 强制刷新。
3. 使用无痕窗口访问。
4. 清理浏览器缓存。
5. 必要时执行无缓存构建。

```bash
cd /opt/saas
docker compose build --no-cache saas-frontend
docker compose up -d saas-frontend
```

进入容器检查实际文件：

```bash
docker exec -it saas-frontend sh
ls -lh /usr/share/nginx/html
ls -lh /usr/share/nginx/html/index.html
exit
```

### 14.6 更新流程速查

| 更新内容 | 上传位置 | 执行命令 |
|---|---|---|
| 仅前端 | `/opt/saas/frontend` | `docker compose up -d --build saas-frontend` |
| 仅后端 | `/opt/saas/backend` | `docker compose up -d --build saas-backend` |
| 前后端 | 对应目录 | `docker compose down && docker compose up -d --build` |
| 构建缓存异常 | 对应目录 | `docker compose build --no-cache` |

> 上传新文件只是第一步，重新构建对应容器后才会真正生效。

---

## 15. 故障排查清单

排查时不要直接根据浏览器现象下结论，应按照访问链路逐层检查：

```text
浏览器
  ↓
宿主机 Nginx
  ↓
127.0.0.1:18080
  ↓
saas-frontend 容器
  ↓
saas-backend 容器
  ↓
宿主机 MySQL
```

### 15.1 页面打不开

**现象：** 页面连接失败、空白，或者返回 502。

**排查步骤：**

```bash
docker compose ps
curl -I http://127.0.0.1:18080
docker logs --tail=100 saas-frontend
nginx -t
cat /etc/nginx/sites-enabled/zhihuitong.conf
```

重点确认：

```nginx
server_name zhihuitong.mlksuper.top;

location / {
    proxy_pass http://127.0.0.1:18080;
}
```

**常见原因：**

- `saas-frontend` 没有启动。
- 端口没有映射到 `127.0.0.1:18080`。
- 子域名没有独立 Nginx 配置。
- Nginx 修改后没有 reload。
- 域名解析没有指向当前服务器。

### 15.2 接口返回 401

先对比本地代理与公网域名：

```bash
curl -i 'http://127.0.0.1:18080/prod-api/api/batches?pageNum=1&pageSize=1'
curl -k -i 'https://zhihuitong.mlksuper.top/prod-api/api/batches?pageNum=1&pageSize=1'
```

如果本地返回 200、公网返回 401，Docker 内部链路正常，问题通常在宿主机 Nginx。

```bash
nginx -T | grep -n "zhihuitong.mlksuper.top\|prod-api\|18080\|8081\|server_name" -C 5
```

常见原因：

- 没有独立的 `server_name zhihuitong.mlksuper.top`。
- 请求被默认 `server` 块接收。
- `/prod-api/` 被代理到第一个网站后端。
- 宿主机 Nginx 错误代理到 `127.0.0.1:8081`。

> 401 不一定是鉴权问题，也可能是请求被代理到了错误后端。

### 15.3 接口返回 502

```bash
curl -i 'http://127.0.0.1:18080/prod-api/api/batches?pageNum=1&pageSize=1'
docker logs --tail=100 saas-frontend
docker compose ps
docker logs --tail=200 saas-backend
cat /opt/saas/frontend/nginx.conf
```

重点确认：

```nginx
location /prod-api/ {
    proxy_pass http://saas-backend:8081/;
}
```

常见原因：

- `saas-backend` 没有启动或反复重启。
- `proxy_pass` 服务名或端口错误。
- 后端实际没有监听 8081。
- Docker 内部网络或服务名解析异常。

### 15.4 后端容器反复重启

```bash
docker ps -a
docker logs --tail=200 saas-backend
docker logs -f saas-backend
```

重点搜索：

```text
YOLO ONNX model file does not exist
Communications link failure
Connection refused
Host ... is not allowed
```

检查配置和挂载：

```bash
docker exec -it saas-backend printenv | grep -E "SERVER_PORT|AI_YOLO|INSPECTION|MYSQL"
docker exec -it saas-backend ls -lh /app/docs/best.onnx
docker exec -it saas-backend ls -lh /app/data
```

常见原因包括模型路径错误、MySQL 连接失败、用户权限不足，以及 jar 中仍使用 Windows 路径。

### 15.5 模型文件不存在

```bash
ls -lh /opt/saas/docs/best.onnx
docker exec -it saas-backend ls -lh /app/docs/best.onnx
cat /opt/saas/docker-compose.yml
docker exec -it saas-backend printenv | grep AI_YOLO_MODEL_PATH
```

Compose 应包含：

```yaml
volumes:
  - /opt/saas/docs:/app/docs:ro
```

环境变量应为：

```text
AI_YOLO_MODEL_PATH=/app/docs/best.onnx
```

常见原因：

- 宿主机文件不存在。
- `volumes` 挂载错误。
- 后端读取 Windows 本地路径。
- 新 jar 导致配置回退。
- 环境变量缩进错误，未配置到 `saas-backend.environment`。

### 15.6 MySQL 连接失败

```bash
systemctl status mysql --no-pager -l
ss -lntp | grep 3306
docker exec -it saas-backend printenv | grep -E "MYSQL_HOST|MYSQL_PORT|MYSQL_DATABASE|MYSQL_USERNAME"
docker exec -it saas-backend getent hosts host.docker.internal
```

正常配置：

```text
MYSQL_HOST=host.docker.internal
MYSQL_PORT=3306
MYSQL_DATABASE=zhihuitong
MYSQL_USERNAME=zhihuitong
```

Compose 应包含：

```yaml
extra_hosts:
  - "host.docker.internal:host-gateway"
```

常见原因：

- 后端仍使用 `localhost`。
- `extra_hosts` 没有配置。
- MySQL 没有运行或未监听可访问地址。
- 数据库端口或环境变量错误。

### 15.7 MySQL 用户权限不足

**现象：**

```text
Host '172.18.0.2' is not allowed to connect to this MySQL server
```

创建业务用户：

```sql
CREATE USER IF NOT EXISTS 'zhihuitong'@'%' IDENTIFIED BY '<DB_PASSWORD>';
GRANT ALL PRIVILEGES ON zhihuitong.* TO 'zhihuitong'@'%';
FLUSH PRIVILEGES;

SELECT user, host FROM mysql.user WHERE user = 'zhihuitong';
SHOW GRANTS FOR 'zhihuitong'@'%';
```

重建后端并查看日志：

```bash
cd /opt/saas
docker compose up -d --build saas-backend
docker logs -f saas-backend
```

正常日志：

```text
HikariPool-1 - Start completed
Tomcat started on port 8081
Started ZhihuitongApplication
```

### 15.8 前端页面还是旧版本

```bash
ls -lh /opt/saas/frontend
cat /opt/saas/frontend/Dockerfile
```

根据 Dockerfile 确认上传位置：

```dockerfile
COPY . /usr/share/nginx/html
```

对应 `/opt/saas/frontend`；如果是：

```dockerfile
COPY dist /usr/share/nginx/html
```

则对应 `/opt/saas/frontend/dist`。

重新构建：

```bash
cd /opt/saas
docker compose up -d --build saas-frontend
```

必要时无缓存构建：

```bash
docker compose build --no-cache saas-frontend
docker compose up -d saas-frontend
```

最后使用 `Ctrl + F5` 或无痕窗口排除浏览器缓存。

### 15.9 子域名访问到了错误网站

```bash
nginx -T | grep -n "zhihuitong.mlksuper.top\|mlksuper.top\|server_name\|18080\|8081" -C 5
```

正确配置应包含：

```nginx
server_name zhihuitong.mlksuper.top;
proxy_pass http://127.0.0.1:18080;
```

不要代理到：

```nginx
proxy_pass http://127.0.0.1:8081;
```

修改后：

```bash
nginx -t
systemctl reload nginx
```

### 15.10 Docker 容器资源占用过高

```bash
docker stats
free -h
df -h
top
cat /opt/saas/docker-compose.yml
```

后端资源限制示例：

```yaml
mem_limit: 800m
cpus: 1.0
```

前端资源限制示例：

```yaml
mem_limit: 128m
cpus: 0.5
```

JVM 参数示例：

```dockerfile
CMD ["java", "-Xms128m", "-Xmx512m", "-XX:MaxMetaspaceSize=128m", "-jar", "/app/app.jar"]
```

先确定是哪个容器占用资源，再检查日志、JVM 参数、上传目录、结果目录和 Docker 镜像缓存。

### 15.11 总体排查顺序

```bash
docker compose ps
docker logs --tail=100 saas-backend
docker logs --tail=100 saas-frontend
curl -I http://127.0.0.1:18080
curl -i 'http://127.0.0.1:18080/prod-api/api/batches?pageNum=1&pageSize=1'
curl -k -i 'https://zhihuitong.mlksuper.top/prod-api/api/batches?pageNum=1&pageSize=1'
nginx -T | grep -n "zhihuitong.mlksuper.top\|18080\|prod-api\|8081\|server_name" -C 5
```

核心判断：

```text
页面问题：先查前端容器。
接口问题：先查后端日志和 /prod-api/ 代理。
本地 18080 正常但公网异常：优先查宿主机 Nginx。
容器路径问题：优先查 volumes 和环境变量。
数据库问题：先查 MYSQL_HOST，再查 MySQL 用户授权。
```

---

## 16. 本次部署经验总结

本次部署的目标是在已经运行第一个网站的腾讯云 Ubuntu 服务器上，通过 Docker Compose 部署第二个网站。部署重点包括端口隔离、容器网络、路径映射、数据库连接和 Nginx 反向代理。

### 16.1 Docker 部署多个网站时的端口规划

第二个网站后端虽然也监听 8081，但没有映射到宿主机，只在 Docker 内部网络中提供服务。前端容器映射到宿主机回环地址：

```yaml
ports:
  - "127.0.0.1:18080:80"
```

端口规划：

| 端口 | 用途 |
|---|---|
| 宿主机 80 / 443 | 宿主机 Nginx 公网入口 |
| 宿主机 8081 | 第一个网站后端 |
| 宿主机 18080 | 第二个网站前端容器映射 |
| 容器内 8081 | 第二个网站后端 |

后端不映射宿主机端口，既减少冲突，也降低直接暴露风险。

### 16.2 宿主机 Nginx 与容器 Nginx 的边界

本次部署同时存在两个 Nginx：

| 组件 | 职责 |
|---|---|
| 宿主机 Nginx | 域名识别、HTTPS、公网入口、代理到 `127.0.0.1:18080` |
| 前端容器 Nginx | 静态页面、SPA 路由、将 `/prod-api/` 转发到后端 |

```text
宿主机 Nginx 负责“进门”
前端容器 Nginx 负责“分流”
```

宿主机 Nginx 不应把第二个网站的 `/prod-api/` 直接代理到 `127.0.0.1:8081`，因为该端口属于第一个网站。

### 16.3 配置项不要写死本地 Windows 路径

错误示例：

```text
D:\lhr\Desktop\saas\docs\best.onnx
```

Docker 后端应使用容器内路径：

```text
/app/docs/best.onnx
/app/data/upload
/app/data/results
```

宿主机与容器通过挂载建立映射：

```yaml
volumes:
  - /opt/saas/docs:/app/docs:ro
  - /opt/saas/data:/app/data
```

核心原则：

```text
本地开发路径不能直接用于服务器部署。
容器中的程序只能使用容器内路径。
部署环境路径应通过环境变量覆盖。
```

### 16.4 后端连接数据库应使用环境变量

```yaml
environment:
  - MYSQL_HOST=host.docker.internal
  - MYSQL_PORT=3306
  - MYSQL_DATABASE=zhihuitong
  - MYSQL_USERNAME=zhihuitong
  - MYSQL_PASSWORD=<DB_PASSWORD>

extra_hosts:
  - "host.docker.internal:host-gateway"
```

这样无需为了修改数据库地址重新打包 jar，也能集中管理不同环境配置。

容器中的 `localhost` 指向容器自身，因此不能用 `localhost:3306` 访问宿主机 MySQL。

> 更安全的生产方案是将密码放入仅服务器可读的 `.env` 文件或 Docker Secret，而不是提交到源码仓库。

### 16.5 业务数据库用户应独立创建

```sql
CREATE USER IF NOT EXISTS 'zhihuitong'@'%' IDENTIFIED BY '<DB_PASSWORD>';
GRANT ALL PRIVILEGES ON zhihuitong.* TO 'zhihuitong'@'%';
FLUSH PRIVILEGES;
```

经验：

- 不让业务服务长期使用 root。
- 每个业务项目创建独立用户。
- 只授权当前业务数据库。
- 不在笔记或源码中记录真实密码。
- 在防火墙或安全组中限制 3306 的公网访问。

### 16.6 排查问题时要分层验证访问链路

```text
浏览器
  ↓
宿主机 Nginx
  ↓
127.0.0.1:18080
  ↓
saas-frontend
  ↓
saas-backend:8081
  ↓
host.docker.internal:3306
```

排查顺序：

```bash
docker compose ps
docker logs --tail=100 saas-backend
curl -I http://127.0.0.1:18080
curl -i 'http://127.0.0.1:18080/prod-api/api/batches?pageNum=1&pageSize=1'
curl -k -i 'https://zhihuitong.mlksuper.top/prod-api/api/batches?pageNum=1&pageSize=1'
```

判断规则：

```text
本地端口正常、公网异常：优先查宿主机 Nginx。
本地 API 异常：优先查前端代理、后端日志和数据库。
后端启动失败：优先查模型路径、环境变量和 MySQL。
前端仍是旧版本：优先查镜像是否重建和浏览器缓存。
```

### 16.7 重新上传文件后必须重新构建镜像

```bash
# 只更新前端
cd /opt/saas
docker compose up -d --build saas-frontend

# 只更新后端
docker compose up -d --build saas-backend

# 前后端同时更新
docker compose down
docker compose up -d --build

# 无缓存重建
docker compose build --no-cache
docker compose up -d
```

上传新文件只是第一步。前端文件和后端 jar 只有重新构建镜像后，才会进入新容器。

### 16.8 最终总结

最终架构：

```text
公网请求
  ↓
宿主机 Nginx
  ↓
127.0.0.1:18080
  ↓
saas-frontend
  ↓
saas-backend:8081
  ↓
host.docker.internal:3306
```

本次部署最重要的经验：

1. 多网站部署前先规划端口。
2. 明确宿主机 Nginx 与容器 Nginx 的职责。
3. 容器内不要使用 Windows 本地路径。
4. 容器访问宿主机 MySQL 不能使用 `localhost`。
5. MySQL 用户权限必须允许容器来源连接。
6. 接口异常应按链路逐层排查。
7. 上传新前端文件或 jar 后必须重建对应容器。

第二个网站最终可通过 `zhihuitong.mlksuper.top` 访问，并与第一个网站 `mlksuper.top` 保持端口和服务隔离。通过 Docker Compose 的资源限制、端口隔离和数据挂载，可以在同一台 4 核 4GB 服务器上运行两个网站。

---
tags:
  - 性能测试
  - 监控
  - Prometheus
  - Grafana
  - SpringBoot
  - Docker
  - JMeter
status: 学习中
---

# Prometheus + Grafana 性能测试监控学习笔记

> [!abstract] 这篇笔记解决什么问题？
>
> 本笔记记录从零开始搭建 Prometheus + Grafana 监控环境的过程，并把它和 JMeter 性能测试连接起来。
>
> 最终目标不是“把图表显示出来”，而是能够回答：
>
> - 请求变慢时，是 CPU、内存、JVM、线程还是数据库连接池出了问题？
> - JMeter 的响应时间、吞吐量、错误率，和服务器指标之间有什么关系？
> - Prometheus、Grafana、Spring Boot、Node Exporter 各自负责哪一段？

## 一、先看最终效果

### 1. 最终数据链路

~~~mermaid
flowchart LR
    A["JMeter<br/>制造请求压力"] --> B["Spring Boot<br/>后端接口 :8080"]
    B --> C["Actuator + Micrometer<br/>暴露 Prometheus 指标"]
    C --> D["Prometheus<br/>采集、保存、查询"]
    D --> E["Grafana<br/>图表展示与分析"]
    F["Node Exporter<br/>操作系统/主机指标"] --> D
    G["Windows / Docker Desktop"] --> F
~~~

### 2. 一句话理解每个组件

| 组件            | 负责什么                       | 类比              |
| ------------- | -------------------------- | --------------- |
| JMeter        | 产生并发请求，记录请求结果              | 压力制造者           |
| Spring Boot   | 真正处理业务请求                   | 被测试的系统          |
| Actuator      | 暴露应用运行状态和指标接口              | 给系统安装仪表盘接口      |
| Micrometer    | 把 Java 指标转换成 Prometheus 格式 | 翻译器             |
| Prometheus    | 定时采集并保存时间序列指标              | 采集器和时间序列数据库     |
| Grafana       | 查询 Prometheus 并画出图表        | 监控大屏            |
| Node Exporter | 暴露操作系统层面的指标                | CPU、内存、磁盘、网络传感器 |
|               |                            |                 |

### 3. 本次实践环境

| 项目 | 本次环境 |
|---|---|
| 操作系统 | Windows |
| 容器工具 | Docker Desktop |
| Prometheus 宿主机端口 | 3030 |
| Prometheus 容器内部端口 | 9090 |
| Grafana 端口 | 3000 |
| Node Exporter 端口 | 9100 |
| Spring Boot 版本 | 3.3.5 |
| Spring Boot 启动方式 | mvn spring-boot:run |
| Spring Boot 后端端口 | 8080 |
| 前端端口 | 5173 |

> [!important] 端口最容易混淆
>
> 3030:9090 表示：
>
> - Windows 浏览器从 localhost:3030 访问；
> - Prometheus 容器内部实际监听 9090。
>
> 因此：
>
> - 浏览器访问 Prometheus：http://localhost:3030
> - Grafana 容器访问 Prometheus：http://prometheus:9090
> - Prometheus 容器访问 Windows 上的 Spring Boot：host.docker.internal:8080

![[01-环境总览.png]]

---

## 二、为什么性能测试必须配合监控？

### 1. 只看 JMeter 还不够

JMeter 可以告诉我们：

- 请求发送了多少次；
- 每秒处理多少请求；
- 平均响应时间是多少；
- P90、P95、P99 响应时间是多少；
- 失败了多少次；
- 哪个请求最慢。

但是 JMeter 通常不能直接回答：

- 服务器 CPU 是否已经接近上限？
- Java 堆内存是否持续上涨？
- JVM 是否频繁垃圾回收？
- Tomcat 工作线程是否不够？
- 数据库连接池是否已经用满？
- 请求慢是因为代码计算，还是因为 SQL 等待？

所以性能测试至少要同时观察两类结果：

| 结果来源 | 关注内容 |
|---|---|
| JMeter | 用户视角：请求是否成功、快不快、吞吐量是否达标 |
| Grafana | 系统视角：资源是否紧张、应用内部哪里可能成为瓶颈 |

### 2. 一个简单的分析例子

假设 JMeter 发现登录接口平均响应时间从 100 ms 上升到 3 s。

只看 JMeter，我们只能知道“接口变慢了”。

如果同时看 Grafana，就可以进一步判断：

| Grafana 现象 | 初步判断 |
|---|---|
| CPU 长时间 95%~100% | 可能是 CPU 或代码计算瓶颈 |
| Heap 持续上涨，GC 越来越频繁 | 可能是内存压力、对象增长或内存泄漏 |
| CPU 正常，但 HikariCP active 接近最大连接数 | 可能是数据库连接池瓶颈 |
| Tomcat 活跃线程接近上限 | 可能是线程池不足，或下游调用阻塞 |
| CPU、内存正常，但网络发送量很高 | 可能是大响应、文件下载或带宽瓶颈 |
| 所有资源正常，但接口仍慢 | 继续看 SQL、外部服务、锁等待或业务代码 |

> [!tip] 性能结论要有证据
>
> “接口慢”是现象，不是结论。
>
> 更完整的结论应该包含：
>
> 1. 哪个接口在什么并发下变慢；
> 2. JMeter 的平均值、P95、错误率如何；
> 3. 同一时间段 CPU、JVM、线程、连接池发生了什么；
> 4. 根据指标得出的瓶颈假设；
> 5. 后续如何验证这个假设。

---

## 三、Prometheus 和 Grafana 的基本概念

### 1. 什么是指标 Metric？

指标就是可以随着时间变化、可以被记录和查询的数值。

例如：

~~~text
jvm_memory_used_bytes 240000000
process_cpu_usage 0.12
http_server_requests_seconds_count 100
~~~

这些数字单独看意义有限，真正有价值的是：

- 数值是多少；
- 数值在什么时候产生；
- 属于哪个应用、接口或实例；
- 随时间是上涨、下降还是稳定。

### 2. 什么是时间序列？

Prometheus 保存的是带有时间的连续数据。

例如 CPU 使用率：

| 时间 | CPU |
|---|---:|
| 10:00:00 | 10% |
| 10:00:15 | 12% |
| 10:00:30 | 68% |
| 10:00:45 | 92% |

Grafana 把这些时间点连起来，就形成了曲线。

### 3. Prometheus 的工作方式

Prometheus 使用“主动拉取”的方式采集数据：

1. 被监控服务暴露一个指标接口；
2. Prometheus 按照 scrape_interval 定时访问这个接口；
3. Prometheus 读取指标文本；
4. Prometheus 给指标附加时间和标签；
5. Prometheus 保存这些时间序列；
6. Grafana 再向 Prometheus 发起查询。

scrape 可以理解为“抓取/采集”。

### 4. Grafana 不负责采集

Grafana 的工作流程是：

~~~text
Grafana
  ↓ 查询
Prometheus
  ↓ 已保存的数据
指标时间序列
~~~

排查问题时要按顺序判断：

1. Spring Boot 指标接口有没有数据；
2. Prometheus Target 是否为 UP；
3. Grafana 数据源是否连接正确；
4. Dashboard 查询的指标名称、标签和时间范围是否正确。

---

## 四、开始前的准备工作

### 1. 需要准备的软件

- Docker Desktop；
- 一个可以正常启动的 Spring Boot 项目；
- JDK 与 Maven；
- 浏览器；
- 后续进行压力测试时使用 JMeter。

### 2. 需要确认的地址

| 地址 | 作用 | 正常现象 |
|---|---|---|
| http://localhost:3030 | Prometheus 首页 | 可以打开 Prometheus |
| http://localhost:3030/targets | Prometheus 目标状态 | 可以查看各个 Target 的 UP/DOWN |
| http://localhost:3000 | Grafana 首页 | 可以打开登录页 |
| http://localhost:8080 | Spring Boot 后端 | 后端接口可以访问 |
| http://localhost:5173 | 前端页面 | 前端页面可以访问 |
| http://localhost:8080/actuator/prometheus | Spring Boot 指标接口 | 页面显示大量指标文本 |

> [!note] 前端需要不需要接入 Prometheus？
>
> 本次主要测试后端接口，因此监控重点是后端 8080。
>
> 前端 5173 主要负责页面渲染，不是本次后端性能监控的核心目标。浏览器端性能可以另行使用前端监控方案。

---

## 五、使用 Docker 部署基础监控环境

### 1. 创建目录

本次示例目录为：

~~~text
D:\monitoring
├── docker-compose.yml
└── prometheus
    └── prometheus.yml
~~~

目录作用：

| 文件/目录 | 作用 |
|---|---|
| docker-compose.yml | 描述需要启动哪些容器、端口如何映射 |
| prometheus/prometheus.yml | 告诉 Prometheus 去哪里采集指标 |

![[02-monitoring目录结构.png]]


### 2. docker-compose.yml

下面是本次实践使用的简化配置：

~~~yaml
services:
  prometheus:
    image: prom/prometheus
    container_name: prometheus
    ports:
      - "3030:9090"
    volumes:
      - ./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    container_name: grafana
    ports:
      - "3000:3000"

  node-exporter:
    image: prom/node-exporter
    container_name: node-exporter
    ports:
      - "9100:9100"
~~~

### 3. 逐项理解配置

#### services

表示要定义多个服务。这里有三个：

- prometheus；
- grafana；
- node-exporter。

#### image

表示容器启动时使用的镜像。如果本地没有，Docker 会尝试拉取。

#### container_name

给容器取一个固定名字。

因为 Prometheus 容器叫 prometheus，Grafana 容器就可以通过：

~~~text
http://prometheus:9090
~~~

访问它。

#### ports

格式是：

~~~text
宿主机端口:容器端口
~~~

例如：

~~~yaml
"3030:9090"
~~~

含义是：

~~~text
Windows:3030  ─────>  Prometheus容器:9090
~~~

#### volumes

把 Windows 上的配置文件映射到容器里面：

~~~yaml
./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
~~~

左边是宿主机文件，右边是容器内文件。修改 Windows 上的 prometheus.yml 后，Prometheus 容器才能读到这份配置。

### 4. 启动容器

打开 PowerShell，执行：

~~~powershell
cd D:\monitoring
docker compose up -d
~~~

参数解释：

| 参数 | 作用 |
|---|---|
| up | 创建并启动服务 |
| -d | 后台运行，不占用当前终端 |

### 5. 查看容器状态

~~~powershell
docker ps
~~~

正常情况下至少应该看到：

~~~text
prometheus     Up
grafana        Up
node-exporter  Up
~~~

端口部分大致如下：

~~~text
prometheus     0.0.0.0:3030->9090/tcp
grafana        0.0.0.0:3000->3000/tcp
node-exporter  0.0.0.0:9100->9100/tcp
~~~


![[03-docker-ps.png]]


### 6. 常用 Docker 命令

~~~powershell
# 查看所有容器，包括已经停止的容器
docker ps -a

# 查看 Prometheus 最后 50 行日志
docker logs prometheus --tail 50

# 查看 Grafana 最后 50 行日志
docker logs grafana --tail 50

# 重启 Prometheus
docker compose restart prometheus

# 停止当前 compose 项目
docker compose stop

# 重新启动已停止的服务
docker compose start
~~~

> [!warning] stop 和 down 不一样
>
> docker compose stop 通常只停止容器；docker compose down 会移除 compose 创建的容器和网络。初学阶段排错优先使用 restart，不要在不清楚影响时随意删除。

---

## 六、配置 Prometheus 采集目标

### 1. Prometheus 配置文件位置

~~~text
D:\monitoring\prometheus\prometheus.yml
~~~

### 2. 当前阶段的完整配置

这份配置包含三个采集目标：

1. Prometheus 自己；
2. Node Exporter；
3. 本机 Windows 上运行的 Spring Boot。

~~~yaml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: "prometheus"
    static_configs:
      - targets:
          - "prometheus:9090"

  - job_name: "node"
    static_configs:
      - targets:
          - "node-exporter:9100"

  - job_name: "springboot"
    metrics_path: "/actuator/prometheus"
    static_configs:
      - targets:
          - "host.docker.internal:8080"
~~~

### 3. scrape_interval

~~~yaml
scrape_interval: 15s
~~~

表示 Prometheus 每隔 15 秒采集一次。

刚修改配置或刚启动服务时，页面短时间出现 UNKNOWN 并不一定是失败，可以先等待一两个采集周期再刷新。

### 4. job_name

job_name 是人为给采集任务起的名字：

~~~yaml
job_name: "springboot"
~~~

以后可以通过下面的 PromQL 查询 Spring Boot 是否正常：

~~~promql
up{job="springboot"}
~~~

### 5. targets

本次三个地址含义不同：

| Target | 含义 |
|---|---|
| prometheus:9090 | Prometheus 容器内部的服务端口 |
| node-exporter:9100 | Node Exporter 容器的服务端口 |
| host.docker.internal:8080 | Docker 容器访问 Windows 宿主机上的 Spring Boot |

> [!important] 不要把 3030 写成 Prometheus 容器内部端口
>
> 最容易犯的错误是把 prometheus:3030 写进 prometheus.yml。
>
> 3030 是 Windows 对外映射的端口，Prometheus 容器内部监听的是 9090。所以容器内部采集 Prometheus 自身时必须写：
>
> ~~~yaml
> prometheus:9090
> ~~~

### 6. 为什么不能写 localhost:8080？

在 Prometheus 容器中，localhost 指的是 Prometheus 容器自己，不是 Windows。

错误或通常不可用：

~~~yaml
localhost:8080
~~~

Windows Docker Desktop 提供了：

~~~yaml
host.docker.internal:8080
~~~

它表示从容器访问宿主机。

### 7. 修改配置后重启 Prometheus

~~~powershell
cd D:\monitoring
docker compose restart prometheus
~~~

等待 15~30 秒，再打开：

~~~text
http://localhost:3030/targets
~~~

---

## 七、验证 Prometheus 是否正常

### 1. 打开 Prometheus 首页

~~~text
http://localhost:3030
~~~

### 2. 查看 Target 健康状态

直接打开：

~~~text
http://localhost:3030/targets
~~~

也可以从菜单进入：

~~~text
Status
  ↓
Target health
~~~

正常时应该看到：

| Job | Endpoint | 状态 |
|---|---|---|
| prometheus | http://prometheus:9090/metrics | UP |
| node | http://node-exporter:9100/metrics | UP |
| springboot | http://host.docker.internal:8080/actuator/prometheus | UP |

![[04-prometheus-targets.png]]


### 3. 使用 Prometheus 自带查询验证

打开：

~~~text
http://localhost:3030/graph
~~~

输入：

~~~promql
up
~~~

结果为 1 表示对应 Target 当前可达，0 表示不可达。

只查看 Spring Boot：

~~~promql
up{job="springboot"}
~~~

只查看 Node Exporter：

~~~promql
up{job="node"}
~~~

如果 Spring Boot 已经接入，还可以尝试：

~~~promql
http_server_requests_seconds_count
~~~

如果能查询到结果，说明 Prometheus 已经采集到了 HTTP 请求指标。

---

## 八、配置 Grafana 连接 Prometheus

### 1. 打开 Grafana

~~~text
http://localhost:3000
~~~

首次登录通常使用：

~~~text
用户名：admin
密码：admin
~~~

首次登录后按页面要求修改密码。

### 2. 添加 Prometheus 数据源

Grafana 新版菜单位置可能略有差异，核心路径是：

~~~text
Connections
  ↓
Data sources
  ↓
Add data source
  ↓
Prometheus
~~~

填写：

| 配置项 | 值 |
|---|---|
| Name | prometheus-local，或自己容易识别的名字 |
| URL | http://prometheus:9090 |
| Access | Server 或 Server (default) |

然后点击：

~~~text
Save & Test
~~~

成功提示类似：

~~~text
Successfully queried the Prometheus API
~~~


![[05-grafana-datasource.png]]


### 3. 为什么 Grafana 里面写 prometheus:9090？

Grafana 也运行在 Docker 容器中。在 Docker Compose 网络中，容器可以通过服务名互相访问：

~~~text
grafana  ─────>  prometheus:9090
~~~

这里使用的是：

- 容器服务名：prometheus；
- Prometheus 容器内部端口：9090。

不要把浏览器访问地址直接复制进 Grafana：

~~~text
http://localhost:3030
~~~

localhost 在 Grafana 容器中代表 Grafana 自己，不代表 Windows，也不一定能找到 Prometheus。

### 4. 本次遇到的数据源问题

之前页面中出现过一个类似：

~~~text
camptocamp-prometheus-alertmanager...
~~~

这不是本次新建的 Prometheus 数据源。排查时应确认：

1. 选择的是自己创建的 Prometheus 数据源；
2. URL 是 http://prometheus:9090；
3. Access 保持 Server；
4. 点击 Save & Test 后提示查询成功。

如果旧数据源配置错误，可以删除旧数据源，再重新创建一个名称清晰的：

~~~text
prometheus-local
~~~

---

## 九、导入 Node Exporter Dashboard

### 1. 导入 Dashboard ID

Grafana 中进入：

~~~text
Dashboards
  ↓
New
  ↓
Import
~~~

在 Grafana.com dashboard URL or ID 中输入：

~~~text
1860
~~~

点击 Load。

1860 是 Node Exporter Full Dashboard 的 ID。

进入导入确认页面后：

1. 确认名称是 Node Exporter Full；
2. 如果页面出现数据源下拉框，选择 prometheus-local；
3. 点击 Import。

	
![[06-import-dashboard-1860.png]]


### 2. 时间范围与数据刷新

导入后如果出现 No data，先不要判断为配置失败。

右上角时间范围建议先设置为：

~~~text
Last 5 minutes
~~~

或者：

~~~text
Last 15 minutes
~~~

然后点击刷新。

原因是当前环境刚刚启动，历史数据很少。如果把时间范围选成不包含当前采集时间的绝对时间段，图表自然没有数据。


![[07-node-exporter-dashboard.png]]

### 3. Node Exporter Dashboard 主要看什么？

#### CPU

回答：机器的计算资源是否紧张？

- CPU 从低水平逐步上升，通常是压力增加的正常表现；
- 长时间接近 95%~100%，同时响应时间明显上升，可能存在 CPU 瓶颈；
- CPU 很低但响应时间很高，不能直接归因于 CPU，需要继续看数据库、网络、锁或外部服务。

#### Memory

重点看使用量曲线是否会在压测结束后回落。

~~~text
启动：4 GB
压测中：6 GB
压测结束：4 GB
~~~

这种趋势通常比“压测中使用了多少”更有参考价值。

如果内存持续上涨，停止压力后也不回落，可能需要排查：

- 缓存是否没有失效；
- 对象是否一直被引用；
- 是否存在内存泄漏；
- JVM 堆和操作系统内存是否被混淆。

#### Disk I/O

如果接口慢、CPU 不高，但磁盘读写非常繁忙，可能与 SQL 读写、日志写入、文件操作或磁盘性能有关。

#### Network

网络接收通常与请求流量有关，网络发送通常与响应大小有关。文件下载、大 JSON、图片或批量数据接口需要特别关注网络发送量。

> [!warning] Node Exporter 的采集对象要确认
>
> 本次是在 Windows + Docker Desktop 环境中运行 prom/node-exporter。Dashboard 能够显示数据，首先说明采集链路和查询是通的；但在严谨的性能测试中，还要确认这些指标究竟代表 Windows 宿主机、Docker 虚拟机还是容器自身。
>
> 如果需要精确监控 Windows 宿主机，后续应单独确认 Windows 主机采集方案，并在笔记中记录“采集对象”。不要看到一个 CPU 曲线就默认它一定是被测后端所在主机的完整 CPU 使用率。

---

## 十、接入 Spring Boot 应用监控

### 1. 本次应用环境

本次关联对话中确认：

~~~text
Spring Boot：3.3.5
启动方式：mvn spring-boot:run
后端端口：8080
前端端口：5173
~~~

Prometheus 需要监控的是后端：

~~~text
http://localhost:8080/actuator/prometheus
~~~

### 2. 添加 Maven 依赖

打开项目的 pom.xml，在 dependencies 中增加：

~~~xml
<!-- 提供 Spring Boot Actuator 监控端点 -->
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-actuator</artifactId>
</dependency>

<!-- 让 Micrometer 输出 Prometheus 格式 -->
<dependency>
    <groupId>io.micrometer</groupId>
    <artifactId>micrometer-registry-prometheus</artifactId>
</dependency>
~~~

Spring Boot 的父工程已经负责版本管理时，通常不需要手动填写版本号。

### 3. 配置 application.yml

文件位置通常是：

~~~text
src/main/resources/application.yml
~~~

本地学习阶段可以使用：

~~~yaml
management:
  endpoints:
    web:
      exposure:
        include: "*"

  endpoint:
    health:
      show-details: always

  metrics:
    tags:
      application: zhihuitong
~~~

配置含义：

| 配置 | 作用 |
|---|---|
| exposure.web.include | 决定哪些 Actuator 端点可以通过 Web 访问 |
| include: "*" | 暴露全部端点，方便本地学习和排查 |
| health.show-details | 在健康检查中显示更多信息 |
| metrics.tags.application | 给指标添加应用名称标签，方便 Grafana 筛选 |

> [!note] zhihuitong 和 mlkspace
>
> 关联对话中曾出现过 mlkspace 和 zhihuitong 两个应用名。它们只是指标标签，不是 Prometheus 的固定要求。
>
> 当前截图中观察到的应用标签是 zhihuitong，所以本笔记使用 zhihuitong 作为示例。实际项目名称可以替换，但要保持配置、Grafana 变量和查询条件一致。

### 4. 暴露全部端点的安全提醒

include: "*" 适合本地学习和临时排查，不建议直接用于生产环境。

生产环境建议：

- 只暴露确实需要的端点；
- 对 /actuator/prometheus 做访问控制；
- 不要把数据库、环境变量、配置等敏感信息暴露给未授权用户；
- 不要为了让 Dashboard 有数据而永久关闭安全认证。

### 5. 启动 Spring Boot

在项目根目录执行：

~~~powershell
mvn spring-boot:run
~~~

启动成功时通常可以看到：

~~~text
Tomcat started on port 8080
~~~


![[08-springboot-start.png]]


### 6. 验证 Actuator 入口

打开：

~~~text
http://localhost:8080/actuator
~~~

正常情况下可以看到 _links，其中应该包含：

~~~json
{
  "_links": {
    "health": {
      "href": "/actuator/health"
    },
    "metrics": {
      "href": "/actuator/metrics"
    },
    "prometheus": {
      "href": "/actuator/prometheus"
    }
  }
}
~~~

最重要的是存在 prometheus。

### 7. 验证 Prometheus 指标文本

打开：

~~~text
http://localhost:8080/actuator/prometheus
~~~

正常会看到大量文本，例如：

~~~text
# HELP jvm_memory_used_bytes
# TYPE jvm_memory_used_bytes gauge
jvm_memory_used_bytes{area="heap"} 2.4E8

# HELP http_server_requests_seconds_count
# TYPE http_server_requests_seconds_count counter
~~~

常见指标：

| 指标 | 说明 |
|---|---|
| jvm_memory_used_bytes | JVM 内存使用量 |
| jvm_gc_pause_seconds | GC 暂停相关指标 |
| jvm_threads_live_threads | 当前存活线程数 |
| process_cpu_usage | Java 进程 CPU 使用率 |
| http_server_requests_seconds_count | HTTP 请求累计次数 |
| http_server_requests_seconds_sum | HTTP 请求累计耗时 |
| hikaricp_connections_active | HikariCP 当前活跃连接数 |
| hikaricp_connections_pending | 等待数据库连接的请求数 |

<!-- 截图占位：09 -->
> [!note] 截图 09：/actuator/prometheus 指标页面
>
> 待插入：浏览器打开指标接口后的页面截图。
>
> 建议截图内容：能够看到 jvm_memory_used_bytes、http_server_requests_seconds_count 等指标名称。
>
> ![[此处放入截图-09-actuator-prometheus.png]]

### 8. 如果访问得到 401

如果 /actuator 或 /actuator/prometheus 返回 401，通常是 Spring Security 拦截了请求。

本地学习阶段可以在安全配置中对 Actuator 做最小放行：

~~~java
.requestMatchers("/actuator/**")
.permitAll()
~~~

完整写法要以项目当前使用的 Spring Security 配置方式为准。

排查思路：

1. 确认访问路径没有写错；
2. 确认 Spring Boot 已重启，配置已加载；
3. 查看 Security 配置是否拦截了 /actuator/**；
4. 只在本地测试环境放行；
5. 生产环境改用认证、网络隔离或专用管理端口。


![[10-actuator.png]]


---

## 十一、让 Prometheus 采集 Spring Boot

### 1. 检查 prometheus.yml

确保包含：

~~~yaml
  - job_name: "springboot"
    metrics_path: "/actuator/prometheus"
    static_configs:
      - targets:
          - "host.docker.internal:8080"
~~~

metrics_path 很重要。

如果不配置，Prometheus 默认会访问 /metrics；但 Spring Boot 的 Prometheus 指标接口是 /actuator/prometheus。

### 2. 重启并等待采集

~~~powershell
cd D:\monitoring
docker compose restart prometheus
~~~

等待 15~30 秒，再打开：

~~~text
http://localhost:3030/targets
~~~

### 3. 判断是否接入成功

看到下面内容时，说明 Spring Boot 已经被 Prometheus 采集：

~~~text
springboot
http://host.docker.internal:8080/actuator/prometheus
UP
~~~

![[Pasted image 20260801220536.png]]


### 4. 三种状态怎么理解？

| 状态 | 含义 | 优先检查 |
|---|---|---|
| UP | Prometheus 成功访问目标并采集到数据 | 采集链路已通 |
| DOWN | 目标存在，但访问失败或返回错误 | Endpoint、端口、日志、权限 |
| UNKNOWN | 还没有足够的采集结果，或刚重启 | 等待一个采集周期后刷新 |

---

## 十二、Grafana 中查看 Spring Boot 指标

### 1. 先确认数据源

Grafana Dashboard 顶部通常有数据源选择项。选择自己创建的：

~~~text
prometheus-local
~~~

不要误选旧的 Alertmanager 或其他无关数据源。

### 2. HTTP 请求指标

重点关注：

- 请求总数；
- 请求速率；
- 平均响应时间；
- P95/P99 响应时间；
- HTTP 状态码；
- 错误率；
- URI、Method、Instance 等标签。

### 3. JVM 指标

重点关注：

- Heap 使用量；
- Non-Heap 使用量；
- GC 次数；
- GC 暂停时间；
- 存活线程数；
- Tomcat 线程；
- 进程 CPU。

### 4. HikariCP 指标

重点关注：

- 当前活跃连接数；
- 最大连接数；
- 空闲连接数；
- 等待连接数；
- 获取连接耗时。

如果 connections_pending 长时间大于 0，通常说明请求在等待数据库连接，需要结合数据库和连接池配置继续分析。

### 5. 时间范围要和测试时间一致

| 场景 | 时间范围 |
|---|---|
| 验证数据是否实时到达 | Last 5 minutes |
| 手工访问接口观察变化 | Last 15 minutes |
| 一次短时压测 | Last 15 minutes 或 Last 30 minutes |
| 分析长时间稳定性 | 自定义压测起止时间 |

如果图表显示 No data，按下面顺序检查：

1. 时间范围是否覆盖了实际请求时间；
2. 右上角是否点击过刷新；
3. 数据源是否选择正确；
4. Prometheus Target 是否为 UP；
5. Prometheus 中是否能查询到目标指标；
6. Dashboard 变量是否选中了正确的 Application、Job、Instance。

<!-- 截图占位：12 -->
> [!note] 截图 12：Spring Boot Dashboard
>
> 待插入：包含 HTTP、JVM、线程或 HikariCP 图表的 Dashboard 截图。
>
> 建议截图内容：顶部 Application、Instance、Data source、时间范围和主要曲线清晰可见。
>
> ![[此处放入截图-12-springboot-dashboard.png]]

---

## 十三、PromQL 入门：用查询理解图表

PromQL 是 Prometheus 的查询语言。先掌握几个最常用的查询即可。

### 1. 查看 Target 是否在线

~~~promql
up
~~~

只看 Spring Boot：

~~~promql
up{job="springboot"}
~~~

### 2. 查看 HTTP 请求累计次数

~~~promql
http_server_requests_seconds_count
~~~

注意：这是累计值，不是每秒请求量。

### 3. 查看每秒请求量

~~~promql
sum by (uri, method, status) (
  rate(http_server_requests_seconds_count[1m])
)
~~~

rate 会根据一段时间内累计值的变化，计算每秒增长速度。

### 4. 查看平均响应时间

~~~promql
1000 *
sum by (uri, method) (
  rate(http_server_requests_seconds_sum[1m])
)
/
sum by (uri, method) (
  rate(http_server_requests_seconds_count[1m])
)
~~~

结果乘以 1000 是为了把秒转换成毫秒。

计算逻辑：

~~~text
平均响应时间
= 一段时间内新增的总耗时
  ÷ 一段时间内新增的请求数
~~~

### 5. 查看 JVM Heap 使用量

~~~promql
jvm_memory_used_bytes{area="heap"}
~~~

如果要按应用查看，可以继续增加 application 标签条件。

### 6. 查看进程 CPU

~~~promql
process_cpu_usage
~~~

### 7. 查看存活线程

~~~promql
jvm_threads_live_threads
~~~

### 8. 查看 HikariCP 连接池

~~~promql
hikaricp_connections_active
~~~

~~~promql
hikaricp_connections_pending
~~~

### 9. P95/P99 的前提

平均响应时间容易被少量极慢请求掩盖。性能测试更常看 P95、P99：

- P95：95% 的请求不超过这个时间；
- P99：99% 的请求不超过这个时间。

如果要用 histogram_quantile 查询 P95，应用需要暴露 histogram bucket。

本地测试配置可以增加：

~~~yaml
management:
  metrics:
    distribution:
      percentiles-histogram:
        http.server.requests: true
~~~

然后尝试：

~~~promql
histogram_quantile(
  0.95,
  sum by (le, uri, method) (
    rate(http_server_requests_seconds_bucket[5m])
  )
)
~~~

> [!warning] P95 查询无数据不一定是 Grafana 故障
>
> 如果没有配置 histogram，http_server_requests_seconds_bucket 可能不存在。此时平均响应时间仍可能可以查询，但 P95/P99 需要先开启直方图或使用其他统计方案。

---

## 十四、第一次手工验证：让曲线动起来

在正式使用 JMeter 之前，先做一个小实验。

### 实验目标

~~~text
手工访问接口
  ↓
Spring Boot 请求指标增加
  ↓
Prometheus 采集到变化
  ↓
Grafana 曲线发生变化
~~~

### 操作步骤

1. Grafana 时间范围设置为 Last 5 minutes；
2. 打开一个可正常访问的后端接口；
3. 连续刷新或调用接口 10 次；
4. 等待至少 15 秒；
5. 回到 Grafana 点击刷新；
6. 观察 Request Count 或请求速率曲线。

### 预期结果

- Request Count 增加；
- 请求速率出现变化；
- 响应时间图表有数据；
- URI、Method、Status 标签能看到刚才调用的接口。


![[13-manual-request-change.png]]


---

## 十五、和 JMeter 配合进行性能测试

### 1. 推荐测试顺序

不要一上来就直接压 100 并发。建议分阶段：

| 阶段 | 目的 |
|---|---|
| 单用户 | 验证接口正确、监控指标正常 |
| 低并发 | 观察基线和初始响应时间 |
| 逐步加压 | 找到吞吐量和响应时间开始恶化的点 |
| 目标并发 | 验证业务目标是否达成 |
| 稳定性测试 | 观察长时间运行后的内存、GC、连接池 |

### 2. 压测前的检查清单

- Spring Boot 可以正常访问；
- /actuator/prometheus 可以打开；
- Prometheus 的 springboot Target 为 UP；
- Grafana 数据源测试成功；
- Dashboard 时间范围已设置；
- 记录当前 CPU、内存、JVM Heap 基线；
- 确认数据库和依赖服务也已启动；
- JMeter 请求参数、认证信息、测试数据准备完成；
- 压测环境与生产环境的差异已经记录。

### 3. 压测时同时观察

#### JMeter

- 吞吐量 / TPS；
- 平均响应时间；
- P90/P95/P99；
- 错误率；
- 各接口的请求数和成功数。

#### Grafana

- CPU；
- 进程 CPU；
- JVM Heap；
- GC；
- 存活线程；
- Tomcat 线程；
- HikariCP active / pending；
- 磁盘 I/O；
- 网络流量。

### 4. 建议的观察时间线

~~~text
压测前 1~2 分钟：观察基线
       ↓
启动低并发：确认指标开始变化
       ↓
逐步加压：记录响应时间和资源变化
       ↓
保持目标并发：观察是否稳定
       ↓
停止压测：观察内存、线程、连接是否回落
~~~

<!-- 截图占位：14 -->
> [!note] 截图 14：JMeter 压测结果
>
> 待插入：JMeter 聚合报告、Summary Report 或实时结果截图。
>
> 建议截图内容：线程数、吞吐量、平均响应时间、错误率、P95 等关键数据。
>
> ![[此处放入截图-14-jmeter-result.png]]

<!-- 截图占位：15 -->
> [!note] 截图 15：压测同时段的 Grafana Dashboard
>
> 待插入：与截图 14 同一时间段的 Grafana 指标截图。
>
> 建议截图内容：时间范围和 JMeter 测试时间相互对应，能够观察资源曲线与压测曲线的关系。
>
> ![[此处放入截图-15-grafana-load-test.png]]

---

## 十六、常见性能现象与分析思路

### 情况 1：CPU 很高，响应时间也很高

现象：

~~~text
JMeter：响应时间上升、吞吐量下降
Grafana：CPU 长时间 95%~100%
~~~

初步判断：

- CPU 计算成为瓶颈；
- 代码存在大量计算；
- JSON 序列化、加密、正则、循环等操作消耗过多；
- GC 或后台任务抢占 CPU。

下一步：

- 区分进程 CPU 和系统 CPU；
- 查看 GC 指标；
- 查看慢接口和慢方法；
- 使用 Java Flight Recorder、Arthas 等工具继续定位。

### 情况 2：CPU 不高，但响应时间高

可能原因：

- 数据库查询慢；
- 等待数据库连接；
- 等待外部 HTTP 服务；
- 锁等待；
- 线程池排队；
- 磁盘或网络 I/O；
- 请求被限流或重试。

此时不能只盯着 CPU。

### 情况 3：Heap 一直上涨

需要观察：

- 停止压测后是否回落；
- GC 后是否能回到相对稳定的水平；
- Old Gen 是否持续增加；
- 是否存在缓存、集合、ThreadLocal 或监听器对象未释放。

单凭一张内存图不能直接下“内存泄漏”结论，只能说“存在内存持续增长的现象，需要进一步验证”。

### 情况 4：HikariCP 等待连接数增加

现象：

~~~text
hikaricp_connections_pending > 0
~~~

可能原因：

- 数据库连接池太小；
- SQL 执行时间太长；
- 事务持有连接时间太长；
- 数据库本身已达到瓶颈；
- 连接没有及时释放。

需要结合 active、max、pending、获取连接耗时以及数据库慢查询一起分析。

### 情况 5：JMeter 报错率上升，但服务器资源正常

需要排查：

- 请求参数或认证是否失效；
- Token 是否过期；
- 测试数据是否重复；
- 服务端业务校验是否拒绝；
- JMeter 连接超时、断言失败；
- 依赖服务返回错误。

资源正常不等于接口一定正常。

---

## 十七、故障排查手册

### 1. Prometheus 端口启动失败

错误示例：

~~~text
port 9090 already in use
~~~

原因：Windows 上的 9090 已被其他程序占用。

解决：

~~~yaml
ports:
  - "3030:9090"
~~~

然后浏览器访问：

~~~text
http://localhost:3030
~~~

### 2. Prometheus Target 显示 prometheus:3030 为 DOWN

原因通常是把宿主机映射端口写进了容器内部地址。

错误：

~~~yaml
- "prometheus:3030"
~~~

正确：

~~~yaml
- "prometheus:9090"
~~~

修改后：

~~~powershell
docker compose restart prometheus
~~~

### 3. Target 刚重启后显示 UNKNOWN

原因：

- Prometheus 刚重启；
- 还没有完成第一次采集；
- 页面缓存了刚才的状态。

处理：

1. 等待 15~30 秒；
2. 刷新 /targets；
3. 如果仍然异常，查看日志：

~~~powershell
docker logs prometheus --tail 50
~~~

### 4. Grafana 数据源 Save & Test 返回 404

重点检查：

- URL 是否只写 http://prometheus:9090；
- 是否误写了 /api；
- 是否选择了错误的旧数据源；
- Grafana 与 Prometheus 是否在同一个 Docker 网络；
- Prometheus 容器是否真的在运行。

可以从 Grafana 容器内部测试：

~~~powershell
docker exec -it grafana sh
~~~

进入容器后：

~~~sh
wget -qO- http://prometheus:9090/api/v1/status/buildinfo
~~~

正常应返回包含下面内容的 JSON：

~~~json
{
  "status": "success"
}
~~~

退出容器：

~~~sh
exit
~~~

### 5. Grafana Dashboard 没有数据

按顺序排查：

1. 右上角时间范围改为 Last 5 minutes；
2. 点击刷新；
3. 查看 Dashboard 顶部数据源是否为 prometheus-local；
4. 查看 /targets 中对应 Job 是否为 UP；
5. 在 Prometheus /graph 中直接查询指标；
6. 检查 Dashboard 的变量是否选择了正确的 Application、Job、Instance；
7. 确认压测或手工请求确实发生在当前时间范围内。

### 6. /actuator/prometheus 返回 401

原因：Spring Security 拦截。

处理：

- 本地测试阶段放行 /actuator/**；
- 生产环境不要直接无保护开放全部 Actuator；
- 修改安全配置后重启 Spring Boot；
- 再次访问指标接口。

### 7. Spring Boot Target 显示 DOWN

先在 Windows 上直接验证：

~~~powershell
Invoke-WebRequest http://localhost:8080/actuator/prometheus
~~~

如果 Windows 浏览器也打不开：

- Spring Boot 没启动；
- 端口不是 8080；
- Actuator 依赖没加载；
- 端点没有暴露；
- Security 返回 401。

如果 Windows 能打开，但 Prometheus 仍 DOWN：

- 检查 host.docker.internal:8080 是否写对；
- 检查 Prometheus 配置缩进；
- 查看 docker logs prometheus --tail 50；
- 重启 Prometheus 后等待采集周期。

---

## 十八、完整验收清单

### Docker 层

- [ ] Docker Desktop 已启动；
- [ ] prometheus 容器状态为 Up；
- [ ] grafana 容器状态为 Up；
- [ ] node-exporter 容器状态为 Up；
- [ ] 3030、3000、9100 端口映射正确。

### Prometheus 层

- [ ] http://localhost:3030 可以打开；
- [ ] /targets 页面可以打开；
- [ ] prometheus Target 为 UP；
- [ ] node Target 为 UP；
- [ ] Spring Boot 启动后 springboot Target 为 UP；
- [ ] PromQL up 可以查询；
- [ ] 可以查询 http_server_requests_seconds_count。

### Grafana 层

- [ ] http://localhost:3000 可以打开；
- [ ] Prometheus 数据源 Save & Test 成功；
- [ ] 数据源 URL 是 http://prometheus:9090；
- [ ] Dashboard 选择了正确的数据源；
- [ ] 时间范围覆盖实际采集时间；
- [ ] Node Exporter Dashboard 可以显示数据；
- [ ] Spring Boot Dashboard 可以显示应用指标。

### Spring Boot 层

- [ ] 已添加 Actuator 依赖；
- [ ] 已添加 Prometheus Registry 依赖；
- [ ] /actuator 可以访问；
- [ ] /actuator/prometheus 可以访问；
- [ ] 页面中存在 JVM 和 HTTP 指标；
- [ ] Security 没有错误拦截；
- [ ] prometheus.yml 使用 host.docker.internal:8080；
- [ ] 修改配置后已重启 Prometheus。

### 性能测试层

- [ ] JMeter 单用户请求成功；
- [ ] 手工请求可以让 Grafana 曲线变化；
- [ ] 记录压测开始和结束时间；
- [ ] JMeter 与 Grafana 使用相同时间范围；
- [ ] 记录 TPS、平均响应时间、P95、错误率；
- [ ] 同时记录 CPU、Heap、GC、线程和连接池；
- [ ] 停止压力后观察资源是否恢复。

---

## 十九、截图清单

建议按下面的编号保存截图，名称和笔记占位符保持一致：

| 编号 | 建议文件名 | 截图内容 |
|---:|---|---|
| 01 | 截图-01-环境总览.png | Docker、Prometheus、Grafana、Spring Boot 总览 |
| 02 | 截图-02-monitoring目录结构.png | D:\monitoring 文件结构 |
| 03 | 截图-03-docker-ps.png | docker ps 三个容器 Up |
| 04 | 截图-04-prometheus-targets.png | Prometheus Target health |
| 05 | 截图-05-grafana-datasource.png | Grafana 数据源配置成功 |
| 06 | 截图-06-import-dashboard-1860.png | 导入 Dashboard 1860 |
| 07 | 截图-07-node-exporter-dashboard.png | Node Exporter Full 图表 |
| 08 | 截图-08-springboot-start.png | Spring Boot 启动成功 |
| 09 | 截图-09-actuator-prometheus.png | Actuator 指标文本 |
| 10 | 截图-10-actuator-401.png | Security 导致的 401（如果遇到） |
| 11 | 截图-11-springboot-target-up.png | Spring Boot Target 为 UP |
| 12 | 截图-12-springboot-dashboard.png | Spring Boot Dashboard |
| 13 | 截图-13-manual-request-change.png | 手工请求后曲线变化 |
| 14 | 截图-14-jmeter-result.png | JMeter 压测结果 |
| 15 | 截图-15-grafana-load-test.png | 压测同时段 Grafana |

> [!tip] 截图怎么截才有复习价值？
>
> 不要只截整个屏幕。每张截图最好能回答一个问题：
>
> - 配置文件截图：哪一行配置解决了什么问题？
> - Target 截图：Prometheus 是否真的采集到了？
> - 数据源截图：Grafana 到底连接了哪个地址？
> - Dashboard 截图：当前时间范围、实例和数据源是什么？
> - 压测截图：JMeter 数据和 Grafana 数据能不能按时间对上？

---

## 二十、后续学习路线

### 已完成的基础链路

- [x] Docker 部署 Prometheus、Grafana、Node Exporter；
- [x] 处理宿主机端口 3030 与容器端口 9090 的区别；
- [x] 配置 Prometheus 自身和 Node Exporter；
- [x] Grafana 连接 Prometheus；
- [x] 导入 Node Exporter Dashboard 1860；
- [x] Spring Boot 接入 Actuator；
- [x] Spring Boot 接入 Micrometer Prometheus Registry；
- [x] Prometheus 采集 Spring Boot /actuator/prometheus；
- [x] 用 Grafana 查看应用、JVM、HTTP 指标。

### 下一步建议

1. 使用 JMeter 对登录接口做低并发基线测试；
2. 逐步增加并发，记录 TPS、平均响应时间、P95 和错误率；
3. 对比 CPU、Heap、GC、线程与 HikariCP；
4. 增加数据库监控；
5. 学习慢 SQL、连接池参数和事务；
6. 使用 Arthas、JFR 或 VisualVM 定位 Java 应用问题；
7. 学习链路追踪，例如 SkyWalking；
8. 将测试结论整理成“现象—证据—判断—验证—结论”的性能报告。

---

## 二十一、复习时最应该记住的 10 句话

1. JMeter 看用户请求结果，Grafana 看系统内部状态。
2. Prometheus 负责采集和保存，Grafana 负责查询和展示。
3. 3030:9090 中，3030 是宿主机端口，9090 是 Prometheus 容器端口。
4. 浏览器访问 Prometheus 用 http://localhost:3030。
5. Grafana 容器访问 Prometheus 用 http://prometheus:9090。
6. Docker 容器访问 Windows 上的 Spring Boot 用 host.docker.internal:8080。
7. Prometheus Target 为 UP，才说明采集链路真正打通。
8. Dashboard No data 时，先检查时间范围、数据源和 Target，不要立刻重装。
9. 平均响应时间不能代替 P95/P99，尤其是在少量慢请求存在时。
10. 看到一个指标异常只能提出假设，性能结论需要结合 JMeter、应用和基础设施多个证据。

# JMeter 实战（二）——性能报告与 Grafana 指标解读

> 面向零基础复盘一次完整查询性能测试。  
> 前置笔记：[[JMeter实战（一）——织慧通完整业务链与数据清理]]  
> 监控搭建：[[prometheus + Grafana]]

---

## 1. 这次性能测试的目标

本次没有把创建订单、分配批次、创建生产计划等写入请求放进正式查询压测，而是复制出查询脚本：

~~~text
D:\app_other\myjmeter\ceshi\zhihuitong_查询性能测试.jmx
~~~

正式查询压测要观察：

- 多个用户同时查询时接口是否变慢；
- 哪个接口最慢；
- 响应时间是否出现长尾；
- JMeter 是否出现错误；
- Spring Boot 的 JVM、GC、HTTP、HikariCP、Tomcat 是否同步异常；
- 主机 CPU、内存、磁盘和网络是否成为瓶颈。

JMeter 告诉我们“请求慢了”，Grafana 和后端日志帮助判断“为什么慢”。

---

## 2. 正式查询脚本配置

### 2.1 线程组参数

| 配置项 | 本次值 | 含义 |
|---|---:|---|
| Number of Threads | 10 | 模拟 10 个并发用户 |
| Ramp-Up Period | 30 秒 | 30 秒内逐渐启动 10 个线程 |
| Loop Count | Forever | 持续循环 |
| Scheduler | 开启 | 使用持续时间控制 |
| Duration | 180 秒 | 持续运行 3 分钟 |
| 结果监听器 | 正式运行时关闭 | 避免 GUI 消耗大量内存 |

### 2.2 Once Only Controller

验证码和登录放在 Once Only Controller 中：

~~~text
线程组
└── Once Only Controller
    ├── 01-获取验证码
    └── 02-用户登录
└── 03～09 查询接口
~~~

Once Only Controller 的意思是“每个线程只执行一次”。因此：

- 10 个线程会登录 10 次；
- 03～09 会在循环中持续执行；
- 登录接口只有 10 个样本，不能与查询接口的几百个样本直接比较。

### 文字记录：查询压测线程组

文字记录：查询压测使用 10 个线程、Ramp-Up 30 秒、Forever 循环、Scheduler 开启、Duration 180 秒。

回顾要点：这是本次查询基线测试的固定配置。

### 文字记录：Once Only Controller

文字记录：01-获取验证码和 02-用户登录位于 Once Only Controller 下，03～09 查询接口反复循环，10～14 写入接口处于禁用状态。

回顾要点：每个线程只登录一次，所以登录样本数只有 10 个。

---

## 3. 非 GUI 运行命令

~~~powershell
jmeter -n -t "D:\app_other\myjmeter\ceshi\zhihuitong_查询性能测试.jmx" -l "D:\app_other\myjmeter\results\query_10u.jtl" -e -o "D:\app_other\myjmeter\results\query_10u_report"
~~~

参数解释：

| 参数 | 全称或含义 | 作用 |
|---|---|---|
| -n | non-GUI | 非图形界面运行 |
| -t | test file | 指定 JMX 脚本 |
| -l | log file | 保存 JTL 结果文件 |
| -e | generate report | 测试结束后生成 HTML 报告 |
| -o | output folder | 指定 HTML 报告目录 |

相关英文：

| 术语 | 中文解释 |
|---|---|
| JMX | JMeter 测试计划文件，本质上是 XML |
| JTL | JMeter 测试结果文件，记录每个样本 |
| HTML Report | 根据 JTL 生成的网页报告 |
| non-GUI | 不打开可视化界面，适合正式压测 |
| GUI | 图形界面，适合编辑和调试 |

### 3.1 为什么修改 GUI 不影响正在运行的 CMD

执行命令时，JMeter 会读取当时保存的 JMX。之后在 GUI 中修改线程数，不会改变已经启动的命令行进程。

正确顺序：

~~~text
GUI 修改
→ Ctrl + S 保存 JMX
→ 停止旧 CMD 进程
→ 重新执行命令
~~~

### 3.2 报告什么时候生成

JTL 文件在测试期间逐渐增长，但 HTML 报告通常在测试结束后才完整生成。

如果命令行仍显示测试没有结束，HTML 报告目录可能不存在或内容不完整。

### 3.3 停止测试

优先使用优雅停止：

~~~powershell
shutdown.cmd
~~~

无法正常结束时再使用：

~~~powershell
stoptest.cmd
~~~

| 命令 | 含义 |
|---|---|
| shutdown.cmd | 请求线程完成当前任务后结束 |
| stoptest.cmd | 更强制地停止测试 |

### 3.4 从 JTL 重新生成 HTML 报告

~~~powershell
jmeter -g "D:\app_other\myjmeter\results\query_10u.jtl" -o "D:\app_other\myjmeter\results\query_10u_report"
~~~

输出目录必须是空目录或不存在的目录。JMeter 不允许把新报告覆盖到已有非空目录。

### 文字记录：CMD 非 GUI 运行

文字记录：使用 jmeter -n -t ... -l ... -e -o ... 命令运行查询脚本，不同时点击 GUI 的启动按钮。

回顾要点：执行前先保存 JMX，修改 GUI 后必须重新启动 CMD 进程。

### 文字记录：JTL 和 HTML 报告目录

文字记录：测试过程中生成 query_10u.jtl，测试结束后生成 query_10u_report，其中包含 index.html 和 statistics.json。

回顾要点：HTML 报告通常在测试结束后才完整生成，重新生成报告时输出目录必须为空。

---

## 4. 本次 10 用户压测真实结果

数据来源：

~~~text
D:\app_other\myjmeter\results\query_10u_report\statistics.json
~~~

### 4.1 总体结果

| 指标 | 本次结果 |
|---|---:|
| 测试时长 | 约 180.823 秒 |
| Samples | 2111 |
| Error Count | 0 |
| Error % | 0% |
| Throughput | 11.67 req/s |
| Average | 790.64 ms |
| Median | 190 ms |
| P90 | 2760.8 ms |
| P95 | 3543.6 ms |
| P99 | 6300.32 ms |
| Max | 15246 ms |

### 4.2 按接口统计

| 请求 | Samples | Average | Median | P90 | P95 | P99 | Max | Error |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 03-当前用户 | 303 | 4.02 ms | 4 ms | 5 ms | 7 ms | 21.64 ms | 27 ms | 0 |
| 04-看板概览 | 303 | 1142.38 ms | 771 ms | 2391 ms | 3269.8 ms | 7253.8 ms | 11240 ms | 0 |
| 05-订单列表 | 303 | 223.70 ms | 177 ms | 308 ms | 510.8 ms | 1133.6 ms | 1772 ms | 0 |
| 06-订单详情 | 303 | 3422.70 ms | 2950 ms | 5075.4 ms | 6389.2 ms | 11510.92 ms | 15246 ms | 0 |
| 07-订单明细 | 293 | 129.17 ms | 97 ms | 178.2 ms | 326.3 ms | 811.7 ms | 1574 ms | 0 |
| 08-批次资源池 | 293 | 402.97 ms | 312 ms | 467.8 ms | 778.4 ms | 2526.06 ms | 4255 ms | 0 |
| 09-工艺路线 | 293 | 140.89 ms | 93 ms | 214.6 ms | 370.5 ms | 879.86 ms | 4704 ms | 0 |
| 01-验证码 | 10 | 238.10 ms | 29 ms | 1318.5 ms | 1380 ms | 1380 ms | 1380 ms | 0 |
| 02-登录 | 10 | 1724.60 ms | 1202.5 ms | 4887.3 ms | 5105 ms | 5105 ms | 5105 ms | 0 |

### 4.3 结果怎么读

初步结论：

1. 2111 个样本全部成功，错误率为 0%；
2. Average 为 790.64 ms，Median 只有 190 ms，说明少量很慢的请求拉高了平均值；
3. 06-获取订单详情是首要慢接口，Average 3422.7 ms，Max 15246 ms；
4. 04-获取看板概览是第二重点，Average 1142.38 ms，P99 7253.8 ms；
5. 登录只有 10 个样本，因为每个线程只登录一次，不能与循环查询接口直接比较；
6. 没有定义 SLA，所以不能仅凭当前数据判定通过或失败；
7. 目前只能确定“请求成功但存在明显长尾”，不能仅凭 JMeter 结果断言是 SQL、CPU、GC 或连接池导致。

优先排查：

~~~text
06 订单详情
→ 04 看板概览
→ 08 批次资源池
→ 与 Grafana 的数据库、JVM、CPU曲线对齐
~~~

### 文字记录：HTML 报告总览

文字记录：HTML Report Dashboard 用于查看总体 Samples、Error%、Average、Throughput 和 Apdex。

回顾要点：总体指标用于观察整体稳定性，接口级指标用于定位具体慢接口。

### 文字记录：HTML 统计表

文字记录：Statistics 表中重点查看 Total、04-看板概览和 06-订单详情的 Samples、Average、P95、P99、Max 和 Error。

回顾要点：06-订单详情是本次最慢接口，不能只看 Total 行。

---

## 5. JMeter HTML 报告英文词汇

| 英文                        | 中文        | 怎么理解             |
| ------------------------- | --------- | ---------------- |
| Samples                   | 样本数       | 实际完成的请求次数        |
| Error Count               | 错误数量      | 失败请求个数           |
| Error %                   | 错误率       | 错误数除以总样本数        |
| Average                   | 平均响应时间    | 所有请求耗时的平均值       |
| Median                    | 中位数       | 一半请求更快，一半请求更慢    |
| Min                       | 最小响应时间    | 最快请求耗时           |
| Max                       | 最大响应时间    | 最慢请求耗时           |
| 90th Percentile / P90     | 90 分位     | 90% 请求不超过该时间     |
| 95th Percentile / P95     | 95 分位     | 95% 请求不超过该时间     |
| 99th Percentile / P99     | 99 分位     | 99% 请求不超过该时间     |
| Throughput                | 吞吐量       | 单位时间完成的请求数       |
| Latency                   | 延迟        | 发出请求到开始收到响应的等待时间 |
| Connect Time              | 连接时间      | 建立网络连接所用时间       |
| Received KB/sec           | 接收速率      | 每秒收到的数据量         |
| Sent KB/sec               | 发送速率      | 每秒发送的数据量         |
| APDEX                     | 用户满意度指数   | 按响应时间阈值估算体验      |
| Response Time Over Time   | 响应时间随时间变化 | 看测试过程中是否越来越慢     |
| Active Threads Over Time  | 活跃线程随时间变化 | 看并发用户是否按计划启动     |
| Transactions per Second   | 每秒事务数     | 看吞吐量随时间变化        |
| Response Time Percentiles | 响应时间分位数   | 看 P90/P95/P99 曲线 |

本次 Average 为 790.64 ms，Median 为 190 ms，说明大多数请求不慢，但少数长尾请求很慢。不能只看 Average，至少同时看 Average、Median、P95、P99、Max。

06 接口的 P95=6389.2 ms、P99=11510.92 ms、Max=15246 ms，说明：

- 95% 的请求不超过约 6.39 秒；
- 仍有 5% 请求更慢；
- 最慢请求约 15.25 秒。

---

## 6. Grafana 的三层监控结构

~~~mermaid
flowchart TB
    A["JMeter：请求结果<br/>TPS、响应时间、错误率"]
    B["Spring Boot APM：应用层<br/>HTTP、Tomcat、HikariCP、日志"]
    C["JVM：进程层<br/>Heap、GC、线程、进程CPU"]
    D["Node Exporter：机器层<br/>CPU、内存、磁盘、网络、TCP"]
    A --> B
    B --> C
    C --> D
~~~

| 层级 | 主要回答的问题 |
|---|---|
| JMeter | 用户请求快不快、有没有错误 |
| Spring Boot APM | 哪类 HTTP 请求、Tomcat 或连接池异常 |
| JVM | Java 进程是否内存紧张、GC 频繁或线程增长 |
| Node Exporter | 操作系统 CPU、内存、磁盘、网络是否饱和 |

---

## 7. Spring Boot APM 指标

### 7.1 Basic Statistics

| 英文 | 中文 | 正常表现 | 需要警惕 |
|---|---|---|---|
| Uptime | 应用运行时间 | 持续增加 | 意外重启、频繁归零 |
| Start time | 启动时间 | 与 Uptime 基本对应 | 多实例或变量选错 |
| Heap Used | 堆内存使用 | 随请求波动，GC 后回落 | GC 后持续增长 |
| Non-Heap Used | 非堆内存使用 | 相对稳定 | Metaspace/Code Cache 持续增长 |
| Process Open Files | 打开文件数 | 稳定 | 接近上限或系统不支持 |
| System CPU Usage | 系统 CPU | 与主机负载相符 | 长期接近 100% |
| Process CPU Usage | Java 进程 CPU | 随业务请求升高 | Java 进程长期接近 100% |
| Load Average | 运行队列压力 | 与 CPU 核数相称 | 长期高于 CPU 核数 |

### 7.2 JVM Memory

| 英文 | 中文 | 正常表现 | 需要警惕 |
|---|---|---|---|
| G1 Eden Space | G1 伊甸区 | 上升后因 Young GC 下降 | 分配速度异常高 |
| G1 Old Gen | G1 老年代 | 相对稳定 | GC 后持续增长 |
| G1 Survivor Space | 幸存者区 | 短时波动 | 晋升异常、老年代同步增长 |
| CodeHeap | JIT 编译代码缓存 | 启动后趋稳 | 持续增长或空间不足 |
| Compressed Class Space | 压缩类指针空间 | 相对稳定 | 动态类加载异常 |
| Metaspace | 元空间 | 启动后趋稳 | 持续增长，怀疑类加载器泄漏 |
| Classes Loaded | 已加载类数 | 启动期增长，之后稳定 | 长期快速增长 |
| Classes Unloaded | 已卸载类数 | 偶尔波动 | 与类加载持续增长一起出现 |
| Direct Buffers | 直接堆外缓冲区 | 网络 I/O 时波动 | 堆外内存持续增长 |
| Mapped Buffers | 内存映射缓冲区 | 不使用时接近 0 | 大量增长且进程内存不足 |

### 7.3 Threads 和对象分配

| 英文 | 中文 | 分析方法 |
|---|---|---|
| Threads | JVM 活跃线程数 | 比较测试前后是否持续增长 |
| Allocated | 对象分配速率 | 高表示创建了很多临时对象 |
| Promoted | 晋升速率 | 高且 Old Gen 增长时关注老年代 |

### 7.4 GC

| 英文 | 中文 | 怎么判断 |
|---|---|---|
| GC Count | GC 次数 | 少量 Young GC 正常，频率持续升高需调查 |
| Young GC / Minor GC | 新生代 GC | 暂停短时通常可接受 |
| Old GC / Major GC | 老年代 GC | 频繁出现会严重影响响应时间 |
| Stop the World Duration | STW 暂停时长 | 与 JMeter P95/P99 同时间对照 |

关联判断：

~~~text
JMeter P99 突然升高
+
GC Stop the World 同时出现尖峰
→ 慢请求可能与 GC 暂停有关
~~~

---

## 8. HikariCP 数据库连接池

HikariCP 是 Spring Boot 常用的数据库连接池。

| 英文 | 中文 | 正常表现 | 需要警惕 |
|---|---|---|---|
| Active | 正在使用的连接 | 随请求升高后回落 | 长期接近 Max |
| Idle | 空闲连接 | 保留一定空闲量 | 长期为 0 且 Pending 增长 |
| Max | 最大连接数 | 配置上限 | Active 长期贴近上限 |
| Min | 最小空闲连接数 | 连接池保底连接数 | 频繁创建连接 |
| Pending | 等待连接的线程数 | 通常为 0 | 持续大于 0 |
| Connection Creation Time | 创建连接耗时 | 通常低且少发生 | 创建大量连接且变慢 |
| Connection Usage Time | 使用连接耗时 | 与 SQL 执行时间相关 | 长期变高 |
| Connection Acquire Time | 获取连接耗时 | 通常很低 | 连接池排队 |

最危险的组合：

~~~text
Active 接近 Max
Pending 持续大于 0
Acquire Time 上升
JMeter 响应时间同步上升
~~~

此时检查连接池大小、慢 SQL、事务范围和连接释放。

---

## 9. HTTP、Response Time 和 Tomcat

### 9.1 Request Count

Request Count 是请求数量或请求速率。图例中的 GET/POST 路径代表不同接口。

它可以回答：

- JMeter 是否真的压到了目标接口；
- 请求量是否符合预期；
- 某个接口是否突然停止；
- 不同接口调用比例是否合理。

### 9.2 Response Time N/A

Response Time 显示 N/A，不一定表示完全没有 HTTP 计时数据。当前面板可能依赖：

~~~text
http_server_requests_seconds_bucket
~~~

如果只采集 count、sum 等指标，没有 histogram bucket，某些 P95/P99 面板就无法计算。

application.yml 可以增加：

~~~yaml
management:
  metrics:
    distribution:
      percentiles-histogram:
        http.server.requests: true
      percentiles:
        http.server.requests: 0.5,0.9,0.95,0.99
~~~

重启后检查 /actuator/prometheus 是否出现 http_server_requests_seconds_bucket。

### 9.3 Tomcat N/A

~~~yaml
server:
  tomcat:
    mbeanregistry:
      enabled: true
~~~

常见 Tomcat 面板：

| 英文 | 中文 | 需要关注 |
|---|---|---|
| Current Threads | 当前线程数 | 当前工作线程 |
| Busy Threads | 忙碌线程数 | 正在处理请求的线程 |
| Max Threads | 最大线程数 | 线程池上限 |
| Active Sessions | 活跃会话数 | 会话量 |
| Error Count | 错误数 | 错误是否增加 |
| Sent Bytes | 发送字节数 | 响应流量 |
| Received Bytes | 接收字节数 | 请求流量 |

Busy Threads 长期接近 Max Threads 时，可能出现排队。

### 9.4 Logback

| 英文 | 中文 |
|---|---|
| ERROR | 错误 |
| WARN | 警告 |
| INFO | 普通运行信息 |
| DEBUG | 调试信息 |
| TRACE | 最详细的跟踪信息 |

正式测试前后比较 ERROR 数量差值，并按时间查看后端日志。

### 文字记录：SpringBoot APM 看板

文字记录：Spring Boot APM 看板用于同时观察 Basic Statistics、JVM、HikariCP、HTTP 和日志指标。

回顾要点：分析压测时必须确认 application、instance 和时间范围正确。

---

## 10. JVM 看板全部 N/A 的排查

如果 SpringBoot APM 已经显示 Heap、GC、线程，而单独的 JVM Micrometer 看板全部 N/A，优先怀疑 dashboard 查询问题，而不是 JVM 指标不存在。

常见原因：

| 原因 | 说明 |
|---|---|
| Data source 错误 | 模板引用了不存在的 Prometheus UID |
| 顶部变量为空 | application、job、instance 没选中 |
| 标签不匹配 | 面板查询的 application 标签实际不存在 |
| 模板版本不兼容 | 指标名、标签或 Micrometer 版本不同 |

进入：

~~~text
Explore / 探索
→ 选择 Prometheus
→ 执行查询
~~~

先验证：

~~~promql
jvm_memory_used_bytes
process_uptime_seconds
jvm_threads_live_threads
jvm_gc_pause_seconds_count
~~~

再查看标签：

~~~promql
count by (job, instance, application) (jvm_memory_used_bytes)
~~~

如果实际没有 application 标签，而 dashboard 查询：

~~~promql
jvm_memory_used_bytes{application=~"$application"}
~~~

结果可能为空。

Spring Boot 可以配置：

~~~yaml
spring:
  application:
    name: zhihuitong

management:
  metrics:
    tags:
      application: ${spring.application.name}
~~~

修改并重启后检查 /actuator/prometheus 是否出现 application 标签。

面板内检查路径：

~~~text
面板标题
→ 编辑
→ Query
→ Data source
→ Inspect / 检查
→ Query / 查询
~~~

不要使用显示为 ${DS_PROMETHEUS}、default、Mixed 或不存在 UID 的数据源。

### 文字记录：JVM 看板 N/A 与 Inspect

文字记录：JVM 看板部分面板显示 N/A 时，进入面板编辑并通过 Inspect → Query 查看实际 PromQL、Data source 和变量替换结果。

回顾要点：先验证 Prometheus 中 JVM 指标存在，再排查仪表板查询和数据源绑定。

### 文字记录：Grafana 数据源和变量

文字记录：在 Explore 中检查 application、job、instance 标签，在面板 Query 中检查 Data source 是否指向当前 Prometheus。

回顾要点：不要把真实 Token 或密码写入学习资料。

---

## 11. Node Exporter Full 指标

### 11.1 可能监控的不是 Windows 主机

Node Exporter 主要用于 Linux/Unix。如果 Spring Boot 运行在 Windows，而 Node Exporter 跑在 Docker Desktop、WSL 或 Linux 容器中，Grafana 显示的可能是 Docker/WSL Linux，而不是 Windows 主机。

查看 dashboard 顶部：

~~~text
job
instance
node
host
~~~

如果出现 node-exporter:9100 或 172.x.x.x:9100，要确认实际对应哪台机器。

Windows 主机通常需要 windows_exporter。不要把 Linux Node Exporter 曲线直接当作 Windows Java 主机 CPU 证据。

### 11.2 CPU

| 英文 | 中文 | 解释 |
|---|---|---|
| CPU Busy | CPU 繁忙率 | 非空闲 CPU 占比 |
| User | 用户态占用 | 应用程序占用 |
| System | 内核态占用 | 操作系统内核占用 |
| Idle | 空闲率 | 未使用 CPU |
| IOWait | 等待磁盘 I/O | CPU 在等磁盘 |
| IRQ | 硬件中断 | 设备产生的中断 |
| SoftIRQ | 软件中断 | 内核软件中断 |
| Steal | 被虚拟化宿主机抢占 | 虚拟机常见 |

判断：

~~~text
CPU Busy 高、IOWait 低
→ 主要是计算压力

CPU Busy 不高、IOWait 高
→ 主要在等待磁盘或数据库 I/O
~~~

### 11.3 Load Average

Load 1、Load 5、Load 15 表示最近 1、5、15 分钟的系统任务压力。

例如 4 核机器长期 Load 接近 4，表示比较繁忙；长期明显高于 4，说明任务可能排队。Windows 下该指标不一定适用，优先看可验证的 CPU 指标。

### 11.4 Memory

| 英文 | 中文 |
|---|---|
| RAM Total | 总物理内存 |
| RAM Used | 已用内存 |
| RAM Available | 可用内存 |
| Cache | 文件缓存 |
| Buffers | 内核缓冲 |
| Swap Used | 已用交换空间 |

不要只看 Used，更重要的是 Available 和 Swap Used。

危险组合：

~~~text
Available 接近 0
+
Swap 持续增加
+
JMeter 响应时间变慢
~~~

### 11.5 Disk

| 英文 | 中文 |
|---|---|
| Read Bytes | 每秒读取数据量 |
| Write Bytes | 每秒写入数据量 |
| Read IOPS | 每秒读操作数 |
| Write IOPS | 每秒写操作数 |
| I/O Time | 磁盘忙碌时间 |
| Utilization | 磁盘利用率 |
| Latency | 磁盘延迟 |
| Queue | 等待磁盘处理的请求队列 |

接口变慢时，如果 Disk Utilization、Disk Latency、IOWait 同时升高，才更像磁盘或数据库 I/O 瓶颈。

### 11.6 Filesystem

| 英文 | 中文 |
|---|---|
| Filesystem Size | 文件系统总容量 |
| Filesystem Used | 已用空间 |
| Filesystem Available | 可用空间 |
| Inodes Used | 已使用文件节点 |
| Read-only | 是否只读 |

磁盘还有空间但 inode 用尽时，同样无法创建文件。

### 11.7 Network 和 TCP

| 英文 | 中文 |
|---|---|
| Receive / RX | 接收流量 |
| Transmit / TX | 发送流量 |
| Packets | 数据包 |
| Errors | 网络错误 |
| Dropped | 丢弃数据包 |
| TCP Connections | TCP 连接数 |
| ESTABLISHED | 已建立连接 |
| TIME_WAIT | 等待连接关闭 |
| CLOSE_WAIT | 对端已关闭，本地尚未释放 |
| LISTEN | 正在监听 |
| SYN_SENT | 正在建立连接 |

CLOSE_WAIT 长期大量增长，可能表示应用没有正确关闭连接。TIME_WAIT 多不一定是故障，要结合短连接数量和端口耗尽判断。

### 11.8 Context Switches、Interrupts、File Descriptors

| 英文 | 中文 | 作用 |
|---|---|---|
| Context Switches | 上下文切换 | 线程/进程切换开销 |
| Interrupts | 中断 | 硬件或软件中断次数 |
| File Descriptors | 文件描述符 | 文件、连接、管道等资源句柄 |

当 CPU 高但吞吐量上不去时，再重点看上下文切换和中断。

File Descriptors 接近上限时，可能出现：

~~~text
Too many open files
~~~

### 文字记录：Node Exporter 看板

文字记录：Node Exporter Full 主要观察 CPU、Memory、Disk、Network、TCP 和顶部 instance。

回顾要点：Windows + Docker Desktop 环境下，先确认 Node Exporter 监控的是 Windows 主机还是 Docker/WSL Linux。

---

## 12. JMeter 与 Grafana 如何联合分析

| JMeter 现象 | Grafana 同时观察 | 可能方向 |
|---|---|---|
| Average、P95、P99 一起升高 | Process CPU、System CPU 升高 | CPU 或计算逻辑 |
| 响应变慢但 CPU 不高 | Hikari Active/Max、Pending、Acquire Time | 数据库连接池排队 |
| P99 尖峰与 GC 停顿同时出现 | Heap、Old Gen、GC Pause | JVM/GC |
| 请求量上升但 Tomcat Busy 接近 Max | Tomcat Threads | Web 线程池不足 |
| CPU 不高、IOWait、Disk Latency 高 | Node Exporter Disk | 磁盘或数据库 I/O |
| CLOSE_WAIT 持续增长 | TCP 连接状态 | 连接释放问题 |
| JMeter 错误率上升、Logback ERROR 增长 | ERROR 日志和后端日志 | 应用异常 |

只有在时间上同时发生、指标上相互印证时，才能把 Grafana 指标作为根因证据。单独看到某条曲线升高，不足以证明它就是瓶颈。

本次 06 订单详情是首要慢接口，下一步应把它的慢请求时间段与数据库连接池、JVM GC、Process CPU、Disk I/O、后端日志逐一对齐。

---

## 13. 操作文字索引

原来需要通过图片回顾的内容，已经全部改成了本篇和上一篇中的文字记录：

| 回顾内容 | 应查看的位置 |
|---|---|
| 端口错误和正确端口 | 上一篇“端口错误：5137、5173、8080”及“文字记录：端口错误的定位” |
| HTTP 默认值 | 上一篇“文字记录：HTTP 请求默认值” |
| 登录 JSON 和 Token | 上一篇“文字记录：登录请求 JSON”和“文字记录：Token 提取” |
| 01～09 请求顺序 | 上一篇“文字记录：完整查询链”及变量传递表 |
| 生产计划 500 | 上一篇“文字记录：生产计划 500 错误与后端日志” |
| JDBC 和清理 | 上一篇“文字记录：JDBC 连接配置”“清理线程组层级”“完整脚本执行结果” |
| 查询压测参数 | 本篇“文字记录：查询压测线程组”和“文字记录：Once Only Controller” |
| 非 GUI 执行 | 本篇“文字记录：CMD 非 GUI 运行”和“JTL 和 HTML 报告目录” |
| HTML 报告 | 本篇“HTML 报告总览”和“HTML 统计表” |
| Grafana 看板 | 本篇“SpringBoot APM 看板”“JVM 看板 N/A 与 Inspect”“Node Exporter 看板” |

因此不再需要准备或插入截图；操作路径、界面名称、关键配置和回顾重点都直接写在文字中。

---

## 14. 本次测试的谨慎结论

本次测试结果：

~~~text
2111 个样本
0 个错误
11.67 req/s
平均响应时间 790.64 ms
P95 3543.6 ms
P99 6300.32 ms
~~~

可以确认：

- 脚本链路能够稳定完成；
- 本次没有 HTTP 错误；
- 06 订单详情存在明显性能问题；
- 04 看板概览也有明显长尾；
- 整体平均值被少量慢请求拉高。

暂时不能确认：

- 慢接口一定是 SQL 慢；
- 一定是 CPU 不足；
- 一定是 JVM GC；
- 一定是 HikariCP 连接池不足；
- 一定满足业务 SLA。

下一次优化实验要保持用户数、持续时间、脚本数据范围和监控时间窗口一致，再比较 Average、P95、P99、Throughput、Error %，并同步核对 Grafana。

---

## 15. 后续聊天中的第二轮基线与 Grafana 排查记录

### 15.1 第二轮 10 用户基线结果

聊天记录中后来又完成了一轮 10 用户、持续约 180 秒的查询基线测试。这一轮与本地 query_10u.jtl 中的 2111 个样本不是同一份结果，因此单独记录，不能直接相加或覆盖前面的数据。

~~~text
并发用户：10
持续时间：约 180 秒
总请求数：7083
错误数：0
错误率：0.00%
总体吞吐量：39.29 次/秒
总体 Apdex：0.933
~~~

接口结果：

| 接口 | 平均响应时间 | P95 | P99 | 其他重点数据 |
|---|---:|---:|---:|---|
| 03-获取当前用户 | 4.06 ms | 5 ms | 8 ms | 响应稳定 |
| 04-获取看板概述 | 299.34 ms | 350.30 ms | 373 ms | 大部分请求低于 400 ms |
| 05-获取订单列表 | 72.55 ms | 90 ms | 94 ms | 响应较快 |
| 06-获取订单详情 | 1055.68 ms | 1181 ms | 1207.88 ms | 中位数 1133 ms，最大 1239 ms，Apdex 0.531 |
| 07-获取订单明细列表 | 45.38 ms | 59 ms | 65 ms | 响应较快 |
| 08-获取批次资源池 | 124.91 ms | 153 ms | 169 ms | 基本稳定 |
| 09-获取可用工艺路线 | 42.53 ms | 57 ms | 61 ms | 响应较快 |

这轮数据说明：

- 06-获取订单详情不是偶发一两个慢请求；
- 平均值约 1056 ms、中位数约 1133 ms、P95 约 1181 ms，说明至少一半请求都在 1 秒以上；
- 06 接口属于持续性的接口级响应延迟，而不是偶发抖动；
- 总体 P95 被 06 接口的大量慢请求拉高；
- 总体数据适合观察吞吐量和错误率，接口数据适合定位具体问题。

可能的定位方向：

- SQL 较复杂或缺少索引；
- 查询多张关联表；
- 存在循环查询或类似 N+1 查询；
- 接口内部进行了较多数据组装；
- 返回数据序列化耗时较高；
- 接口内部存在固定等待或其他业务调用。

这些只是排查方向，不能仅凭 JMeter 报告确定具体根因。

### 15.2 第二轮 Grafana 监控结论

聊天中观察到的服务端指标：

~~~text
Heap 使用率：约 1.5%～1.76%
Non-Heap 使用率：约 9%～9.11%
JVM 进程 CPU：约 5%～6%，整体较低
线程数：基本稳定
GC Pressure：接近 0%
Minor GC：毫秒级
5xx 错误：没有明显增加
~~~

因此目前没有证据表明系统受到以下资源限制：

~~~text
JVM 堆内存不足
频繁 Full GC
线程大量堆积
JVM 进程 CPU 达到瓶颈
~~~

系统 CPU 曾出现约 50% 以上的尖峰，但 JMeter、浏览器、Docker、Prometheus 和后端可能运行在同一台电脑上，不能把全部 System CPU 都算到 Spring Boot。判断后端 CPU 时，优先看 Process CPU Usage。

### 15.3 JVM 看板实际排查顺序

这次 JVM 看板排查不能一上来就修改几十个面板，正确顺序是先证明数据存在，再定位变量、查询和仪表板配置。

开始排查前先固定看板上下文：

~~~text
仪表板：JVM (Micrometer) 或 JVM (Micrometer) - 修复版
Application：zhihuitong
Instance：host.docker.internal:8080
时间范围：最近 15 分钟
自动刷新：5 秒或 10 秒
~~~

如果时间范围没有覆盖应用启动和 Prometheus 抓取时间，或者 Instance 选成了其他目标，后面的 N/A 判断都没有意义。

#### 第一步：用 up 判断 Prometheus 目标

在 Grafana 的 Explore / 探索中执行：

~~~promql
up
~~~

这次看到的目标包括：

| job | instance | 含义 |
|---|---|---|
| springboot | host.docker.internal:8080 | Spring Boot 后端 |
| node | node-exporter:9100 | Node Exporter 所在环境 |
| prometheus | prometheus:9090 | Prometheus 自身 |

up 的值：

- 1：最近一次抓取成功；
- 0：最近一次抓取失败。

曾经看到 Spring Boot 目标短暂变成 0，可能与应用重启、端口暂时不可用或抓取超时有关。这个判断需要结合后端启动日志，不能直接当作 JVM 看板问题。

#### 第二步：确认 Spring Boot 真的有 JVM 指标

~~~promql
count by (__name__) (
  {job="springboot", __name__=~"jvm_.*"}
)
~~~

结果中出现过：

~~~text
jvm_memory_used_bytes
jvm_memory_max_bytes
jvm_memory_committed_bytes
jvm_threads_live_threads
jvm_gc_pause_seconds_count
jvm_classes_loaded_classes
jvm_buffer_memory_used_bytes
~~~

这一步证明 Spring Boot 和 Prometheus 都正常，不能再把 N/A 简单归因于“没有 JVM 数据”。

#### 第三步：确认指标的标签

~~~promql
count by (job, instance, application) (
  jvm_memory_used_bytes{job="springboot"}
)
~~~

实际标签中存在：

~~~text
job="springboot"
instance="host.docker.internal:8080"
application="zhihuitong"
~~~

因此 application 标签缺失也被排除了。

#### 第四步：检查 application 变量，不要误改示例正则

变量 application 的实际配置应记录为：

~~~text
数据源：prometheus
Query type：Label values
Label：application
Metric：留空
正则表达式：留空
预览值：zhihuitong
~~~

曾经看到过：

~~~text
/.*-(?<text>.*)-(?<value>.*)-.*/
~~~

这只是旧模板中的正则写法，不适合只有 zhihuitong 一个简单值的项目。清空后预览值仍为 zhihuitong，变量才不会被错误拆分。

这里需要特别纠正一个容易误导的说法：这次打开变量配置页面时，页面实际没有显示 `Multi-value` 或 `Include All option`，所以没有“关闭这两个选项”这一步，也没有对不存在的开关做任何修改。之前把它们写成排查步骤，是把 Grafana 的通用配置项误套到了当前页面。实际处理的是清空不适用的 `Regex`，并确认预览值为 `zhihuitong`。

#### 第五步：用 Uptime 面板区分“数据问题”和“变量问题”

原 Uptime 查询类似：

~~~promql
process_uptime_seconds{
  application="$application",
  instance="$instance"
}
~~~

面板显示 N/A 时，先把变量临时替换为固定值：

~~~promql
process_uptime_seconds{
  application="zhihuitong",
  instance="host.docker.internal:8080"
}
~~~

固定值查询返回约 10.2 mins，说明：

- process_uptime_seconds 指标存在；
- Prometheus 数据正常；
- application 和 instance 的真实值正确；
- 原问题位于变量传递、面板初始化或数据源引用，而不是 JVM 本身。

之后再恢复为单选变量的精确匹配：

~~~promql
process_uptime_seconds{
  application="$application",
  instance="$instance"
}
~~~

#### 第六步：用 Start time 验证变量替换

Start time 使用：

~~~promql
process_start_time_seconds{
  application="$application",
  instance="$instance"
} * 1000
~~~

面板后来显示了真实启动时间，例如 2026-08-03 20:19:40。这证明 application 和 instance 已经可以正确替换，不能继续把所有 N/A 都归因于变量。

#### 第七步：再处理面板刷新和初始化

曾经出现的现象是：

~~~text
仪表板刚打开：多个面板 N/A
进入某个面板编辑并退出：该面板出现数据
~~~

进入编辑器会强制该面板重新初始化并执行查询，因此它可以暂时显示数据，但这不是正确的长期修复方案。

可用于临时重新触发查询的动作：

~~~text
退出仪表板编辑模式
→ 切换 Application 或 Instance 后再切回
→ 或临时切换时间范围
→ Ctrl + F5 强制刷新
→ 等待 Prometheus 新一轮抓取
~~~

最终仍应导出完整仪表板 JSON，批量检查 Data source、PromQL、变量、schemaVersion 和 panel pluginVersion，而不是逐个点击所有面板。

### 15.4 先排除时间不同步

用于检查 Prometheus 最新采样时间的 PromQL：

~~~promql
time() - timestamp(up{job="springboot"})
~~~

这次结果约为 2.105 秒，说明 Prometheus 当前时间与 Spring Boot 最近一次采集时间只差约 2 秒，时间同步不是 JVM 面板 N/A 的主要原因。

### 15.5 堆内存面板的正确计算

实际查到的原始数据约为：

~~~text
jvm_memory_used_bytes：72,073,200 字节
jvm_memory_max_bytes：4,097,835,006 字节
~~~

正确计算：

~~~text
堆使用率 = 已使用堆内存 ÷ 最大堆内存 × 100%
结果约为 1.76%
~~~

如果只查询 jvm_memory_max_bytes，却把面板单位设置为百分比，Grafana 可能把 4,097,835,006 字节错误显示成 4097835006.00%。这不是实际使用率，而是面板单位配置与原始数据类型不匹配。

单选 application 和 instance 变量时，推荐使用精确匹配：

~~~promql
100 *
sum(
  jvm_memory_used_bytes{
    application="$application",
    instance="$instance",
    area="heap"
  }
)
/
sum(
  jvm_memory_max_bytes{
    application="$application",
    instance="$instance",
    area="heap"
  }
)
~~~

### 15.6 为什么不能盲目使用 regex 变量

曾经尝试过：

~~~promql
application=~"${application:regex}"
instance=~"${instance:regex}"
~~~

随后出现：

~~~text
unknown escape sequence U+002E '.'
~~~

原因是 Grafana 的 regex 格式化会把 host.docker.internal 中的点转成带反斜杠的形式，而 PromQL 字符串中不能直接使用这种转义。

结论：

- 这次实际使用的是单值变量，因此使用 `=` 和普通变量即可；
- 这次变量页面没有显示 `Multi-value` 或 `Include All option`，本次排查不涉及这些选项；
- `=~` 只是在确实需要匹配多个值时的 PromQL 通用写法，不能因为看起来更通用，就给当前单值变量强行加 `${变量:regex}` 格式化。

### 15.7 JVM 看板 N/A 的真实排查结论

排查过程中已经确认：

- Prometheus 的 up 指标正常；
- job=springboot、instance=host.docker.internal:8080 存在；
- jvm_memory_used_bytes、jvm_memory_max_bytes 等 JVM 指标存在；
- application=zhihuitong 标签存在；
- 固定值 PromQL 可以返回数据；
- 单独进入面板编辑后，面板会重新初始化并显示数据。

最终发现导入的 JVM 仪表板中有大量面板仍然引用：

~~~text
${DS_PROMETHEUS}
~~~

聊天中统计到约 48 处。这是一个数据源占位符，但当前仪表板没有定义名为 DS_PROMETHEUS 的有效数据源变量；application 和 instance 变量却绑定到了当前 Prometheus 数据源。

当时当前环境中变量实际指向的 Prometheus 数据源 UID 是 bftvbu0rcevpcf。这个 UID 只属于当前 Grafana 环境，不能机械复制到其他电脑或其他 Grafana 实例；迁移仪表板时应重新选择当前有效的 Prometheus 数据源。

所以现象是：

~~~text
仪表板首次打开
→ 部分面板无法解析数据源占位符或没有完成初始化
→ 显示 N/A
→ 进入面板编辑
→ Grafana 重新初始化并执行查询
→ 面板暂时出现数据
~~~

这不是 JVM 指标消失，也不是 Prometheus 没采集。最终真正解决问题的动作是：修改导出的仪表板 JSON 代码，把面板里无效的数据源占位符改成当前有效的 Prometheus 数据源引用，然后将修改后的 JSON 重新导入 Grafana。

#### 最终修复：修改 JSON 代码，而不是逐个面板手动修复

下面是这次实际处理的完整逻辑。

1. **先保留原看板，不直接覆盖。**

   原来的 JVM 看板先保留，避免 JSON 修改错误后无法回退。修复后的看板使用了新的标题：

   ~~~text
   JVM (Micrometer) - 修复版
   ~~~

2. **打开 Grafana 的仪表板 JSON。**

   不同 Grafana 版本的入口文字可能略有差别，通常在以下路径之一：

   ~~~text
   仪表板
   → 打开 JVM 看板
   → 设置 / Dashboard settings
   → JSON Model
   ~~~

   或者：

   ~~~text
   仪表板
   → 导出 / Export
   → 下载或复制完整 JSON
   ~~~

   这里必须拿到完整看板 JSON，而不是只复制某一个面板的 PromQL。因为问题分布在多个面板的数据源配置中。

3. **在 JSON 中搜索错误的数据源占位符。**

   使用编辑器的搜索功能查找：

   ~~~text
   ${DS_PROMETHEUS}
   ~~~

   当时统计到大约 48 处。它表示“请使用名为 DS_PROMETHEUS 的数据源变量”，但这份看板中并没有定义一个有效的 `DS_PROMETHEUS` 变量。与此同时，`application` 和 `instance` 变量却已经绑定到了当前可用的 Prometheus 数据源，因此才会出现“变量能查到值，但部分面板 N/A”的矛盾现象。

4. **只修改数据源引用，不改业务查询。**

   JSON 中的具体字段可能因 Grafana 版本不同而表现为 `name` 或 `uid`，但修改原则相同：把无效的 `${DS_PROMETHEUS}` 改为当前 Grafana 中真实存在的 Prometheus 数据源引用。

   结构示意如下：

   修改前，面板类似这样引用未解析的数据源变量：

   ~~~json
   {
     "datasource": {
       "type": "prometheus",
       "name": "${DS_PROMETHEUS}"
     }
   }
   ~~~

   修改后，面板应绑定当前 Grafana 中真实存在的 Prometheus 数据源。具体字段以导出的 JSON 为准：

   ~~~json
   {
     "datasource": {
       "type": "prometheus",
       "uid": "当前 Grafana 中 Prometheus 数据源的 UID"
     }
   }
   ~~~

   这次环境中实际看到的 Prometheus 数据源 UID 是：

   ~~~text
   bftvbu0rcevpcf
   ~~~

   这个 UID 只属于当时这台 Grafana，换到其他电脑、其他 Grafana 实例或重新创建数据源后可能不同。因此学习时不要死记这个 UID；迁移看板时应在目标 Grafana 中重新选择 Prometheus 数据源，或者先查出目标环境的 UID。

   修改时保留以下内容不动：

   - 每个面板原有的 PromQL；
   - `application` 和 `instance` 变量的定义；
   - 面板标题、布局、单位、阈值和图例；
   - `schemaVersion`、面板类型和其他插件配置。

   也就是说，这一步不是重新编写 JVM 查询，更不是删除 N/A 面板，而是修正面板“去哪个数据源查询”的配置。

5. **保存修改后的 JSON，并重新导入为新看板。**

   实际操作顺序可以记录为：

   ~~~text
   Grafana
   → 仪表板
   → 新建
   → 导入
   → 上传或粘贴修改后的完整 JSON
   → 选择当前 Prometheus 数据源（如果页面要求选择）
   → 完成导入
   ~~~

   导入后打开 `JVM (Micrometer) - 修复版`，设置：

   ~~~text
   Application：zhihuitong
   Instance：host.docker.internal:8080
   时间范围：最近 15 分钟
   ~~~

6. **验证修复结果。**

   修复后不需要再进入几十个面板逐个编辑。直接刷新看板，检查 Heap、Non-Heap、GC、Threads、Metaspace 等面板是否能正常执行查询；再进入某个面板的 `Query` / `Data source` 查看它是否已经指向有效 Prometheus 数据源。

   如果修复后仍有 `I/O Overview`、`Tomcat Threads`、`Jetty Threads` 等少数面板 N/A，应单独检查这些面板依赖的指标是否真的被当前 Windows 环境和 Spring Boot 暴露。它们可能是“对应指标不存在”，不再等同于整张 JVM 看板的数据源配置错误。

#### 为什么“进入编辑再退出”会暂时有效？

当时观察到：看板刚打开时很多面板是 N/A，进入某一个面板的编辑页面再退出，该面板暂时出现数据。编辑页面会促使 Grafana 重新解析数据源、重新替换变量并重新执行查询，所以它能掩盖初始化问题；但它没有修复 JSON 中的错误引用。刷新页面或重新打开看板后，问题仍可能回来。

因此，最终应记住这条排查结论：

> 编辑面板后暂时有数据，只能说明“重新初始化后查询成功”，不能说明看板配置已经修好。真正的修复是找到导出 JSON 中的 `${DS_PROMETHEUS}`，将其批量改为有效的 Prometheus 数据源引用，再导入修复版看板。

面板排查路径：

~~~text
面板标题
→ 编辑
→ Query
→ Data source
→ Inspect / 检查
→ Query / 查询
~~~

### 15.8 哪些 N/A 可以接受

I/O Overview 在 Windows 环境中可能没有对应的进程磁盘 I/O 指标，显示 N/A 不一定代表故障。

同理，Tomcat Threads、Jetty Threads 等面板在当前应用没有暴露对应指标时也可能显示 N/A。先到 /actuator/prometheus 搜索对应指标名；确认指标根本不存在后，应记录为“当前环境不提供”，不要为了消除 N/A 虚构数据。

Grafana 中 Errors 显示无数据，也可能表示当前查询时间范围内没有 5xx 错误，不一定是监控坏了。应结合 Prometheus 查询、Spring Boot 日志和 JMeter Error % 判断。

---

## 16. 最终复盘清单

- [ ] 查询脚本没有启用 10～14 写入接口；
- [ ] 01、02 放在 Once Only Controller；
- [ ] 线程数、Ramp-Up、Duration 已保存到 JMX；
- [ ] 正式运行关闭 View Results Tree；
- [ ] JTL 和 HTML 报告路径已记录；
- [ ] 报告目录为空或不存在后再生成；
- [ ] 登录 10 个样本没有与循环查询样本直接比较；
- [ ] 同时观察 Average、Median、P95、P99、Max；
- [ ] Grafana 时间范围覆盖测试时间；
- [ ] Grafana Data source 和 instance 正确；
- [ ] JVM N/A 先查 PromQL、变量和标签；
- [ ] Response Time N/A 先查 histogram bucket；
- [ ] Tomcat N/A 先查 MBean Registry；
- [ ] Node Exporter 确认监控的是目标机器；
- [ ] 用 JMeter 定位现象，用 Grafana 和日志寻找原因；
- [ ] 没有 SLA 时不直接写“测试通过”。

---

## 17. 这次学习内容对应实际工作

这次学习的内容并不只是“会操作 JMeter”，而是覆盖了测试岗位中常见的一条完整链路：

| 学习内容 | 工作中的对应任务 |
|---|---|
| 织慧通业务链 | 阅读需求并设计真实业务流程 |
| JMeter HTTP 请求 | 接口功能测试、接口自动化、性能测试 |
| Token 和 JSONPath | 登录鉴权、接口关联、测试数据传递 |
| SQL 和 JDBC | 校验数据库结果、准备和清理测试数据 |
| 后端日志 | 根据异常堆栈定位问题归属 |
| Prometheus 和 Grafana | 观察应用和服务器资源，分析性能瓶颈 |
| JMeter HTML 报告 | 输出测试结果和性能基线 |

以后工作中经常会遇到：

~~~text
功能测试
→ 接口测试
→ SQL 和日志分析
→ 接口自动化
→ Linux、Docker、Git、Jenkins
→ 性能测试
→ 测试开发或质量平台
~~~

目前最值得继续掌握的核心指标是：

~~~text
响应时间
P95/P99
吞吐量
错误率
CPU
内存
GC
线程
数据库连接池
~~~

暂时不需要为了学习而研究所有 JVM 面板。能做到“发现接口变慢、拿出数据、结合监控判断方向、写出清晰结论”，就已经是一次完整的性能测试能力。

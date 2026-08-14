# JMeter 实战（一）——织慧通完整业务链与数据清理

> 面向零基础学习者，记录织慧通项目从接口链路、变量传递到测试数据清理的完整过程。  
> 配套笔记：[[JMeter实战（二）——性能报告与Grafana指标解读]]、[[prometheus + Grafana]]

---

## 1. 先理解：这次到底做了什么

一个可重复的性能脚本必须同时解决：

1. 请求发到正确的端口；
2. 登录成功后自动提取 Token；
3. 前一步返回的订单、批次、路线 ID 能传给后一步；
4. 写入测试数据后能够自动清理；
5. 清理结束后还能查询数据库，确认残留数量为 0。

本次脚本的主流程：

~~~mermaid
flowchart LR
    A["01 验证码"] --> B["02 登录"]
    B --> C["提取 token"]
    C --> D["03 当前用户"]
    D --> E["04 看板概览"]
    E --> F["05 订单列表"]
    F --> G["提取 orderId"]
    G --> H["06 订单详情"]
    H --> I["07 订单明细"]
    I --> J["08 批次资源池"]
    J --> K["09 工艺路线"]
    K --> L["10-14 创建测试数据"]
    L --> M["15 调用清理存储过程"]
    M --> N["16 查询残留数量并断言"]
~~~

本地文件：

~~~text
完整脚本：
D:\app_other\myjmeter\ceshi\zhihuitong.jmx

查询性能脚本：
D:\app_other\myjmeter\ceshi\zhihuitong_查询性能测试.jmx
~~~

---

## 2. JMeter、Prometheus、Grafana 分别做什么

| 工具 | 负责什么 | 不负责什么 |
|---|---|---|
| JMeter | 模拟用户、调用接口、记录响应时间和错误 | 不负责长期保存 CPU/JVM 曲线 |
| Prometheus | 抓取并保存时间序列指标 | 不负责绘制漂亮的图表 |
| Grafana | 查询 Prometheus 并绘图 | 不主动给 Spring Boot 施压 |

老师课程中出现的工具也需要知道：

| 工具                           | 含义                           |
| ---------------------------- | ---------------------------- |
| Badboy                       | 较早的浏览器操作录制工具                 |
| ServerAgent                  | 较早的主机资源采集代理                  |
| PerfMon                      | 依赖 ServerAgent 的 JMeter 监控插件 |
| HTTP(S) Test Script Recorder | JMeter 自带的 HTTP 录制器          |

当前项目更适合使用：

~~~text
JMeter：产生压力
Spring Boot Actuator/Micrometer：暴露应用指标
Prometheus：采集指标
Grafana：展示指标
~~~

旧版 PerfMon/ServerAgent 出现 EXCEPTION_ACCESS_VIOLATION 时，优先理解为工具兼容性问题，不要和 HTTP 接口连接失败混为一谈。

---

## 3. 端口错误：5137、5173、8080

### 3.1 报错的含义

~~~text
Connect to localhost:5137 failed: Connection refused
~~~

Connection refused 表示：

> JMeter 找到了 localhost，但 5137 端口没有程序监听。

这是 TCP 连接阶段失败，不是后端业务代码返回的 4xx/5xx。

### 3.2 三个端口的关系

| 端口 | 对应程序 | 本次是否作为 JMeter 后端目标 |
|---|---|---|
| 5137 | 错误填写的端口 | 否 |
| 5173 | Vite 前端开发服务器 | 一般不作为后端接口压测目标 |
| 8080 | Spring Boot 后端 | 是 |

当前脚本变量：

~~~text
protocol = http
host = localhost
port = 8080
apiPrefix = 空
~~~

最终请求类似：

~~~text
http://localhost:8080/auth/login
http://localhost:8080/api/orders
~~~

PowerShell 检查端口：

~~~powershell
Test-NetConnection localhost -Port 8080
~~~

浏览器也可以访问：

~~~text
http://localhost:8080/actuator/prometheus
~~~

### 文字记录：端口错误的定位

文字记录：JMeter 中 Port 错误填写为 5137，View Results Tree 中出现 Connection refused。

操作路径：

~~~text
选中 HTTP Request
→ 查看 Server Name or IP、Port
→ View Results Tree
→ 查看错误
~~~

回顾要点：确认错误端口是 5137，正确后端端口是 8080。

---

## 4. HTTP 请求默认值和变量

### 4.1 用户定义的变量

| 变量 | 作用 | 当前值或说明 |
|---|---|---|
| protocol | 请求协议 | http |
| host | 后端地址 | localhost |
| port | 后端端口 | 8080 |
| apiPrefix | 接口统一前缀 | 空 |
| username | 登录名 | 笔记不记录真实值 |
| password | 登录密码 | 笔记不记录真实值 |
| connectTimeout | 建立连接超时 | 5000 ms |
| responseTimeout | 响应等待超时 | 30000 ms |

真实密码、Token、验证码不写入笔记。

### 4.2 HTTP Request Defaults

公共配置：

~~~text
Protocol：${protocol}
Server Name or IP：${host}
Port Number：${port}
~~~

配置了默认值后，子请求通常只填写 Method 和 Path。

最容易犯的错误是把 $、${token} 或 JSONPath 填进 Server Name or IP。这样 JMeter 会把它当成主机名，报：

~~~text
UnknownHostException: ($)
~~~

UnknownHostException 的意思是“无法解析主机名”。这时不要先改 DNS，先检查请求字段是否放错位置。

### 文字记录：HTTP 请求默认值

文字记录：HTTP Request Defaults 中填写 Protocol=http、Server Name or IP=localhost、Port Number=8080。

回顾要点：子请求只填写 Method 和 Path，不能把 $ 或变量误填到 Server Name or IP。

---

## 5. 01～09：登录和查询链路

### 5.1 01-获取验证码

~~~text
GET ${apiPrefix}/auth/captcha
~~~

响应关键结构：

~~~json
{
  "data": {
    "uuid": "验证码唯一标识"
  }
}
~~~

JSON Extractor：

~~~text
Reference Name：captchaUuid
JSONPath Expressions：$.data.uuid
~~~

JSONPath 中：

- $：JSON 根节点；
- .data：进入 data 对象；
- .uuid：取得 uuid 字段。

### 5.2 02-用户登录

~~~text
POST ${apiPrefix}/auth/login
~~~

Body Data：

~~~json
{
  "username": "${username}",
  "password": "${password}"
}
~~~

Header Manager：

~~~text
Accept: application/json
Content-Type: application/json
~~~

415 Unsupported Media Type 表示服务端不接受当前请求体格式。常见原因是 JSON 放在 Parameters，或者没有设置 Content-Type。

登录成功后提取：

~~~text
token：$.data.token
expiresIn：$.data.expiresIn
~~~

后续请求的认证头：

~~~text
Authorization: Bearer ${token}
~~~

Bearer 表示“携带这个 Token 访问”，Bearer 和 Token 之间要有空格。

401 Unauthorized 表示身份认证失败。检查登录响应、JSON Extractor 层级、JSONPath 和 Authorization Header。

### 文字记录：登录请求 JSON

文字记录：02-用户登录使用 POST，JSON 放在 Body Data，Header Manager 配置 Accept 和 Content-Type，响应返回 data.token。

回顾要点：请求体必须是合法 JSON，Content-Type 必须是 application/json，真实密码和 Token 不记录。

### 文字记录：Token 提取

文字记录：在 02-用户登录下面添加 JSON Extractor，Reference Name 为 token，JSONPath 为 $.data.token。

回顾要点：提取器必须挂在登录请求下面，后续请求使用 Authorization: Bearer ${token}。

### 5.3 03-获取当前用户

~~~text
GET ${apiPrefix}/auth/me
Authorization: Bearer ${token}
~~~

作用：验证登录 Token 可用。

### 5.4 04-获取看板概览

~~~text
GET ${apiPrefix}/api/dashboard/overview
Authorization: Bearer ${token}
~~~

作用：模拟用户进入首页后加载看板。

### 5.5 05-获取订单列表

~~~text
GET ${apiPrefix}/api/orders
Authorization: Bearer ${token}
~~~

提取第一条订单：

~~~text
Reference Name：orderId
JSONPath：$.rows[0].orderId
~~~

[0] 代表数组中的第一项，前提是 rows 至少有一条数据。

### 5.6 06-获取订单详情

~~~text
GET ${apiPrefix}/api/orders/${orderId}
Authorization: Bearer ${token}
~~~

### 5.7 07-获取订单明细列表

~~~text
GET ${apiPrefix}/api/orders/${orderId}/items
Authorization: Bearer ${token}
~~~

提取：

~~~text
Reference Name：orderItemId
JSONPath：$.data[0].orderItemId
~~~

### 5.8 08-获取批次资源池

~~~text
GET ${apiPrefix}/api/batches/resource-pool
Authorization: Bearer ${token}
~~~

提取：

~~~text
Reference Name：batchId
JSONPath：$.rows[0].batchId
~~~

### 5.9 09-获取可用工艺路线

~~~text
GET ${apiPrefix}/api/process-routes
Authorization: Bearer ${token}
~~~

按路线名提取 routeId：

~~~text
$.rows[?(@.routeName == '锦棉功能整理路线')].routeId
~~~

问号条件表示“只保留 routeName 符合条件的数组项”。

### 5.10 变量传递表

| 产生步骤 | 变量 | JSONPath 或来源 | 使用步骤 |
|---|---|---|---|
| 01 验证码 | captchaUuid | $.data.uuid | 登录或校验 |
| 02 登录 | token | $.data.token | 03～14 |
| 02 登录 | expiresIn | $.data.expiresIn | 有效期记录 |
| 05 订单列表 | orderId | $.rows[0].orderId | 06、07 |
| 07 订单明细 | orderItemId | $.data[0].orderItemId | 12、13 |
| 08 批次池 | batchId | $.rows[0].batchId | 12、13 |
| 09 工艺路线 | routeId | 按路线名筛选 | 13 |
| 10 创建订单 | testOrderId | $.data.orderId | 11～14、清理 |
| 11 创建明细 | testOrderItemId | $.data.orderItemId | 12、清理 |
| 12 分配批次 | testLinkId | $.data.linkId | 清理 |
| 13 创建计划 | testPlanId | $.data.planId | 14、清理 |

### 文字记录：完整查询链

文字记录：请求顺序为验证码、登录、当前用户、看板、订单列表、订单详情、订单明细、批次资源池、工艺路线。

回顾要点：每个后续请求都依赖前一步提取出的变量，尤其是 token、orderId、batchId 和 routeId。

---

## 6. 10～14：创建隔离的测试数据

写入接口会修改数据库，不能直接使用真实订单。当前脚本使用 JM- 前缀和 JMETER_TEST 标记。

### 6.1 10-创建测试订单

~~~json
{
  "orderNo": "JM-${__time(yyyyMMddHHmmss,)}-${__threadNum}",
  "customerName": "JMeter性能测试客户",
  "priority": "NORMAL",
  "status": "NEW",
  "remark": "JMETER_TEST"
}
~~~

${__time(...)} 生成时间，${__threadNum} 表示当前线程号。

### 6.2 11-创建测试订单明细

~~~text
POST ${apiPrefix}/api/orders/${testOrderId}/items
~~~

使用 JM-P- 商品编码和 JMETER_TEST 标记。

### 6.3 12-测试订单分配批次

~~~json
{
  "orderItemId": ${testOrderItemId},
  "batchId": ${batchId},
  "allocatedQuantity": 10,
  "allocatedWeight": 10,
  "remark": "JMETER_TEST"
}
~~~

数字 ID 不要加引号，字符串字段要加引号。

### 6.4 13-创建生产计划

~~~json
{
  "orderId": ${testOrderId},
  "orderItemId": ${testOrderItemId},
  "batchId": ${batchId},
  "routeId": ${routeId},
  "planStartTime": "测试开始时间",
  "planEndTime": "测试结束时间",
  "remark": "JMETER_TEST"
}
~~~

### 6.5 14-获取生产计划甘特图

请求：

~~~text
GET ${apiPrefix}/api/production-plans/${testPlanId}/gantt
Authorization: Bearer ${token}
~~~

这一步使用 13-创建生产计划返回的 testPlanId，查询该生产计划的甘特图数据。它是写入业务链之后的查询验证步骤，不会再次创建数据。

文字记录：13 成功提取 testPlanId 后，14 将它放到 URL 路径中；如果 testPlanId 没有提取成功，URL 会出现空值或字面变量，应该先回到 13 的响应和 JSON Extractor 排查。

### 6.6 500 错误的真实原因

后端日志出现：

~~~text
Field 'deptId' doesn't have a default value
~~~

意思是数据库的 deptId 字段必填，但插入时没有值，也没有默认值。

真实链路：

~~~text
JMeter 请求
→ Controller
→ Service
→ INSERT productionplan
→ 数据库拒绝
→ HTTP 500
~~~

这通常应修复后端插入逻辑或数据库设计，不要为了让 JMeter 通过而随意伪造 deptId、createdBy 等用户归属字段。更合理的做法是后端从登录用户上下文推导或补齐。

### 文字记录：生产计划 500 错误与后端日志

文字记录：13-创建生产计划返回 500，后端日志显示 Field 'deptId' doesn't have a default value。

回顾要点：根因是数据库必填字段没有值，不应为了让 JMeter 通过而随意伪造用户归属字段。

---

## 7. 15～16：自动清理并验证

### 7.1 tearDown Thread Group

tearDown Thread Group 是主线程组结束后执行的清理线程组。空的 tearDown 不会自动删除数据，必须添加 JDBC Request。

### 7.2 JDBC Connection Configuration

连接池名：

~~~text
zhihuitongDb
~~~

推荐配置：

~~~text
Database URL:
jdbc:mysql://localhost:3306/zhihuitong?useUnicode=true&characterEncoding=UTF-8&serverTimezone=Asia/Shanghai&useSSL=false&allowPublicKeyRetrieval=true

JDBC Driver class:
com.mysql.cj.jdbc.Driver

Validation Query:
SELECT 1
~~~

驱动 JAR 应放在：

~~~text
D:\app_other\myjmeter\apache-jmeter-5.6.3\lib
~~~

放入后完全关闭并重新打开 JMeter。

### 7.3 15-自动清理 JMETER 测试数据

~~~text
Variable Name of Pool：zhihuitongDb
Query Type：Callable Statement
SQL Query：{call zhihuitong.cleanup_jmeter_test_data()}
Query Timeout：60
~~~

Callable Statement 表示调用存储过程或函数。

### 7.4 存储过程的删除顺序

必须从子表向父表删除：

1. 检验附件；
2. 质检记录；
3. 异常记录；
4. 工艺参数；
5. AI 排产记录；
6. 计划工序；
7. 生产计划；
8. 订单批次关联；
9. 订单明细；
10. 测试订单。

存储过程：

~~~sql
DROP PROCEDURE IF EXISTS cleanup_jmeter_test_data;
DELIMITER $$

CREATE PROCEDURE cleanup_jmeter_test_data()
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;

    START TRANSACTION;

    DELETE idata
    FROM inspectiondata idata
    JOIN qcrecord qc ON qc.inspectionId = idata.qcRecordId
    JOIN planstep ps ON ps.planStepId = qc.planStepId
    JOIN productionplan pp ON pp.planId = ps.planId
    JOIN orderinfo o ON o.orderId = pp.orderId
    WHERE o.orderNo LIKE 'JM-%' AND o.remark = 'JMETER_TEST';

    DELETE qc
    FROM qcrecord qc
    JOIN planstep ps ON ps.planStepId = qc.planStepId
    JOIN productionplan pp ON pp.planId = ps.planId
    JOIN orderinfo o ON o.orderId = pp.orderId
    WHERE o.orderNo LIKE 'JM-%' AND o.remark = 'JMETER_TEST';

    DELETE er
    FROM exceptionrecord er
    JOIN planstep ps ON ps.planStepId = er.planStepId
    JOIN productionplan pp ON pp.planId = ps.planId
    JOIN orderinfo o ON o.orderId = pp.orderId
    WHERE o.orderNo LIKE 'JM-%' AND o.remark = 'JMETER_TEST';

    DELETE param_data
    FROM processparameter param_data
    JOIN planstep ps ON ps.planStepId = param_data.planStepId
    JOIN productionplan pp ON pp.planId = ps.planId
    JOIN orderinfo o ON o.orderId = pp.orderId
    WHERE o.orderNo LIKE 'JM-%' AND o.remark = 'JMETER_TEST';

    DELETE ai
    FROM aischedulerecord ai
    JOIN productionplan pp ON pp.planId = ai.planId
    JOIN orderinfo o ON o.orderId = pp.orderId
    WHERE o.orderNo LIKE 'JM-%' AND o.remark = 'JMETER_TEST';

    DELETE ps
    FROM planstep ps
    JOIN productionplan pp ON pp.planId = ps.planId
    JOIN orderinfo o ON o.orderId = pp.orderId
    WHERE o.orderNo LIKE 'JM-%' AND o.remark = 'JMETER_TEST';

    DELETE pp
    FROM productionplan pp
    JOIN orderinfo o ON o.orderId = pp.orderId
    WHERE o.orderNo LIKE 'JM-%' AND o.remark = 'JMETER_TEST';

    DELETE obl
    FROM orderbatchlink obl
    JOIN orderinfo o ON o.orderId = obl.orderId
    WHERE o.orderNo LIKE 'JM-%' AND o.remark = 'JMETER_TEST';

    DELETE oi
    FROM orderitem oi
    JOIN orderinfo o ON o.orderId = oi.orderId
    WHERE o.orderNo LIKE 'JM-%' AND o.remark = 'JMETER_TEST';

    DELETE FROM orderinfo
    WHERE orderNo LIKE 'JM-%' AND remark = 'JMETER_TEST';

    COMMIT;
END$$
DELIMITER ;
~~~

含义：

- START TRANSACTION：开始事务；
- COMMIT：全部成功后提交；
- ROLLBACK：异常时回滚；
- RESIGNAL：把数据库异常继续抛给 JMeter；
- JM- 和 JMETER_TEST：双重安全过滤。

执行前应确认表名和字段名与当前数据库一致。

### 7.5 16-验证测试数据已清空

~~~text
Variable Name of Pool：zhihuitongDb
Query Type：Select Statement
~~~

SQL：

~~~sql
SELECT
    (
        SELECT COUNT(*)
        FROM orderinfo
        WHERE orderNo LIKE 'JM-%'
          AND remark = 'JMETER_TEST'
    ) AS order_count,
    (
        SELECT COUNT(*)
        FROM orderitem
        WHERE productCode LIKE 'JM-P-%'
           OR remark = 'JMETER_TEST'
    ) AS item_count,
    (
        SELECT COUNT(*)
        FROM orderbatchlink
        WHERE remark = 'JMETER_TEST'
    ) AS link_count,
    (
        SELECT COUNT(*)
        FROM productionplan
        WHERE remark = 'JMETER_TEST'
    ) AS plan_count;
~~~

Variable names：

~~~text
order_count,item_count,link_count,plan_count
~~~

JMeter 读取第一行后生成：

~~~text
order_count_1
item_count_1
link_count_1
plan_count_1
~~~

### 7.6 JSR223 Assertion

~~~groovy
def counts = [
    order_count: vars.get('order_count_1'),
    item_count : vars.get('item_count_1'),
    link_count : vars.get('link_count_1'),
    plan_count : vars.get('plan_count_1')
]

log.info('JMeter测试数据清理验证结果：' + counts)

def invalidItems = counts.findAll { name, value ->
    value == null || value.trim() != '0'
}

if (!invalidItems.isEmpty()) {
    AssertionResult.setFailure(true)
    AssertionResult.setFailureMessage(
        '测试环境恢复失败，仍有残留数据：' + invalidItems
    )
}
~~~

四项全是 0 才通过；变量不存在或不等于字符串 0 都失败。

### 7.7 断言层级错误

正确层级：

~~~text
测试数据清理
├── 15-自动清理JMETER测试数据
└── 16-验证测试数据已清空
    └── 断言-测试数据全部为0
~~~

如果断言挂在 15 下，16 还没有执行，变量会是 null，导致误报。

### 文字记录：JDBC 连接配置

文字记录：连接池名为 zhihuitongDb，驱动类为 com.mysql.cj.jdbc.Driver，Validation Query 为 SELECT 1，MySQL 驱动放在 JMeter 的 lib 目录。

### 文字记录：清理线程组层级

文字记录：测试数据清理下面依次是 15-自动清理JMETER测试数据、16-验证测试数据已清空，JSR223 Assertion 必须挂在 16 下面。

### 文字记录：完整脚本执行结果

文字记录：完整执行时 01～16 应全部绿色；最少要确认 15 清理成功、16 的四个残留数量都是 0。

---

## 8. 常见错误速查

| 现象 | 含义 | 优先检查 |
|---|---|---|
| Connection refused | 端口没有服务监听 | 端口、后端是否启动 |
| UnknownHostException: ($) | $ 被当成主机名 | Server Name or IP 是否误填变量 |
| 415 Unsupported Media Type | 请求体格式不被接受 | Body Data、Content-Type |
| 401 Unauthorized | Token 无效或未发送 | 登录、JSON Extractor、Authorization |
| 500 + deptId | 数据库必填字段没有值 | 后端插入逻辑和表结构 |
| Access denied | MySQL 账号或密码失败 | JDBC 配置、授权 |
| PROCEDURE does not exist | 存储过程不存在或数据库不对 | SHOW PROCEDURE STATUS |
| Cannot load JDBC driver | 驱动 JAR 不在 JMeter 类路径 | lib 目录、重启 |
| 15 绿、16 红 | 清理不完整或断言配置错误 | COUNT、变量名、清理条件 |
| 变量为 null | 提取器或执行顺序错误 | 组件层级、JSONPath |

排错顺序：

~~~text
查看结果树
→ 取样器结果
→ 响应数据
→ 后端控制台日志
~~~

“请求”选项卡只显示发送内容，SQLException 往往在响应数据或后端日志中。

---

## 9. 英文界面词汇表

| 英文 | 中文 | 作用 |
|---|---|---|
| Test Plan | 测试计划 | 脚本根节点 |
| Thread Group | 线程组 | 模拟并发用户 |
| Sampler | 取样器 | 发出请求 |
| HTTP Request | HTTP 请求 | 调用接口 |
| HTTP Request Defaults | HTTP 请求默认值 | 提供公共主机和端口 |
| Server Name or IP | 服务器名称或 IP | localhost |
| Port Number | 端口号 | 8080 |
| Path | 路径 | 接口路径 |
| Body Data | 请求体 | 放原始 JSON |
| Parameters | 参数 | 表单或 URL 参数 |
| Header Manager | 信息头管理器 | 配置请求头 |
| Content-Type | 内容类型 | 说明请求体格式 |
| Accept | 接受类型 | 希望收到的响应格式 |
| JSON Extractor | JSON 提取器 | 从响应提取变量 |
| JSONPath | JSON 路径 | 定位 JSON 字段 |
| Assertion | 断言 | 判断结果是否正确 |
| Response Assertion | 响应断言 | 判断状态码或文本 |
| JSR223 Assertion | 脚本断言 | 用 Groovy 自定义判断 |
| Once Only Controller | 仅一次控制器 | 每个线程只登录一次 |
| tearDown Thread Group | 清理线程组 | 主线程结束后执行 |
| JDBC Connection Configuration | JDBC 连接配置 | 创建连接池 |
| JDBC Request | JDBC 请求 | 执行 SQL |
| Variable Name of Pool | 连接池变量名 | 连接池引用名 |
| Callable Statement | 可调用语句 | 调用存储过程 |
| Select Statement | 查询语句 | 执行 SELECT |
| Query Timeout | 查询超时 | SQL 最长等待时间 |
| View Results Tree | 查看结果树 | 调试请求 |

---

## 10. 最终检查清单

- [ ] 后端端口为 8080，不是前端 5173；
- [ ] HTTP Request Defaults 配置正确；
- [ ] POST JSON 放在 Body Data；
- [ ] Header 有 Content-Type: application/json；
- [ ] 登录后成功提取 token；
- [ ] 后续请求使用 Authorization: Bearer ${token}；
- [ ] orderId、orderItemId、batchId、routeId 路径正确；
- [ ] 写入数据使用 JM- 和 JMETER_TEST；
- [ ] deptId 等归属字段由后端正确处理；
- [ ] JDBC 驱动放在 JMeter lib 并重启；
- [ ] 15 使用 Callable Statement；
- [ ] 16 使用 Select Statement；
- [ ] 断言挂在 16 下；
- [ ] 四个残留数量最终都是 0；
- [ ] 正式压测前关闭 View Results Tree；
- [ ] 笔记没有真实密码和 Token。

> 下一篇记录查询压测脚本、非 GUI 执行、JMeter HTML 报告和 Grafana 指标解读。

# 介绍

Vue.js是一套构建用户界面的渐进式框架，采用自底向上增量开发的设计，核心库只关注视图层。另一方面，Vue完全有能力驱动采用[单文件组件](https://baike.baidu.com/item/%E5%8D%95%E6%96%87%E4%BB%B6%E7%BB%84%E4%BB%B6/62176189?fromModule=lemma_inlink)和Vue生态系统支持的库开发的复杂[单页](https://baike.baidu.com/item/%E5%8D%95%E9%A1%B5/7631394?fromModule=lemma_inlink)应用。

Vue是一个框架，也是一个生态。可以通过渐进式增强静态的HTML、作为Web Components嵌入、单页应用 （[SPA](https://baike.baidu.com/item/SPA/17536313?fromModule=lemma_inlink)）、全栈/服务端渲染（[SSR](https://baike.baidu.com/item/SSR/58244646?fromModule=lemma_inlink)）、Jamstack/静态站点生成（SSG）、桌面端、移动端、[WebGL](https://baike.baidu.com/item/WebGL/592485?fromModule=lemma_inlink)，[命令行](https://baike.baidu.com/item/%E5%91%BD%E4%BB%A4%E8%A1%8C/196110?fromModule=lemma_inlink)终端中界面等方式使用Vue。

- 观察发现vue的变量方法的使用和其他语言也是由很大的区别
	- ref 一般存放普通数据类型
	- reactive 用来存放复杂对象 比如数组，对象等
- 方法的使用也有区别 
	- 方法的定义也需要用const
```vue
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <!-- 第一步：导入vue.js文件 -->
     <script src ="https://unpkg.com/vue@3/dist/vue.global.js"></script>
    <title>vue内容</title>
</head>
<body>
    <!-- 第二步：创建一个vue容器 -->
     <div id="app">
        <p>学校名称:{{name}}</p>
        <p>学生人数:{{stuCount}}</p>
        <h2>四大名著西游记</h2>
        <p>书名:{{book.name}}</p>
        <p>价格:${{book.price}}</p>
        <p>作者:{{book.author}}</p>
        <button @click="add">点击增加</button>
     </div>
</body>
<script>
    // 第三步：编写vue代码
    const{createApp,ref,reactive} = Vue
    createApp({
        setup(){
            //定义变量和方法
            const name = ref("江西服装学院")
            const stuCount = ref(12896)
            const book = reactive({
                name:"西游记",
                price:95.5,
                author:"吴承恩"
            })
            const add = () => {
                stuCount.value += 100
            }
            return {
                //定义返回的变量和方法
                name,
                stuCount,
                book,
                add
            }
        }
    }).mount("#app")// 挂载容器
</script>
</html>
```

# vue的双向绑定
```vue
<div>
            <input type="text" v-model="inputMessage">
            <button @click="onClick">确认</button>
            <p>输入框内容：{{newContent}}</p>
        </div>
```
这里的 v-model inputMessage和newContent绑定
```vue
            const inputMessage = ref("")
            const newContent = ref("")
            const onClick = () => {
                newContent.value = inputMessage.value
                inputMessage.value = ""
            }
```
## 我的模板
```vue
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="../js/vue.js"></script>
    <title>vue two</title>
</head>
<body>
    <div class="drc">
    
    </div>
</body>
<script>
    const {createApp,ref,reactive} = vue
    createApp({
        setup(){
            //定义方法和变量
            return{
                //返回方法和变量
            }
        }
    }).mount(".drc")
</script>
</html>
```
- 注意在script中createApp的 .mount(".drc")是根据容器的名字来写的 如果是class就是 .如果是id就是#
## click
![[click.png]]


## 选项卡
- 首先用盒子装选项卡
```vue
<div class="drc">
        <div v-show="showCard=='one'" style="width: 300px;height: 300px;background-color: #15d13e;">选项卡1</div>
        <div v-show="showCard=='two'" style="width: 300px;height: 300px;background-color: #f3d10e;">选项卡2</div>
        <div>
            <button @click="showCard='one'">卡片1</button>
            <button @click="showCard='two'">卡片2</button>
        </div>
    </div>
```
这里的drc在<script 中有
### v-show
1. **条件显示**：`v-show="showCard=='one'"` 表示只有当 `showCard` 的值等于 `'one'` 时，这个 div 才会显示
    
2. **CSS 控制**：`v-show` 通过 CSS 的 `display` 属性来控制显示/隐藏
    
    - 条件为 true：`display: block`（或其他合适的显示值）
        
    - 条件为 false：`display: none`
        
3. **多选一模式**：通过改变同一个变量 `showCard` 的值，实现多个选项卡中只显示一个的效果
#### 与 `v-if` 的区别
```vue
<!-- v-show：总是渲染，只是控制CSS显示 -->
<div v-show="condition">内容</div>
<!-- v-if：条件为false时不渲染 -->
<div v-if="condition">内容</div>
```

### v-if
#### 1. **真正的条件渲染**

- 条件为 `true` 时：元素会被渲染到 DOM 中
    
- 条件为 `false` 时：元素会从 DOM 中完全移除
    

#### 2. **与 `v-show` 的区别**

|特性|`v-if`|`v-show`|
|---|---|---|
|**DOM 操作**|添加/移除 DOM 元素|切换 CSS `display` 属性|
|**初始渲染**|惰性的，条件为 false 不渲染|总是渲染，初始成本高|
|**切换开销**|高（涉及 DOM 操作）|低（只是 CSS 切换）|
|**适用场景**|不常切换的条件|频繁切换的显示/隐藏|

```vue
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="../js/vue.js"></script>
    <title>pageCard</title>
</head>
<body>
    <div class="drc">
        <div v-show="showCard=='one'" style="width: 300px;height: 300px;background-color: #15d13e;">选项卡1</div>
        <div v-show="showCard=='two'" style="width: 300px;height: 300px;background-color: #f3d10e;">选项卡2</div>
        <div>
            <button @click="showCard='one'" :style="showCard=='one'?'background-color:#15d13e;':''">卡片1</button>
            <button @click="showCard='two'" :style="showCard=='one'?'background-color:#f3d10e;':''">卡片2</button>
        </div>
    </div>
</body>
<Script>
    const {createApp,ref,reactive} = Vue
    createApp({
        setup(){
            //定义方法和变量
            const showCard = ref("one")
            return{
                showCard,
            }
        }
    }).mount(".drc")
</Script>
</html>
```

##### 在选项按钮中
```vue
<style>

        .checkedStyle{

            background-color: #506bef;

            color: aliceblue;

        }

    </style>
```
```vue
<div>

            <button @click="showCard='one'" :class="showCard=='one'?'checkedStyle':''">卡片1</button>

            <button @click="showCard='two'" :class="showCard=='two'?'checkedStyle':''">卡片2</button>

        </div>
```
- 这里使用三元运算符还有style样式对选项按钮被选中时的样式 ，==但是在使用是class前需要加冒号==

## 轮播图
```vue
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="../js/vue.js"></script>
    <title>carousel</title>
    <style>
        .imgStyle{
            width: 250px;
            height: 250px;
            border-radius: 8px;
            padding: 5px;
        }
    </style>
</head>
<body>
    <div class="drc">
        <img :src="imageArr[index]" class="imgStyle">
        <button @click="prev">上一张</button>
        <button @click="next">下一张</button>
    </div>
</body>
<script>
    const {createApp,ref,reactive} = Vue
    createApp({
        setup(){
            const imageArr = reactive([
                "../images/404.png",
                "../images/500.png",  
                "../images/null.png"
            ])
            const index = ref(0)
            const prev = () =>{
                if(index.value == 0){
                    index.value = imageArr.length - 1
                }else{
                    index.value--
                }
            }
            const next = () =>{
                if(index.value == imageArr.length - 1){  
                    index.value = 0
                }else{
                    index.value++  
                }
            }
  

            return{

                imageArr,

                index,

                prev,

                next,

            }

        }

    }).mount(".drc")

</script>

</html>
```
## v-for循环
```vue
<body>
    <div class="drc">
        <h2>学生名单</h2>
        <ul>
           <li v-for="(name, index) in nameArr">{{ index + 1 }}. {{ name }}</li>
        </ul>
        <h2>书本信息</h2>
        <ul>
            <li v-for="book in bookArr">
                <span>书名:{{book.name}}</span><br>
                <span>价格:{{book.price}}</span><br>
                <span>作者:{{book.author}}</span><br>
            </li>
        </ul>
    </div>
</body>
<script>
    const {createApp,ref,reactive} = Vue
    createApp({
        setup(){
            //定义方法和变量
            const nameArr = reactive(["张三","李四","王五","赵六","孙七"])
            const bookArr = reactive([
                {name:"张三的书",price:50,author:"张三"},
                {name:"李四的书",price:49,author:"李四"},
                {name:"王五的书",price:90,author:"王五"},
                {name:"赵六的书",price:67,author:"赵六"},
            ])
            return{
                //返回方法和变量
                nameArr,
                bookArr
            }
        }
    }).mount(".drc")
</script>
```

## 路由守卫
```vue
  

/*

*代码要写在app.mount("#app")之前

*全局前置守卫(路由拦截器)：作用如：如果没有登陆，则不能进入主页面

* to : 即将进入的路由

* from: 即将离开的路由

* next: 放行

*/

router.beforeEach((to, from, next) => {

    // console.log("to====",to)

    // console.log("from====",from)

     if (to.href == "/index") {//如果访问的路由路径为 /register

        //   next(false) //不放行

        alert("请先登陆")

        next("/two")

          return

      }

      next() //放行
```

## pinia

- 在终端下载
```
 npm install pinia
```

```
npm i pinia-plugin-persistedstate
```


### 修改main.js
```vue
//1.导入pinia

import { createPinia } from 'pinia'

//2.导入pinia持久化存储插件

import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

//3.得到pinia对象

const pinia = createPinia()

//4.添加插件到pinia对象中

pinia.use(piniaPluginPersistedstate)

。。。。。。

const app = createApp(App) //挂载

app.use(pinia)//挂载pinia

app.use(router) //挂载路由
```


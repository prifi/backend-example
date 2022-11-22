import Vue from 'vue'
import App from './App.vue' // 组件
import router from './router' // 静态路由，前端路由
import './plugins/element.js' // 按需导入Element UI
import './assets/css/main.css' // 导入全局css样式
import axios from 'axios' // 导入异步请求

// axios全局设置
// 添加全局请求拦截器，只要发起异步请求都需要带上token
axios.interceptors.request.use(config => {
  // 在发送请求之前做些什么
  config.headers.Authorization = 'JWT ' + window.localStorage.getItem('token')
  return config
})

// 添加响应拦截器
// 监控响应code如果不是正常响应码跳转登录页
axios.interceptors.response.use(
  response => {
    // console.log(response)
    // 2xx 范围内的状态码都会触发该函数。
    // 对响应数据做点什么
    if (response.data.code && response.data.code < 100) {
      // 小于100的错误码（认证相关）需要
      router.push('/login')
      return response
    } else {
      return response
    }
  })

Vue.prototype.$http = axios // 增加全局属性$http
axios.defaults.baseURL = '/api/v1' // 默认值，缺省URL // 访问自己，相对，vue.config.js 代理到 http://127.0.0.1:5000/
Vue.config.productionTip = false

new Vue({
  router,
  render: h => h(App) // App是组件
}).$mount('#root') // 网页html挂载点

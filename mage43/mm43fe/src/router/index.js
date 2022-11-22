import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../views/LoginView.vue'
import Welcome from '../views/WelcomeView'
import Home from '../views/HomeView'
import User from '../views/user/UserView'
import Perm from '../views/user/PermView'
import Role from '../views/user/RoleView'
import CiType from '../views/cmdb/CiTypeView'
import Ci from '../views/cmdb/CiView'
import Org from '../views/jumpserver/OrgView'
import WebShell from '../views/jumpserver/WebShell'

Vue.use(VueRouter)

// 路由表
const routes = [
  { path: '/', redirect: '/login' }, // 重定向
  { path: '/login', component: Login },
  {
    path: '/home',
    component: Home,
    redirect: '/welcome',
    children: [ // 嵌套路由
      { path: '/welcome', component: Welcome },
      { path: '/users', component: User },
      { path: '/users/perms', component: Perm },
      { path: '/users/roles', component: Role },
      { path: '/cmdb/citypes', component: CiType },
      { path: '/cmdb/cis', component: Ci },
      { path: '/jumpserver/orgs', component: Org }
    ]
  },
  { path: '/jumpserver/webshell/:hostid', component: WebShell }
]

const router = new VueRouter({
  routes
})

// 前置导航守卫，每一次路由前检查是否登录(有无设置token)
router.beforeEach((to, from, next) => {
  // to.name
  if (to.path === '/login') {
    next()
  } else {
    // 检查是否有token，由服务器检查token是否有效
    const token = window.localStorage.getItem('token') // 获取taoken
    if (!token) {
      next('/login') // 如果没有token, 去login
    } else {
      next()
    }
  }
})

export default router

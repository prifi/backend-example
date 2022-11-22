<template>
  <el-container>
    <el-header>
      <div class="logo">
        <img src="../assets/logo.png" alt="logo" />
        <div class="title">FlyOps</div>
        <i :class="isCollapse ? 'el-icon-s-unfold' : 'el-icon-s-fold'" @click="isCollapse = !isCollapse"></i>
      </div>
      <div class="info">
        <!-- <el-button type="primary" @click="logout">退出</el-button> -->
        <el-dropdown @command="handleCommand">
          <span class="el-dropdown-link">
            <!-- 链接跳转的3种方式 -->
            <!-- <a href="/#/Welcome">{{ user.username }}</a> -->
            <!-- <el-link href="/#/Welcome">{{ user.username }}</el-link> -->
            <router-link to="/Welcome">{{ user.username }}</router-link>
            <i class="el-icon-arrow-down el-icon--right"></i>
          </span>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item icon="el-icon-check" command="chpwd">修改密码</el-dropdown-item>
            <el-dropdown-item icon="el-icon-circle-check" divided command="logout">退出 </el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </div>
      <!-- 修改密码对话框 -->
      <el-dialog title="修改密码" :visible.sync="chpwdDialogVisible" width="30%" @close="resetForm('chpwd')">
        <el-form :model="chpwdForm" :rules="chpwdRules" ref="chpwd" label-width="100px">
          <el-form-item label="用户名">
            {{ user.username }}
          </el-form-item>
          <el-form-item label="旧密码" prop="oldPassword">
            <el-input type="password" placeholder="旧密码" show-password v-model="chpwdForm.oldPassword"></el-input>
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input type="password" placeholder="新密码" show-password v-model="chpwdForm.password"></el-input>
          </el-form-item>
          <el-form-item label="确认密码" prop="checkPass">
            <el-input type="password" placeholder="确认新密码" show-password v-model="chpwdForm.checkPass"></el-input>
          </el-form-item>
        </el-form>
        <span slot="footer" class="dialog-footer">
          <el-button @click="chpwdDialogVisible = false">取 消</el-button>
          <el-button type="primary" @click="changePassword">确 定</el-button>
        </span>
      </el-dialog>
    </el-header>
    <el-container>
      <el-aside :width="isCollapse ? '64px' : '240px'">
        <el-menu
          router
          default-active="101"
          background-color="#545c64"
          text-color="#fff"
          active-text-color="#ffd04b"
          :collapse="isCollapse"
        >
          <!-- 获取菜单 id唯一 -->
          <el-submenu :index="item.id.toString()" v-for="item in menuList" :key="item.id">
            <template slot="title">
              <i class="el-icon-menu"></i>
              <span>{{ item.name }}</span>
            </template>
            <el-menu-item :index="sub.path" v-for="sub in item.children" :key="sub.id">
              {{ sub.name }}
            </el-menu-item>
          </el-submenu>
        </el-menu>
      </el-aside>
      <!-- 嵌套路由 呈现子组件 -->
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
import { resetFormMixin } from '../mixins'
export default {
  mixins: [resetFormMixin],
  created() {
    // 生命周期钩子函数。该组件加载时调用
    this.getMenuList()
    // 登录时加载用户信息
    this.getUserInfo()
  },
  data() {
    const validatePass = (rule, value, callback) => {
      if (value !== this.chpwdForm.password) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    }
    return {
      isCollapse: false,
      menuList: [
        // 后端模拟生成
        // {
        //   id: 1,
        //   name: 'test1',
        //   children: [
        //     { id: 101, name: 'test101' },
        //     { id: 102, name: 'test102' }
        //   ]
        // },
        // { id: 2, name: 'test2', children: [] }
      ],
      // 用户信息
      user: {},
      // 修改密码
      chpwdDialogVisible: false,
      chpwdRules: {
        oldPassword: [
          { required: true, message: '请输入旧密码', trigger: 'blur' },
          { min: 4, max: 16, message: '长度在 4 到 16 个字符', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入新密码', trigger: 'blur' },
          { min: 4, max: 16, message: '长度在 4 到 16 个字符', trigger: 'blur' }
        ],
        checkPass: [
          { required: true, message: '请输入确认密码', trigger: 'blur' }, // 可以使用自定义校验器实现
          { validator: validatePass, trigger: 'blur' } // 自定义校验器
        ]
      },
      chpwdForm: {
        oldPassword: '',
        passwod: '',
        checkPass: ''
      }
    }
  },
  methods: {
    logout() {
      window.localStorage.removeItem('token')
      this.$router.push('/login')
    },
    async getMenuList() {
      // 每个请求都要带token，使用全局axios拦截器实现
      // const { data: response } = await this.$http.get('??/', {
      //   params: { a: 1, b: 2 }, // 查询字符串
      //   headers: { Autorization: 'JWT ' + window.localStorage.getItem('token') }
      // }) // 需要带token
      // 后台获取菜单列表
      const { data: response } = await this.$http.get('menulist/') // token header 拦截器实现
      if (response.code) {
        return this.$message.error(response.message)
      }
      this.menuList = response
    },
    async getUserInfo() {
      const { data: response } = await this.$http.get('users/mgr/whoami/')
      if (response.code) {
        return this.$message.error(response.message)
      }
      this.user = response.user
    },
    handleCommand(command) {
      if (command === 'logout') {
        this.logout()
      } else if (command === 'chpwd') {
        this.chpwdDialogVisible = true
      }
    },
    // 关闭Dialog之前重置表单
    // resetForm(formName) {
    //   this.$refs[formName].resetFields()
    // },
    changePassword() {
      const formName = 'chpwd'
      this.$refs[formName].validate(async valid => {
        if (valid) {
          const { data: response } = await this.$http.post('users/mgr/set_self_pwd/', this.chpwdForm)
          if (response.code) {
            return this.$message.error(response.message)
          }
          this.chpwdDialogVisible = false
          this.$message.success('密码修改成功')
          this.logout()
        }
      })
    }
  }
}
</script>

<style lang="less" scoped>
.el-container {
  height: 100%;
}
.el-aside {
  background-color: #545c64;
}
.el-main {
  background-color: #f0f2f4;
}
.el-header {
  display: flex; // 主轴x两端对齐
  justify-content: space-between; // 侧轴y居中
  align-items: center;
  padding-left: 10px;
  .logo {
    .title {
      font-size: 20px;
      margin-left: 3px;
    }
    img {
      height: 30px;
    }
    i {
      font-size: 30px;
      margin-left: 5px;
    }
    display: flex;
    align-items: center;
  }
}
.el-menu {
  border-right: none;
}
</style>
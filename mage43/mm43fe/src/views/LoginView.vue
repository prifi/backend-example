<template>
  <div class="login_container">
    <div class="login_box">
      <div class="avatar_box">
        <img src="../assets/logo.png" alt="logo" />
      </div>
      <el-form class="login_from" :model="loginForm" ref="loginForm" :rules="loginRules" label-width="100px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="loginForm.username" placeholder="请输入用户名" prefix-icon="el-icon-user"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            prefix-icon="el-icon-warning-outline"
            @keyup.enter.native="login"
            show-password
          ></el-input>
        </el-form-item>
        <el-form-item class="lgoin_button">
          <el-button type="primary" icon="el-icon-user" @click="login">登录</el-button>
          <el-button type="info" icon="el-icon-circle-close" @click="resetForm('loginForm')">重置</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  // data () {return {xxx:yyy}}
  data() {
    // var validatePass = (rule, value, callback) => {
    //   if (value === '') {
    //     callback(new Error('请输入密码'))
    //   } else {
    //     if (this.loginForm.password !== '') {
    //       this.$refs.loginForm.validateField('password')
    //     }
    //     callback()
    //   }
    // }
    // var validatePass2 = (rule, value, callback) => {
    //   字段级校验
    //   if (value === '') {
    //     callback(new Error('请再次输入密码'))
    //   } else if (value !== this.ruleForm.pass) {
    //     callback(new Error('两次输入密码不一致!'))
    //   } else {
    //     callback()
    //   }
    // }
    return {
      loginForm: {
        // 用于提交到后台
        username: '',
        password: ''
      },
      loginRules: {
        // 用于表单验证
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 3, max: 18, message: '长度在 3 到 18 个字符', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 4, max: 18, message: '长度在 5 到 18 个字符', trigger: 'blur' }
        ]
        // 自定义验证
        // password: [{ validator: validatePass, trigger: 'blur' }]
      }
    }
  },
  methods: {
    // 重置
    resetForm(formName) {
      this.$refs[formName].resetFields()
    },
    login() {
      // this 是谁？ => 当前组件本身，data属性会挂到this上
      // console.log(this)
      // this.loginForm.username = 'xiaopf' // 双向数据绑定
      // console.log(this.loginForm.username, this.loginForm.password)
      // 对象级别校验, Form表单数据提交到后台
      this.$refs.loginForm.validate(async (valid, obj) => {
        // valid: 是否校验通过 bool
        if (valid) {
          const { data: response } = await this.$http.post('login/', this.loginForm) // axios异步提交表单数据，自动转换为json格式提交到后台
          // const { status, data } = response // 解构响应
          // console.log(response) // 解构，重命名
          if (response.code) {
            // 如果code不为0或者undefined，失败提示!!!
            this.$message.error(response.message) // 认证失败，错误消息提示
          } else {
            // code为0或不为undefined，成功跳转!!!
            this.$message.success('登录成功')
            window.localStorage.setItem('token', response.access) // 认证成功保存token
            this.$router.push('/home') // 认证成功，跳转主页
          }
        } else {
          // 校验失败, obj: 失败时返回失败规则
          console.log(obj, '+++')
        }
      })
    }
  }
}
</script>

<style lang="less" scoped>
.login_container {
  background-color: #2b4b6b;
  height: 100%;
}

.login_box {
  width: 450px;
  height: 250px;
  background-color: #fff;
  border-radius: 5px;
  position: absolute;
  // position: relative; // 相对
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);

  .avatar_box {
    height: 100px;
    width: 100px;
    padding: 10px;
    position: absolute;
    left: 50%;
    transform: translate(-50%, -50%);
    img {
      width: 100%;
      height: 100%;
      border-radius: 40%;
    }
  }

  .login_from {
    position: absolute;
    bottom: 0;
    width: 100%;
    padding: 0 20px;
    box-sizing: border-box;
  }
}
</style>

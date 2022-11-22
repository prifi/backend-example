<template>
  <div class="console">
    <div>
      <el-input placeholder="请输入命令" v-model="command" @keyup.enter.native="handleCommand"></el-input>
    </div>
    <hr />
    <div class="output" v-for="(output, index) in outputList" :key="index">>> {{ output }}</div>
    <hr />
  </div>
</template>

<script>
// 路由匹配创建组件
export default {
  created() {
    this.getHost()
  },
  data() {
    return {
      outputList: [],
      command: ''
    }
  },
  methods: {
    async getHost() {
      // this.$route.params拿到路由传参hostid
      const { hostid: hostId } = this.$route.params
      // 通过主机id返回主机详情，内容不带密码和密钥
      const { data: response } = await this.$http.get(`jumpserver/hosts/${hostId}/`)
      if (response.code) {
        return this.$message.error(response.message)
      }
      console.log('主机详情 Client >>:', response)
      const { ip, username } = response
      const line = `正在连接到主机${ip}，使用的用户名是${username}`
      this.outputList.push(line)

      // 服务端建立ws连接
      if ('WebSocket' in window) {
        // Create WebSocket connection.
        const remoteWsServer = '192.168.56.102' // 127.0.0.1 堡垒机IP
        const remoteWsPort = '10800' // 服务端需要监听
        const ws = new WebSocket(`ws://${remoteWsServer}:${remoteWsPort}/webshell`)

        // 建立连接，发送token及主机id
        ws.onopen = event => {
          // ws.send('建立连接', event)
          this.outputList.push(`连接到${remoteWsServer}:${remoteWsPort}...`)
          ws.send(
            JSON.stringify({
              token: window.localStorage.getItem('token'),
              hostId // 后端查询主机密码或密钥需要
            })
          )
        }

        // 接收消息
        ws.onmessage = event => {
          console.log('接收消息', event.data)
          this.outputList.push(event.data)
        }

        // 发生错误
        ws.onerror = event => {
          console.log('发生错误', event)
        }

        // 关闭连接
        ws.onclose = event => {
          console.log('关闭连接', event)
          this.outputList.push(`与主机${ip}的连接断开`, event.reason)
        }

        // 绑定全局变量
        this.ws = ws
      } else {
        this.$message.error('该浏览器不支持WebSocket, 请更新浏览器到最新版本或更换浏览器')
      }
    },
    // 发送给后台命令
    handleCommand() {
      console.log('发送消息 Client >>:', this.command)
      this.ws.send(this.command)
      this.command = ''
    }
  }
}
</script>

<style lang="less" scoped>
.console {
  background: #000;
  min-height: 300px;
  color: #fff;
  padding: 5px;
  height: 100%;
}
</style>>
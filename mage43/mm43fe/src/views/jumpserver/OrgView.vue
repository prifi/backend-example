<template>
  <div>
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>JumpServer</el-breadcrumb-item>
      <el-breadcrumb-item>组织管理</el-breadcrumb-item>
    </el-breadcrumb>
    <!-- 组织树 -->
    <el-card>
      <el-tree
        :data="dataList"
        node-key="id"
        default-expand-all
        :props="defaultProps"
        :expand-on-click-node="false"
        @node-click="handleNodeClick"
      >
        <span class="custom-tree-node" slot-scope="{ node, data }">
          <span>{{ node.label }}-{{ data.id }}</span>
          <span>
            <el-dropdown @command="handleCommand">
              <span trigger="hover" class="el-dropdown-link"> <i class="el-icon-setting el-icon--right"></i> </span>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item :command="[1, node, data]" icon="el-icon-plus">增加分组</el-dropdown-item>
                <el-dropdown-item :command="[2, node, data]" icon="el-icon-minus">删除分组</el-dropdown-item>
                <el-dropdown-item
                  v-if="data.id !== null"
                  :command="[3, node, data]"
                  icon="el-icon-circle-plus-outline"
                  divided
                  >增加主机</el-dropdown-item
                >
              </el-dropdown-menu>
            </el-dropdown>
          </span>
        </span>
      </el-tree>
      <!-- 主机列表 -->
      <el-table border stripe :data="hostList" style="width: 100%">
        <el-table-column type="index"></el-table-column>
        <el-table-column prop="id" label="ID" width="70"></el-table-column>
        <el-table-column prop="ip" label="IP"> </el-table-column>
        <el-table-column prop="username" label="登录名"> </el-table-column>
        <!-- <el-table-column prop="password" label="登录密码"> </el-table-column> -->
        <el-table-column prop="org" label="组织ID"> </el-table-column>
        <el-table-column label="操作" #default="{ row }">
          <el-tooltip placement="bottom" effect="light" content="WebShell">
            <!-- <el-button
              size="mini"
              type="success"
              icon="el-icon-monitor"
              // @click="$router.push(`/jumpserver/webshell/${row.id}`)"  跳转新页面 or a标签方式，不推荐
            ></el-button> -->
            <!-- 推荐使用 router-link 跳转新页面 -->
            <router-link target="_blank" :to="{ path: `/jumpserver/webshell/${row.id}` }">
              <el-button size="mini" type="primary" icon="el-icon-monitor"></el-button>
            </router-link>
          </el-tooltip>
          <el-tooltip placement="bottom" effect="light" content="编辑">
            <el-button size="mini" type="success" icon="el-icon-edit"></el-button>
          </el-tooltip>
          <el-tooltip placement="bottom" effect="light" content="删除">
            <el-button size="mini" type="danger" icon="el-icon-delete"></el-button>
          </el-tooltip>
        </el-table-column>
      </el-table>
      <el-pagination
        @current-change="handleCurrentChange"
        :current-page="pagination.page"
        :page-size="pagination.size"
        layout="total, prev, pager, next, jumper"
        :total="pagination.total"
      >
      </el-pagination>
    </el-card>
    <!-- 新增分组 -->
    <el-dialog
      :title="`[${addForm.parentName}] 增加分组`"
      :visible.sync="addDialogVisible"
      width="40%"
      @close="resetForm('add')"
    >
      <el-form :model="addForm" :rules="addRules" ref="add" label-width="100px">
        <el-form-item label="名称" prop="name">
          <el-input placeholder="请输入名称" v-model="addForm.name"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="addDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="add('add')">确 定</el-button>
      </span>
    </el-dialog>
    <!-- 新增主机 -->
    <el-dialog
      :title="`[${addHostForm.parentName}] 增加主机`"
      :visible.sync="addHostDialogVisible"
      width="40%"
      @close="resetForm('addHost')"
    >
      <el-form :model="addHostForm" :rules="addHostRules" ref="addHost" label-width="100px">
        <el-form-item label="管理IP" prop="ip">
          <el-input placeholder="请输入管理IP" v-model="addHostForm.ip"></el-input>
        </el-form-item>
        <el-form-item label="登录用户名" prop="username">
          <el-input placeholder="请输入登录用户名" v-model="addHostForm.username"></el-input>
        </el-form-item>
        <el-form-item label="登录密码" prop="password">
          <el-input placeholder="请输入登录密码" v-model="addHostForm.password"></el-input>
        </el-form-item>
        <!-- 文件上传，手动加header头带token -->
        <el-form-item label="私钥文件">
          <el-upload
            :action="`${$http.defaults.baseURL}/jumpserver/upload/`"
            :headers="getheader()"
            :on-preview="handlePreview"
            :on-remove="handleRemove"
            :before-remove="beforeRemove"
            :limit="1"
            :on-exceed="handleExceed"
            :file-list="fileList"
            :on-success="handleSuccess"
          >
            <el-button size="small" type="primary">点击上传</el-button>
            <div slot="tip" class="el-upload__tip">只能上传1个私钥文件，且不超过500kb</div>
          </el-upload>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="addHostDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="addHost">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  created() {
    this.getList()
  },
  data() {
    // 自定义校验器
    const validatePassOrPkey = (rule, value, callback) => {
      if (value === '' && this.addHostForm.ssh_pkey_path === '') {
        callback(new Error('密码和私钥至少提供一个!'))
      } else {
        callback()
      }
    }
    return {
      // 数据展示
      dataList: [],
      pagination: { total: 0, page: 1, size: 20 },
      defaultProps: { label: 'name', children: 'children' },
      // 新增分组
      addForm: { name: '' },
      addDialogVisible: false,
      addRules: {
        name: [
          { required: true, message: '请输入名称', trigger: 'blur' },
          { min: 1, max: 16, message: '长度在 1 到 16 个字符', trigger: 'blur' }
        ]
      },
      // 新增主机
      addHostForm: { ip: '', username: '', password: '', ssh_pkey_path: '' },
      addHostDialogVisible: false,
      addHostRules: {
        ip: [
          { required: true, message: '请输入管理IP', trigger: 'blur' }
          // 自定义校验器，IPv4或IPv6正则校验器校验
        ],
        username: [
          { required: true, message: '请输入登录用户名', trigger: 'blur' },
          { min: 4, max: 16, message: '长度在 4 到 16 个字符', trigger: 'blur' }
        ],
        password: [
          // { required: false, message: '请输入登录密码', trigger: 'blur' },
          // { min: 4, max: 16, message: '长度在 4 到 16 个字符', trigger: 'blur' },
          { validator: validatePassOrPkey, trigger: 'blur' }
        ]
      },
      fileList: [],
      hostList: []
    }
  },
  methods: {
    // 重置
    resetForm(formName) {
      this.$refs[formName].resetFields()
    },
    // 分页
    handleCurrentChange(val) {
      // console.log(`当前页: ${val}`)
      this.getList(val)
    },
    // 组列表
    async getList() {
      const { data: response } = await this.$http.get('jumpserver/orgs/tree/')
      if (response.code) {
        return this.$message.error(response.message)
      }
      // this.dataList = response.results
      const vroot = { id: null, name: '资产树', parent: null, children: null }
      vroot.children = response.results
      this.dataList = [vroot]
    },
    // 下拉菜单
    handleCommand(command) {
      const [i, node, data] = command
      console.log(node, data, '点击下拉菜单 handleCommand ~~~')
      if (i === 1) {
        // 弹出组织填写对话框
        // node节点对象，data当前节点数据
        this.addForm.parent = data.id
        this.addForm.parentName = data.name
        this.addDialogVisible = true
      } else if (i === 2) {
        // 分组删除
        this.delOrg(data)
      } else if (i === 3) {
        // 增加主机
        this.addHostForm.org = data.id
        this.addHostForm.parentName = data.name
        this.addHostDialogVisible = true
      }
    },
    // 新增分组
    add(formName) {
      this.$refs[formName].validate(async valid => {
        if (valid) {
          console.log(this.addForm, '---')
          const { data: response } = await this.$http.post('jumpserver/orgs/', this.addForm)
          if (response.code) {
            return this.$message.error(response.message)
          }
          console.log(response)
          this.addDialogVisible = false
          this.getList()
        }
      })
    },
    // 删除分组
    delOrg(data) {
      console.log('删除分组', data)
      const { id, name } = data
      this.$confirm('此操作将永久删除该分组及子分组，以及其下所有主机<br/>是否继续?', `删除分组 ${name}`, {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'error',
        dangerouslyUseHTMLString: true
      })
        .then(async () => {
          // 后台调用update, 逻辑删除
          const { data: response } = await this.$http.delete(`/jumpserver/orgs/${id}/`)
          if (response.code) {
            return this.$message.error(response.message)
          }
          this.$message({
            type: 'success',
            message: '删除成功!'
          })
          this.getList()
          this.getHostList()
        })
        .catch(() => {})
    },
    // 文件上传/移除
    handleRemove(file, fileList) {
      console.log(file, fileList)
      // this.fileList = []
      this.addHostForm.ssh_pkey_path = ''
    },
    handlePreview(file) {
      console.log(file)
    },
    handleExceed(files, fileList) {
      this.$message.warning(
        `当前限制选择 1 个文件，本次选择了 ${files.length} 个文件，共选择了 ${files.length + fileList.length} 个文件`
      )
    },
    beforeRemove(file, fileList) {
      console.log(file) // 本次文件对象
      console.log(fileList) // 增加后文件列表
      console.log(this.fileList) // this的，初始定义的
      return this.$confirm(`确定移除 ${file.name}？`)
    },
    handleSuccess(response, file, fileList) {
      console.log(response)
      console.log(file.response === response)
      console.log(fileList[0] === file)
      // this.fileList = [response]
      this.addHostForm.ssh_pkey_path = response.url
    },
    // 上传文件添加token
    getheader() {
      return { Authorization: 'JWT ' + window.localStorage.getItem('token') }
    },
    // 新增主机
    addHost() {
      const name = 'addHost'
      this.$refs[name].validate(async valid => {
        if (valid) {
          const { data: response } = await this.$http.post('jumpserver/hosts/', this.addHostForm)
          if (response.code) {
            // 失败(非0，有code)
            return this.$message.error(response.message)
          }
          this.addHostDialogVisible = false
          this.resetForm(name)
          this.getHostList()
        }
      })
    },
    // 点击节点返回主机, Tree回调事件
    handleNodeClick(data, node, c) {
      // console.log(data)
      const { id: org } = data
      this.getHostList(1, org)
    },
    async getHostList(page = 1, org) {
      if (!page) {
        page = 1
      }
      // 返回列表页数据，填充table表格
      // jumpserver/hosts/?page=1&org=<id>
      const { data: response } = await this.$http.get('jumpserver/hosts/', {
        params: {
          page,
          org
        }
      })
      if (response.code) {
        return this.$message.error(response.message)
      }
      this.pagination = response.pagination
      this.hostList = response.results
    }
  }
}
</script>

<style lang="less" scoped>
.el-tree {
  background-color: #fafafa;
  min-height: 300px;
}
.custom-tree-node {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
  padding-right: 8px;
}
.el-tooltip .el-button {
  margin-right: 10px;
}
</style>
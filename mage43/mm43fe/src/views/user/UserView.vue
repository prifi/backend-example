<template>
  <div>
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>用户管理</el-breadcrumb-item>
      <el-breadcrumb-item>用户列表</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card>
      <el-row :gutter="10">
        <el-col :span="6">
          <el-input placeholder="请输入内容" v-model="search" @keyup.enter.native="getList(1)">
            <el-button slot="append" icon="el-icon-search" @click="getList(1)"></el-button>
          </el-input>
        </el-col>
        <el-col :span="6">
          <el-button type="primary" @click="addDialogVisible = true">添加用户</el-button>
        </el-col>
      </el-row>
      <el-table border stripe :data="dataList" style="width: 100%">
        <el-table-column prop="id" label="ID" width="70"></el-table-column>
        <el-table-column prop="username" label="姓名"> </el-table-column>
        <el-table-column prop="email" label="邮箱"> </el-table-column>
        <el-table-column prop="phone" label="电话"> </el-table-column>
        <el-table-column prop="is_active" label="激活">
          <!-- 作用域插槽 -->
          <template #default="{ row }">
            <el-switch v-model="row.is_active" @change="handleChange(row)"> </el-switch>
          </template>
        </el-table-column>
        <el-table-column prop="is_superuser" label="管理员">
          <template #default="{ row }">
            <!-- 未实现 -->
            <el-switch v-model="row.is_superuser"> </el-switch>
          </template>
        </el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <!-- 禁止删除id为1的管理员(不展示) -->
            <el-tooltip v-if="scope.row.id !== 1" content="分配角色" placement="bottom" effect="light">
              <el-button size="mini" type="primary" icon="el-icon-setting" @click="handleSetRole(scope.row)"></el-button>
            </el-tooltip>
            <el-tooltip v-if="scope.row.id !== 1" :content="'编辑 ' + scope.row.username" placement="bottom" effect="light">
              <el-button size="mini" type="success" icon="el-icon-edit" @click="handleEdit(scope.row)"></el-button>
            </el-tooltip>
            <el-tooltip v-if="scope.row.id !== 1" :content="'删除 ' + scope.row.username" placement="bottom" effect="light">
              <el-button size="mini" type="danger" icon="el-icon-delete" @click="handleDelete(scope.row)"></el-button>
            </el-tooltip>
            <el-tooltip v-if="scope.row.id !== 1" content="重置密码" placement="bottom" effect="light">
              <el-button size="mini" type="warning" icon="el-icon-refresh" @click="handleRestPwd(scope.row)"></el-button>
            </el-tooltip>
          </template>
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
    <!-- 新增 -->
    <el-dialog title="添加用户" :visible.sync="addDialogVisible" width="30%" @close="resetForm('add')">
      <el-form :model="addForm" :rules="addRules" ref="add" label-width="100px">
        <el-form-item label="用户名" prop="username">
          <el-input placeholder="请输入用户名" v-model="addForm.username"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input type="password" placeholder="请输入密码" show-password v-model="addForm.password"></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="checkPass">
          <el-input type="password" placeholder="请输入确认密码" show-password v-model="addForm.checkPass"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input type="email" placeholder="请输入邮箱" v-model="addForm.email"></el-input>
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-input type="phone" placeholder="请输入电话" v-model="addForm.phone"></el-input>
        </el-form-item>
        <!-- <el-form-item> -->
        <!-- <el-button type="primary" @click="submitForm('add')">创建</el-button> -->
        <!-- <el-button @click="resetForm('add')">重置</el-button> -->
        <!-- </el-form-item> -->
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="addDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="add('add')">确 定</el-button>
      </span>
    </el-dialog>
    <!-- 修改 -->
    <el-dialog title="修改用户" :visible.sync="editDialogVisible" width="30%" @close="resetForm('edit')">
      <el-form :model="editForm" :rules="editRules" ref="edit" label-width="100px">
        <el-form-item label="用户名" prop="username">{{ editForm.username }}</el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input type="email" placeholder="请输入邮箱" v-model="editForm.email"></el-input>
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-input type="phone" placeholder="请输入电话" v-model="editForm.phone"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="edit('edit')">确 定</el-button>
      </span>
    </el-dialog>
    <!-- 重置密码 -->
    <el-dialog title="重置密码" :visible.sync="resetPwdDialogVisible" width="30%" @close="resetForm('resetPwd')">
      <el-form :model="resetPwdForm" :rules="resetPwdRules" ref="resetPwd" label-width="100px">
        <el-form-item label="用户名">{{ resetPwdForm.username }}</el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input type="password" placeholder="新密码" show-password v-model="resetPwdForm.password"></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="checkPass">
          <el-input type="password" placeholder="确认新密码" show-password v-model="resetPwdForm.checkPass"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="resetPwdDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="resetPassword">确 定</el-button>
      </span>
    </el-dialog>
    <!-- 分配角色 -->
    <el-dialog
      :title="`[${currentUser.username}]分配权限`"
      :visible.sync="addRoleDialogVisible"
      width="30%"
      @close="resetTree"
    >
      <el-tree
        :data="roleList"
        :props="{ label: 'name' }"
        show-checkbox
        node-key="id"
        ref="tree"
        default-expand-all
        :default-checked-keys="selecdtedIds"
      ></el-tree>
      <span slot="footer" class="dialog-footer">
        <el-button @click="addRoleDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="addRole('tree')">确 定</el-button>
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
    const validatePass = (rule, value, callback) => {
      if (value !== this.addForm.password) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    }
    const validateRestPass = (rule, value, callback) => {
      if (value !== this.resetPwdForm.password) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    }
    return {
      // 搜索
      search: '',
      // 数据显示
      dataList: [],
      // 分页
      pagination: {
        total: 0,
        page: 1,
        size: 2
      },
      // 新增
      addDialogVisible: false, // 控制dialog显示/隐藏
      addForm: {
        username: '',
        password: '',
        checkPass: '',
        email: '',
        phone: ''
      },
      addRules: {
        username: [
          { required: true, message: '请输入用户名称', trigger: 'blur' },
          { min: 4, max: 16, message: '长度在 4 到 16 个字符', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 4, max: 16, message: '长度在 4 到 16 个字符', trigger: 'blur' }
        ],
        checkPass: [
          { required: true, message: '请输入确认密码', trigger: 'blur' }, // 可以使用自定义校验器实现
          { min: 4, max: 16, message: '长度在 4 到 16 个字符', trigger: 'blur' },
          { validator: validatePass, trigger: 'blur' } // 自定义校验器
        ]
      },
      // 修改
      editDialogVisible: false,
      editForm: {
        username: '',
        email: '',
        phone: ''
      },
      editRules: {},
      // 重置密码
      resetPwdDialogVisible: false,
      resetPwdForm: {
        username: '',
        password: '',
        checkPass: ''
      },
      resetPwdRules: {
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 4, max: 16, message: '长度在 4 到 16 个字符', trigger: 'blur' }
        ],
        checkPass: [
          { required: true, message: '请输入确认密码', trigger: 'blur' },
          { validator: validateRestPass, trigger: 'blur' }
        ]
      },
      // 分配角色
      addRoleDialogVisible: false,
      roleList: [],
      // defaultProps: {
      //   children: 'children',
      //   label: 'name'  写在绑定属性中
      // },
      currentUser: {},
      selecdtedIds: []
    }
  },
  methods: {
    handleCurrentChange(val) {
      // console.log(`当前页: ${val}`)
      this.getList(val)
    },
    // 关闭Dialog之前重置表单
    resetForm(formName) {
      this.$refs[formName].resetFields()
    },
    // 新增
    add(formName) {
      // 数据校验，检验通过发往后端
      this.$refs[formName].validate(async valid => {
        if (valid) {
          console.log(this.addForm, '校验成功')
          const { data: response } = await this.$http.post('users/mgr/', this.addForm)
          if (response.code) {
            // 失败(非0，有code)
            return this.$message.error(response.message)
          }
          this.addDialogVisible = false // 提交完也需要重置
          // 成功(0 undefined) -> 显示用户列表，后台拿数据
          this.getList()
        }
      })
    },
    // 返回列表页
    async getList(page = 1) {
      if (!page) {
        page = 1
      }
      // 返回列表页数据，填充table表格
      const { data: response } = await this.$http.get('users/mgr/', {
        params: {
          page,
          // username: this.search
          search: this.search
        }
      })
      if (response.code) {
        return this.$message.error(response.message)
      }
      // console.log(response) // {pagination: {total, page, size}, results}
      this.pagination = response.pagination
      this.dataList = response.results
    },
    // 激活
    async handleChange(row) {
      // 激活按钮变化，修改后台值
      const { data: response } = await this.$http.patch(`users/mgr/${row.id}/`, {
        is_active: row.is_active
      })
      if (response.code) {
        return this.$message.error(response.message)
      }
      // 更新完强制刷新当前页
      this.getList(this.pagination.page)
    },
    // 修改
    handleEdit(row) {
      const { id, username, email, phone } = row // 解构，节约对象
      this.editForm = { id, username, email, phone }
      this.editDialogVisible = true
    },
    edit(formName) {
      this.$refs[formName].validate(async valid => {
        if (valid) {
          const { data: response } = await this.$http.patch(`/users/mgr/${this.editForm.id}/`, this.editForm)
          if (response.code) {
            return this.$message.error(response.message)
          }
          this.editDialogVisible = false
          this.getList(this.pagination.page) // 刷新用户列表
        }
      })
    },
    // 删除
    handleDelete(row) {
      this.$confirm('此操作将永久删除该用户, 是否继续?', `删除用户 ${row.username}`, {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(async () => {
          const { data: response } = await this.$http.delete(`/users/mgr/${row.id}/`)
          if (response.code) {
            return this.$message.error(response.message)
          }
          this.$message({
            type: 'success',
            message: '删除成功!'
          })
          this.getList()
        })
        .catch(() => {})
    },
    // 重置密码
    handleRestPwd(row) {
      const { id, username, password, checPass } = row
      this.resetPwdForm = { id, username, password, checPass }
      this.resetPwdDialogVisible = true
    },
    resetPassword() {
      const formName = 'resetPwd'
      const { id, password } = this.resetPwdForm
      this.$refs[formName].validate(async valid => {
        if (valid) {
          const { data: response } = await this.$http.post(`users/mgr/${id}/setpwd/`, { password })
          if (response.code) {
            return this.$message.error(response.message)
          }
          this.resetPwdDialogVisible = false
          this.$message.success('密码修改成功')
        }
      })
    },
    // 分配角色
    async handleSetRole(row) {
      const { id } = row
      const { data: response } = await this.$http.get(`users/mgr/${id}/roles/`)
      if (response.code) {
        return this.$message.error(response.message)
      }
      this.roleList = response.allRoles
      this.selecdtedIds = response.roles
      this.currentUser = row
      this.addRoleDialogVisible = true
    },
    async addRole(formName) {
      const roles = this.$refs[formName].getCheckedKeys()
      const { id } = this.currentUser
      const { data: response } = await this.$http.put(`users/mgr/${id}/roles/`, { roles })
      if (response.code) {
        return this.$message.error(response.message)
      }
      this.getList()
      this.addRoleDialogVisible = false
    },
    resetTree() {
      this.roleList = []
      this.selecdtedIds = []
      this.currentUser = {}
    }
  }
}
</script>

<style>
</style>
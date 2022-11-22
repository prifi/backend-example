<template>
  <div>
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>角色管理</el-breadcrumb-item>
      <el-breadcrumb-item>角色列表</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card>
      <el-row :gutter="10">
        <el-col :span="6">
          <el-input placeholder="请输入内容" v-model="search" @keyup.enter.native="getList(1, action)">
            <el-button slot="append" icon="el-icon-search" @click="getList(1, action)"></el-button>
          </el-input>
        </el-col>
        <el-col :span="6">
          <el-button type="primary" @click="addDialogVisible = true">添加角色</el-button>
        </el-col>
      </el-row>
      <el-table border stripe :data="dataList" style="width: 100%">
        <el-table-column prop="id" label="ID" width="70"></el-table-column>
        <el-table-column prop="name" label="名称"> </el-table-column>
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-tooltip content="分配权限" placement="bottom" effect="light">
              <el-button size="mini" type="primary" icon="el-icon-setting" @click="handleSetPerm(scope.row)"></el-button>
            </el-tooltip>
            <el-tooltip content="编辑" placement="bottom" effect="light">
              <el-button size="mini" type="success" icon="el-icon-edit" @click="handleEdit(scope.row)"></el-button>
            </el-tooltip>
            <el-tooltip content="删除" placement="bottom" effect="light">
              <el-button size="mini" type="danger" icon="el-icon-delete" @click="handleDelete(scope.row)"></el-button>
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
    <!-- 添加 -->
    <el-dialog title="添加角色" :visible.sync="addDialogVisible" width="30%" @close="resetForm('add')">
      <el-form :model="addForm" :rules="addRules" ref="add" label-width="100px">
        <el-form-item label="角色名" prop="name">
          <el-input placeholder="请输入角色名称" v-model="addForm.name"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="addDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="add('add')">确 定</el-button>
      </span>
    </el-dialog>
    <!-- 修改 -->
    <el-dialog title="修改角色" :visible.sync="editDialogVisible" width="30%" @close="resetForm('edit')">
      <el-form :model="editForm" :rules="editRules" ref="edit" label-width="100px">
        <el-form-item label="角色名" prop="name">
          <el-input placeholder="请输入角色名称" v-model="editForm.name"></el-input>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="edit('edit')">确 定</el-button>
      </span>
    </el-dialog>
    <!-- 分配权限 -->
    <el-dialog :title="`[${currentRole.name}]分配权限`" :visible.sync="addPermDialogVisible" width="30%" @close="resetTree">
      <el-tree
        :data="permList"
        :props="defaultProps"
        show-checkbox
        node-key="id"
        ref="tree"
        default-expand-all
        :default-checked-keys="selecdtedIds"
      ></el-tree>
      <span slot="footer" class="dialog-footer">
        <el-button @click="addPermDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="addPerm('tree')">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { resetFormMixin, paginationMixin, getListMixin, addMixin, editMixin, delteMixin } from '../../mixins'
export default {
  mixins: [resetFormMixin, paginationMixin, getListMixin, addMixin, editMixin, delteMixin],
  created() {
    this.getList(1, 'users/roles/')
  },
  data() {
    return {
      // 列表
      action: 'users/roles/',
      // 添加
      addForm: {
        name: ''
      },
      addRules: {
        name: [
          { required: true, message: '请输入名称', trigger: 'blur' },
          { min: 4, max: 16, message: '长度在 4 到 16 个字符', trigger: 'blur' }
        ]
      },
      // 修改
      editForm: {
        name: ''
      },
      editRules: {
        name: [
          { required: true, message: '请输入名称', trigger: 'blur' },
          { min: 4, max: 16, message: '长度在 4 到 16 个字符', trigger: 'blur' }
        ]
      },
      // 分配权限
      addPermDialogVisible: false,
      permList: [], // 放置对象{}, 下一级children, label 对象的什么属性显示节点名字
      defaultProps: {
        children: 'children',
        label: 'name'
      },
      currentRole: {},
      selecdtedIds: []
    }
  },
  methods: {
    // CRUD Mixin
    // 修改
    handleEdit(row) {
      const { id, name } = row // 解构
      this.editForm = { id, name }
      this.editDialogVisible = true
    },
    // 分配权限
    async handleSetPerm(row) {
      const { id } = row
      const { data: response } = await this.$http.get(`users/roles/${id}/perms/`) // 获取某个角色的权限 -> users/roles/100/perms/, 增加全部权限字段 allPers
      if (response.code) {
        return this.$message.error(response.message)
      }
      this.permList = response.allPerms
      this.selecdtedIds = response.permissions
      this.currentRole = row
      this.addPermDialogVisible = true
    },
    async addPerm(formName) {
      const permissions = this.$refs[formName].getCheckedKeys() // 获取tree选择perms id列表
      const { id } = this.currentRole
      const { data: response } = await this.$http.patch(`users/roles/${id}/`, { permissions }) // 更新权限 -> users/roles/100/
      if (response.code) {
        return this.$message.error(response.message)
      }
      this.getList()
      this.addPermDialogVisible = false
    },
    resetTree() {
      this.currentRole = {}
      this.selecdtedIds = []
      this.permList = []
    }
  }
}
</script>

<style>
</style>
<template>
  <div>
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>资产管理</el-breadcrumb-item>
      <el-breadcrumb-item>资产列表</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card>
      <el-row :gutter="10">
        <el-col :span="6">
          <el-input placeholder="请输入内容" v-model="search" @keyup.enter.native="getList(1, action)">
            <el-button slot="append" icon="el-icon-search" @click="getList(1, action)"></el-button>
          </el-input>
        </el-col>
        <el-col :span="6">
          <el-button type="primary" @click="addDialogVisible = true">添加资产</el-button>
        </el-col>
      </el-row>
      <el-table border stripe :data="dataList" style="width: 100%">
        <el-table-column prop="id" label="ID"></el-table-column>
        <el-table-column prop="fields.0.value" label="资产名称"> </el-table-column>
        <!-- 插槽方式获取字段 -->
        <!-- <el-table-column label="名称">
          <template #default="{ row }">
            {{ row.fields[0].value }}
          </template>
        </el-table-column> -->
        <el-table-column prop="name" label="资产类型"></el-table-column>
        <el-table-column prop="version" label="资产版本"></el-table-column>
        <el-table-column label="操作">
          <el-tooltip content="编辑" placement="bottom" effect="light">
            <el-button size="mini" type="success" icon="el-icon-edit"></el-button>
          </el-tooltip>
          <el-tooltip content="删除" placement="bottom" effect="light">
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
    <!-- 添加 -->
    <el-dialog title="添加资产" :visible.sync="addDialogVisible" width="50%" @close="resetForm('add')">
      <el-form :model="addForm" :rules="addRules" ref="add" label-width="100px">
        <el-form-item label="资产类型" prop="citype">
          <el-select v-model="addForm.citype" placeholder="请选择资产类型" @change="handleCiTypeChange">
            <el-option v-for="c in citypes" :key="c.id" :label="c.label" :value="c.id"></el-option>
          </el-select>
        </el-form-item>
        <!-- 根据上面选择的资产类型，动态增加表单项 -->
        <el-form-item
          v-for="(f, index) in addForm.fields"
          :label="f.label"
          :key="f.name"
          :prop="'fields.' + index + '.value'"
          :rules="
            f.required
              ? {
                  required: true,
                  message: f.label + '不能为空',
                  trigger: 'blur'
                }
              : {}
          "
        >
          <el-input v-if="f.type === 'str'" v-model="f.value"></el-input>
          <!-- 日期类型？ -->
          <!-- <div class="block" v-if="f.type === 'date'">
            <el-date-picker
              v-model="f.value"
              type="date"
              placeholder="选择日期"
              format="yyyy 年 MM 月 dd 日"
              value-format="yyyy-MM-dd HH:mm:ss"
            ></el-date-picker>
          </div> -->
          <div v-else-if="f.type.startsWith('list:')">
            List:Network Intface
            <el-button icon="el-icon-plus" plain type="priamy" size="mini" @click="handleAddChild(f)"></el-button>
            <el-card v-for="(c, i) in f.children" :key="`${f.name}.children.${i}`">
              <!-- {{ c }}---{{ i }} -->
              <el-form-item
                v-for="(s, j) in c.fields"
                :label="s.label"
                :key="s.name"
                :prop="'fields.' + index + '.children.' + i + '.fields.' + j + '.value'"
                :rules="
                  s.required
                    ? {
                        required: true,
                        message: s.label + '不能为空',
                        trigger: 'blur'
                      }
                    : {}
                "
              >
                <el-input v-if="s.type === 'str'" v-model="s.value"></el-input>
              </el-form-item>
            </el-card>
          </div>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="addDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="add('add')">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  created() {
    this.getList(1, 'cmdb/cis/')
    this.getCitypeList()
  },
  data() {
    return {
      action: 'cmdb/cis/',
      // 添加
      addDialogVisible: false,
      addForm: {
        citype: '',
        fields: []
      },
      addRules: {
        citype: [{ required: true, message: '请输入资产类型', trigger: 'blur' }]
      },
      // 数据展示
      dataList: [],
      citypes: [],
      // 分页
      pagination: {
        total: 0,
        page: 1,
        size: 2
      },
      // 搜索
      search: ''
    }
  },
  methods: {
    resetForm(formName) {
      this.$refs[formName].resetFields()
      this.addForm.fields = []
    },
    handleCurrentChange(val) {
      this.getList(val)
    },
    async getList(page = 1, action = this.action) {
      if (!page) {
        page = 1
      }
      // 返回列表页数据，填充table表格
      const { data: response } = await this.$http.get(action, {
        params: {
          page,
          search: this.search
        }
      })
      if (response.code) {
        return this.$message.error(response.message)
      }
      this.pagination = response.pagination
      this.dataList = response.results
    },
    // 查询资产类型列表
    async getCitypeList() {
      // 返回所有资产类型(搜索关键字），不分页； 或者使用树状结构懒加载
      const { data: response } = await this.$http.get('/cmdb/citypes/all/')
      if (response.code) {
        return this.$message.error(response.message)
      }
      this.citypes = response
    },
    // Select触发事件，获取类型fields列表
    async handleCiTypeChange(id) {
      // 拿到ID字段，返回带fields的数据
      // console.log(this.addForm.citype)
      // console.log(args)
      const { data: response } = await this.$http.get(`/cmdb/citypes/${id}/`) // 详情页
      if (response.code) {
        return this.$message.error(response.message)
      }
      // this.addForm.fields = response.fields
      this.$set(this.addForm, 'fields', response.fields) // 反应式对象
      this.addForm.name = response.name
      this.addForm.version = response.version
      this.addForm.label = response.label
      console.log(this.addForm.fields, 'handleCiTypeChange ~~~')
    },
    // 增加子网络接口
    async handleAddChild(currentField) {
      // 返回字段类型 list:Network Interface:1 带最新版本号去后台查询类型字段定义
      const [, name, version = 1] = currentField.type.split(':')
      const { data: response } = await this.$http.get(`/cmdb/citypes/${name}/${version}/`)
      if (response.code) {
        return this.$message.error(response.message)
      }
      if ('children' in currentField === false) {
        this.$set(currentField, 'children', [])
      }
      currentField.children.push(response)
      console.log(this.addForm, 'handleAddChild ~~~')
    },
    // 增加资产列表
    add(formName) {
      this.$refs[formName].validate(async valid => {
        if (valid) {
          console.log(this.addForm, 'add ~~~')
          const { data: response } = await this.$http.post('/cmdb/cis/', this.addForm)
          if (response.code) {
            return this.$message.error(response.message)
          }
          console.log(response, 'add ~~~')
          // this.resetForm(formName)
          this.addDialogVisible = false
          this.getList()
        }
      })
    }
  }
}
</script>

<style lang="less" scoped>
.el-form-item .el-form-item {
  margin-bottom: 22px;
}
</style>
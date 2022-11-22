<template>
  <div>
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>资产管理</el-breadcrumb-item>
      <el-breadcrumb-item>资产类型</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card>
      <el-table border stripe :data="dataList" style="width: 100%">
        <el-table-column prop="id" label="ID"></el-table-column>
        <el-table-column prop="version" label="版本"></el-table-column>
        <el-table-column prop="label" label="名称"> </el-table-column>
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
  </div>
</template>

<script>
export default {
  created() {
    this.getList(1, 'cmdb/citypes/')
  },
  data() {
    return {
      action: 'cmdb/citypes/',
      dataList: [],
      pagination: {
        total: 0,
        page: 1,
        size: 2
      }
    }
  },
  methods: {
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
    }
  }
}
</script>

<style>
</style>
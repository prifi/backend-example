<template>
  <div>
    <el-breadcrumb separator="/">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>权限管理</el-breadcrumb-item>
      <el-breadcrumb-item>权限列表</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card>
      <el-row :gutter="10">
        <el-col :span="6">
          <el-input placeholder="请输入内容" v-model="search" @keyup.enter.native="getList(1, action)">
            <el-button slot="append" icon="el-icon-search" @click="getList(1, action)"></el-button>
          </el-input>
        </el-col>
      </el-row>
      <el-table border stripe :data="dataList" style="width: 100%">
        <el-table-column prop="id" label="ID" width="70"></el-table-column>
        <el-table-column prop="name" label="名称"> </el-table-column>
        <el-table-column prop="app_label" label="应用"> </el-table-column>
        <el-table-column prop="model" label="模型"> </el-table-column>
        <el-table-column prop="codename" label="标识"> </el-table-column>
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
import { resetFormMixin, paginationMixin, getListMixin } from '../../mixins'
export default {
  mixins: [resetFormMixin, paginationMixin, getListMixin],
  created() {
    this.getList(1, 'users/perms/')
  },
  data() {
    return {
      action: 'users/perms/'
    }
  },
  methods: {}
}
</script>

<style>
</style>
// 重置
const resetFormMixin = {
  methods: {
    resetForm(formName) {
      this.$refs[formName].resetFields()
    }
  }
}

// 分页
const paginationMixin = {
  data() {
    return {
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
    }
  }
}

// 获取列表
const getListMixin = {
  data() {
    return {
      search: '',
      dataList: []
    }
  },
  methods: {
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

// 添加
const addMixin = {
  data() {
    return {
      addDialogVisible: false
    }
  },
  methods: {
    add(formName) {
      this.$refs[formName].validate(async valid => {
        if (valid) {
          const { data: response } = await this.$http.post(this.action, this.addForm)
          if (response.code) {
            return this.$message.error(response.message)
          }
          this.addDialogVisible = false
          this.getList()
        }
      })
    }
  }
}

// 编辑
const editMixin = {
  data() {
    return {
      editDialogVisible: false
    }
  },
  methods: {
    edit(formName) {
      this.$refs[formName].validate(async valid => {
        if (valid) {
          const { data: response } = await this.$http.patch(`${this.action}${this.editForm.id}/`, this.editForm)
          if (response.code) {
            return this.$message.error(response.message)
          }
          this.editDialogVisible = false
          this.getList(this.pagination.page)
        }
      })
    }
  }
}

// 删除
const delteMixin = {
  methods: {
    // 删除
    handleDelete(row) {
      this.$confirm('此操作将永久删除该用户, 是否继续?', '删除', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(async () => {
          const { data: response } = await this.$http.delete(`${this.action}${row.id}/`)
          if (response.code) {
            return this.message.error(response.message)
          }
          this.$message({
            type: 'success',
            message: '删除成功!'
          })
          this.getList()
        })
        .catch(() => {})
    }
  }
}

export { resetFormMixin, paginationMixin, getListMixin, addMixin, editMixin, delteMixin }
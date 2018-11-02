<template>
<div class="app-container">
  <div>
    <div class="key-search">
    <el-button type="primary" @click="centerDialogVisible = true" size="small">添加密钥</el-button>
    <el-dialog :visible.sync="centerDialogVisible" width="40%" :title="title" center>
  <el-form label-width="100px" size="small" ref="keyForm" :model="addkey">
    <el-form-item label="名称:" prop="name">
      <el-input v-model="addkey.name"></el-input>
    </el-form-item>
    <el-form-item label="用户名:" prop="username">
      <el-input v-model="addkey.username" ></el-input>
    </el-form-item>
    <el-form-item label="私钥保存路径:" prop="keyPath">
      <el-input v-model="addkey.keyPath" placeholder="私钥保存路径"></el-input>
    </el-form-item>
    <el-form-item label="私钥密码:" prop="password">
      <el-input v-model="addkey.password"></el-input>
    </el-form-item>
    <el-form-item label="创建时间:" prop="createTime">
      <el-input v-model="addkey.createTime" :disabled="true"></el-input>
    </el-form-item>
    <el-form-item label="修改时间:" prop="changeTime">
      <el-input v-model="addkey.changeTime" :disabled="true" ></el-input>
    </el-form-item>
  </el-form>
  <span slot="footer" class="dialog-footer">
    <el-button @click="centerDialogVisible = false">取 消</el-button>
    <el-button type="primary" @click="addkeySubmit">确 定</el-button>
  </span>
</el-dialog>
   <el-autocomplete v-model="state4" :fetch-suggestions="querySearchAsync" placeholder="请输入查询内容" @select="handleSelect" 
   aria-setsize="small"
  prefix-icon="el-icon-search" value-key="ip"
></el-autocomplete>
    </div>
    <div class="key-table">
  <el-table
    :data="tableData.list"
    style="width: 100%">
    <el-table-column
      prop="name"
      label="名称"
      sortable
      width="180"
    >
    </el-table-column>
    <el-table-column
      prop="username"
      label="用户名"
      width="130">
    </el-table-column>
    <el-table-column
      prop="keyPath"
      label="路径"
      width="150">
    </el-table-column >
    <el-table-column
      prop="password"
      label="密码"
      width="90">
    </el-table-column >
    <el-table-column
      prop="createTime"
      label="创建时间"
      width="180">
    </el-table-column >
    <el-table-column
      prop="changeTime"
      label="修改时间"
      width="180">
    </el-table-column >
    <el-table-column label="操作">
      <template slot-scope="scope">
        <el-button size="mini" @click="editSubmit(scope.row.id, tableData)">编辑</el-button>

    <el-button @click="removeSubmit(scope.row.id, tableData)" size="mini" type="danger" >删除</el-button>
        </template>
    </el-table-column>
  </el-table>
    </div>
      <div class="block">
    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="searchOption.page"
      :page-sizes="[5,10,20]"
      :page-size="searchOption.size"
      layout="total, sizes, prev, pager, next, jumper"
      :total="tableData.total">
    </el-pagination>
      </div>
  </div>
</div>
</template>

<script>
  import request from '@/utils/request'
  import { deepClone } from '@/utils'
  const sT = {
    id: '',
    name: '',
    username: '',
    keyPath: '',
    password: 'NULL'
  }
  export default {
    data() {
      return {
        visible2: false,
        centerDialogVisible: false,
        value4: false,
        textarea: '',
        restaurants: [],
        state4: '',
        tableData: {},
        tableData1: {},
        searchOption: {
          size: 10,
          page: 1
        },
        addkey: deepClone(sT)
      }
    },
    computed: {
      title: function() {
        return this.addkey.id ? '编辑密钥' : '添加密钥'
      }
    },
    watch: {
      searchOption: {
        deep: true,
        handler: function(val, olval) {
          this.showkey()
        }
      },
      centerDialogVisible: function(val, oldvale) {
        if (!val) {
          // this.$refs['keyForm'].resetFields()
          this.addkey = deepClone(sT)
        }
      },
      midvisble: function(val, oldvale) {
        console.log('123')
        this.showServer()
      }
    },
    methods: {
      showServer() {
        request({
          method: 'get',
          url: 'http://127.0.0.1:8000/hostApi/',
          params: this.searchOption
        }).then(Response => {
          this.tableData1 = Response.data
        })
      },
      filterTag(value, row) {
        return row.tag === value
      },
      filterHandler(value, row, column) {
        const property = column['property']
        return row[property] === value
      },
      handleSelect(item) {
        console.log(item)
      },
      loadAll() {
        return [this.tableData]
      },
      querySearchAsync(queryString, cb) {
        var restaurants = this.restaurants
        var results = queryString ? restaurants.filter(this.createStateFilter(queryString)) : restaurants

        clearTimeout(this.timeout)
        this.timeout = setTimeout(() => {
          cb(results)
        }, 3000 * Math.random())
      },
      createStateFilter(queryString) {
        return (state) => {
          return (state.value.toLowerCase().indexOf(queryString.toLowerCase()) === 0)
        }
      },
      handleSizeChange(val) {
        this.searchOption.size = val
        console.log(`每页 ${val} 条`)
      },
      handleCurrentChange(val) {
        this.searchOption.page = val
        console.log(`当前页: ${val}`)
      },
      showkey() {
        request({
          method: 'get',
          url: 'http://127.0.0.1:8000/keyApi/',
          params: this.searchOption
        }).then(Response => {
          this.tableData = Response.data
        })
      },
      addkeySubmit() {
        if (this.addkey.id) {
          request({
            method: 'put',
            url: 'http://127.0.0.1:8000/keyApi/' + this.addkey.id + '/',
            data: this.addkey
          }).then(res => {
            this.$message.success('操作成功')
            this.centerDialogVisible = false
            this.showkey()
          })
        } else {
          request({
            method: 'post',
            url: 'http://127.0.0.1:8000/keyApi/',
            data: this.addkey
          }).then(res => {
            this.$message.success('操作成功')
            this.centerDialogVisible = false
            this.showkey()
          })
        }
      },
      removeSubmit(id, row) {
        request({
          method: 'delete',
          url: 'http://127.0.0.1:8000/keyApi/' + id + '/'
        }).then(res => {
          this.visible2 = false
          this.$message.success('删除成功')
          this.showkey()
        })
      },
      editSubmit(id, row) {
        request({
          method: 'get',
          url: 'http://127.0.0.1:8000/keyApi/' + id + '/'
        }).then(Response => {
          this.centerDialogVisible = true
          this.addkey = Response.data
        })
      }
    },
    mounted() {
      this.showkey()
      this.showServer()
      // this.restaurants = this.loadAll()
    }
  }
</script>

<style rel="stylesheet/scss" lang="scss">
    .left {
      float:left;
      width:50%;
    }
    .right {
      float:left;  
      width:50%;  
    }
    .key-search {
      margin: 10px 10px 0px 10px;
    }
    .block {
      margin-top: 10px;
      margin-left: 50%;
      }
    .el-dialog .el-form .el-form-item .el-input { 
      width: 70%;
    }
    .el-dialog h3 {
      line-height: 30px;
      color: #303133;
      margin-top: 0px;
      text-align: center;
      font-family: Helvetica Neue, Helvetica, PingFang SC, Hiragino Sans GB, Microsoft YaHei, Arial, sans-serif;
      background: #4deb4d;
    }
    .el-dialog .el-form .el-form-item .lable {
      text-align: right;
      white-space: normal;
      word-break: break-all;
      line-height: 23px;
      color: #606266;
      font-family: Helvetica Neue, Helvetica, PingFang SC, Hiragino Sans GB, Microsoft YaHei, Arial, sans-serif;
    }
    .el-dialog .el-form .el-switch {
      margin-left: 8%;
    }
    .el-dialog .span {
      margin-top: 7px;
      align-content: right;
    }
</style>

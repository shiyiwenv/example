<template>
<div class="app-container">
  <div>
    <div class="server-search">
    <el-button type="primary" @click="centerDialogVisible = true" size="small" icon="el-icon-circle-plus" round>添加主机</el-button>
    <el-dialog :visible.sync="centerDialogVisible" width="40%" :title="title" center>
      <!-- <h3>{{ title }}</h3> -->
  <el-form label-width="80px" size="small" ref="serverForm" :model="addserver">
    <el-form-item label="主机名:" prop="hostname">
      <el-input v-model="addserver.hostname"></el-input>
    </el-form-item>
    <el-form-item label="IP地址:" prop="ip">
      <el-input v-model="addserver.ip"></el-input>
    </el-form-item>
    <el-form-item label="CPU:" prop="cpusum">
      <el-input v-model="addserver.cpusum" placeholder="CPU核心数"></el-input>
    </el-form-item>
    <el-form-item label="内存:" prop="memory">
      <el-input v-model="addserver.memory"></el-input>
    </el-form-item>
    <el-form-item label="操作系统:" prop="os_version">
      <el-input v-model="addserver.os_version"></el-input>
    </el-form-item>
    <el-form-item label="机位:" prop="postion">
      <el-input v-model="addserver.postion" placeholder="BJDZ-6B1001-1" suffix-icon="el-icon-location"></el-input>
    </el-form-item>
    <el-form-item label="型号:" prop="mode">
      <el-input v-model="addserver.mode" placeholder="R720"></el-input>
    </el-form-item>
    <el-form-item label="备注:" prop="ps">
      <el-input type="textarea" :rows="2" placeholder="请输入内容" v-model="addserver.ps" size="small"></el-input>
    </el-form-item>
    <el-form-item label="运行状态:" prop="status">
      <el-switch style="display: block" v-model="addserver.status" active-color="#13ce66" inactive-color="#ff4949" active-text="运行中" inactive-text="已关机">
      </el-switch>
    </el-form-item>
  </el-form>
  <span slot="footer" class="dialog-footer">
    <el-button @click="centerDialogVisible = false">取 消</el-button>
    <el-button type="primary" @click="addserverSubmit">确 定</el-button>
  </span>
</el-dialog>
   <el-autocomplete v-model="state4" :fetch-suggestions="querySearchAsync" placeholder="请输入查询内容" @select="handleSelect" 
   aria-setsize="small"
  prefix-icon="el-icon-search" value-key="ip"
></el-autocomplete>
    </div>
    <div class="server-table">
  <el-table
    :data="tableData.list"
    style="width: 100%"
    :row-class-name="tableRowClassName">
    <el-table-column
      prop="hostname"
      label="主机名"
      sortable
      width="90"
    >
    </el-table-column>
    <el-table-column
      prop="ip"
      label="IP地址"
      width="130">
    </el-table-column>
    <el-table-column
      prop="cpusum"
      label="CPU核心数"
      width="100">
    </el-table-column >
    <el-table-column
      prop="memory"
      label="内存"
      width="90">
    </el-table-column >
    <el-table-column
      prop="os_version"
      label="操作系统"
      width="130">
    </el-table-column >
    <el-table-column
      prop="postion"
      label="机位"
      width="180">
    </el-table-column >
    <el-table-column
      prop="mode"
      label="型号"
      width="90">
    </el-table-column >
    <el-table-column
      prop="ps"
      label="备注"
      width="180">
    </el-table-column >
    <el-table-column label="操作">
      <template slot-scope="scope">
        <el-button
          size="mini"
          @click="editSubmit(scope.row.id, tableData)">编辑</el-button>
        <el-button
          size="mini"
          type="danger"
          @click="removeSubmit(scope.row.id, tableData)">删除</el-button>
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
    hostname: '',
    ip: '',
    cpusum: '',
    memory: '',
    os_version: '',
    postion: '',
    mode: '',
    ps: '',
    status: false
  }
  export default {
    data() {
      return {
        centerDialogVisible: false,
        value4: false,
        textarea: '',
        restaurants: [],
        state4: '',
        tableData: {},
        searchOption: {
          size: 10,
          page: 1
        },
        addserver: deepClone(sT)
      }
    },
    computed: {
      title: function() {
        // if (this.addserver.id) {
        //   return '编辑主机'
        // } else {
        //   return '新增主机'
        // }
        return this.addserver.id ? '编辑主机' : '添加主机'
      }
    },
    watch: {
      searchOption: {
        deep: true,
        handler: function(val, olval) {
          this.showServer()
        }
      },
      centerDialogVisible: function(val, oldvale) {
        console.log('123')
        if (!val) {
          // this.$refs['serverForm'].resetFields()
          this.addserver = deepClone(sT)
        }
      }
    },
    methods: {
      tableRowClassName({ row, rowIndex }) {
        if (row.status) {
          return ''
        } else {
          return 'shutdown-row'
        }
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
      showServer() {
        request({
          method: 'get',
          url: 'http://127.0.0.1:8000/hostApi/',
          params: this.searchOption
        }).then(Response => {
          this.tableData = Response.data
        })
      },
      addserverSubmit() {
        if (this.addserver.id) {
          request({
            method: 'put',
            url: 'http://127.0.0.1:8000/hostApi/' + this.addserver.id + '/',
            data: this.addserver
          }).then(res => {
            this.$message.success('操作成功')
            this.centerDialogVisible = false
            this.showServer()
          })
        } else {
          request({
            method: 'post',
            url: 'http://127.0.0.1:8000/hostApi/',
            data: this.addserver
          }).then(res => {
            this.$message.success('操作成功')
            this.centerDialogVisible = false
            this.showServer()
          })
        }
      },
      removeSubmit(id, row) {
        request({
          method: 'delete',
          url: 'http://127.0.0.1:8000/hostApi/' + id + '/'
        }).then(res => {
          this.$message.success('删除成功')
          this.showServer()
        })
      },
      editSubmit(id, row) {
        request({
          method: 'get',
          url: 'http://127.0.0.1:8000/hostApi/' + id + '/'
        }).then(Response => {
          this.centerDialogVisible = true
          this.addserver = Response.data
        })
      }
    },
    mounted() {
      this.showServer()
      this.restaurants = this.loadAll()
    }
  }
</script>

<style rel="stylesheet/scss" lang="scss">
    .server-search {
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
    .el-table .shutdown-row{
      background: hsl(60, 4%, 69%);
    }
    .el-dialog .el-form .el-switch {
      margin-left: 8%;
    }
    .el-dialog .span {
      margin-top: 7px;
      align-content: right;
    }
</style>

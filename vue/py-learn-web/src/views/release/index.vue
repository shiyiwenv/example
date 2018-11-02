<template>
<div class="app-container">
      <div class="project-search">
          <el-button type="primary" @click="releasediglog = true" size="small" icon="el-icon-circle-plus" round>添加发布</el-button>
      </div>
  <el-dialog :visible.sync="releasediglog" width="50%" title="发布项目" :modal="false" center>
          <el-form label-width="100px" size="small" ref="projectForm" :model="tableData">
            <el-form-item label="项目名:" prop="name">
              <el-select v-model="tableData.name" placeholder="请选择" style="width:40%">
                <el-option v-for="name in tableData.list" :key="name.id" :label="name.name" :value="name.id">
                </el-option>
              </el-select>
            </el-form-item>
          </el-form>
          <span slot="footer" class="dialog-footer">
            <el-button size="mini" @click="releasediglog = false">取 消</el-button>
            <el-button size="mini" type="primary" @click="releaseSubmit(tableData.name)">发布</el-button>
          </span>
  </el-dialog>
  <el-dialog :visible.sync="centerDialogVisible" width="50%" :title="title" :modal="false" center>
          <el-input type="textarea" :rows="15" v-model="tasklog.log"></el-input>
  </el-dialog>
  <div>
      <!-- 项目列表 -->
      <div class="project-table">
        <el-table :data="taskData.list" style="width: 100%">
          <el-table-column prop="project" label="项目" sortable width="90" > </el-table-column>
          <el-table-column prop="percentage" label="发布状态"  width="130"> 
            <template slot-scope="scope" >
              <el-progress type="circle" :percentage="scope.row.percentage" :width="40" :perstatus="scope.row.perstatus"></el-progress>
            </template>
          </el-table-column>
          <el-table-column prop="execUser" label="执行用户" width="150"> </el-table-column >
          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-button size="mini" @click="showlog(scope.row.id, taskData)">查看日志</el-button>
              <el-button @click="removeSubmit(scope.row.id, taskData)" size="mini" type="danger" >取消</el-button>
              </template>
          </el-table-column>
        </el-table>
      </div>
<!-- 分页 -->
      <div class="block">
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="searchOption.page"
          :page-sizes="[5,10,20]"
          :page-size="searchOption.size"
          layout="total, sizes, prev, pager, next, jumper"
          :total="taskData.total">
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
    log: '',
    percentage: '',
    project: '',
    execUser: ''
  }
  export default {
    data() {
      return {
        perstatus: '',
        data: [],
        visible2: false,
        releasediglog: false,
        centerDialogVisible: false,
        value4: false,
        textarea: '',
        restaurants: [],
        tasklog: '',
        tableData: {},
        tableData1: {},
        taskData: {},
        addtask: {},
        searchOption: {
          size: 10,
          page: 1
        },
        addproject: deepClone(sT)
      }
    },
    computed: {
      title: function() {
        return this.tasklog.id ? '日志控制台' : '添加项目'
      }
    },
    watch: {
      searchOption: {
        deep: true,
        handler: function(val, olval) {
          this.showproject()
        }
      },
      centerDialogVisible: function(val, oldvale) {
        if (!val) {
          // this.$refs['projectForm'].resetFields()
          this.addproject = deepClone(sT)
        }
      }
    },
    methods: {
      showproject() {
        request({
          method: 'get',
          url: 'http://127.0.0.1:8000/ProApi/',
          params: this.searchOption
        }).then(Response => {
          this.tableData = Response.data
        })
      },
      showtask() {
        request({
          method: 'get',
          url: 'http://127.0.0.1:8000/TaskApi/',
          params: this.searchOption
        }).then(Response => {
          this.taskData = Response.data
          if (this.taskData.list.percentage === 0) {
            this.perstatus = 'exception'
          } else if (this.taskData.list.percentage === 100) {
            this.perstatus = 'success'
          }
        })
      },
      showlog(id, row) {
        request({
          method: 'get',
          url: 'http://127.0.0.1:8000/TaskApi/' + id + '/',
          params: this.searchOption
        }).then(Response => {
          this.centerDialogVisible = true
          this.tasklog = Response.data
        }
        )
      },
      releaseSubmit(id) {
        request({
          method: 'post',
          url: 'http://127.0.0.1:8000/ProApi/' + id + '/buildjob/'
        }).then(Response => {
          this.releasediglog = false
          this.addtask = Response.data
          console.log(this.addtask)
          // request({
          //   method: 'post',
          //   url: 'http://127.0.0.1:8000/oldtaskApi/',
          //   data: {
          //     projectid: Response.data.id,
          //     name: Response.data.name,
          //     version: Response.data.defaultBranch,
          //     gitversion: Response.data.gitVersion,
          //     email: Response.data.pushMessage,
          //     servers: Response.data.postServer,
          //     repertory: Response.data.gitAddress,
          //     // before_secretkey:
          //     before_server: Response.data.preserver,
          //     // before_port
          //     // before_user
          //     before_script: Response.data.preScriptPath,
          //     // before_config  预处理配置
          //     // before_include 依赖模块
          //     // channel_secretkey 中转服务器key
          //     channel_server: Response.data.middleServer,
          //     channel_port: 22022,
          //     // channel_user
          //     // after_secretkey
          //     // after_user
          //     // after_port
          //     after_script: Response.data.postScriptPath
          //   }
          // })
        })
      },
      handleSizeChange(val) {
        this.searchOption.size = val
        console.log(`每页 ${val} 条`)
      },
      handleCurrentChange(val) {
        this.searchOption.page = val
        console.log(`当前页: ${val}`)
      }
    },
    mounted() {
      this.showproject()
      this.showtask()
    }
  }
</script>

<style rel="stylesheet/scss" lang="scss">
    .app-container {
      width: 85%
    }
    .notify1 {
      width: 15%;
    }
    .left {
      float:left;
      width:50%;
    }
    .right {
      float:left;  
      width:50%;  
    }
    .project-search {
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

<template>
<div class="app-container">
<el-dialog :visible.sync="centerDialogVisible" width="60%" :title="title" center top="4%">
    <el-form label-width="100px" size="small" ref="projectForm" :model="addproject">
      <div class="left">
        <el-form-item label="项目名:" prop="name">
          <el-input v-model="addproject.name"></el-input>
        </el-form-item>
        <el-form-item label="数据源:" prop="gitAddress">
          <el-input v-model="addproject.gitAddress"></el-input>
        </el-form-item>
        <el-form-item label="Git分支:" prop="gitVersion">
          <el-input v-model="addproject.gitVersion" placeholder="Git分支"></el-input>
        </el-form-item>
        <el-form-item label="回滚版本:" prop="RocllgitVersion">
          <el-input v-model="addproject.RocllgitVersion"></el-input>
        </el-form-item>
        <el-form-item label="默认版本:" prop="defaultBranch">
          <el-input v-model="addproject.defaultBranch"></el-input>
        </el-form-item>
        <el-form-item label="中转服务器:" prop="middleServer">
          <el-select v-model="addproject.middleServer" placeholder="请选择" style="width:70%">
            <el-option v-for="middleServer in tableData1.list" :key="middleServer.id" :label="middleServer.hostname" :value="middleServer.id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="预处理服务器:" prop="preServer">
          <el-select v-model="addproject.preServer" placeholder="请选择" style="width:70%">
            <el-option v-for="preServer in tableData1.list" :key="preServer.id" :label="preServer.hostname" :value="preServer.id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="目标key:" prop="dstServerKey">
          <el-select v-model="addproject.dstServerKey" placeholder="请选择" style="width:70%">
            <el-option v-for="dstServerKey in tableDatakey.list" :key="dstServerKey.id" :label="dstServerKey.name" :value="dstServerKey.id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="更新后脚本:" prop="postScriptPath">
          <el-input v-model="addproject.postScriptPath"></el-input>
        </el-form-item>
        <el-form-item label="备份路径:" prop="backupPath">
          <el-input v-model="addproject.backupPath"></el-input>
        </el-form-item>
        <el-form-item label="预处理脚本:" prop="preScriptPath">
          <el-button size="mini" type="info" @click="afterscriptdialog = true" icon="el-icon-edit" round>编辑脚本</el-button>
        </el-form-item>
      </div>
      <div class="right">
          <el-form-item label="排除列表:" prop="excludeList">
            <el-input type="textarea" :rows="4" placeholder="相对路径" v-model="addproject.excludeList" style="width:70%"></el-input>
          </el-form-item>
          <el-form-item label="推送通知:" prop="pushMessage">
            <el-input v-model="addproject.pushMessage"></el-input>
          </el-form-item>
          <el-form-item label="服务器端口:" prop="serverPort">
            <el-input-number v-model="addproject.serverPort" controls-position="right" size="small" style="width:50%"></el-input-number>
          </el-form-item>
          <el-form-item label="线程数:" prop="threadNum">
            <el-input-number v-model="addproject.threadNum" controls-position="right" size="small" style="width:50%"></el-input-number>
          </el-form-item>
          <el-form-item label="项目模板:" prop="isTemplate">
            <el-tooltip :content="'Switch value: ' + addproject.isTemplate" placement="top">
                <el-switch v-model="addproject.isTemplate" active-color="#13ce66" inactive-color="#ff4949" :active-value=true
            :inactive-value=false>
              </el-switch>
            </el-tooltip>
          </el-form-item>
          <el-form-item label="同步:" prop="changeUser">
        <el-tooltip :content="'Switch value: ' + addproject.sync" placement="top">
        <el-switch v-model="addproject.sync" active-color="#13ce66" inactive-color="#ff4949" :active-value=true
          :inactive-value=false>
        </el-switch>
      </el-tooltip>
        </el-form-item>
          <el-form-item label="创建时间:" prop="createTime">
            <el-input v-model="addproject.createTime" :disabled="true"></el-input>
          </el-form-item>
          <el-form-item label="修改时间:" prop="changeTime">
            <el-input v-model="addproject.changeTime" :disabled="true" ></el-input>
          </el-form-item>

          <el-form-item label="status:" prop="status">
            <el-input v-model="addproject.status" :disabled="true"></el-input>
          </el-form-item>
          <el-form-item label="createUser:" prop="createUser">
            <el-input v-model="addproject.createUser" :disabled="true"></el-input>
          </el-form-item>
      </div>
    </el-form>
    <el-dialog :visible.sync="afterscriptdialog" width="40%" title="Shell脚本" append-to-body>
        <el-input type="textarea" :rows="15" placeholder="预处理脚本" v-model="addproject.preScriptPath"></el-input>
    </el-dialog>
      <span slot="footer" class="dialog-footer">
        <el-button size="mini" @click="centerDialogVisible = false">取 消</el-button>
        <el-button size="mini" type="primary" @click="addprojectSubmit">确 定</el-button>
      </span>
</el-dialog>
<el-dialog title="项目服务器" :visible.sync="centerDialogVisible1" width="45%" center>

    <el-transfer v-model="addproject.postServer" filterable 
    :titles="['服务器列表', '发布服务器']" :data="data" v-if="centerDialogVisible1" filter-placeholder="请输入ip地址"></el-transfer>

  <span slot="footer" class="dialog-footer">
    <el-button size="mini" @click="centerDialogVisible1 = false">取 消</el-button>
    <el-button size="mini" type="primary" @click="projectaddSubmit">确 定</el-button>
  </span>
</el-dialog>
  <div>
    <!-- 搜索框 -->
      <div class="project-search">
            <el-button type="primary" @click="centerDialogVisible = true" size="small" icon="el-icon-circle-plus" round>添加项目</el-button>
          <el-autocomplete v-model="state4" :fetch-suggestions="querySearchAsync" placeholder="请输入查询内容" @select="handleSelect" 
          aria-setsize="small"
          prefix-icon="el-icon-search" value-key="ip"
        ></el-autocomplete>
      </div>
      <!-- 项目列表 -->
      <div class="project-table">
        <el-table :data="tableData.list" style="width: 100%">
          <el-table-column prop="name" label="项目" sortable width="90" > </el-table-column>
          <el-table-column prop="gitVersion" label="Git分支"  width="130"> </el-table-column>
          <el-table-column prop="gitAddress" label="Git源" width="150"> </el-table-column >
          <el-table-column prop="RocllgitVersion" label="回滚版本" width="90"> </el-table-column >
          <el-table-column label="操作">
            <template slot-scope="scope">
              <el-button size="mini" type="info" plain @click="projecteditSubmit(scope.row.id, tableData)">项目主机</el-button>
              <el-button size="mini" @click="editSubmit(scope.row.id, tableData)">编辑</el-button>
              <el-button @click="removeSubmit(scope.row.id, tableData)" size="mini" type="danger" >删除</el-button>
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
    gitAddress: '',
    gitVersion: '',
    RocllgitVersion: '',
    defaultBranch: '',
    middleServer: '',
    preServer: '',
    preScriptPath: '',
    pushMessage: '',
    excludeList: '',
    dstServerKey: '',
    serverPort: '',
    postScriptPath: '',
    threadNum: '',
    sync: false,
    isTemplate: false,
    backupPath: '',
    status: ''
  }
  export default {
    data() {
      return {
        data: [],
        visible2: false,
        afterscriptdialog: false,
        centerDialogVisible1: false,
        centerDialogVisible: false,
        value4: false,
        textarea: '',
        restaurants: [],
        state4: '',
        tableData: {},
        tableData1: {},
        tableDatakey: {},
        searchOption: {
          size: 10,
          page: 1
        },
        addproject: deepClone(sT)
      }
    },
    computed: {
      title: function() {
        return this.addproject.id ? '编辑项目' : '添加项目'
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
      },
      centerDialogVisible1(val, oldval) {
        this.data = this.tableData1.list.map(x => ({
          key: x.id,
          label: x.ip
        }))
      }
    },
    methods: {
      handleChange(value, direction, movedKeys) {
        console.log(value, direction, movedKeys)
      },
      showServer() {
        request({
          method: 'get',
          url: 'http://127.0.0.1:8000/hostApi/',
          params: { size: 100 }
        }).then(Response => {
          this.tableData1 = Response.data
        })
      },
      showkey() {
        request({
          method: 'get',
          url: 'http://127.0.0.1:8000/keyApi/',
          params: this.searchOption
        }).then(Response => {
          this.tableDatakey = Response.data
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
      showproject() {
        request({
          method: 'get',
          url: 'http://127.0.0.1:8000/ProApi/',
          params: this.searchOption
        }).then(Response => {
          this.tableData = Response.data
        })
      },
      addprojectSubmit() {
        if (this.addproject.id) {
          request({
            method: 'put',
            url: 'http://127.0.0.1:8000/ProApi/' + this.addproject.id + '/',
            data: this.addproject
          }).then(res => {
            this.$message.success('操作成功')
            this.centerDialogVisible = false
            this.showproject()
          })
        } else {
          request({
            method: 'post',
            url: 'http://127.0.0.1:8000/ProApi/',
            data: this.addproject
          }).then(res => {
            this.$message.success('操作成功')
            this.centerDialogVisible = false
            this.showproject()
          })
        }
      },
      removeSubmit(id, row) {
        request({
          method: 'delete',
          url: 'http://127.0.0.1:8000/ProApi/' + id + '/'
        }).then(res => {
          this.visible2 = false
          this.$message.success('删除成功')
          this.showproject()
        })
      },
      editSubmit(id, row) {
        request({
          method: 'get',
          url: 'http://127.0.0.1:8000/ProApi/' + id + '/'
        }).then(Response => {
          this.centerDialogVisible = true
          this.addproject = Response.data
        })
      },
      projecteditSubmit(id, row) {
        request({
          method: 'get',
          url: 'http://127.0.0.1:8000/ProApi/' + id + '/'
        }).then(Response => {
          this.centerDialogVisible1 = true
          this.addproject = Response.data
          this.value1 = Response.data.postServer
        })
      },
      projectaddSubmit() {
        request({
          method: 'put',
          url: 'http://127.0.0.1:8000/ProApi/' + this.addproject.id + '/',
          data: this.addproject
        }).then(res => {
          this.$message.success('操作成功')
          this.centerDialogVisible1 = false
        })
      }
    },
    mounted() {
      this.showproject()
      this.showkey()
      this.showServer()
      // this.restaurants = this.loadAll()
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

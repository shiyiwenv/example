<template>
  <el-dialog
  title="添加服务器"
  :visible.sync="centerDialogVisible"
  width="40%"
  center>
  <el-form  label-width="80px" size="small">
    <el-form-item label="主机名:">
      <el-input v-model="addserver.hostname"></el-input>
    </el-form-item>
        <el-form-item label="IP地址:">
      <el-input v-model="addserver.ip"></el-input>
    </el-form-item>
        <el-form-item label="CPU:">
      <el-input v-model="addserver.cpusum" placeholder="CPU核心数"></el-input>
    </el-form-item>
        <el-form-item label="内存:">
      <el-input v-model="addserver.memory"></el-input>
    </el-form-item>
        <el-form-item label="操作系统:">
      <el-input v-model="addserver.os_version"></el-input>
    </el-form-item>
        <el-form-item label="机位:">
      <el-input v-model="addserver.postion" placeholder="BJDZ-6B1001-1" suffix-icon="el-icon-location"></el-input>
    </el-form-item>
        <el-form-item label="型号:">
      <el-input v-model="addserver.mode" placeholder="R720"></el-input>
    </el-form-item>
        <el-form-item label="备注:">
      <el-input type="textarea" :rows="2" placeholder="请输入内容" v-model="addserver.ps" size="small">
</el-input>
    </el-form-item>
    <el-switch style="display: block" v-model="addserver.status" active-color="#13ce66" inactive-color="#ff4949" active-text="运行中" inactive-text="已关机">
</el-switch>
  </el-form>
  <span slot="footer" class="dialog-footer">
    <el-button @click="centerDialogVisible = false">取 消</el-button>
    <el-button type="primary" @click="addserverSubmit">确 定</el-button>
  </span>
</el-dialog>
</template>

<script>
export default {
  data() {
    return {
      centerDialogVisible: false
    }
  },
  props: ['centerDialogVisible']
}
</script>

<style rel="stylesheet/scss" lang="scss">
    .el-dialog .el-form .el-form-item .el-input { 
      width: 70%;
    }
    .el-dialog .title {
      line-height: 30px;
      color: #303133;
      font-family: Helvetica Neue, Helvetica, PingFang SC, Hiragino Sans GB, Microsoft YaHei, Arial, sans-serif;
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

#!/usr/bin/env python
#encoding=utf-8
import commands



cpuinfo=map(int,commands.getoutput("cat /proc/stat|grep -w cpu|awk '{$1=\"\"; print $0}'").split())
cputime=sum(cpuinfo)
sirq=cpuinfo[6]

print format(100*(float(sirq)/cputime),'.1f')
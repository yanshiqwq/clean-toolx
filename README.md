# clean-toolx

~~一个屑初中生瞎写的阴间程序()~~

一个普通的命令行清理工具...

插件格式(json):
```
{
	"name": "插件名",
	"author": "插件作者",
	"version_name": "版本名",
	"version_code": 版本号,
	"min_version": 最低支持clean-toolx版本,
	"platform": "操作系统",
	"rules": [
		{
			"name": "规则名",
			"warning_level": 警告值,
			"folders": [
				{
					"path": "文件夹路径",
					"extension": "文件后缀或者'*'"
				},
				......
			]
		},
		......
	]
}
```

## [最新] v1.1版本日志
\+ 路径支持环境变量${xxx}
\+ 支持警告值
\+ 会检查插件是否能在当前操作系统运行
\-  大改插件格式,不兼容v1.0版本
× 不支持检测最低版本

### v1.0版本日志
\+ 基础功能
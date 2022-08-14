# UCAS 每日健康上报

自动每日健康信息填报，内容与上次填报相同。如果你因为改变位置等原因需要修改填报信息，请在程序运行之前手动填报。

# 参数说明

| 变量名称      | 参数名称        | 命令行选项 | 解释                                                                        |
|:----------|-------------|-------|---------------------------------------------------------------------------|
| `USER`    | SEP账号       | `-u`  | 用于登录的账号，一般为电子邮件地址                                                         |
| `PASS`    | SEP密码       | `-p`  | SEP账号对应的密码                                                                |
| `API_KEY` | 微信通知API_KEY | `-n`  | *可选* 用于向你的微信推送填报结果，如果你没有API_KEY，可以在[这里](https://sct.ftqq.com/sendkey)免费获取 |

# 使用方法

## 手动调用

如果你有可以运行定时任务的服务器（可以是连接网络的任何能运行Python的设备），那么你可以将这个程序部署在上面。

1. 安装依赖（只需要执行一次）

```shell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

2. 运行

```shell
python ./main.py -u [SEP账号] -p [SEP密码] -n [微信通知API_KEY]
```

3. 查阅相应操作系统的定时任务设置方法并设置定时任务




## 通过GitHub Actions自动调用

如果你没有可以运行定时任务的服务器，那就不如让GitHub免费送你的CI/CD解放双手。

1. Fork走这个仓库
2. 进入`Actions`页面，开启本仓库的Actions。
3. 进入`Settings`页面，选择`Security > Secrets > Actions > New repository secret`，按照*参数说明*中的*变量名称*分别设置表格中提到的变量，注意所有内容均**区分大小写**
   > 不用担心账号和密码的安全问题，Secrets设置后仅对程序可见，对其余所有人（包括你自己）均不可见。
   
   > 如果你对程序本身的安全性有顾虑，请尝试阅读代码（包含足量注释）。
4. 服务器会在每天23点（UTC时间，即北京时间7点）自动填报，并向绑定的微信推送填报结果
   > 填报时间可以在`./.github/workflows/task.yml`中修改
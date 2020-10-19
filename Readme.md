# 创建、查看、删除github仓库的脚本
不打开网页，直接建立仓库。
使用[GitHub REST API][1]

写完代码想把它上传到github上，又不想打开网页操作，只想简单创建一个仓库，所以编写了这个脚本程序。
## 使用

1. 在 github 上用自己的账号创建一个 OAuth Token, 是一个类似下面这样的字符串：
 e6df79d9e62795297e3aabd0945ea33bd6a78501
2. 把它设置到环境变量 GH_TOKEN 中
3. 执行命令行命令即可
```sh
python -m pip install chx-gh
python -m chx.gh --help
python -m chx.gh create --repo hello
```

[1]: "https://docs.github.com/en/free-pro-team@latest/rest"
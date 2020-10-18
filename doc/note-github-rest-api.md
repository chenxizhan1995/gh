[GitHub REST API](https://docs.github.com/en/free-pro-team@latest/rest)
## API 版本
 当前（2020年10月18日）github rest api 版本是 3，所有发送给
https://api.github.com 的请求默认使用版本 3 的api。但是最好在http头中显式
指定api版本。`Accept: application/vnd.github.v3+json`

```sh
$ curl -H 'Accept: application/vnd.github.v3+json' https://api.github.com/users/octocat/orgs -i

HTTP/1.1 200 OK
date: Sat, 17 Oct 2020 16:38:41 GMT
content-type: application/json; charset=utf-8
content-length: 5
server: GitHub.com
status: 200 OK
cache-control: public, max-age=60, s-maxage=60
vary: Accept, Accept-Encoding, Accept, X-Requested-With, Accept-Encoding
etag: "d41c935eb5c029c094b396655d6701ed2035fea14feb9434d73918c953bbc336"
x-github-media-type: github.v3; format=json
access-control-expose-headers: ETag, Link, Location, Retry-After, X-GitHub-OTP, X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Used, X-RateLimit-Reset, X-OAuth-Scopes, X-Accepted-OAuth-Scopes, X-Poll-Interval, X-GitHub-Media-Type, Deprecation, Sunset
access-control-allow-origin: *
strict-transport-security: max-age=31536000; includeSubdomains; preload
x-frame-options: deny
x-content-type-options: nosniff
x-xss-protection: 1; mode=block
referrer-policy: origin-when-cross-origin, strict-origin-when-cross-origin
content-security-policy: default-src 'none'
X-Ratelimit-Limit: 60
X-Ratelimit-Remaining: 56
X-Ratelimit-Reset: 1602954562
X-Ratelimit-Used: 4
Accept-Ranges: bytes
X-GitHub-Request-Id: 11AD:4C84:1A839B5:2002BE8:5F8B1E11

[

]

```

空白字段返回 null 而不是省略。
所有时间戳都以 ISO 8601 格式返回：`YYYY-MM-DDTHH:MM:SSZ`
## 认证
当访问需要认证的api时，会返回 404 Not Found，而不是 403 Forbidden。这样做是为了避免
泄露用户的私有仓库名称。
另外，未认证的访问，也是有频率限制的。
有两种认证方式:
- 基础认证 `$ curl -u "username" https://api.github.com`
- OAuth2 令牌认证 `$ curl -H "Authorization: token OAUTH-TOKEN" https://api.github.com`

建议使用 Authorization 发送 OAuth2 令牌作为认证手段。

github 有登录失败的次数限制。

## 参数
GET 方法，参数放在url的查询字符串中即可 
`$ curl -i "https://api.github.com/repos/vmg/redcarpet/issues?state=closed"`
POST,PATCH,PUT,DELETE 方法，参数要以JSON格式放在请求体中发送，并设置 `Content-Type of 'application/json'`:

`$ curl -i -u username -d '{"scopes":["public_repo"]}' https://api.github.com/authorizations`

## 查询
GET 请求访问根URL，可以获取各类 REST API 的如口点
`$ curl -H 'Accept: application/vnd.github.v3+json' https://api.github.com`

## 错误码
## 分页
对于包含多条结果的返回值，默认分页，每页30条。可以指定分页大小和页码。
页码从1开始，缺省返回第一页。
`curl 'https://api.github.com/user/repos?page=2&per_page=100'`
## User-Agent 头
必须指定合法的Use-Agent头，否则返回 403 Forbidden。
建议使用你的github账号或者app名字作为首部，以便遇到问题
时我们联系你。cURL 会自动添加合法 User-Agent 首部。

## API
### 获取用户的代码库列表 get /users/{username}/projects
### 创建仓库：post /user/repos
    权限：使用 OAuth 认证时，令牌权限
        创建共有仓库：public_repo scope 或 repo
        创建私有仓库：repo
    
`curl -H 'Authorization: token  e6df79d9e62795297e3aabd0945ea33bd6a78510' https://api.github.com/user/repos -d '{"name":"test_hello"}'`
    
响应码: 
Status: 201 Created
Status: 304 Not Modified
Status: 400 Bad Request
Status: 401 Unauthorized
Status: 403 Forbidden
Status: 404 Not Found


```sh
# 测试。响应结果是 github 设计理念中随机选择的一条
curl https://api.github.com/zen

# 查询用户 defunkt 的信息
curl https://api.github.com/users/defunkt

# 列出用户 twbs 仓库 bootstrap 的详细信息
curl -i https://api.github.com/repos/twbs/bootstrap

# 如果指定了 OAuth 令牌，则 /user 指代当前用户

curl -H 'Authorization: token 5199831f4dd3b79e7c5b7e0ebe75d67aa66e79d4' \
     https://api.github.com/user
# 查看当前用户的仓库列表
curl -i -H "Authorization: token 5199831f4dd3b79e7c5b7e0ebe75d67aa66e79d4" \
    https://api.github.com/user/repos
# 返回的信息将取决于我们进行身份验证时令牌所具有的作用域：
  #  具有 public_repo 作用域的令牌返回的响应包含我们在 github.com 上有权查看的所有公共仓库。
  #  具有 repo 作用域的令牌返回的响应包含我们在 github.com 上有权查看的所有公共和私有仓库。


# 列出其他用户的仓库：
$ curl -i https://api.github.com/users/octocat/repos
# 列出组织的仓库：
$ curl -i https://api.github.com/orgs/octo-org/repos

# 创建仓库
$ curl -i -H "Authorization: token 5199831f4dd3b79e7c5b7e0ebe75d67aa66e79d4" \
    -d '{ \
        "name": "blog", \
        "auto_init": true, \
        "private": true, \
        "gitignore_template": "nanoc" \
      }' \
    https://api.github.com/user/repos
# 要在您拥有的组织下创建仓库，只需将 API 方法从 /user/repos 更改为 /orgs/<org_name>/repos
```









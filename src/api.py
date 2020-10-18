'''
Created on 2020年10月18日

命令行参数，环境变量，配置文件

1. 正式开始运行之前，把所有这些配置信息合并到一起。
2. 环境变量的名字是不会变的，硬编码即可（区分大小写）
3. 配置文件位置，有默认值，但可以通过环境变量和命令行参数指定别的位置。
4. 分层
    1. 第一层，解析命令行参数，选择不同子命令运行
    2. 第二层，子命令根据命令行参数和环境变量加载配置文件，并执行实际操作
    3. 实际操作主要涉及仓库信息的增删改查，这些封装到类中

@author: chenx
'''
import os
import configparser
import requests

_config_file = 'gh.conf'
_config_file_path = os.path.abspath(os.path.expanduser(
    os.path.join('~', '.config', _config_file)))

def load_config(file):
    config = configparser.ConfigParser()
    config.read(file, encoding='UTF-8')
    print('打开文件')
    return config

def _get_token():
    config = load_config(_config_file_path)
    main = config['main']
    return main['token']

class BaseCmd:
    base_url = 'https://api.github.com'
    version_header = {'Accept': 'application/vnd.github.v3+json'}
    auth_header = {'Authorization': 'token ' + _get_token()}
    def __init__(self, name, user_name, token):
        self.name = name
        self.user_name = user_name
        self.token = token
    
    def __call__(self):
        raise NotImplemented

class CreateRepo(BaseCmd):
    '''
    post /user/repos
    Status: 201 Created
    
    OAuth
    - public_repo scope or repo scope to create a public repository
    - repo scope to create a private repository
    '''
    
    def __init__(self, name, user_name = None, token = None):
        super().__init__(name, user_name, token)
    
    
    def __call__(self, args):
        print('创建仓库')
        pth = '/user/repos'
        data = {
            'name':args.repo
        }
        
        headers = {**self.version_header, **self.auth_header}
        
        res = requests.post(self.base_url + pth, headers = headers, json = data)

        if res.status_code == 201:
            print('创建成功')
        else:
            print('创建失败,', res.reason)
            print(res.headers['status'])
        

class DeleteRepo(BaseCmd):
    '''
    删除仓库的api
    [仓库 - GitHub Docs](https://docs.github.com/cn/free-pro-team@latest/rest/reference/repos#delete-a-repository)
    '''
    
    def __init__(self, name, user_name = None, token = None):
        super().__init__(name, user_name, token)
    
    
    def __call__(self, args):
        print('删除仓库')
        pth = '/repos/chenxizhan1995/' + args.repo

        headers = {**self.version_header, **self.auth_header}
        
        res = requests.delete(self.base_url + pth, headers = headers)

        if res.status_code == 204: #
            print('删除成功')
        elif res.status_code == 403:
            print('无删除权限')
        elif res.status_code == 404:
            print('仓库不存在')
        else:
            print('删除失败:' + res.reason)

class ListRepo(BaseCmd):
    '''
    get /user/repos
    Status: 200 OK
    '''
    def __init__(self, name, user_name = None, token = None):
        super().__init__(name, user_name, token)
    
    def __call__(self, args):
        print('列举仓库')
        pth = '/user/repos'

        headers = {**self.version_header, **self.auth_header}
        params = {
            'per_page':'100'
        }
        res = requests.get(self.base_url + pth, headers = headers, params = params)
        if res.status_code == 200: #
            repos = res.json()
            print('一共 %d 个仓库' %(len(repos)))
            for idx, repo in enumerate(repos, 1):
                print(idx, '-'*60)
                print('%s' %(repo['full_name']))
                if repo['private']: print('私有')
                if repo['fork']: print('fork')
                print('描述：', repo['description'])
        else:
            print('失败:' + res.reason)


class ShowRepo(BaseCmd):
    '''
    
    get /repos/{owner}/{repo}
    Status: 200 OK
    
    [仓库 - GitHub Docs](https://docs.github.com/cn/free-pro-team@latest/rest/reference/repos#get-a-repository)
    
    '''
    
    def __init__(self, name, user_name = None, token = None):
        super().__init__(name, user_name, token)
    
    def __call__(self, args):
        import json
        pth = '/repos/' + args.repo

        headers = {**self.version_header, **self.auth_header}

        res = requests.get(self.base_url + pth, headers = headers)
        print(json.dumps(res.json(), indent=4))

_list = ListRepo('list')
_create_repo_cmd = CreateRepo('create')
_show_repo_cmd = ShowRepo('show')
_delete_repo_cmd = DeleteRepo('delete')

__all__ = [_list, _create_repo_cmd, _delete_repo_cmd, _show_repo_cmd]

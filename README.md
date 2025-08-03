# knowledge-rag

django前后端分离：https://www.zhihu.com/tardis/zm/art/128976272?source_id=1003

django入门：https://docs.djangoproject.com/en/5.2/intro/tutorial01/

restful入门：https://www.django-rest-framework.org/tutorial/quickstart/

## 启动项目
#### 后端
1、安装python环境
```
brew install pyenv
brew install  pyenv-virtualenv

pyenv install 3.10.0
pyenv virtualenv 3.10.0 venv-3.10.0
pyenv activate venv-3.10.0
```

2、启动服务
```
cd knowledge-rag/backend
python manage.py makemigrations # 生成迁移文件
python manage.py migrate # 迁移到数据库
python manage.py runserver
```

#### 前端
1、安装依赖
2、启动服务
```
npm run dev
```
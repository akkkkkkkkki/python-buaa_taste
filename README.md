# python-buaa_taste

“航味“APP是一款面向北航学生的美食APP，其中记录了北航的食堂、柜台以及各类菜品。用户可以使用本app来检索、记录和收藏菜品，并和其他用户对菜品进行线上交流。本app还能根据用户的用餐记录来智能推荐一日菜品，解决“今天吃什么”的难题。另外，app支持管理员账号，管理员可以对菜品、柜台、和食堂的信息进行添加和编辑。

本app的logo由一个带叉勺的盘子和一个星环组成。带叉勺的盘子表明app是美食主题；带双引号的星环代表这是一个沟通交流的space。整体用红色过渡橘色过渡黄色，表明食物带给人温暖。

### 功能简述

航味app的页面包括：home页、搜索页、分类页、用户页（./pages文件夹下)。每个页面有各种component组成（./components文件夹下）。home页包括每日推荐、我的收藏、倍受好评、热门菜品。分类页按照菜品的tags进行分类。用户中心包括历史记录管理和注销按钮。管理员可以点击用户中心的菜品、柜台、食堂管理按钮来进行增删改，支持图片添加和多个食堂柜台。

在搜索页和分类页，点击菜品的卡片可以跳转到菜品详情，用户可以在详情页看到菜品详细的星级评分、描述、所在柜台，最近评论等信息。用户可以点击收藏按钮收藏该菜品，或者点击记录按钮来记录吃过的时间。此外，详情页还支持评论发表，用户可以输入评论内容、标题，并对菜品进行打分。另外，对已有的评论，用户可以点赞或点踩来发表态度。登录后点击评论卡片可以跳转到回复页，用户可以查看该评论的回复，或者对该评论进行回复。

### 项目运行

环境要求如下：

```
PySide6<=6.4.2
PySideSix-Frameless-Window 
darkdetect 
password_strength
```

安装完插件后，运行最外层文件夹下的main.py即可。

### 参考

- 本项目使用第三方组件qmaterialwidget开发，项目地址：https://github.com/zhiyiYo/QMaterialWidgets

- pyside6官方文档

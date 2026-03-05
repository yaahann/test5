# 智能求职推荐系统 (Job Recommend System)

## 1. 项目概述

本项目是一个功能完善的求职与招聘服务平台，专为求职者、招聘企业及平台管理员设计。系统的核心亮点是内置了**基于内容的智能推荐引擎**。
**主要特性：**

* **多角色支持**：支持管理员、求职者、招聘者三种角色体系，提供专属的数据看板（Dashboard）。
* **智能双向推荐**：根据求职者的技能标签、学历、期望职位，以及企业的职位描述与要求，进行双向的个性化推荐（为求职者推荐岗位，为企业推荐候选人）。
* **完整的招聘生态**：包含职位发布、职位收藏、企业主页浏览、站内私信系统以及求职新闻资讯聚合。

## 2. 技术栈

### 前端 (Frontend)

* **核心框架**: Vue 3 (基于 Vite 构建)
* **状态管理**: Pinia
* **路由控制**: Vue Router 4
* **网络请求**: Axios
* **UI组件库**: Bootstrap 5

### 后端 (Backend)

* **核心框架**: Python 3, Django 5.0
* **API 接口**: Django REST Framework (DRF)
* **身份认证**: djangorestframework-simplejwt (JWT Token机制，支持 Refresh Token)
* **推荐算法**: `scikit-learn` (TF-IDF 特征提取, 余弦相似度计算), `jieba` (中文分词)
* **跨域处理**: django-cors-headers

### 数据库 (Database)

* **关系型数据库**: MySQL (默认端口 3306)

## 3. 项目架构

项目采用典型的 B/S 架构与前后端分离设计：

* **数据流向**：客户端（Vue SPA）通过 Axios 携带 JWT Token 向后端发起 RESTful API 请求。后端（Django）接收请求后进行权限校验与数据读写，最终将结果序列化为 JSON 返回给客户端。
* **推荐系统设计**：当用户请求推荐列表时，后端会提取“求职者画像文本”（技能、学历、期望等）与全库处于“招聘中”的“职位画像文本”。系统使用 `jieba` 过滤停用词，借助 `TfidfVectorizer` 将文本向量化，并计算余弦相似度（Cosine Similarity）。系统会过滤掉低于阈值的匹配项并返回 Top 10，同时设计了冷启动兜底策略（当资料不完善时，默认推荐最新职位）。
* **模块化解耦**：后端按业务逻辑被拆分为 `users`（用户与资料）、`jobs`（职位与资讯）、`recruitment`（投递与招聘流程）、`recommendations`（AI推荐服务）四大 App。

## 4. 目录结构

```text
├── job-web/                              # 前端 Vue 项目根目录
│   ├── public/                           # 静态资源 (如 favicon.ico)
│   ├── src/                              # 前端核心业务代码
│   │   ├── router/                       # 路由配置 (index.js)
│   │   ├── stores/                       # Pinia 状态管理 (user.js, counter.js)
│   │   ├── views/                        # 视图页面 (包含多个角色的 Dashboard 及详情页)
│   │   ├── App.vue                       # 前端根组件
│   │   └── main.js                       # 前端项目入口
│   ├── package.json                      # 前端依赖配置
│   └── vite.config.js                    # Vite 构建配置
│
├── job_recommend_system/                 # 后端 Django 项目根目录
│   ├── job_recommend_system/             # 全局项目配置
│   │   ├── settings.py                   # 数据库、JWT、中间件及 App 注册中心
│   │   └── urls.py                       # 主路由入口
│   ├── users/                            # 用户管理 App (包含角色、求职者档案、企业认证、私信)
│   ├── jobs/                             # 职位管理 App (包含职位发布、收藏、资讯)
│   ├── recommendations/                  # 推荐引擎 App (包含 TF-IDF 核心算法)
│   ├── recruitment/                      # 招聘流程 App
│   ├── media/                            # 媒体文件目录 (存储用户上传的简历、营业执照等)
│   └── manage.py                         # Django 管理脚本
└── main.py                               # 根目录项目运行/测试入口

```


## 5. 核心文件说明

### 项目入口与配置文件

* **`job_recommend_system/settings.py`**: 后端核心配置。定义了 MySQL 连接参数，注册了4个自定义核心 App，并配置了 SimpleJWT 认证策略（访问 Token 有效期延长至 7 天，刷新 Token 14 天）和 CORS 跨域许可。
* **`job-web/package.json`**: 前端依赖清单，清晰展示了项目基于 Vue 3 体系，并整合了 Bootstrap 样式库与 Axios 请求库。

### 核心业务逻辑实现

* **`job_recommend_system/recommendations/views.py`**: 项目的**智能大脑**。实现了两个核心接口 `ContentBasedRecommendationView` 和 `CandidateRecommendationView`。它利用 `jieba` 进行中文分词处理，将用户多维特征（赋予核心字段三倍权重）拼接为文本段落，通过 `TfidfVectorizer` 计算文本向量特征，最后通过 `cosine_similarity` 给岗位/候选人打分并排序。

### 数据模型和 API 接口

* **`job_recommend_system/users/models.py`**: 定义了系统的基础用户生态。通过重写 `AbstractUser` 添加了 `role_type`（管理员/求职者/招聘者）。并利用 `OneToOneField` 延展出了 `JobSeeker`（含核心的技能标签 `skills` 和期望职位字段）与 `Recruiter`（含公司认证体系与审核状态）模型。同时构建了底层的 `Message` 站内私信表。
* **`job_recommend_system/jobs/models.py`**: 职位数据模型 `Job`。绑定了发布企业，记录了职位的核心匹配字段 `job_tags`。同时提供了 `JobCollection`（收藏表，设有联合唯一索引防止重复收藏）以及 `News`（求职资讯表）。

### 关键组件和服务模块

* **`job-web/src/router/index.js`**: 前端路由中枢。定义了基于角色的分发页面（如 `SeekerDashboard` 和 `RecruiterDashboard`），以及公共的职位列表、企业详情和求职资讯页面。结合 Vue-Router 支持了单页面应用（SPA）的无刷新跳转体验。

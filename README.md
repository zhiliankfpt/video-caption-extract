# 智凌API短视频文案提取 · Python封装
🔥 基于智凌API开放平台免费接口封装，**一键提取抖音/快手/视频号短视频文案**，开箱即用，完全免费；

## 接口来源
- 提交任务：https://open.17zhilian.cn/doc/111
- 查询结果：https://open.17zhilian.cn/doc/101
- 官方文档：https://open.17zhilian.cn

## 功能特点
- ✅ 免费版直接可用，无需复杂配置
- ✅ 自动任务提交 + 轮询查询结果
- ✅ 异常捕获、超时处理、错误提示
- ✅ 极简调用，一行代码提取文案
- ✅ 支持抖音、快手、视频号等主流平台

## 快速开始
### 1. 安装依赖
```bash
pip install requests
```

### 2. 申请 API Key（必须操作）
访问智凌开放平台：https://open.17zhilian.cn
注册账号，进入控制台 → 密钥管理，获取个人 key
免费版每日有免费额度，可直接测试
### 3. 配置并运行
下载本项目代码
打开 video_text_extract.py，将代码中 API_KEY = "" 替换为你自己的密钥
修改测试用的短视频链接
运行脚本：
```bash
python video_text_extract.py
```

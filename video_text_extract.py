import requests
import time
import json

# ===================== 配置项（请修改为你自己的apikey）=====================
API_KEY = ""  # 去 https://open.17zhilian.cn 注册获取
SUBMIT_URL = "https://open.17zhilian.cn/api/asr/parse-video-url-free"  # 提交任务（免费版）
# SUBMIT_URL = "https://open.17zhilian.cn/api/asr/parse-video-url"  # 提交任务（正式版，量大请使用该接口）
QUERY_URL = "https://open.17zhilian.cn/api/asr/task-status"    # 查询结果
POLL_INTERVAL = 2  # 轮询间隔 秒，免费版建议2-3秒
MAX_POLL_TIMES = 30  # 最大轮询次数，超时退出
# ======================================================================

def submit_task(video_url: str) -> str:
    """
    提交视频链接，获取task_id
    :param video_url: 抖音/快手/视频号等短视频链接
    :return: task_id 任务ID
    """
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=utf-8;"
    }
    params = {
        "key": API_KEY
    }
    data = {
        "videoUrl": video_url
    }
    resp = requests.post(SUBMIT_URL, params=params, data=data, headers=headers, timeout=15)
    res = resp.json()

    if res.get("code") != 200:
        raise Exception(f"提交任务失败：{res.get('msg', '未知错误')}")

    return res["data"]

def get_extract_result(task_id: str) -> dict:
    """
    根据task_id轮询获取文案提取结果（GET 官方最新接口）
    接口地址：https://open.17zhilian.cn/api/asr/task-status
    请求方式：GET
    状态：SUCCESS=成功，ING=处理中，WAIT_HANDLE=待处理，FAIL=失败
    """
    # GET 请求参数（严格按官方要求）
    params = {
        "key": API_KEY,
        "taskId": task_id
    }

    # 轮询逻辑
    for i in range(MAX_POLL_TIMES):
        resp = requests.get(QUERY_URL, params=params, timeout=10)
        res = resp.json()

        # 接口请求失败
        if res.get("code") != 200:
            raise Exception(f"查询失败：{res.get('msg', '未知错误')}")

        # 取出状态（官方字段：schedule）
        schedule = res["data"]["schedule"]

        # 成功 → 返回数据
        if schedule == "SUCCESS":
            return res["data"]

        # 失败 → 抛出异常
        elif schedule == "FAIL":
            raise Exception("视频文案提取失败，可能是链接无效或视频无法解析")

        # 待处理 / 处理中 → 继续轮询
        print(f"正在提取中... 状态：{schedule}，第{i+1}次轮询")
        time.sleep(POLL_INTERVAL)

    raise Exception("提取超时，请更换视频链接或稍后重试")

def extract_video_text(video_url: str) -> str:
    """
    一键调用：传入视频链接，直接返回纯文案
    """
    task_id = submit_task(video_url)
    result = get_extract_result(task_id)
    return result.get("content", "")


if __name__ == "__main__":
    # 测试示例，替换成你的短视频链接
    test_video_url = "https://v.douyin.com/*a**a**"
    try:
        text = extract_video_text(test_video_url)
        print("提取成功！\n=====视频文案=====")
        print(text)
    except Exception as e:
        print(f"错误：{str(e)}")

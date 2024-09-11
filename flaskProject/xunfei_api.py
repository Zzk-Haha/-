from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage

# 星火认知大模型Spark Max的URL值，其他版本大模型URL值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_URL = 'wss://spark-api.xf-yun.com/v3.5/chat'
# 星火认知大模型调用秘钥信息，请前往讯飞开放平台控制台（https://console.xfyun.cn/services/bm35）查看
SPARKAI_APP_ID = 'b96d1d8f'
SPARKAI_API_SECRET = 'YjcxMDRkZjE3ZWM1MjNjYjMzOGUzMWJm'
SPARKAI_API_KEY = '7b37099589c8d9e2f9850a16db15bb27'
# 星火认知大模型Spark Max的domain值，其他版本大模型domain值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_DOMAIN = 'generalv3.5'

class CustomChunkPrintHandler(ChunkPrintHandler):
    def __init__(self):
        super().__init__()
        self.text = ""

    def handle_chunk(self, chunk):
        self.text += chunk


def use_xunfei_api(prompt):
    historyA = ''
    historyQ = ''

    # 历史记录
    history = historyQ + historyA
    spark = ChatSparkLLM(
        spark_api_url=SPARKAI_URL,
        spark_app_id=SPARKAI_APP_ID,
        spark_api_key=SPARKAI_API_KEY,
        spark_api_secret=SPARKAI_API_SECRET,
        spark_llm_domain=SPARKAI_DOMAIN,
        streaming=False,
    )
    messages = [ChatMessage(
        role="user",
        content=history + prompt
    )]

    handler = CustomChunkPrintHandler()
    response = spark.generate([messages], callbacks=[handler])

    # 检查 response 是否正确获取到了生成的内容
    if response and response.generations and response.generations[0]:
        content = response.generations[0][0].text
        # 历史问题
        historyQ = '你的历史问题是:' + prompt
        # 历史回答
        historyA = '你的历史回答是:' + content
        return {'content': content}
    else:
        # 如果 response 不正确，返回错误信息
        return {'error': 'Failed to generate response'}


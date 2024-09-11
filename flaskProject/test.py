# response = {
#     "generations": [
#         [
#             {
#                 "text": "你好！有什么我可以帮助你的吗？",
#                 "message": {
#                     "content": "你好！有什么我可以帮助你的吗？"
#                 }
#             }
#         ]
#     ],
#     "llm_output": {
#         "token_usage": {
#             "question_tokens": 1,
#             "prompt_tokens": 1,
#             "completion_tokens": 8,
#             "total_tokens": 9
#         }
#     },
#     "run": [
#         {
#             "run_id": "8ef01f88-e0b2-4708-99ff-26b75beba4c0"
#         }
#     ]
# }
#
# text = response["generations"][0][0]["text"]
response = "generations=[[ChatGeneration(text='你好！有什么我可以帮助你的吗？', message=AIMessage(content='你好！有什么我可以帮助你的吗？'))]] llm_output={'token_usage': {'question_tokens': 1, 'prompt_tokens': 1, 'completion_tokens': 8, 'total_tokens': 9}} run=[RunInfo(run_id=UUID('8ef01f88-e0b2-4708-99ff-26b75beba4c0'))]"

# 将字符串转换为字典
import ast
response_dict = ast.literal_eval(response)

# 提取text信息
text = response_dict["generations"][0][0].text


print(text)
print(response)
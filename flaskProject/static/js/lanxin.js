// 初始化历史信息
historyA = ''
historyQ = ''
historyMessage = ''
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('myForm');

    form.addEventListener('submit', function(event) {
        // 阻止表单默认提交行为
        event.preventDefault();

        historyMessage = historyMessage + historyA + historyQ
        // 获取用户输入的文本
        const textInput = historyMessage + document.getElementById('textInput').value;
        historyQ = '我的历史问题是:' + document.getElementById('textInput').value;

        // 发送AJAX请求到服务器
        fetch('/api/vivogpt', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: textInput }),
        })
        .then(response => response.json())
        .then(data => {
            // 显示API调用结果
            document.getElementById('result').textContent = data.content;
            historyA = '你的历史回答是:' + data.content;
        })
        .catch(error => {
            console.error('请求失败:', error);
        });
    console.log(textInput)
    });


});


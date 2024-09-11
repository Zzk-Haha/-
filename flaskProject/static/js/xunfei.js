document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('xunfei');

    form.addEventListener('submit', function(event) {
        // 阻止表单默认提交行为
        event.preventDefault();

        // 获取用户输入的文本
        const textInput = document.getElementById('newTextInput').value;

        // 发送AJAX请求到服务器
        fetch('/api/xunfei', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: textInput }),
        })
        .then(response => response.json())
        .then(data => {
            // 显示API调用结果
            document.getElementById('xunfeiAnswer').textContent = data.content;
        })

    console.log(textInput)
    });


});


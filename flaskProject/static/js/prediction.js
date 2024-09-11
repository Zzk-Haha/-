// 确保您的HTML文档加载完成后执行以下代码
$(document).ready(function() {
    // 绑定点击事件
    $('#predict-btn').click(function(event) {
        // 阻止默认行为，例如表单提交
        event.preventDefault();
        // 执行预测函数

        predict();
    });

    // 预测函数
    function predict() {
        // 这里编写预测逻辑
        console.log('开始执行预测');
        // 获取文件
        var fileInput = document.getElementById('file-input');
        var file = fileInput.files[0];
        // 如果没有选择文件，则返回
        if (!file) {
            alert('请先选择一个文件！');
            return;
        }
        // 创建formData对象
        var formData = new FormData();
        formData.append('file', file);

        // 发送ajax请求
        $.ajax({
            url: '/auth/predict',// 确保这个URL是正确的
            method: 'POST',
            // 发送 FormData对象
            data: formData,
            contentType: false, // 必须设置，因为发送的是FormData
            processData: false, // 必须设置，因为发送的是FormData
            success: function(data) {
                // 处理预测结果
                console.log('预测结果:', data);
                $('#result').text(data.result); // 假设 data.result 是预测结果的字段
            },
            error: function(error) {
                console.error('预测失败:', error);
                $('#result').text('预测失败，请重试。');
            }
        });
    }
});

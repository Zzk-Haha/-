function bindEmailCaptchaClick (){
    $('#captcha-btn').click(function (event){
        // $this代表当前按钮的query对象
        var $this=$(this);
        // 阻止默认的事件
        event.preventDefault();
        //$('#exampleInputEmail1')
        //通过name获取
        var email=$("input[name='email']").val();
        //ajax发送请求，还可以用get，post
        $.ajax({
            //http://127.0.0.1:500
            url:'/auth/captcha/email?email='+email,
            method:'GET',
            success:function(result){
                var code=result['code'];
                if(code==200){
                    var countdown=60;
                    $this.off('click');
                    var timer = setInterval(function(){
                        $this.text(countdown);
                        countdown-=1;
                        if(countdown<=0){
                            // 清理定时器
                            clearInterval(timer);
                            $this.text('获取验证码');
                            //重新绑定点击事件
                            bindEmailCaptchaClick();
                        }
                    },1000)

                    alert('邮箱验证码发送成功!');
                }else{
                    alert(result['message']);
                }

            },
            fail:function(error){
                console.log(error);
            }
        })
    });
}
// 当整个网页都加载完毕后再执行
$(function(){
    bindEmailCaptchaClick();
});



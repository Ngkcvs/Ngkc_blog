# -*- coding: utf-8 -*-
from flask import Flask, request, session
import random
import os
import sys

app = Flask(__name__)
app.secret_key = 'your_secure_key_here'  # 生产环境务必修改

def generate_5digit_expr():
    """生成5位数运算表达式及正确答案"""
    nums = [str(random.randint(10000, 99999)) for _ in range(8)]  # 严格5位数
    ops = random.choices(['+', '-', '*'], k=7)

    expr_display = nums[0]
    expr_calc = nums[0]
    for i in range(7):
        expr_display += f" {ops[i].replace('*', '×')} {nums[i + 1]}"
        expr_calc += f" {ops[i]} {nums[i + 1]}"
    return expr_display, eval(expr_calc)

@app.route('/', methods=['GET', 'POST'])
def challenge():
    # GET请求生成新题目
    if request.method == 'GET':
        expr, ans = generate_5digit_expr()
        session['expr'] = expr
        session['answer'] = ans  # 答案存入session

    # POST请求验证答案
    elif request.method == 'POST':
        try:
            user_answer = int(request.form['answer'])
            if 'answer' in session and user_answer == session['answer']:
                flag = f"flag{{秋名山码神_速算王_{random.randint(1000000000, 9999999999)}}}"
                return f'''<!DOCTYPE html>
<html>
<body style="text-align:center;font-family:Arial">
    <h1 style="color:green">✓ 挑战成功！</h1>
    <div style="font-size:24px">{flag}</div>
</body>
</html>'''
        except:
            pass
        
        # 答案错误时生成新题目
        expr, ans = generate_5digit_expr()
        session['expr'] = expr
        session['answer'] = ans

    # 返回当前题目页面
    return f'''<!DOCTYPE html>
<html>
<body style="text-align:center;font-family:Arial">
    <h1>秋名山码神_速算挑战</h1>
    <div style="font-size:20px;margin:20px">{session['expr']} = ?</div>
    <form method="POST">
        <input type="number" name="answer" required style="padding:10px;font-size:16px">
        <button type="submit" style="padding:10px 20px;background:#4CAF50;color:white;border:none">提交</button>
    </form>
</body>
</html>'''

if __name__ == '__main__':
    # 添加后台运行选项
    if len(sys.argv) > 1 and sys.argv[1] == '-d':
        # 创建守护进程
        if os.fork():
            sys.exit()
        
        # 分离文件描述符
        os.setsid()
        os.umask(0)
        
        # 二次fork确保脱离终端
        if os.fork():
            sys.exit()
        
        # 重定向标准IO
        sys.stdout.flush()
        sys.stderr.flush()
        
        # 启动服务
        print(f"Server started in background (PID: {os.getpid()})")
        app.run(host='0.0.0.0', port=5000, debug=False)
    else:
        app.run(host='0.0.0.0', port=5000, debug=False)


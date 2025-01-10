'''
Author: shysgsg 1054733568@qq.com
Date: 2025-01-10 22:46:06
LastEditors: shysgsg 1054733568@qq.com
LastEditTime: 2025-01-10 22:55:55
FilePath: \autoAccountor\server.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''

from flask import Flask, jsonify, request
import subprocess

app = Flask(__name__)

@app.route('/run_script', methods=['POST'])
def run_script():
    try:
        # 运行 autoAccountor.py
        result = subprocess.run(['python', 'F:/autoAccountor/autoAccountor.py'], capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify({'message': 'Script executed successfully', 'output': result.stdout}), 200
        else:
            return jsonify({'message': 'Script execution failed', 'error': result.stderr}), 500
    except Exception as e:
        return jsonify({'message': 'Error occurred', 'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

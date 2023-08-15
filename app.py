from flask import Flask, request, render_template, session
import subprocess
import os
import re

app = Flask(__name__)
app.secret_key = '1234'

def execute_code(lang, code, inp):
    output = ""
    file = ""

    if lang == "python":
        file = "program.py"
        cmd = ["python", "program.py"]
    elif lang == "text/x-csrc":
        file = "program.c"
        compile_cmd = ["gcc", file, "-o", "program.o"]
    elif lang == "text/x-c++src":
        file = "program.cpp"
        compile_cmd = ["g++", file, "-o", "program.o"]
    elif lang == "text/x-java":
        class_name = re.search(r"(?<=public\sclass\s)\w+(?=\s*\{)", code).group()
        file = f"{class_name}.java"
        compile_cmd = ["javac", file]

    if file:
        with open(file, 'w') as f:
            for line in code.splitlines():
                f.write(line + '\n')
        cleanup_files = [file]
        try:
            if lang in ["text/x-csrc", "text/x-c++src"]:
                subprocess.run(compile_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, timeout=5)
                cleanup_files.extend(["program.o"])
                process = subprocess.run('./program.o', input=inp, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, timeout=10)
                output = process.stdout + process.stderr
            elif lang == "text/x-java":
                subprocess.run(compile_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, timeout=5)
                classes = re.findall(r"(?<=class\s)\w+", code)
                cleanup_files.extend([f"{cls}.class" for cls in classes])
                process = subprocess.run(["java",class_name], input=inp, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, timeout=10)
                output = process.stdout + process.stderr
            else:
                process = subprocess.run(cmd, input=inp, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
                output = process.stdout + process.stderr
        except subprocess.CalledProcessError as error:
            output = error.stderr
        except subprocess.TimeoutExpired:
            output = "Error: Code execution timed out (possible infinite loop)."
        finally:
            for file in cleanup_files:
                if os.path.exists(file):
                    os.remove(file)
    return output

@app.route('/', methods=['GET', 'POST'])
def index():
    output = ""
    if request.method == 'POST':
        code = request.form.get('code')
        lang = request.form.get('language')
        inp = request.form.get('input')
        theme = request.form.get('theme')

        output = execute_code(lang, code, inp)

        session['language'] = lang
        session['input'] = inp
        session['theme'] = theme

    return render_template('index.html', language=session.get('language'), theme=session.get('theme'), output=output, input=session.get('input'))

if __name__ == '__main__':
    app.run(debug=True)

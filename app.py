from flask import Flask, request, session, render_template
import subprocess
import os
import re
import uuid
import shutil

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'
job_data = {}

def execute_code(lang, code, inp, job_id):
    output = ""
    file = ""
    job_dir = ""
    if lang == "Python":
        file = f"program_{job_id}.py"
        cmd = ["python", file]
    elif lang == "C":
        file = f"program_{job_id}.c"
        compile_cmd = ["gcc", file, "-o", f"program_{job_id}.o"]
    elif lang == "C++":
        file = f"program_{job_id}.cpp"
        compile_cmd = ["g++", file, "-o", f"program_{job_id}.o"]
    elif lang == "Java":
        job_dir = f"job_{job_id}"
        os.makedirs(job_dir, exist_ok=True)

        class_name_match = re.search(r"(?<=public\sclass\s)(\w+)", code)
        if class_name_match:
            class_name = class_name_match.group(1)
            file = os.path.join(job_dir, f"{class_name}.java")

            with open(file, 'w') as f:
                f.write(code)

            compile_cmd = ["javac", file]
        else:
            return "Error: Java class name not found in code"

    elif lang == "JavaScript":
        file = f"program_{job_id}.js"
        cmd = ["node", file]

    if file:
        with open(file, 'w') as f:
            for line in code.splitlines():
                f.write(line + '\n')
        cleanup_files = [file]
        try:
            if lang in ["C", "C++"]:
                subprocess.run(compile_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, timeout=5)
                cleanup_files.extend([f"program_{job_id}.o"])
                process = subprocess.run([f'./program_{job_id}.o'], input=inp, stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE, universal_newlines=True, timeout=10)
                output = process.stdout + process.stderr
            elif lang == "Java":
                subprocess.run(compile_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, timeout=5)
                process = subprocess.run(["java", "-cp", job_dir, class_name], input=inp, stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE, universal_newlines=True, timeout=10)
                output = process.stdout + process.stderr
            else:
                process = subprocess.run(cmd, input=inp, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                         timeout=10)
                output = process.stdout + process.stderr
        except subprocess.CalledProcessError as error:
            output = error.stderr
        except subprocess.TimeoutExpired:
            output = "Error: Code execution timed out (possible infinite loop)."
        finally:
            for file in cleanup_files:
                if os.path.exists(file):
                    os.remove(file)
            if os.path.exists(job_dir):
                shutil.rmtree(job_dir)
    return output

@app.route('/', methods=['GET', 'POST'])
def index():
    output = ""
    if request.method == 'POST':
        code = request.form.get('editor')
        lang = request.form.get('language')
        inp = request.form.get('input')
        theme = request.form.get('theme')
        job_id = str(uuid.uuid4())
        output = execute_code(lang, code, inp, job_id)
        if isinstance(output, bytes):
            output = output.decode('utf-8')
        session['code'] = code
        session['language'] = lang
        session['input'] = inp
        session['theme'] = theme
    return render_template('index.html', language=session.get('language'), theme=session.get('theme'), output=output, input=session.get('input'))

if __name__ == '__main__':
    app.run(debug=True)

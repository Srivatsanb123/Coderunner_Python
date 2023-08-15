function saveCodeToLocalStorage() {
    var codeTextArea = document.getElementById("code");
    var code = codeTextArea.value;
    localStorage.setItem("savedCode", code);
}

const codeTextArea = document.getElementById('code');
const languageSelect = document.getElementById('language');
const themeSelect = document.getElementById('theme');
const codeEditor = CodeMirror.fromTextArea(codeTextArea, {
    lineNumbers: true,
    matchBrackets: true,
    indentUnit: 4,
    autoCloseBrackets: true,
    mode: languageSelect.value,
    theme: themeSelect.value
});

window.onload = function() {
    var savedCode = localStorage.getItem("savedCode");
    if (savedCode) {
        codeEditor.setValue(savedCode);
    }
};

function saveToFile() {
    var textarea = document.getElementById("code");
    var text = textarea.value;
    var fname = document.getElementById("filename").value;
    var blob = new Blob([text], { type: "text/plain;charset=utf-8" });
    console.log(text);
    saveAs(blob, fname);
}

function loadFile() {
    const fileInput = document.getElementById('fileInput');
    const file = fileInput.files[0];
    const reader = new FileReader();

    reader.onload = function(e) {
        const content = e.target.result;
        codeEditor.setValue(content);
    };

    reader.readAsText(file);
}

languageSelect.addEventListener('change', () => {
    codeEditor.setOption('mode', languageSelect.value);
});

themeSelect.addEventListener('change', () => {
    codeEditor.setOption('theme', themeSelect.value);
});

document.getElementById("form").addEventListener("submit", saveCodeToLocalStorage);

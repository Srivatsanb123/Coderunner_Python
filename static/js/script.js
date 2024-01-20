// Setting up Ace Editor
var codeEditor = ace.edit("code");
var languageSelect = document.getElementById('language');
var themeSelect = document.getElementById('theme');
codeEditor.setOption("showPrintMargin", false)

function setEditorMode(selectedLanguage) {
    var mode;
    switch (selectedLanguage) {
        case 'Python':
            mode = 'ace/mode/python';
            break;
        case 'C':
        case 'C++':
            mode = 'ace/mode/c_cpp';
            break;
        case 'Java':
            mode = 'ace/mode/java';
            break;
        case 'JavaScript':
            mode = 'ace/mode/javascript';
            break;
        default:
            mode = 'ace/mode/text';
            break;
    }
    codeEditor.getSession().setMode(mode); // Set the mode here
}

function setEditorTheme(selectedTheme){
    codeEditor.setTheme("ace/theme/" + selectedTheme);
}
// Initialize Ace Editor mode based on the initial selected language and theme
setEditorMode(languageSelect.value);
setEditorTheme(themeSelect.value);

// Saving/loading code in/from local storage
window.onload = function() {
    var savedCode = localStorage.getItem("savedCode");
    if (savedCode) {
        codeEditor.setValue(savedCode);
    }
};

function saveCodeToLocalStorage() {
    var codeInput = document.getElementById("editor");
    var code = codeEditor.getValue();
    codeInput.value = code;
    localStorage.setItem("savedCode", code);
}

// Save and load file
function saveToFile() {
    var code = codeEditor.getValue();
    var fname = document.getElementById("filename").value;
    var blob = new Blob([code], { type: "text/plain;charset=utf-8" });
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

// Language selection
languageSelect.addEventListener('change', () => {
    var selectedLanguage = languageSelect.value;
    setEditorMode(selectedLanguage); // Update the Ace Editor mode
});

// Theme selection
themeSelect.addEventListener('change', () => {
    setEditorTheme(themeSelect.value);
    localStorage.setItem("savedTheme", selectedTheme);
});

// Save code in local storage on submission
//document.getElementById("form").addEventListener("submit", saveCodeToLocalStorage);
function  sendcode(){
    saveCodeToLocalStorage();
    document.getElementById("form").submit();
}
var editor;

// On document ready this function will be called and initialize the complete website.
docReady(function(){
    // Setup the editor
    editor = ace.edit("editor");
    editor.setTheme("ace/theme/tomorrow_night");
    editor.session.setMode("ace/mode/python");
});

function newFile() {
    editor.setValue('# Write down your code ...\n');
}

function loadFile(data) {
    if (data) {
        editor.setValue(data);
    }
    apendConsoleLog('Python code loaded.');
}

function getPythonCode() {
    return editor.getValue();
}

function getFileData() {
    return editor.getValue();
}

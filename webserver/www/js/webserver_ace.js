var editor;

// On document ready this function will be called and initialize the complete website.
docReady(function(){
    // Setup the editor
    editor = ace.edit("editor");
    editor.setTheme("ace/theme/tomorrow_night");
    editor.session.setMode("ace/mode/python");
});

// Clear the workspace.
function newFile() {
    editor.setValue('# Write down your code ...\n');
}

// This function will be called after the load dialog form is shown and the load button within this dialog is pressed.
function loadFile(e) {
    var pythonCode = e.target.result;
    if (pythonCode) {
        editor.setValue(pythonCode);
    }
    apendConsoleLog('Python code loaded from local disk.');
}

function saveFile() {
    file = new File([editor.getValue()], 'HackerSchool.py', {type: 'text/plain;charset=utf-8'});
    saveAs(file);
    apendConsoleLog('Python code saved on local disk.')
}

function getPythonCode() {
    return editor.getValue();
}

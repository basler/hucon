var editor;

// On document ready this function will be called and initialize the complete website.
docReady(function(){
    ajax('POST', 'get_version', '', function(message) {
        var data = JSON.parse(message);
        console.log(data['version'])
        document.getElementById('version').innerHTML = data['version'];
    });

    // Setup the editor
    editor = ace.edit("editor");
    editor.setTheme("ace/theme/tomorrow_night");
    editor.session.setMode("ace/mode/python");
    editor.$blockScrolling = Infinity
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

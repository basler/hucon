var editor;

// On document ready this function will be called and initialize the complete website.
$(document).ready(function () {

    var sizes = localStorage.getItem('horizontalSplit-sizes');
    if (sizes) {
        sizes = JSON.parse(sizes)
    } else {
        sizes = [70, 30]  // default sizes
    }

    $.ajax('/get_version', {
        method: 'POST',
        success: function(message) {
            var data = JSON.parse(message);
            $('#version').html(data['version']);
        },
        error: appendErrorLog
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
}

function getPythonCode() {
    return editor.getValue();
}

function getFileData() {
    return editor.getValue();
}

function appendConsoleLog(message) {
    $('#consoleLog').append(message.replace(/\n/g, '<br>'));
    $("#logArea").scrollTop($("#logArea")[0].scrollHeight);
}

function appendErrorLog(request, status, error) {
    appendConsoleLog(error + ' : ' + request.responseText + '\n');
}

var currentFile = '';

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    fileDialog = document.getElementById('fileDialog');
    if (event.target == fileDialog) {
        closeFileDialog();
    }
    consoleLogDialog = document.getElementById('consoleLogDialog');
    if (event.target == consoleLogDialog) {
        closeConsoleLogDialog();
    }
}

// Open the load file dialog.
function openFileDialog(load, extension) {
    var parameter = {};
    parameter['load'] = load;
    parameter['extension'] = extension;

    console.log('currentFile: ' + currentFile);

    var title = '';
    var buttonText = '';

    if (load) {
        title = 'Load file';
        buttonText = 'Load';
    } else {
        title = 'Save file';
        buttonText = 'Save';
    }

    document.getElementById('fileText').hidden = load
    document.getElementById('fileOkButton').value = JSON.stringify(parameter);
    document.getElementById('fileDialogTitle').innerHTML = title;
    document.getElementById('fileOkButton').innerHTML = buttonText;

    fileDialog = document.getElementById('fileDialog');
    fileDialog.style.display = 'block';

    var data = {};
    data['command'] = 'get_file_list';

    ajax('POST', '__COMMAND__', JSON.stringify(data), function(message) {
        selection = document.getElementById('fileSelect');
        for(i = selection.options.length - 1 ; i >= 0 ; i--) {
            selection.remove(i);
        }

        var data = JSON.parse(message);
        // Create an empty option for the save dialog to prevent an overwrite of existing files.
        if (!load) {
            var opt = document.createElement('option');
            opt.text = '';
            opt.value = '';
            selection.options.add(opt);
        }

        var selectedIndex = 0;
        for (i=0; i<data['files'].length; i++) {
            var filename = data['files'][i]
            if (filename.endsWith(extension)) {
                var opt = document.createElement('option');
                var value = filename.slice(0, -extension.length);
                opt.text = value;
                opt.value = value;
                selection.options.add(opt);
                if (value == currentFile) {
                    selectedIndex = selection.options.length - 1;
                }
            }
        }

        selection.options[selectedIndex].selected = true;
        document.getElementById('fileText').value = selection.options[selection.selectedIndex].value;
    });
}

// This function will be called after the load dialog form is shown and the load button within this dialog is pressed.
function fileDialogOk() {
    var parameter = JSON.parse(document.getElementById('fileOkButton').value);
    var filename = document.getElementById('fileText').value;
    var command = '';
    var data = '';
    var callback;

    // Check the file name restrictions
    var reg = /^[A-Za-z0-9_]+$/;
    if (!reg.test(filename)) {
        alert('You have to enter a valid filename.\nOnly characters from a-z, numbers and _ are allowed.');
        return;
    }

    currentFile = filename;

    if (parameter['load']) {
        command = 'load';
        callback = function(message) {
            var fileData = message;
            if (parameter['extension'] == '.py') {
                fileData = fileData.replace(/HSTerm.term_exec/g, 'print')
            }
            loadFile(fileData);
        };
    } else {
        command = 'save';
        data = getFileData();
        if (parameter['extension'] == '.py') {
            data = data.replace(/print/g, 'HSTerm.term_exec');
        }
        callback = apendConsoleLog;
    }

    // Hide the load dialog modal.
    closeFileDialog();

    var url = '__FILE_ACCESS__?command=' + command + '&filename=' + filename + parameter['extension'];
    ajax('POST', url, data, callback);

    // Store also the python code when blockly code is saved.
    if (!parameter['load'] && parameter['extension'] != '.py') {
        var code = getPythonCode().replace(/print/g, 'HSTerm.term_exec');

        var url = '__FILE_ACCESS__?command=' + command + '&filename=' + filename + '.py';
        ajax('POST', url, code, callback);
    }
}

// Close the load file dialog
function closeFileDialog() {
    fileialog = document.getElementById('fileDialog');
    fileDialog.style.display = 'none';
}

// This fnction will show up the console log and insert the message into it.
function apendConsoleLog(message) {
    var time = new Date().toLocaleTimeString().replace('/.*(\d{2}:\d{2}:\d{2}).*/', '$1');
    var log = document.getElementById('consoleLog').value;
    document.getElementById('consoleLog').value = time + '\n' + message + '\n' + log;

    try {
        openConsoleLogDialog()
    }
    catch(err) {}
}

// Open the load file dialog.
function openConsoleLogDialog() {
    consoleLogDialog = document.getElementById('consoleLogDialog');
    consoleLogDialog.style.display = 'block';
}

// Close the load file dialog
function closeConsoleLogDialog() {
    consoleLogDialog = document.getElementById('consoleLogDialog');
    consoleLogDialog.style.display = 'none';
}

// This function will send via ajax a message to the server.
function command(value) {

    if (value == 'set_wifi') {
        var data = {};
        data['command'] = value;
        data['apName'] = document.getElementById('wifiText').value;
        data['password'] = document.getElementById('password').value;
        ajax('POST', '__COMMAND__', JSON.stringify(data), apendConsoleLog);

    } else if (value == 'execute') {
        var url = '__FILE_ACCESS__?command=execute';
        var code = getPythonCode().replace(/print/g, 'HSTerm.term_exec')

        ajax('POST', url, code, apendConsoleLog);

    } else if (value == 'save_password') {
        oldUsername = document.getElementById('current_username').value;
        oldPassword = document.getElementById('current_password').value;
        newUsername = document.getElementById('new_username').value;
        newPassword = document.getElementById('new_password').value;
        confirmPassword = document.getElementById('confirm_password').value;

        if (oldUsername == '' || oldPassword == '' || newUsername == '' || newPassword == '' || confirmPassword == '') {
            apendConsoleLog('You must fill every element.');
            return
        }

        if (newPassword != confirmPassword) {
            apendConsoleLog('The new and confirmed password are not the same.');
            return
        }

        oldKey = btoa(oldUsername + ':' + oldPassword);
        newKey = btoa(newUsername + ':' + newPassword);

        var data = {};
        data['command'] = value;
        data['oldKey'] = oldKey;
        data['newKey'] = newKey;
        ajax('POST', '__COMMAND__', JSON.stringify(data), apendConsoleLog);

    } else if (value == 'run') {

        var data = {};
        data['command'] = 'run'
        data['filename'] = document.getElementById('fileText').value + '.py';

        ajax('POST', '__COMMAND__', JSON.stringify(data), apendConsoleLog);
    }

}

// This function will handle an easy acces to some server requests.
function ajax(type, url, data, callback) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
            if (this.status == 200) {
                callback(this.responseText)
            } else if (this.status == 500) {
                apendConsoleLog(this.responseText);
            } else {
                alert('Could not get any access on the server.');
            }
        }
    };
    xhttp.open(type, url, false);
    xhttp.send(data);
}

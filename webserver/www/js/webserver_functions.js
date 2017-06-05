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
    document.getElementById('fileText').hidden = load
    document.getElementById('fileOkButton').value = load
    if (load) {
        document.getElementById('fileDialogTitle').innerHTML = 'Load File';
        document.getElementById('fileOkButton').innerHTML = 'Load';
    } else {
        document.getElementById('fileDialogTitle').innerHTML = 'Save File';
        document.getElementById('fileOkButton').innerHTML = 'Save';
    }

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

        for (i=0; i<data['files'].length; i++) {
            var filename = data['files'][i]
            if (filename.endsWith(extension)) {
                var opt = document.createElement('option');
                opt.text = filename;
                opt.value = filename;
                selection.options.add(opt);
            }
        }

        document.getElementById('fileText').value = selection.options[selection.selectedIndex].value;
    });
}

// This function will be called after the load dialog form is shown and the load button within this dialog is pressed.
function fileOkClicked() {
    var load = JSON.parse(document.getElementById('fileOkButton').value);

    var data = {}
    if (load) {
        data['command'] = 'get_file_data';
    } else {
        data['command'] = 'save_file_data';
        data['code'] = getFileData()
    }
    data['filename'] = document.getElementById('fileText').value;

    if (data['filename'] == '') {
        if (load) {
            alert('Please select a file load.')
        } else {
            alert('Write a name for the file to save.')
        }
        return
    }

    // Hide the load dialog modal.
    closeFileDialog();

    ajax('POST', '__COMMAND__', JSON.stringify(data), function(message) {
        if (load) {
            loadFile(message);
        } else {
            apendConsoleLog(message);
        }
    });
}

// Close the load file dialog
function closeFileDialog() {
    fileialog = document.getElementById('fileDialog');
    fileDialog.style.display = 'none';
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

    var data = {};
    data['command'] = value;

    if (value == 'execute') {
        data['code'] = getPythonCode()

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

        data['oldKey'] = oldKey;
        data['newKey'] = newKey;
    }

    ajax('POST', '__COMMAND__', JSON.stringify(data), function(message) {
        apendConsoleLog(message);
    });
}

// This fnction will show up the console log and insert the message into it.
function apendConsoleLog(message) {
    var time = new Date().toLocaleTimeString().replace('/.*(\d{2}:\d{2}:\d{2}).*/', '$1');
    document.getElementById('consoleLog').value = time + '\n\n' + message;

    openConsoleLogDialog()
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

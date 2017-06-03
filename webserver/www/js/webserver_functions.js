// On document ready this function will be called and initialize the complete website.
docReady(function(){
    // Add the change event to show the filename instead.
    input = document.getElementById('fileinput')
    if (input) {
        input.addEventListener( 'change', function( e )
        {
            var fileName = '';
            if( this.files && this.files.length > 1 )
                fileName = ( this.getAttribute( 'data-multiple-caption' ) || '' ).replace( '{count}', this.files.length );
            else
                fileName = e.target.value.split( '\\' ).pop();

            if( fileName )
                document.getElementById('fileLabel').querySelector( 'span' ).innerHTML = fileName;
        });
    }
});

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
    loadDialog = document.getElementById('loadDialog');
    if (event.target == loadDialog) {
        closeLoadDialog();
    }
    consoleLogDialog = document.getElementById('consoleLogDialog');
    if (event.target == consoleLogDialog) {
        closeConsoleLogDialog();
    }
}

// Open the load file dialog.
function openLoadDialog() {
    loadDialog = document.getElementById('loadDialog');
    loadDialog.style.display = 'block';
}

// This function will be called after the load dialog form is shown and the load button within this dialog is pressed.
function loadSelectedFile() {
    // Hide the load dialog modal.
    closeLoadDialog();

    var input, file, fr;

    if (typeof window.FileReader !== 'function') {
        alert('The file API is not supported on this browser yet.');
        return;
    }

    input = document.getElementById('fileinput');
    if (!input) {
        alert('Um, could not find the fileinput element.');
    }
    else if (!input.files) {
        alert('This browser does not seem to support the `files` property of file inputs.');
    }
    else if (!input.files[0]) {
        alert('Please select a file before clicking `Load`');
    }
    else {
        file = input.files[0];
        fr = new FileReader();
        fr.onload = loadFile;
        fr.readAsText(file);
    }
}

// Close the load file dialog
function closeLoadDialog() {
    loadDialog = document.getElementById('loadDialog');
    loadDialog.style.display = 'none';
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
    if (value == 'execute') {
        val = getPythonCode()

        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4) {
                if (this.status == 200) {
                    apendConsoleLog(this.responseText);
                } else {
                    alert('Could not set execute the command on the server.');
                }
            }
        };
        xhttp.open('POST', '__Execute__', false);
        xhttp.send(val);
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

        var val = 'command:save_password&oldKey:' + oldKey + '&newKey:' + newKey;
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4) {
                if (this.status == 200) {
                    apendConsoleLog(this.responseText);
                } else {
                    alert('Could not save the password on the server.');
                }
            }
        };
        xhttp.open('POST', '__Set__', false);
        xhttp.send(val);
    }
}

function apendConsoleLog(message) {
    var time = new Date().toLocaleTimeString().replace('/.*(\d{2}:\d{2}:\d{2}).*/', '$1');
    document.getElementById('consoleLog').value = time + '\n\n' + message;

    openConsoleLogDialog()
}

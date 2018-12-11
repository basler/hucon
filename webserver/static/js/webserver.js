// 2018-12-11
//
// Base javascript file to handle the communication between the browser and web server.
//
// Author: Sascha.MuellerzumHagen@baslerweb.com

// Ask the user to go before he goes.
$(window).bind("beforeunload", function(){
    if (HuConApp.UnsavedContent) {
        return "Do you really want to go?\nAll your unsaved data will be lost.";
    }
});

// On document ready this function will be called and do a base initialization.
$(document).ready(function () {
    // Update the version information on the ui
    HuConApp.updateVersion();

    // Set the button states based on running.
    HuConApp.isRunning();
});

// Handle some key bindings
$(window).bind('keydown', function(event) {
    if (event.ctrlKey || event.metaKey) {
        switch (String.fromCharCode(event.which).toLowerCase()) {
        case 'n':
            event.preventDefault();
            newFile();
            break;
        case 'o':
            event.preventDefault();
            openFileModal();
            break;
        case 's':
            event.preventDefault();
            saveFileModal();
            break;
        case 'r':
            event.preventDefault();
            run();
            break;
        case 'h':
            event.preventDefault();
            stop();
            break;
        }
    }
});

// HuCon Name-space
var HuConApp = {}

// Id for JSON-RPC protocol
HuConApp.RpcId = 0;

// Folder path to save and load on the device
HuConApp.Folder = '';

// File extension which is currently used.
HuConApp.FileExt = '';

// Remeber any changes after save.
HuConApp.UnsavedContent = false;

// Get a new JSON-RPC message data with a new id.
HuConApp.getRpcRequest = function() {
    jsonRpc = {};
    jsonRpc['jsonrpc'] = '2.0';
    jsonRpc['method'] = '';
    jsonRpc['params'] = '';
    jsonRpc['id'] = HuConApp.RpcId;

    // Increment the id for the next request.
    HuConApp.RpcId = HuConApp.RpcId + 1;

    return jsonRpc;
}

// Check the rpc response and return true whenever there is an error occurred.
// On error the message will printed on console log.
HuConApp.isResponseError = function(rpcResponse) {
    if (rpcResponse['error']) {
        HuConApp.appendConsoleLog(rpcResponse['error'], 'red');
        return true;
    }

    return false;
}

// Get the version from the server and update the ui.
HuConApp.updateVersion = function() {
    $('#version').hide();

    var rpcRequest = HuConApp.getRpcRequest();
    rpcRequest['method'] = 'get_version';

    $.ajax('/API', {
        method: 'POST',
        data: JSON.stringify(rpcRequest),
        dataType: 'json',
        success: function(rpcResponse) {
            if (HuConApp.isResponseError(rpcResponse)) {
                return;
            }

            $('#version').html(rpcResponse['result']);
            $('#version').show();
        },
        error: HuConApp.appendErrorLog
    });
}

// Poll for a new message.
HuConApp.poll = function() {
    var rpcRequest = HuConApp.getRpcRequest();
    rpcRequest['method'] = 'poll';

    $.ajax('/API', {
        method: 'POST',
        data: JSON.stringify(rpcRequest),
        dataType: 'json',
        success: function(rpcResponse) {

            if (rpcResponse['result'].length) {
                HuConApp.appendConsoleLog(rpcResponse['result']);
            };
            setTimeout(HuConApp.poll, 500);
        },
        error: function(message) {
            HuConApp.appendErrorLog(message);
            setTimeout(HuConApp.poll, 500);
        }
    });
}

// Run the code on the device and set the button states.
HuConApp.execute = function() {
    $('#consoleLog').html('');
    HuConApp.appendConsoleLog('Loading program ...', 'green');

    var rpcRequest = HuConApp.getRpcRequest();
    rpcRequest['method'] = 'execute';
    rpcRequest['params'] = getPythonCode();

    $.ajax('/API', {
        method: 'POST',
        data: JSON.stringify(rpcRequest),
        dataType: 'json',
        success: function(rpcResponse) {
            if (rpcResponse['result'] !== undefined) {
                HuConApp.appendConsoleLog(rpcResponse['result']);
            };
        },
        error: HuConApp.appendErrorLog
    });

    $('#runButton').addClass('disabled');
    $('#stopButton').removeClass('disabled');
    setTimeout(HuConApp.isRunning, 1000);
}

// Run the file directly from the device.
HuConApp.run = function() {
    $('#consoleLog').html('');
    HuConApp.appendConsoleLog('Loading program ...', 'green');

    var rpcRequest = HuConApp.getRpcRequest();
    rpcRequest['method'] = 'run';
    rpcRequest['params'] = HuConApp.Folder + '/' + $('#chooseFilename').val();

    $.ajax('/API', {
        method: 'POST',
        data: JSON.stringify(rpcRequest),
        dataType: 'json',
        success: function(rpcResponse) {
            if (rpcResponse['result'] !== undefined) {
                HuConApp.appendConsoleLog(rpcResponse['result']);
            };
        },
        error: HuConApp.appendErrorLog
    });

    $('#runButton').addClass('disabled');
    $('#stopButton').removeClass('disabled');
    setTimeout(HuConApp.isRunning, 1000);
}

// Stop the user application.
HuConApp.stop = function() {
    var rpcRequest = HuConApp.getRpcRequest();
    rpcRequest['method'] = 'kill';

    $.ajax('/API', {
        method: 'POST',
        data: JSON.stringify(rpcRequest),
        dataType: 'json',
        success: function(rpcResponse) {
            if (rpcResponse['result'] !== undefined) {
                HuConApp.appendConsoleLog(rpcResponse['result'], 'red');
            };
        },
        error: HuConApp.appendErrorLog
    });
}

// Check if the device is still running and set the button states.
HuConApp.isRunning = function() {
    var rpcRequest = HuConApp.getRpcRequest();
    rpcRequest['method'] = 'is_running';

    $.ajax('/API', {
        method: 'POST',
        data: JSON.stringify(rpcRequest),
        dataType: 'json',
        success: function(rpcResponse) {
            if (HuConApp.isResponseError(rpcResponse)) {
                return;
            }

            if (rpcResponse['result']) {
                $('#runButton').addClass('disabled');
                $('#stopButton').removeClass('disabled');
                setTimeout(HuConApp.isRunning, 1000);
            } else {
                $('#runButton').removeClass('disabled');
                $('#stopButton').addClass('disabled');
                HuConApp.appendConsoleLog('Done ...', 'green');
            }
        },
        error: HuConApp.appendErrorLog
    });
}

// Append a new message from the server or any script to the console.
HuConApp.appendConsoleLog = function(messages, colour) {
    if (Array.isArray(messages)) {
        messages.forEach(function(message) {
            HuConApp.appendConsoleLogMessage(message, colour);
        });
    } else {
        HuConApp.appendConsoleLogMessage(messages, colour);
    }
}

// Append an error message to the console and color it red.
HuConApp.appendErrorLog = function(request, status, error) {
    rpcResponse = JSON.parse(request.responseText)
    HuConApp.appendConsoleLog(error + ': ' + rpcResponse['error'], 'red');
}

// Append the message, which can be a an array, to the console output.
HuConApp.appendConsoleLogMessage = function(message, colour) {

    if (message === undefined) {
        return;
    }

    if (colour === undefined) {
        colour = 'black';
    }

    if (message.includes('Error:')) {
        colour = 'red';
    }

    $('#consoleLog').append($('<span>').css('color', colour).text(message)).append($('<br>'))
    $('#logArea').scrollTop($('#logArea')[0].scrollHeight);
}

// Show the code or hide it.
HuConApp.showCode = function() {
    show = localStorage.getItem('CodeShow');

    if (show === 'no') {
        $('#codeButton').removeClass('active');
        $('#blocklyArea').removeClass('twelve wide column');
        $('#blocklyArea').addClass('sixteen wide column');
        $('#codeArea').hide();
    } else {
        $('#codeButton').addClass('active');
        $('#blocklyArea').removeClass('sixteen wide column');
        $('#blocklyArea').addClass('twelve wide column');
        $('#codeArea').show();
    }

    window.dispatchEvent(new Event('resize'));
}

// Show/Hide the code view.
HuConApp.toggleCodeView = function() {

    if ($('#codeButton').hasClass('active')) {
        // collapse
        localStorage.setItem('CodeShow', 'no');
    } else {
        // show
        localStorage.setItem('CodeShow', 'yes');
    }

    HuConApp.showCode();
}

// Show the console or hide it.
HuConApp.showConsole = function() {
    show = localStorage.getItem('ConsoleShow');

    if (show === 'no') {
        $('#consoleButton').removeClass('active');
        $('#mainArea').removeClass('shortHeight');
        $('#mainArea').addClass('fullHeight');
        $('#logArea').hide();
    } else {
        $('#consoleButton').addClass('active');
        $('#mainArea').addClass('shortHeight');
        $('#mainArea').removeClass('fullHeight');
        $('#logArea').show();
    }

    window.dispatchEvent(new Event('resize'));
}

// Show/Hide the console view.
HuConApp.toggleConsoleView = function() {
    if ($('#consoleButton').hasClass('active')) {
        // collapse
        localStorage.setItem('ConsoleShow', 'no');
    } else {
        // show
        localStorage.setItem('ConsoleShow', 'yes');
    }

    HuConApp.showConsole();
}

// Show button Modal.
HuConApp.buttonModal = function() {
    $('#buttonModal').modal('show');
    $('#buttonEmbed').embed();
}

// Set the breadcrump based on the current folder.
HuConApp.setBreadcrumb = function(modal) {
    modal.html('<div class="divider">/</div>');

    var folderPath = HuConApp.Folder.split('/');
    for (var i = 0; i < folderPath.length; i++) {
        if (folderPath[i] != '') {
            modal.append('<div class="section">' + folderPath[i] + '</div>');
            modal.append('<div class="divider">/</div>');
        }
    }
}

// Show a form to create a new folder.
HuConApp.createNewFolder = function() {
    foldername = $('#folderFilename').val();

    if (foldername != '') {
        var rpcRequest = HuConApp.getRpcRequest();
        rpcRequest['method'] = 'create_folder';
        rpcRequest['params'] = HuConApp.Folder + '/' + foldername;

        $.ajax('/API', {
            method: 'POST',
            data: JSON.stringify(rpcRequest),
            dataType: 'json',
            error: HuConApp.appendErrorLog
        });

        HuConApp.saveFileModal(HuConApp.Folder);
    }
    console.log($('#folderFilename'));
}

// Show the file open modal and list all folder.
HuConApp.openFileModal = function(newFolder) {

    if (newFolder != undefined) {
        HuConApp.Folder = newFolder;
    }

    HuConApp.setBreadcrumb($('#openBreadcrumb'));

    var rpcRequest = HuConApp.getRpcRequest();
    rpcRequest['method'] = 'get_file_list';
    rpcRequest['params'] = HuConApp.Folder;

    $.ajax('/API', {
        method: 'POST',
        data: JSON.stringify(rpcRequest),
        dataType: 'json',
        success: function(rpcResponse) {
            HuConApp.configureLoadSaveModal(rpcResponse, $('#openFileList'), 'openFileModal', 'open');

            $('#openModal').modal('show');
        },
        error: function(request, status, error) {
            HuConApp.Folder = '';
            HuConApp.appendErrorLog(request, status, error);
        }
    });
}

// Hide the open file modal and load the content from the file.
HuConApp.loadFileFromDevice = function(filename) {
    $('#openModal').modal('hide');
    $('#consoleLog').html('');

    var rpcRequest = HuConApp.getRpcRequest();
    rpcRequest['method'] = 'load_file';
    rpcRequest['params'] = HuConApp.Folder + '/' + filename;

    // Store the filename for the save dialog
    $('#saveFilename').val(filename);

    $.ajax('/API', {
        method: 'POST',
        data: JSON.stringify(rpcRequest),
        dataType: 'json',
        success: function(rpcResponse) {
            if (HuConApp.isResponseError(rpcResponse)) {
                return
            }

            if (rpcResponse['result']) {
                setFileContent(rpcResponse['result']);

                HuConApp.appendConsoleLog('File "' + HuConApp.Folder + '/' + filename + '" loaded from local device.', 'green');

                HuConApp.UnsavedContent = false;
            }
        },
        error: HuConApp.appendErrorLog
    });
}

// Show the save file modal and load the file list from the device.
HuConApp.saveFileModal = function(newFolder) {

    // Set the new Folder
    if (newFolder != undefined) {
        HuConApp.Folder = newFolder;
    }

    // The example folder is read only, so go back to root on save.
    if (HuConApp.Folder == '/examples') {
        HuConApp.Folder = '';
    }

    HuConApp.setBreadcrumb($('#saveBreadcrumb'));

    var rpcRequest = HuConApp.getRpcRequest();
    rpcRequest['method'] = 'get_file_list';
    rpcRequest['params'] = HuConApp.Folder;

    $.ajax('/API', {
        method: 'POST',
        data: JSON.stringify(rpcRequest),
        dataType: 'json',
        success: function(rpcResponse) {
            HuConApp.configureLoadSaveModal(rpcResponse, $('#saveFileList'), 'saveFileModal', 'save');

            $('#saveModal').modal('show');
        },
        error: function(request, status, error) {
            HuConApp.Folder = '';
            HuConApp.appendErrorLog(request, status, error);
        }
    });
}

// Save the file on the device and hide the file save modal.
HuConApp.saveFileOnDevice = function() {
    $('#saveModal').modal('hide');

    $('#consoleLog').html('');

    // Abort on write within the example folder
    if (HuConApp.Folder == '/examples') {
        HuConApp.appendConsoleLog('The file is not written on device.\nThe examples folder is read only!', 'red');
        return;
    }

    // Get the filename without any extension.
    filename = $('#saveFilename').val();
    if (filename.substr(-HuConApp.FileExt.length) == HuConApp.FileExt) {
        filename = filename.slice(0, -HuConApp.FileExt.length);
    }
    $('#saveFilename').val(filename + HuConApp.FileExt);

    var rpcRequest = HuConApp.getRpcRequest();
    rpcRequest['method'] = 'save_file';
    rpcRequest['params'] = {};

    // Store the blockly code if needed
    if (HuConApp.FileExt == '.xml') {
        rpcRequest['params']['filename'] = HuConApp.Folder + '/' + filename + '.xml';
        rpcRequest['params']['data'] = getBlocklyCode();
        $.ajax('/API', {
            method: 'POST',
            data: JSON.stringify(rpcRequest),
            dataType: 'json',
            success: function (rpcResponse) {
                if (HuConApp.isResponseError(rpcResponse)) {
                    return
                }

                HuConApp.appendConsoleLog(rpcResponse['result']);
            },
            error: HuConApp.appendErrorLog
        });
    }

    // Store the python code
    rpcRequest['params']['filename'] = HuConApp.Folder + '/' + filename + '.py';
    rpcRequest['params']['data'] = getPythonCode();
    $.ajax('/API', {
        method: 'POST',
        data: JSON.stringify(rpcRequest),
        dataType: 'json',
        success: function (rpcResponse) {
            if (HuConApp.isResponseError(rpcResponse)) {
                return
            }

            HuConApp.appendConsoleLog(rpcResponse['result']);
        },
        error: HuConApp.appendErrorLog
    });

    HuConApp.UnsavedContent = false;
}

// Configure the load or save modal correctly.
HuConApp.configureLoadSaveModal = function(rpcResponse, modal, folderCallback, state) {
    // clear the list
    modal.html('');

    if (HuConApp.isResponseError(rpcResponse)) {
        return
    }

    folderHtml = `
    <div onclick="HuConApp.{1}(\'{2}\')" class="item ok">
        <i class="folder icon"></i>
        <div class="content header">{3}</div>
    </div>
    `;

    // Append the folder up if needed.
    if (HuConApp.Folder != '') {
        // Determine the parent folder
        var upperFolder = HuConApp.Folder.slice(0, HuConApp.Folder.lastIndexOf('/'));
        modal.append(HuConApp.formatVarString(folderHtml, folderCallback, upperFolder, '..'));
    }

    // Add the folder to the empty list
    for (i=0; i<rpcResponse['result'].length; i++) {
        var filename = rpcResponse['result'][i];
        if (filename.indexOf('.') === -1) {
            var newFolder = HuConApp.Folder + '/' + filename;

            // Do not show the examples folder as possible folder.
            if ((state == 'save') && (newFolder == '/examples')) {
                continue;
            }

            modal.append(HuConApp.formatVarString(folderHtml, folderCallback, newFolder, filename));
        }
    }

    fileHtml = '';
    if (state == 'open') {
        fileHtml = `
        <div onclick="HuConApp.loadFileFromDevice(\'{1}\');" class="item ok">
            <i class="file icon"></i>
            <div class="content header">{1}</div>
        </div>
        `;
    } else if(state == 'save') {
        fileHtml = `
        <div onclick="$(\'#saveFilename\').val(\'{1}\');" class="item ok">
            <i class="file icon"></i>
            <div class="content header">{1}</div>
        </div>
        `;
    } else {
        fileHtml = `
        <div onclick="HuConApp.setFileFromDevice(\'{1}\');" class="item ok">
            <i class="file icon"></i>
            <div class="content header">{1}</div>
        </div>
        `;
    }

    // Add the files to the empty list
    for (i=0; i<rpcResponse['result'].length; i++) {
        var filename = rpcResponse['result'][i];
        if (filename.substr(-HuConApp.FileExt.length) === HuConApp.FileExt) {
            modal.append(HuConApp.formatVarString(fileHtml, filename));
        }
    }
}

// Show the choose file modal and load the file list from the device.
HuConApp.chooseFileModal = function(newFolder) {

    // Set the new Folder
    if (newFolder != undefined) {
        HuConApp.Folder = newFolder;
    }

    HuConApp.setBreadcrumb($('#chooseBreadcrumb'));

    var rpcRequest = HuConApp.getRpcRequest();
    rpcRequest['method'] = 'get_file_list';
    rpcRequest['params'] = HuConApp.Folder;

    $.ajax('/API', {
        method: 'POST',
        data: JSON.stringify(rpcRequest),
        dataType: 'json',
        success: function(rpcResponse) {
            HuConApp.configureLoadSaveModal(rpcResponse, $('#chooseFileList'), 'chooseFileModal', 'choose');

            $('#chooseModal').modal('show');
        },
        error: function(request, status, error) {
            HuConApp.Folder = '';
            HuConApp.appendErrorLog(request, status, error);
        }
    });
}

// Set the file to run it on the mobile page.
HuConApp.setFileFromDevice = function(filename) {

    $('#chooseFilename').val(filename);
    $('#chooseModal').modal('hide');
}

HuConApp.formatVarString = function() {
    var args = [].slice.call(arguments);
    if(this.toString() != '[object Object]')
    {
        args.unshift(this.toString());
    }

    var pattern = new RegExp('{([1-' + args.length + '])}','g');
    return String(args[0]).replace(pattern, function(match, index) { return args[index]; });
}

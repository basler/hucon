// On document ready this function will be called and do a base initialization.
$(document).ready(function () {
    // Update the version information on the ui
    HuConApp.updateVersion();
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
    rpcRequest['params'] = document.getElementById('filename').value;

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

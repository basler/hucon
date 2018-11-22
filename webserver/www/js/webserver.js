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

// Get the version from the server and update the ui.
function updateVersion() {

    $('#version').hide();

    $.ajax('/get_version', {
        method: 'POST',
        dataType: 'json',
        success: function(data) {
            $('#version').html(data['version']);
            $('#version').show();
        },
        error: appendErrorLog
    });

}

// Poll for a new message.
function poll() {
    $.ajax('/poll', {
        method: 'POST',
        dataType: 'json',
        success: function(data) {

            if (data['message'].length) {
                appendConsoleLog(data['message']);
            };
            setTimeout(poll, 500);
        },
        error: function(message) {
            appendErrorLog(message);
            setTimeout(poll, 500);
        }
    });
}

// Run the code on the device and set the button states.
function run() {
    $('#consoleLog').html('');
    appendConsoleLog('Loading program ...', 'green');

    var data = {};
    data['data'] = getPythonCode();
    $.ajax('/execute', {
        method: 'POST',
        data: JSON.stringify(data),
        success: appendConsoleLog,
        error: appendErrorLog
    });

    $('#runButton').addClass('disabled');
    $('#stopButton').removeClass('disabled');
    setTimeout(isRunning, 1000);
}

// Stop the user application.
function stop() {
    $.ajax('/kill', {
        method: 'POST',
        success: function(message) {
            appendConsoleLog(message, 'red');
        },
        error: appendErrorLog
    });
}

// Check if the device is still running and set the button states.
function isRunning() {
    $.ajax('/is_running', {
        method: 'POST',
        dataType: 'json',
        success: function(data) {
            if (data['is_running']) {
                setTimeout(isRunning, 1000);
            } else {
                $('#runButton').removeClass('disabled');
                $('#stopButton').addClass('disabled');
                appendConsoleLog('Done ...', 'green');
            }
        },
        error: appendErrorLog
    });
}

// Append a new message from the server or any script to the console.
function appendConsoleLog(messages, colour) {
    if (Array.isArray(messages)) {
        messages.forEach(function(message) {
            appendConsoleLogMessage(message, colour);
        });
    } else {
        appendConsoleLogMessage(messages, colour);
    }
}

// Append an error message to the console and color it red.
function appendErrorLog(request, status, error) {
    appendConsoleLog(error + ' : ' + request.responseText, 'red');
}

// Append the message, which can be a an array, to the console output.
function appendConsoleLogMessage(message, colour) {

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
function showCode() {
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
function toggleCodeView() {

    if ($('#codeButton').hasClass('active')) {
        // collapse
        localStorage.setItem('CodeShow', 'no');
        showCode();
    } else {
        // show
        localStorage.setItem('CodeShow', 'yes');
        showCode();
    }
}

// Show the console or hide it.
function showConsole() {
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
function toggleConsoleView() {
    if ($('#consoleButton').hasClass('active')) {
        // collapse
        localStorage.setItem('ConsoleShow', 'no');
        showConsole();
    } else {
        // show
        localStorage.setItem('ConsoleShow', 'yes');
        showConsole();
    }
}

// Show button Modal.
function buttonModal() {
    $('#buttonModal').modal('show');
    $('#buttonEmbed').embed();
}


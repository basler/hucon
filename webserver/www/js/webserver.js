function poll() {
    $.ajax('/poll', {
        method: 'POST',
        dataType: 'json',
        success: function(data) {

            if (data['message'].length) {
                console.log(data['message'])
                appendConsoleLog(data['message']);
            };
            setTimeout(poll, 500);
        },
        error: function(message) {
            console.log(message)
            appendErrorLog(message);
            setTimeout(poll, 500);
        }
    });
}

function appendConsoleLog(messages, colour='black') {
    if (Array.isArray(messages)) {
        messages.forEach(function(message) {
            appendConsoleLogMessage(message, colour);
        });
    } else {
        appendConsoleLogMessage(messages, colour);
    }
}

function appendErrorLog(request, status, error) {
    appendConsoleLog(error + ' : ' + request.responseText, 'red');
}


var blocklyWorkspace;

// On document ready this function will be called and initialize the complete website.
$(document).ready(function () {

    window.addEventListener('resize', onResize);

    $.ajax('/get_version', {
        method: 'POST',
        success: function(message) {
            var data = JSON.parse(message);
            $('#version').html(data['version']);
        },
        error: appendErrorLog
    });

    $.ajax('xml/toolbox.xml', {
        method: 'GET',
        dataType: 'text',
        success: function (message) {
            console.log(message);
            // Initialize blockly
            // Do this as a last step in this function to calculate the size correctly!
            var blocklyDiv = document.getElementById('blocklyDiv');
            blocklyWorkspace = Blockly.inject(blocklyDiv, {toolbox: message});

            // Add the listener on resize to call the onResize function
            onResize();
            Blockly.svgResize(blocklyWorkspace);

            // Add the listener on every change to update the code
            blocklyWorkspace.addChangeListener(udpateCode);
        },
        error: appendErrorLog
    });
});

function onResize(){
    var blocklyArea = document.getElementById('mainArea');
    var blocklyDiv = document.getElementById('blocklyDiv');

    // Position blocklyDiv over blocklyArea.
    blocklyDiv.style.left = '0px';
    blocklyDiv.style.top = '0px';
    blocklyDiv.style.width = (blocklyArea.offsetWidth - 2) + 'px';
    blocklyDiv.style.height = (blocklyArea.offsetHeight - 2) + 'px';
};

function toggleCodeView() {

    if ($('#codeButton').hasClass('active')) {
        // collapse
        $('#codeButton').removeClass('active');
        $('#mainArea').removeClass('shortWidth');
        $('#mainArea').addClass('fullWidth');
        $('#codeArea').hide();
    } else {
        // show
        $('#codeButton').addClass('active');
        $('#mainArea').addClass('shortWidth');
        $('#mainArea').removeClass('fullWidth');
        $('#codeArea').show();
    }

    window.dispatchEvent(new Event('resize'));
}

function newFile() {
    Blockly.mainWorkspace.clear();
    $('#consoleLog').html('');
}

function loadFile(data) {
    if (data) {
        Blockly.mainWorkspace.clear();
        xmlDom = Blockly.Xml.textToDom(data);
        Blockly.Xml.domToWorkspace(xmlDom, Blockly.mainWorkspace);
    }
    appendConsoleLog('Blockly workspace loaded from local device.\n');
}

function getPythonCode() {
    return Blockly.Python.workspaceToCode(blocklyWorkspace);
}

function getFileData() {
    var xmlDom = Blockly.Xml.workspaceToDom(Blockly.mainWorkspace);
    var xmlText = Blockly.Xml.domToPrettyText(xmlDom);

    return xmlText;
}

// This function will be called whenever an element on the workspace is changed
// to update the code and show it on the page.
function udpateCode(event) {
    var code = Blockly.Python.workspaceToCode(blocklyWorkspace);
    code = code.replace(/\n/g, '<br>');
    $('#pythonCode').html(code);
}

function appendConsoleLog(message) {
    $('#consoleLog').append(message.replace(/\n/g, '<br>'));
    $("#logArea").scrollTop($("#logArea")[0].scrollHeight);
}

function appendErrorLog(request, status, error) {
    appendConsoleLog(error + ' : ' + request.responseText + '\n');
}

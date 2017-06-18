var blocklyWorkspace;

// On document ready this function will be called and initialize the complete website.
docReady(function(){
    ajax('GET', 'xml/toolbox.xml', '', function(message) {
        // Initialize blockly
        // Do this as a last step in this function to calculate the size correctly!
        var blocklyArea = document.getElementById('blocklyArea');
        var blocklyDiv = document.getElementById('blocklyDiv');
        blocklyWorkspace = Blockly.inject(blocklyDiv, {toolbox: message});

        // Add the listener on resize to call the onResize function
        window.addEventListener('resize', onResize, false);
        onResize();
        Blockly.svgResize(blocklyWorkspace);

        // Add the listener on every change to update the code
        blocklyWorkspace.addChangeListener(udpateCode);
    });
});

function newFile() {
    Blockly.mainWorkspace.clear();
}

function loadFile(data) {
    if (data) {
        Blockly.mainWorkspace.clear();
        xmlDom = Blockly.Xml.textToDom(data);
        Blockly.Xml.domToWorkspace(xmlDom, Blockly.mainWorkspace);
    }
    apendConsoleLog('Blockly workspace loaded from local disk.\n');
}

function getPythonCode() {
    return Blockly.Python.workspaceToCode(blocklyWorkspace);
}

function getFileData() {
    var xmlDom = Blockly.Xml.workspaceToDom(Blockly.mainWorkspace);
    var xmlText = Blockly.Xml.domToPrettyText(xmlDom);

    return xmlText;
}

// On every change of the window, this function will be called to update the
// blockly size area.
function onResize(e) {
    var blocklyArea = document.getElementById('blocklyArea');
    var blocklyDiv = document.getElementById('blocklyDiv');

    // Compute the absolute coordinates and dimensions of blocklyArea.
    var element = blocklyArea;
    var x = 0;
    var y = 0;
    do {
        x += element.offsetLeft;
        y += element.offsetTop;
        element = element.offsetParent;
    } while (element);

    // Position blocklyDiv over blocklyArea.
    blocklyDiv.style.left = x + 'px';
    blocklyDiv.style.top = y + 'px';
    blocklyDiv.style.width = blocklyArea.offsetWidth + 'px';
    blocklyDiv.style.height = (blocklyArea.offsetHeight - 20) + 'px';
}

// This function will be called whenever an element on the workspace is changed
// to update the code and show it on the page.
function udpateCode(event) {
    var code = Blockly.Python.workspaceToCode(blocklyWorkspace);
    document.getElementById('pythonCode').value = code;
}

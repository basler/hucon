// We need for the update of the code the blockly workspace.
var blocklyWorkspace;

// On document ready this function will be called and initialize the complete website.
docReady(function(){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4) {
            if (this.status == 200) {
                // Initialize blockly
                // Do this as a last step in this function to calculate the size correctly!
                var blocklyArea = document.getElementById('blocklyArea');
                var blocklyDiv = document.getElementById('blocklyDiv');
                blocklyWorkspace = Blockly.inject(blocklyDiv, {toolbox: this.responseText});

                // Add the listener on resize to call the onResize function
                window.addEventListener('resize', onResize, false);
                onResize();
                Blockly.svgResize(blocklyWorkspace);

                // Add the listener on every change to update the code
                blocklyWorkspace.addChangeListener(udpateCode);
            } else {
                alert('Could not load the blockly toolbox!');
            }
        }
    };
    xhttp.open('GET', 'xml/toolbox.xml', false);
    xhttp.send();
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

// Clear the workspace.
function newFile() {
    Blockly.mainWorkspace.clear();
}

// This function will be called after the load dialog form is shown and the load button within this dialog is pressed.
function loadFile(e) {
    var xmlText = e.target.result;
    if (xmlText) {
        Blockly.mainWorkspace.clear();
        xmlDom = Blockly.Xml.textToDom(xmlText);
        Blockly.Xml.domToWorkspace(Blockly.mainWorkspace, xmlDom);
    }
    apendConsoleLog('Blockly workspace loaded from local disk.');
}

function saveFile() {
    var xmlDom = Blockly.Xml.workspaceToDom(Blockly.mainWorkspace);
    var xmlText = Blockly.Xml.domToPrettyText(xmlDom);

    file = new File([xmlText], 'HackerSchool-blockly.xml', {type: 'text/plain;charset=utf-8'});
    saveAs(file);
    apendConsoleLog('Blockly workspace save on local disk.')
}

function getPythonCode() {
    return Blockly.Python.workspaceToCode(blocklyWorkspace);
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

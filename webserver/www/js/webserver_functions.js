// We need for the update of the code the blockly workspace.
var blocklyWorkspace;


// On document ready this function will be called and initialize the complete website.
$(document).ready(function(){

    // Define the load dialog to load the blockly file from a local file.
    var dialog = $("#load-dialog").dialog({
        autoOpen: false,
        height: 200,
        width: 450,
        modal: true,
        buttons: {
            "Load": loadFile,
            Cancel: function() {
                dialog.dialog( "close" );
            }
        }
    });

    // Initialize the JQery UI elements
    $("#newCommand").button({
        icons: {primary: 'fa fa-file-o'},
        showLabel: false
    }).click(clearWorkspace);

    $("#loadCommand").button({
        icons: {primary: 'fa fa-folder-open-o'},
        showLabel: false
    }).click(openLoadDialog);

    $("#saveCommand").button({
        icons: {primary: 'fa fa-floppy-o'},
        showLabel: false
    }).click(saveWorkspace);

    $("#runCommand").button({
        icons: {primary: 'fa fa-play'},
        showLabel: false
    }).click(setCommand);

    // hide the alert view
    $("#alertView").hide();

    // Initialize blockly
    // Do this as a last setp in this function to calculate the size correctly!
    var blocklyArea = document.getElementById('blocklyArea');
    var blocklyDiv = document.getElementById('blocklyDiv');
    blocklyWorkspace = Blockly.inject(blocklyDiv, {toolbox: document.getElementById('toolbox')});

    // Add the listener on resize to call the onResize function
    window.addEventListener('resize', onResize, false);
    onResize();
    Blockly.svgResize(blocklyWorkspace);

    // Add the listener on every change to update the code
    blocklyWorkspace.addChangeListener(udpateCode);

});


// Clear the workspace.
function clearWorkspace() {
    Blockly.mainWorkspace.clear();
}


// Open the load file dialog
function openLoadDialog() {
    var dialog = $("#load-dialog");
    dialog.dialog( "open" );
}


// This function will be called after the load dialog form is shown and the load button within this dialog is pressed.
function loadFile() {
    $("#load-dialog").dialog( "close" );
    var input, file, fr;

    if (typeof window.FileReader !== 'function') {
      alert("The file API isn't supported on this browser yet.");
      return;
    }

    input = document.getElementById('fileinput');
    if (!input) {
      alert("Um, couldn't find the fileinput element.");
    }
    else if (!input.files) {
      alert("This browser doesn't seem to support the `files` property of file inputs.");
    }
    else if (!input.files[0]) {
      alert("Please select a file before clicking 'Load'");
    }
    else {
      file = input.files[0];
      fr = new FileReader();
      fr.onload = receivedText;
      fr.readAsText(file);
    }

    function receivedText(e) {
        var xmlText = e.target.result;
        if (xmlText) {
            Blockly.mainWorkspace.clear();
            xmlDom = Blockly.Xml.textToDom(xmlText);
            Blockly.Xml.domToWorkspace(Blockly.mainWorkspace, xmlDom);
        }
        showAlertView("Blockly workspace load from local disk.")
    }
}


// Save the workspace on the local browser cache.
function saveWorkspace() {
    var xmlDom = Blockly.Xml.workspaceToDom(Blockly.mainWorkspace);
    var xmlText = Blockly.Xml.domToPrettyText(xmlDom);

    // localStorage.setItem("blockly_hackerschool.xml", xmlText);
    file = new File([xmlText], 'HackerSchool-blockly.xml', {type: "text/plain;charset=utf-8"});
    saveAs(file);
    showAlertView("Blockly workspace save on local disk.")
}


// This function will send via ajax a message to the server.
function setCommand() {
    command = $(this).val();

    if (command == "execute") {
        val = Blockly.Python.workspaceToCode(blocklyWorkspace);

        $.ajax({
            type: 'POST',
            url: '__Execute__',
            async: false,
            data: val
        })
        .done(function(result) {
            // TODO: Formate the text in a better way!
            showAlertView("Data send.<br>Result:<br>\n" + result);
        })
        .fail(function() {
            showAlertView("Could not set execute the command on the server.");
        });
    }
}


// Whenever this function will be called, a message will shown on the bottom
// page and the message will be hidden after a short time.
function showAlertView(message) {
    // change the text
    $("#errorMessage").html(message)
    // show the alert div
    var options = {};
    $("#alertView").show("drop", options, 500, hideAlertView);
}


// This function will hide the allert div.
function hideAlertView() {
    setTimeout(function() {
        $("#alertView:visible").removeAttr("style").fadeOut();
    }, 10000 );
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

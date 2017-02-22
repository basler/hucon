// We need for the update of the code the blockly workspace.
var blocklyWorkspace;

// On document ready this function will be called and initialize the complete website.
$(document).ready(function(){

    // Initialize blockly
    var blocklyArea = document.getElementById('blocklyArea');
    var blocklyDiv = document.getElementById('blocklyDiv');
    blocklyWorkspace = Blockly.inject(blocklyDiv, {toolbox: document.getElementById('toolbox')});

    // Add the listener on resize to call the onResize function
    window.addEventListener('resize', onResize, false);
    onResize();
    Blockly.svgResize(blocklyWorkspace);

    // Add the listener on every change to update the code
    blocklyWorkspace.addChangeListener(udpateCode);

    // Initialize the JQery UI elements
    $("#RunCommand").button().click(setCommand);
    $("#RunCommand-icon").button({
        icon: "ui-icon-play",
        showLabel: false
    }).click(setCommand)
    $("#StopCommand-icon").button({
        icon: "ui-icon-stop",
        showLabel: false
    }).click(setCommand)

    // hide the alert view
    $("#alertView").hide();
});

// This function will be called whenever an element on the workspace is changed
// to update the code and show it on the page.
function udpateCode(event) {
    var code = Blockly.Python.workspaceToCode(blocklyWorkspace);
    console.log(code);
    document.getElementById('pythonCode').innerHTML = code;
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
    blocklyDiv.style.height = blocklyArea.offsetHeight + 'px';
};

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

// This function will send via ajax a message to the server.
function setCommand() {
    var name = $(this).attr('id');
    var val = "";

    console.log("set others");
    val = $(this).val();

    $.ajax({
        type: 'POST',
        url: '__SetValue__',
        async: false,
        data: name + '=' + val
    })
    .fail(function() { showAlertView("Could not set " + name); });

    showAlertView("Command set " + val);

    return true;
}

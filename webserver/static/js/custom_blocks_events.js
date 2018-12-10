const COLOR_EVENTS = 250;

var eventDict = null;

// This function will crate the dictionary for the Event object.
// There is a hack insisde this function to detect that there is a redraw of the blockly engine.
// It should be rewritten when I understand the system a little bit more.
function appendEvent(eventName, funcName) {
    // add the nedded include
    Blockly.Python.definitions_['import_event'] = 'from hucon import Event, Button';

    // Create or append the event to the list
    if (Blockly.Python.definitions_['eventDict'] == undefined) {
        Blockly.Python.definitions_['eventDict'] = '';
        eventDict = `events_dict = {
  "${eventName}": Button(${funcName})
}

process_events = Event(events_dict)
`;
    } else {
        eventDict = eventDict.replace('\n}', `,\n  "${eventName}": Button(${funcName})\n}`);
    }
}


Blockly.Blocks['event_init'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("Init events");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(COLOR_EVENTS);
        this.setTooltip("Initialize the event engine.");
    }
};
Blockly.Python['event_init'] = function(block) {
    return eventDict;
};


Blockly.Blocks['event_run_endless'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("Run endless ...");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(COLOR_EVENTS);
        this.setTooltip("Run a process in an endless loop to catch all events.");
    }
};
Blockly.Python['event_run_endless'] = function(block) {
    return 'process_events.run()\n';
};


Blockly.Blocks['event_stop_endless'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("Stop endless process");
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(COLOR_EVENTS);
        this.setTooltip("Stop the current endless running event process.");
    }
};
Blockly.Python['event_stop_endless'] = function(block) {
    return 'process_events.stop()\n';
};


Blockly.Blocks['event_button_object'] = {
    init: function() {
        this.appendDummyInput()
            .appendField("Button Event");
        this.appendStatementInput("function")
            .setCheck(null)
            .appendField(new Blockly.FieldTextInput("EventName"), "EventName");
        this.setColour(COLOR_EVENTS);
        this.setTooltip("The content of this block is called whenever the event occurred.");
        this.setHelpUrl("");
    }
};
Blockly.Python['event_button_object'] = function(block) {
    // Catch all global variables.
    var globals = [];
    globals.push('process_events');
    var variables = Blockly.Variables.allUsedVarModels(block.workspace) || [];
    for (var i = 0, variable; variable = variables[i]; i++) {
        globals.push(Blockly.Python.variableDB_.getName(variable.name, Blockly.Variables.NAME_TYPE));
    }
    globals = globals.length ? Blockly.Python.INDENT + 'global ' + globals.join(', ') + '\n' : '';

    var statementsFunc = Blockly.Python.statementToCode(block, 'function');

    var funcName = Blockly.Python.variableDB_.getName(block.getFieldValue('EventName'), Blockly.Procedures.NAME_TYPE);

    if (statementsFunc == '') {
        statementsFunc = Blockly.Python.PASS;
    }

    var code = `def ${funcName}():
${globals}${statementsFunc}
`
    code = Blockly.Python.scrub_(block, code)
    Blockly.Python.definitions_['%' + funcName] = code;

    appendEvent(block.getFieldValue('EventName'), funcName);
    return null;
};

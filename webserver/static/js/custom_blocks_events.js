// custom_blocks_events.js - Blockly blocks to support events.
//
// Copyright (C) 2019 Basler AG
// All rights reserved.
//
// This software may be modified and distributed under the terms
// of the BSD license.  See the LICENSE file for details.

var eventDict = null;

// This function will crate the dictionary for the Event object.
// There is a hack insisde this function to detect that there is a redraw of the blockly engine.
// It should be rewritten when I understand the system a little bit more.
function appendEvent(eventName, funcName, x, y, width, height) {
    // add the nedded include
    Blockly.Python.definitions_.import_event = 'from hucon import EventSystem, ButtonEvent';

    // Create or append the event to the list
    if (Blockly.Python.definitions_['eventDict'] == undefined) {
        Blockly.Python.definitions_.eventDict = '';
        eventDict = [
            '# Map event name to callback.',
            'events_dict = {',
            '  "{1}": ButtonEvent(register_callback={2}, x={3}, y={4}, width={5}, height={6})',
            '}',
            '',
            '# Setup event system.',
            'process_events = EventSystem(events_dict)',
            ''
        ].join('\n');
    } else {
        eventDict = eventDict.replace('\n}', ',\n  "{1}": ButtonEvent(register_callback={2}, x={3}, y={4}, width={5}, height={6})\n}');
    }

    eventDict = HuConApp.formatVarString(eventDict, eventName, funcName, x, y, width, height);
}

Blockly.Blocks.event_init = {
    init: function () {
        this.appendDummyInput()
            .appendField(Blockly.Msg['HUCON_EVENTS_INIT']);
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(Blockly.Msg['HUCON_EVENTS_HUE']);
        this.setTooltip(Blockly.Msg['HUCON_EVENTS_TOOLTIP']);
    }
};
Blockly.Python.event_init = function(block) {
    return eventDict;
};

Blockly.Blocks.event_run_endless = {
    init: function () {
        this.appendDummyInput()
            .appendField(Blockly.Msg['HUCON_EVENTS_RUN_ENDLESS']);
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(Blockly.Msg['HUCON_EVENTS_HUE']);

        this.setTooltip(Blockly.Msg['HUCON_EVENTS_RUN_ENDLESS_TOOLTIP']);
    }
};
Blockly.Python.event_run_endless = function(block) {
    return 'process_events.run()\n';
};

Blockly.Blocks.event_stop_endless = {
    init: function () {
        this.appendDummyInput()
            .appendField(Blockly.Msg['HUCON_EVENTS_STOP_ENDLESS']);
        this.setPreviousStatement(true, null);
        this.setNextStatement(true, null);
        this.setColour(Blockly.Msg['HUCON_EVENTS_HUE']);
        this.setTooltip(Blockly.Msg['HUCON_EVENTS_STOP_ENDLESS_TOOLTIP']);
    }
};
Blockly.Python.event_stop_endless = function(block) {
    return 'process_events.stop()\n';
};

Blockly.Blocks.event_button_object = {
    init: function () {
        this.appendDummyInput()
            .appendField(Blockly.Msg['HUCON_EVENTS_BUTTON']);
        this.appendDummyInput('Values')
            .appendField(Blockly.Msg['HUCON_EVENTS_BUTTON_X'])
            .appendField(new Blockly.FieldNumber(0, 0, 9, 1), 'X')
            .appendField(Blockly.Msg['HUCON_EVENTS_BUTTON_Y'])
            .appendField(new Blockly.FieldNumber(0, 0, 9, 1), 'Y')
            .appendField(Blockly.Msg['HUCON_EVENTS_BUTTON_WIDTH'])
            .appendField(new Blockly.FieldNumber(1, 1, 10, 1), 'Width')
            .appendField(Blockly.Msg['HUCON_EVENTS_BUTTON_HEIGHT'])
            .appendField(new Blockly.FieldNumber(1, 1, 10 ,1), 'Height');
        // this.setInputsInline(true);
        this.appendStatementInput('function')
            .setCheck(null)
            .appendField(new Blockly.FieldTextInput(Blockly.Msg['HUCON_EVENTS_FUNC']), 'EventName');
        this.setColour(Blockly.Msg['HUCON_EVENTS_HUE']);

        var thisBlock = this;
        this.setTooltip(function () {
            return Blockly.Msg['HUCON_EVENTS_BUTTON_TOOLTIP_1'] + thisBlock.getFieldValue('EventName') + Blockly.Msg['HUCON_EVENTS_BUTTON_TOOLTIP_2'];
        });

        this.setOnChange(function (changeEvent) {
            if (changeEvent.type === Blockly.Events.BLOCK_CHANGE) {
                let values = this.getInput('Values')

                let x = values.fieldRow.find(({name}) => name === 'X').getValue()
                let y = values.fieldRow.find(({name}) => name === 'Y').getValue()
                let width  = values.fieldRow.find(({name}) => name === 'Width').getValue()
                let height = values.fieldRow.find(({name}) => name === 'Height').getValue()

                if ((x + width) > 10)
                    values.fieldRow.find(({name}) => name === 'Width').setValue(10 - x);

                if ((y + height) > 10)
                    values.fieldRow.find(({name}) => name === 'Height').setValue(10 - y);
            }
            });
    },
};
Blockly.Python.event_button_object = function(block) {
    // Catch all global variables.
    var globals = [];
    globals.push('process_events');
    var variables = Blockly.Variables.allUsedVarModels(block.workspace) || [];
    for (var i = 0, variable; variable = variables[i]; i++) {
        globals.push(Blockly.Python.variableDB_.getName(variable.name, Blockly.Variables.NAME_TYPE));
    }
    globals = globals.length ? Blockly.Python.INDENT + 'global ' + globals.join(', ') + '\n' : '';

    var statementsFunc = Blockly.Python.statementToCode(block, 'function');

    var eventName = block.getFieldValue('EventName');
    var funcName = Blockly.Python.variableDB_.getName(eventName, Blockly.Procedures.NAME_TYPE);
    var x = Blockly.Python.valueToCode(block, 'X', Blockly.Python.ORDER_ATOMIC) || '0';
    var y = Blockly.Python.valueToCode(block, 'Y', Blockly.Python.ORDER_ATOMIC) || '0';
    var width = Blockly.Python.valueToCode(block, 'Width', Blockly.Python.ORDER_ATOMIC) || '1';
    var height = Blockly.Python.valueToCode(block, 'Height', Blockly.Python.ORDER_ATOMIC) || '1';

    if (statementsFunc == '') {
        statementsFunc = Blockly.Python.PASS;
    }

    var code = [
        'def {1}():',
        '  """ Callback for Button \'{2}\' event.',
        '  """',
        globals + statementsFunc,
        ''
    ].join('\n');
    code = HuConApp.formatVarString(code, funcName, eventName);

    code = Blockly.Python.scrub_(block, code);
    Blockly.Python.definitions_['%' + funcName] = code;

    appendEvent(eventName, funcName, x, y, width, height);
    return null;
};

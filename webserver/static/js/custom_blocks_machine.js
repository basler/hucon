// custom_blocks_machine.js - Blockly blocks to support roboter based things.
//
// Copyright (C) 2019 Basler AG
// All rights reserved.
//
// This software may be modified and distributed under the terms
// of the BSD license.  See the LICENSE file for details.

Blockly.Blocks.machine_sleep = {
    init: function () {
        this.setColour(Blockly.Msg['HUCON_SYSTEM_HUE']);

        this.appendDummyInput()
            .appendField(Blockly.Msg['HUCON_SYSTEM_SLEEP_FOR'])
            .appendField(new Blockly.FieldNumber('100'), 'Milliseconds')
            .appendField(Blockly.Msg['HUCON_SYSTEM_SLEEP_TIME']);
        this.setPreviousStatement(true);
        this.setNextStatement(true);

        this.setTooltip(Blockly.Msg['HUCON_SYSTEM_SLEEP_TOOLTIP']);
    }
};
Blockly.Python.machine_sleep = function(block) {
    Blockly.Python.definitions_.import_time = 'import time';
    var time = block.getFieldValue('Milliseconds');

    var code = 'time.sleep(' + time / 1000 + ')\n';
    return code;
};

Blockly.Blocks.machine_sleep_value = {
    init: function () {
        this.setColour(Blockly.Msg['HUCON_SYSTEM_HUE']);

        this.appendDummyInput()
            .appendField(Blockly.Msg['HUCON_SYSTEM_SLEEP_FOR'])
            .appendField(new Blockly.FieldVariable(Blockly.Msg['HUCON_SYSTEM_SLEEP_VAR']), 'VAR');
        this.appendDummyInput()
            .appendField(Blockly.Msg['HUCON_SYSTEM_SLEEP_TIME']);
        this.setInputsInline(true);
        this.setPreviousStatement(true);
        this.setNextStatement(true);

        this.setTooltip(Blockly.Msg['HUCON_SYSTEM_SLEEP_TOOLTIP']);
    }
};
Blockly.Python.machine_sleep_value = function(block) {
    Blockly.Python.definitions_.import_time = 'import time';
    var varName = Blockly.Python.variableDB_.getName(block.getFieldValue('VAR'), Blockly.Variables.NAME_TYPE);

    var code = 'time.sleep(' + varName + ' / 1000)\n';
    return code;
};

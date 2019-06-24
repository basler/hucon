// 2018-12-11
//
// Blockly blocks to support roboter based things.
//
// Author: Sascha.MuellerzumHagen@baslerweb.com

var COLOR_MACHINE = 180;
var COLOR_EYE = 0;
var COLOR_SERVO = 30;
var COLOR_MOTOR = 60;

Blockly.Blocks.machine_sleep = {
    init: function () {
        this.setColour(COLOR_MACHINE);

        this.appendDummyInput()
            .appendField('sleep for')
            .appendField(new Blockly.FieldNumber('100'), 'Milliseconds')
            .appendField('milliseconds');
        this.setPreviousStatement(true);
        this.setNextStatement(true);

        this.setTooltip('Sleep for an amout of time.');
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
        this.setColour(COLOR_MACHINE);

        this.appendDummyInput()
            .appendField('sleep for')
            .appendField(new Blockly.FieldVariable('index'), 'VAR');
        this.appendDummyInput()
            .appendField('milliseconds');
        this.setInputsInline(true);
        this.setPreviousStatement(true);
        this.setNextStatement(true);

        this.setTooltip('Sleep for an amout of time.');
    }
};
Blockly.Python.machine_sleep_value = function(block) {
    Blockly.Python.definitions_.import_time = 'import time';
    var varName = Blockly.Python.variableDB_.getName(block.getFieldValue('VAR'), Blockly.Variables.NAME_TYPE);

    var code = 'time.sleep(' + varName + ' / 1000)\n';
    return code;
};

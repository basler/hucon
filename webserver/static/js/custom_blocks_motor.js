// custom_blocks_motor.js - Blockly blocks to support pwm motors.
//
// Copyright (C) 2019 Basler AG
// All rights reserved.
//
// This software may be modified and distributed under the terms
// of the BSD license.  See the LICENSE file for details.

var COLOR_MOTOR = 60;
var MACHINE_MOTOR_PINS = [
    ['channel 1', '0'],
    ['channel 2', '1'],
    ['channel 3', '2'],
    ['channel 4', '3'],
    ['channel 5', '4'],
    ['channel 6', '5'],
    ['channel 7', '6'],
    ['channel 8', '7'],
    ['channel 9', '8'],
    ['channel 10', '9'],
    ['channel 11', '10'],
    ['channel 12', '11'],
    ['channel 13', '12'],
    ['channel 14', '13']
];

Blockly.Blocks.machine_motor_channel = {
    init: function () {
        this.setColour(COLOR_MOTOR);

        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown(MACHINE_MOTOR_PINS), 'MotorChannel');
        this.setOutput(true, 'MachineMotorChannel');

        this.setTooltip('Get the right number for the given motor channel.');
    }
};
Blockly.Python.machine_motor_channel = function(block) {
    var channel = block.getFieldValue('MotorChannel');
    return [channel, Blockly.Python.ORDER_ATOMIC];
};

Blockly.Blocks.motor_object = {
    init: function () {
        this.setColour(COLOR_MOTOR);

        this.appendValueInput('Pin')
            .setCheck('MachineMotorChannel')
            .appendField('create motor on');
        this.setOutput(true, 'Motor');

        this.setTooltip('Create a motor object which is conntected to the given channel.');
    }
};
Blockly.Python.motor_object = function (block) {
    Blockly.Python.definitions_.import_motor = 'from hucon import Motor';
    var argument0 = Blockly.Python.valueToCode(block, 'Pin', Blockly.Python.ORDER_ATOMIC) || 'NULL';

    var code = 'Motor(' + argument0 + ')';
    return [code, Blockly.Python.ORDER_ATOMIC];
};

Blockly.Blocks.motor_set_offset = {
    init: function () {
        this.setColour(COLOR_MOTOR);

        this.appendDummyInput()
            .appendField('set')
            .appendField(new Blockly.FieldVariable('motor'), 'VAR');
        this.appendValueInput('Offset')
            .setCheck('Number')
            .appendField('offset');
        this.setInputsInline(true);
        this.setPreviousStatement(true);
        this.setNextStatement(true);

        this.setTooltip('Set the motor offset. The Value can be between -100 and 100.');
    }
};
Blockly.Python.motor_set_offset = function (block) {
    var varName = Blockly.Python.variableDB_.getName(block.getFieldValue('VAR'), Blockly.Variables.NAME_TYPE);
    var offset = Blockly.Python.valueToCode(block, 'Offset', Blockly.Python.ORDER_ATOMIC) || '0';

    var code = varName + '.offset = ' + offset + '\n';
    return code;
};

Blockly.Blocks.motor_set_speed = {
    init: function () {
        this.setColour(COLOR_MOTOR);

        this.appendDummyInput()
            .appendField('set')
            .appendField(new Blockly.FieldVariable('motor'), 'VAR');
        this.appendValueInput('Value')
            .setCheck('Number')
            .appendField('speed to');
        this.setInputsInline(true);
        this.setPreviousStatement(true);
        this.setNextStatement(true);

        this.setTooltip('Set the motor speed between -100 (backward) and 100 (forward).');
    }
};
Blockly.Python.motor_set_speed = function (block) {
    var varName = Blockly.Python.variableDB_.getName(block.getFieldValue('VAR'), Blockly.Variables.NAME_TYPE);
    var value = Blockly.Python.valueToCode(block, 'Value', Blockly.Python.ORDER_ATOMIC) || '0';

    var code = varName + '.set_speed(' + value + ')\n';
    return code;
};

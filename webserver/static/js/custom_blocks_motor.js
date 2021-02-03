// custom_blocks_motor.js - Blockly blocks to support pwm motors.
//
// Copyright (C) 2019 Basler AG
// All rights reserved.
//
// This software may be modified and distributed under the terms
// of the BSD license.  See the LICENSE file for details.

var MACHINE_MOTOR_PINS = [
    [Blockly.Msg['HUCON_MOTOR_CHANNEL_1'], '0'],
    [Blockly.Msg['HUCON_MOTOR_CHANNEL_2'], '1'],
    [Blockly.Msg['HUCON_MOTOR_CHANNEL_3'], '2'],
    [Blockly.Msg['HUCON_MOTOR_CHANNEL_4'], '3'],
    [Blockly.Msg['HUCON_MOTOR_CHANNEL_5'], '4'],
    [Blockly.Msg['HUCON_MOTOR_CHANNEL_6'], '5'],
    [Blockly.Msg['HUCON_MOTOR_CHANNEL_7'], '6'],
    [Blockly.Msg['HUCON_MOTOR_CHANNEL_8'], '7'],
    [Blockly.Msg['HUCON_MOTOR_CHANNEL_9'], '8'],
    [Blockly.Msg['HUCON_MOTOR_CHANNEL_10'], '9'],
    [Blockly.Msg['HUCON_MOTOR_CHANNEL_11'], '10'],
    [Blockly.Msg['HUCON_MOTOR_CHANNEL_12'], '11'],
    [Blockly.Msg['HUCON_MOTOR_CHANNEL_13'], '12'],
    [Blockly.Msg['HUCON_MOTOR_CHANNEL_14'], '13']
];

Blockly.Blocks.machine_motor_channel = {
    init: function () {
        this.setColour(Blockly.Msg['HUCON_MOTOR_HUE']);

        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown(MACHINE_MOTOR_PINS), 'MotorChannel');
        this.setOutput(true, 'MachineMotorChannel');

        this.setTooltip(Blockly.Msg['HUCON_MOTOR_CHANNEL_TOOLTIP']);
    }
};
Blockly.Python.machine_motor_channel = function(block) {
    var channel = block.getFieldValue('MotorChannel');
    return [channel, Blockly.Python.ORDER_ATOMIC];
};

Blockly.Blocks.motor_object = {
    init: function () {
        this.setColour(Blockly.Msg['HUCON_MOTOR_HUE']);

        this.appendValueInput('Pin')
            .setCheck('MachineMotorChannel')
            .appendField(Blockly.Msg['HUCON_MOTOR_OBJECT_CREATE']);
        this.setOutput(true, 'Motor');

        this.setTooltip(Blockly.Msg['HUCON_MOTOR_OBJECT_TOOLTIP']);
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
        this.setColour(Blockly.Msg['HUCON_MOTOR_HUE']);

        this.appendDummyInput()
            .appendField(Blockly.Msg['HUCON_MOTOR_OFFSET_SET'])
            .appendField(new Blockly.FieldVariable(Blockly.Msg['HUCON_MOTOR_VAR']), 'VAR');
        this.appendValueInput('Offset')
            .setCheck('Number')
            .appendField(Blockly.Msg['HUCON_MOTOR_OFFSET_OFFSET']);
        this.setInputsInline(true);
        this.setPreviousStatement(true);
        this.setNextStatement(true);

        this.setTooltip(Blockly.Msg['HUCON_MOTOR_OFFSET_TOOLTIP']);
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
        this.setColour(Blockly.Msg['HUCON_MOTOR_HUE']);

        this.appendDummyInput()
            .appendField(Blockly.Msg['HUCON_MOTOR_SPEED_SET'])
            .appendField(new Blockly.FieldVariable(Blockly.Msg['HUCON_MOTOR_VAR']), 'VAR');
        this.appendValueInput('Value')
            .setCheck('Number')
            .appendField(Blockly.Msg['HUCON_MOTOR_SPEED_SPEED']);
        this.setInputsInline(true);
        this.setPreviousStatement(true);
        this.setNextStatement(true);

        this.setTooltip(Blockly.Msg['HUCON_MOTOR_SPEED_TOOLTIP']);
    }
};
Blockly.Python.motor_set_speed = function (block) {
    var varName = Blockly.Python.variableDB_.getName(block.getFieldValue('VAR'), Blockly.Variables.NAME_TYPE);
    var value = Blockly.Python.valueToCode(block, 'Value', Blockly.Python.ORDER_ATOMIC) || '0';

    var code = varName + '.set_speed(' + value + ')\n';
    return code;
};

Blockly.Blocks.motor_set_speed_simple = {
    init: function () {
        this.setColour(Blockly.Msg['HUCON_MOTOR_HUE']);

        this.appendDummyInput()
            .appendField(Blockly.Msg['HUCON_MOTOR_SPEED_SIMPLE_SET'])
            .appendField(new Blockly.FieldDropdown(MACHINE_MOTOR_PINS), 'channel');
        this.appendValueInput('Speed')
            .setCheck('Number')
            .appendField(Blockly.Msg['HUCON_MOTOR_SPEED_SIMPLE_SPEED']);
        this.setInputsInline(true);
        this.setPreviousStatement(true);
        this.setNextStatement(true);

        this.setTooltip(Blockly.Msg["HUCON_MOTOR_SPEED_SIMPLE_TOOLTIP"]);
    }
};
Blockly.Python.motor_set_speed_simple = function(block) {
    Blockly.Python.definitions_.import_motor = 'from hucon import Motor';

    var channel = block.getFieldValue('channel');
    var speed = Blockly.Python.valueToCode(block, 'Speed', Blockly.Python.ORDER_ATOMIC) || '0';

    var code = 'Motor(' + channel + ')' + '.set_speed(' + speed + ')\n';
    return code;
};

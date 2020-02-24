// custom_blocks_servo.js - Blockly blocks to support servos.
//
// Copyright (C) 2019 Basler AG
// All rights reserved.
//
// This software may be modified and distributed under the terms
// of the BSD license.  See the LICENSE file for details.

var MACHINE_SERVO_PINS = [
    [Blockly.Msg['HUCON_SERVO_CHANNEL_1'], '0'],
    [Blockly.Msg['HUCON_SERVO_CHANNEL_2'], '1'],
    [Blockly.Msg['HUCON_SERVO_CHANNEL_3'], '2'],
    [Blockly.Msg['HUCON_SERVO_CHANNEL_4'], '3'],
    [Blockly.Msg['HUCON_SERVO_CHANNEL_5'], '4'],
    [Blockly.Msg['HUCON_SERVO_CHANNEL_6'], '5'],
    [Blockly.Msg['HUCON_SERVO_CHANNEL_7'], '6'],
    [Blockly.Msg['HUCON_SERVO_CHANNEL_8'], '7'],
    [Blockly.Msg['HUCON_SERVO_CHANNEL_9'], '8'],
    [Blockly.Msg['HUCON_SERVO_CHANNEL_10'], '9'],
    [Blockly.Msg['HUCON_SERVO_CHANNEL_11'], '10'],
    [Blockly.Msg['HUCON_SERVO_CHANNEL_12'], '11'],
    [Blockly.Msg['HUCON_SERVO_CHANNEL_13'], '12'],
    [Blockly.Msg['HUCON_SERVO_CHANNEL_14'], '13']
];

Blockly.Blocks.machine_servo_channel = {
    init: function () {
        this.setColour(Blockly.Msg['HUCON_SERVO_HUE']);

        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown(MACHINE_SERVO_PINS), 'ServoChannel');
        this.setOutput(true, 'MachineServoChannel');

        this.setTooltip(Blockly.Msg['HUCON_SERVO_CHANNEL_TOOLTIP']);
    }
};
Blockly.Python.machine_servo_channel = function(block) {
    var channel = block.getFieldValue('ServoChannel');
    return [channel, Blockly.Python.ORDER_ATOMIC];
};


Blockly.Blocks.servo_object = {
    init: function () {
        this.setColour(Blockly.Msg['HUCON_SERVO_HUE']);

        this.appendValueInput('VAR')
            .setCheck('MachineServoChannel')
            .appendField(Blockly.Msg['HUCON_SERVO_OBJECT_CREATE']);
        this.setOutput(true, 'Servo');

        this.setTooltip(Blockly.Msg['HUCON_SERVO_OBJECT_TOOLTIP']);
    }
};
Blockly.Python.servo_object = function (block) {
    Blockly.Python.definitions_.import_servo = 'from hucon import Servo';
    var argument0 = Blockly.Python.valueToCode(block, 'VAR', Blockly.Python.ORDER_ATOMIC) || 'NULL';

    var code = 'Servo(' + argument0 + ')';
    return [code, Blockly.Python.ORDER_ATOMIC];
};

Blockly.Blocks.servo_set_offset = {
    init: function () {
        this.setColour(Blockly.Msg['HUCON_SERVO_HUE']);

        this.appendDummyInput()
            .appendField(Blockly.Msg['HUCON_SERVO_OFFSET_SET'])
            .appendField(new Blockly.FieldVariable(Blockly.Msg['HUCON_SERVO_VAR']), 'VAR');
        this.appendValueInput('Offset')
            .setCheck('Number')
            .appendField(Blockly.Msg['HUCON_SERVO_OFFSET_OFFSET']);
        this.setInputsInline(true);
        this.setPreviousStatement(true);
        this.setNextStatement(true);

        this.setTooltip(Blockly.Msg['HUCON_SERVO_OFFSET_TOOLTIP']);
    }
};
Blockly.Python.servo_set_offset = function (block) {
    var varName = Blockly.Python.variableDB_.getName(block.getFieldValue('VAR'), Blockly.Variables.NAME_TYPE);
    var offset = Blockly.Python.valueToCode(block, 'Offset', Blockly.Python.ORDER_ATOMIC) || '0';

    var code = varName + '.offset = ' + offset + '\n';
    return code;
};

Blockly.Blocks.servo_set_angle = {
    init: function () {
        this.setColour(Blockly.Msg['HUCON_SERVO_HUE']);

        this.appendDummyInput()
            .appendField(Blockly.Msg['HUCON_SERVO_ANGLE_SET'])
            .appendField(new Blockly.FieldVariable(Blockly.Msg['HUCON_SERVO_VAR']), 'VAR');
        this.appendValueInput('Angle')
            .setCheck('Number')
            .appendField(Blockly.Msg['HUCON_SERVO_ANGLE_ANGLE']);
        this.setInputsInline(true);
        this.setPreviousStatement(true);
        this.setNextStatement(true);

        this.setTooltip(Blockly.Msg['HUCON_SERVO_ANGLE_TOOLTIP']);
    }
};
Blockly.Python.servo_set_angle = function (block) {
    var varName = Blockly.Python.variableDB_.getName(block.getFieldValue('VAR'), Blockly.Variables.NAME_TYPE);
    var angle = Blockly.Python.valueToCode(block, 'Angle', Blockly.Python.ORDER_ATOMIC) || '0';

    var code = varName + '.set_angle(' + angle + ')\n';
    return code;
};

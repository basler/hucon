// custom_blocks_eye.js - Blockly blocks to support RGB LEDs (eyes).
//
// Copyright (C) 2019 Basler AG
// All rights reserved.
//
// This software may be modified and distributed under the terms
// of the BSD license.  See the LICENSE file for details.

var MACHINE_EYES_CODE = [
    [Blockly.Msg['HUCON_EYE_CODE_RGB'], 'Eye.RGB'],
    [Blockly.Msg['HUCON_EYE_CODE_RBG'], 'Eye.RBG'],
    [Blockly.Msg['HUCON_EYE_CODE_GBR'], 'Eye.GBR'],
    [Blockly.Msg['HUCON_EYE_CODE_GRB'], 'Eye.GRB'],
    [Blockly.Msg['HUCON_EYE_CODE_BGR'], 'Eye.BGR'],
    [Blockly.Msg['HUCON_EYE_CODE_BRG'], 'Eye.BRG']
];
var MACHINE_EYES = [
    [Blockly.Msg['HUCON_EYE_POSITION_1'], '1'],
    [Blockly.Msg['HUCON_EYE_POSITION_2'], '2'],
    [Blockly.Msg['HUCON_EYE_POSITION_3'], '3'],
    [Blockly.Msg['HUCON_EYE_POSITION_4'], '4']
];

Blockly.Blocks.machine_eye = {
    init: function () {
        this.setColour(Blockly.Msg['HUCON_EYE_HUE']);

        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown(MACHINE_EYES), 'Eye');
        this.setOutput(true, 'MachineEye');

        this.setTooltip(Blockly.Msg['HUCON_EYE_OBJECT_TOOLTIP']);
    }
};
Blockly.Python.machine_eye = function(block) {
    var channel = block.getFieldValue('Eye');
    return [channel, Blockly.Python.ORDER_ATOMIC];
};

Blockly.Blocks.eye_object_code = {
    init: function () {
        this.setColour(Blockly.Msg['HUCON_EYE_HUE']);

        this.appendValueInput('Position')
            .appendField(new Blockly.FieldDropdown(MACHINE_EYES_CODE), 'ColorCoding')
            .setCheck('MachineEye');
        this.setOutput(true, 'Eye');

        this.setTooltip(Blockly.Msg['HUCON_EYE_OBJECT_CODE_TOOLTIP']);
    }
};
Blockly.Python.eye_object_code = function(block) {
    Blockly.Python.definitions_.import_eye = 'from hucon import Eye';
    var argument0 = Blockly.Python.valueToCode(block, 'Position', Blockly.Python.ORDER_ATOMIC) || 'NULL';
    var colorCoding = block.getFieldValue('ColorCoding');

    var code = 'Eye(' + argument0 + ', ' + colorCoding + ')';
    return [code, Blockly.Python.ORDER_ATOMIC];
};

// This block is deprecated!
Blockly.Blocks.eye_object = {
    init: function () {
        this.setColour(Blockly.Msg['HUCON_EYE_HUE']);

        this.appendValueInput('Position')
            .setCheck('MachineEye')
            .appendField('create eye for');
        this.setOutput(true, 'Eye');

        this.setTooltip('Create an eye object which is on the given position.');
    }
};
Blockly.Python.eye_object = function(block) {
    Blockly.Python.definitions_.import_eye = 'from hucon import Eye';
    var argument0 = Blockly.Python.valueToCode(block, 'Position', Blockly.Python.ORDER_ATOMIC) || 'NULL';

    var code = 'Eye(' + argument0 + ')';
    return [code, Blockly.Python.ORDER_ATOMIC];
};

Blockly.Blocks.eye_colour = {
    init: function () {
        this.setColour(Blockly.Msg['HUCON_EYE_HUE']);

        this.appendDummyInput()
            .appendField(Blockly.Msg['HUCON_EYE_COLOUR_SET'])
            .appendField(new Blockly.FieldVariable(Blockly.Msg['HUCON_EYE_VAR']), 'VAR');
        this.appendDummyInput()
            .appendField(Blockly.Msg['HUCON_EYE_COLOUR_EYE_COLOR'])
            .appendField(new Blockly.FieldColour('#ff0000'), 'Colour');
        this.setInputsInline(true);
        this.setPreviousStatement(true);
        this.setNextStatement(true);

        this.setTooltip(Blockly.Msg['HUCON_EYE_COLOUR_TOOLTIP']);
    }
};
Blockly.Python.eye_colour = function(block) {
    var varName = Blockly.Python.variableDB_.getName(block.getFieldValue('VAR'), Blockly.Variables.NAME_TYPE);
    var colour = block.getFieldValue('Colour');
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(colour);
    var r = parseInt(result[1], 16);
    var g = parseInt(result[2], 16);
    var b = parseInt(result[3], 16);

    var code = varName + '.set_color(' + r + ', ' + g + ', ' + b + ')\n';
    return code;
};

Blockly.Blocks.eye_colour_rgb = {
    init: function () {
        this.setColour(Blockly.Msg['HUCON_EYE_HUE']);

        this.appendDummyInput()
            .appendField(Blockly.Msg['HUCON_EYE_COLOUR_SET'])
            .appendField(new Blockly.FieldVariable(Blockly.Msg['HUCON_EYE_VAR']), 'VAR');
        this.appendDummyInput()
            .appendField(Blockly.Msg['HUCON_EYE_COLOUR_EYE_COLOR']);
        this.appendValueInput('R')
            .setCheck('Number')
            .appendField(Blockly.Msg['HUCON_EYE_COLOUR_RGB_RED']);
        this.appendValueInput('G')
            .setCheck('Number')
            .appendField(Blockly.Msg['HUCON_EYE_COLOUR_RGB_GREEN']);
        this.appendValueInput('B')
            .setCheck('Number')
            .appendField(Blockly.Msg['HUCON_EYE_COLOUR_RGB_BLUE']);
        this.setInputsInline(true);
        this.setPreviousStatement(true);
        this.setNextStatement(true);

        this.setTooltip(Blockly.Msg['HUCON_EYE_COLOUR_RGB_TOOLTIP']);
    }
};
Blockly.Python.eye_colour_rgb = function(block) {
    var varName = Blockly.Python.variableDB_.getName(block.getFieldValue('VAR'), Blockly.Variables.NAME_TYPE);
    var r = Blockly.Python.valueToCode(block, 'R', Blockly.Python.ORDER_ATOMIC) || '0';
    var g = Blockly.Python.valueToCode(block, 'G', Blockly.Python.ORDER_ATOMIC) || '0';
    var b = Blockly.Python.valueToCode(block, 'B', Blockly.Python.ORDER_ATOMIC) || '0';

    var code = varName + '.set_color(' + r + ', ' + g + ', ' + b + ')\n';
    return code;
};


Blockly.Blocks.eye_colour_rgb_simple = {
    init: function () {
        this.setColour(Blockly.Msg['HUCON_EYE_HUE']);

        this.appendDummyInput()
            .appendField(Blockly.Msg['HUCON_EYE_SIMPLE_SET']);
        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown(MACHINE_EYES), 'Eye');
        this.appendValueInput('R')
            .setCheck('Number')
            .appendField(Blockly.Msg['HUCON_EYE_COLOUR_RGB_RED']);
        this.appendValueInput('G')
            .setCheck('Number')
            .appendField(Blockly.Msg['HUCON_EYE_COLOUR_RGB_GREEN']);
        this.appendValueInput('B')
            .setCheck('Number')
            .appendField(Blockly.Msg['HUCON_EYE_COLOUR_RGB_BLUE']);
        this.setInputsInline(true);
        this.setPreviousStatement(true);
        this.setNextStatement(true);

        this.setTooltip(Blockly.Msg["HUCON_EYE_SIMPLE_TOOLTIP"]);
    }
};
Blockly.Python.eye_colour_rgb_simple = function(block) {
    Blockly.Python.definitions_.import_eye = 'from hucon import Eye';

    var channel = block.getFieldValue('Eye');
    var r = Blockly.Python.valueToCode(block, 'R', Blockly.Python.ORDER_ATOMIC) || '0';
    var g = Blockly.Python.valueToCode(block, 'G', Blockly.Python.ORDER_ATOMIC) || '0';
    var b = Blockly.Python.valueToCode(block, 'B', Blockly.Python.ORDER_ATOMIC) || '0';

    var code = 'Eye(' + channel + ', Eye.RGB)' + '.set_color(' + r + ', ' + g + ', ' + b + ')\n';
    return code;
};

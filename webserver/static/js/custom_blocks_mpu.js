// custom_blocks_mpu.js - Blockly blocks to support mpu devices.
//
// Copyright (C) 2019 Basler AG
// All rights reserved.
//
// This software may be modified and distributed under the terms
// of the BSD license.  See the LICENSE file for details.

Blockly.Blocks.mpu_object = {
    init: function () {
        this.setColour(Blockly.Msg['HUCON_MPU_HUE']);

        this.appendDummyInput()
            .appendField(Blockly.Msg['HUCON_MPU_OBJECT']);
        this.setOutput(true, 'MPU');

        this.setTooltip(Blockly.Msg['HUCON_MPU_OBJECT_TOOLTIP']);
    }
};
Blockly.Python.mpu_object = function (block) {
    Blockly.Python.definitions_.import_mpu = 'from hucon import Mpu6050';

    var code = 'Mpu6050()';
    return [code, Blockly.Python.ORDER_ATOMIC];
};

Blockly.Blocks.mpu_get_temperature = {
    init: function () {
        this.setColour(Blockly.Msg['HUCON_MPU_HUE']);

        this.appendDummyInput()
            .appendField(Blockly.Msg['HUCON_MPU_GET_TEMP'])
            .appendField(new Blockly.FieldVariable(Blockly.Msg['HUCON_MPU_VAR']), 'VAR');
        this.setOutput(true, 'Number');

        this.setTooltip(Blockly.Msg['HUCON_MPU_GET_TEMP_TOOLTIP']);
    }
};
Blockly.Python.mpu_get_temperature = function (block) {
    var varName = Blockly.Python.variableDB_.getName(block.getFieldValue('VAR'), Blockly.Variables.NAME_TYPE);

    var code = varName + '.get_temp()';
    return [code, Blockly.Python.ORDER_ATOMIC];
};

Blockly.Blocks.mpu_get_accelerometer_data = {
    init: function () {
        this.setColour(Blockly.Msg['HUCON_MPU_HUE']);

        this.appendDummyInput()
            .appendField(Blockly.Msg['HUCON_MPU_GET_ACC_DATA'])
            .appendField(new Blockly.FieldVariable(Blockly.Msg['HUCON_MPU_VAR']), 'VAR');
        this.setOutput(true, 'MPU_Data');

        this.setTooltip(Blockly.Msg['HUCON_MPU_GET_ACC_TOOLTIP']);
    }
};
Blockly.Python.mpu_get_accelerometer_data = function (block) {
    var varName = Blockly.Python.variableDB_.getName(block.getFieldValue('VAR'), Blockly.Variables.NAME_TYPE);

    var code = varName + '.get_accel_data()';
    return [code, Blockly.Python.ORDER_ATOMIC];
};

Blockly.Blocks.mpu_get_gyroscope_data = {
    init: function () {
        this.setColour(Blockly.Msg['HUCON_MPU_HUE']);

        this.appendDummyInput()
            .appendField(Blockly.Msg['HUCON_MPU_GET_GYR_DATA'])
            .appendField(new Blockly.FieldVariable(Blockly.Msg['HUCON_MPU_VAR']), 'VAR');
        this.setOutput(true, 'MPU_Data');

        this.setTooltip(Blockly.Msg['HUCON_MPU_GET_GYR_TOOLTIP']);
    }
};
Blockly.Python.mpu_get_gyroscope_data = function (block) {
    var varName = Blockly.Python.variableDB_.getName(block.getFieldValue('VAR'), Blockly.Variables.NAME_TYPE);

    var code = varName + '.get_gyro_data()';
    return [code, Blockly.Python.ORDER_ATOMIC];
};

var MPU_POSITION = [
    ['X', 'x'],
    ['Y', 'y'],
    ['Z', 'z']
];
Blockly.Blocks.mpu_get_mpu_data = {
    init: function () {
        this.setColour(Blockly.Msg['HUCON_MPU_HUE']);

        this.appendDummyInput()
            .appendField(Blockly.Msg['HUCON_MPU_GET_DATA'])
            .appendField(new Blockly.FieldVariable(Blockly.Msg['HUCON_MPU_VAR']), 'VAR');
        this.appendDummyInput()
            .appendField(Blockly.Msg['HUCON_MPU_GET_POSITION'])
            .appendField(new Blockly.FieldDropdown(MPU_POSITION), 'Position');
        this.setInputsInline(true);
        this.setOutput(true, 'Number');

        this.setTooltip(Blockly.Msg['HUCON_MPU_GET_TOOLTIP']);
    }
};
Blockly.Python.mpu_get_mpu_data = function (block) {
    var varName = Blockly.Python.variableDB_.getName(block.getFieldValue('VAR'), Blockly.Variables.NAME_TYPE);
    var position = block.getFieldValue('Position');

    var code = varName + '[\'' + position + '\']';
    return [code, Blockly.Python.ORDER_ATOMIC];
};

// 2018-12-11
//
// Blockly blocks to support pwm motors.
//
// Author: Sascha.MuellerzumHagen@baslerweb.com

var COLOR_MOTOR = 60;

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

var COLOR_MOTOR = 60;

Blockly.Blocks['motor_object'] = {
    init: function() {
        this.setColour(COLOR_MOTOR);

        this.appendValueInput('Pin')
            .setCheck('MachineMotorChannel')
            .appendField('create Motor on');
        this.setOutput(true, 'Motor');

        this.setTooltip(function() {
            return 'Create a motor object which is conntected to the given pin.';
        });
    }
}
Blockly.Python['motor_object'] = function(block) {
    Blockly.Python.definitions_['import_motor'] = 'from hackerschool import Motor';

    var argument0 = Blockly.Python.valueToCode(block, 'Pin', Blockly.Python.ORDER_ATOMIC) || 'NULL';
    var code = 'Motor(' + argument0 + ')';
    return [code, Blockly.Python.ORDER_ATOMIC];
};

Blockly.Blocks['motor_set_offset'] = {
    init: function() {
        this.setColour(COLOR_MOTOR);

        this.appendDummyInput()
            .appendField('Set')
            .appendField(new Blockly.FieldVariable('motor'), 'VAR');
        this.appendValueInput('Offset')
            .setCheck('Number')
            .appendField('offset');
        this.setInputsInline(true);
        this.setPreviousStatement(true);
        this.setNextStatement(true);

        var thisBlock = this;
        this.setTooltip(function() {
            return 'Set the motor offset for channel ' + thisBlock.getFieldValue('VAR');
        });
    }
};
Blockly.Python['motor_set_offset'] = function(block) {
    var varName = Blockly.Python.variableDB_.getName(block.getFieldValue('VAR'), Blockly.Variables.NAME_TYPE);
    var offset = Blockly.Python.valueToCode(block, 'Offset', Blockly.Python.ORDER_ATOMIC) || '0';
    var code = varName + '.offset = ' + offset + '\n';
    return code;
};

Blockly.Blocks['motor_set_speed'] = {
    init: function() {
        this.setColour(COLOR_MOTOR);

        this.appendDummyInput()
            .appendField('Set')
            .appendField(new Blockly.FieldVariable('motor'), 'VAR');
        this.appendValueInput('Time')
            .setCheck('Number')
            .appendField('speed to');
        this.setInputsInline(true);
        this.setPreviousStatement(true);
        this.setNextStatement(true);

        var thisBlock = this;
        this.setTooltip(function() {
            return 'Set the motor speed on pin ' + thisBlock.getFieldValue('VAR');
        });
    }
};
Blockly.Python['motor_set_speed'] = function(block) {
    var varName = Blockly.Python.variableDB_.getName(block.getFieldValue('VAR'), Blockly.Variables.NAME_TYPE);
    var time = Blockly.Python.valueToCode(block, 'Time', Blockly.Python.ORDER_ATOMIC) || '0';
    var code = varName + '.set_speed(' + time + ')\n';
    return code;
};

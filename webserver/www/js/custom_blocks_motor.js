Blockly.Blocks['motor_object'] = {
    init: function() {
        this.setColour(208);

        this.appendValueInput('Pin')
            .setCheck('MachinePin')
            .appendField('create Motor on')
        this.appendValueInput('Offset')
            .setCheck('Number')
            .appendField('with offset');
        this.setInputsInline(true);
        this.setOutput(true, 'Motor');

        this.setTooltip(function() {
            return 'Create a motor object which is conntected to the given pin.';
        });
    }
}
Blockly.Python['motor_object'] = function(block) {
    Blockly.Python.definitions_['import_motor'] = 'from hs_motor import HSMotor as HSMotor';

    var argument0 = Blockly.Python.valueToCode(block, 'Pin', Blockly.Python.ORDER_ATOMIC) || 'NULL';
    var argument1 = Blockly.Python.valueToCode(block, 'Offset', Blockly.Python.ORDER_ATOMIC) || 'NULL';
    var code = 'HSMotor(' + argument0 + ', ' + argument1 + ')';
    return [code, Blockly.Python.ORDER_ATOMIC];
};

Blockly.Blocks['motor_object_param'] = {
    init: function() {
        this.setColour(208);

        this.appendValueInput('Pin')
            .setCheck('MachinePin')
            .appendField('create Motor on')
        this.appendValueInput('Offset')
            .setCheck('Number')
            .appendField('with offset');
        this.appendValueInput('Freq')
            .setCheck('Number')
            .appendField('and frequency');
        this.setInputsInline(true);
        this.setOutput(true, 'Motor');

        this.setTooltip(function() {
            return 'Create a motor object which is conntected to the given pin.';
        });
    }
}
Blockly.Python['motor_object_param'] = function(block) {
    Blockly.Python.definitions_['import_motor'] = 'from hs_motor import HSMotor as HSMotor';

    var argument0 = Blockly.Python.valueToCode(block, 'Pin', Blockly.Python.ORDER_ATOMIC) || 'NULL';
    var argument1 = Blockly.Python.valueToCode(block, 'Offset', Blockly.Python.ORDER_ATOMIC) || 'NULL';
    var argument2 = Blockly.Python.valueToCode(block, 'Freq', Blockly.Python.ORDER_ATOMIC) || 'NULL';
    var code = 'HSMotor(' + argument0 + ', ' + argument1 + ', ' + argument2 + ')';
    return [code, Blockly.Python.ORDER_ATOMIC];
};

Blockly.Blocks['motor_set_speed'] = {
    init: function() {
        this.setColour(208);

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

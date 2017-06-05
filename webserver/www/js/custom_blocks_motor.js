Blockly.Blocks['motor_object'] = {
    init: function() {
        this.setColour(208);

        this.appendValueInput('VAR')
            .setCheck('MachinePin')
            .appendField('create Motor on')
        this.setOutput(true, 'Motor');

        this.setTooltip(function() {
            return 'Create a motor object which is conntected to the given pin.';
        });
    }
}
Blockly.Python['motor_object'] = function(block) {
    Blockly.Python.definitions_['import_motor'] = 'from hs_motor import HSMotor as HSMotor';

    var argument0 = Blockly.Python.valueToCode(block, 'VAR', Blockly.Python.ORDER_ATOMIC) || 'NULL';
    var code = 'HSMotor(' + argument0 + ')';
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

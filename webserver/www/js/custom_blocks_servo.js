Blockly.Blocks['servo_object'] = {
    init: function() {
        this.setColour(208);

        this.appendValueInput('VAR')
            .setCheck('MachinePin')
            .appendField('create Servo on')
        this.setOutput(true, 'Servo');

        this.setTooltip(function() {
            return 'Create a servo object which is conntected to the given pin.';
        });
    }
}
Blockly.Python['servo_object'] = function(block) {
    Blockly.Python.definitions_['import_servo'] = 'from hs_servo import HSServo as HSServo';

    var argument0 = Blockly.Python.valueToCode(block, 'VAR', Blockly.Python.ORDER_ATOMIC) || 'NULL';
    var code = 'HSServo(' + argument0 + ')';
    return [code, Blockly.Python.ORDER_ATOMIC];
};

Blockly.Blocks['servo_set_angle'] = {
    init: function() {
        this.setColour(208);

        this.appendDummyInput()
            .appendField('Set')
            .appendField(new Blockly.FieldVariable('servo'), 'VAR');
        this.appendValueInput('Angle')
            .setCheck('Number')
            .appendField('angle');
        this.setInputsInline(true);
        this.setPreviousStatement(true);
        this.setNextStatement(true);

        var thisBlock = this;
        this.setTooltip(function() {
            return 'Set the servo angle on pin ' + thisBlock.getFieldValue('VAR');
        });
    }
};
Blockly.Python['servo_set_angle'] = function(block) {
    var varName = Blockly.Python.variableDB_.getName(block.getFieldValue('VAR'), Blockly.Variables.NAME_TYPE);
    var angle = Blockly.Python.valueToCode(block, 'Angle', Blockly.Python.ORDER_ATOMIC) || '0';
    var code = varName + '.set_angle(' + angle + ')\n';
    return code;
};

Blockly.Blocks['python_int'] = {
    init: function() {
        this.setColour(208);

        this.appendValueInput('Value')
            .setCheck('Number')
            .appendField('convert to integer');
        this.setInputsInline(true);
        this.setOutput(true, 'Number');

        var thisBlock = this;
        this.setTooltip(function() {
            return 'Try to convert any object to an integer value.';
        });
    }
}
Blockly.Python['python_int'] = function(block) {
    var input = Blockly.Python.valueToCode(block, 'Value', Blockly.Python.ORDER_ATOMIC) || '0';
    return ['int(' + input + ')', Blockly.Python.ORDER_ATOMIC];
};

Blockly.Blocks['python_float'] = {
    init: function() {
        this.setColour(208);

        this.appendValueInput('Value')
            .setCheck('Number')
            .appendField('convert to float');
        this.setInputsInline(true);
        this.setOutput(true, 'Number');

        var thisBlock = this;
        this.setTooltip(function() {
            return 'Try to convert any object to a float value.';
        });
    }
}
Blockly.Python['python_float'] = function(block) {
    var input = Blockly.Python.valueToCode(block, 'Value', Blockly.Python.ORDER_ATOMIC) || '0.0';
    return ['float(' + input + ')', Blockly.Python.ORDER_ATOMIC];
};

Blockly.Blocks['python_string'] = {
    init: function() {
        this.setColour(208);

        this.appendValueInput('Value')
            .appendField('convert to string');
        this.setInputsInline(true);
        this.setOutput(true, 'String');

        var thisBlock = this;
        this.setTooltip(function() {
            return 'Try to convert any object to a string value.';
        });
    }
}
Blockly.Python['python_string'] = function(block) {
    var input = Blockly.Python.valueToCode(block, 'Value', Blockly.Python.ORDER_ATOMIC) || '';
    return ['str(' + input + ')', Blockly.Python.ORDER_ATOMIC];
};
var COLOR_EYE = 0;

Blockly.Blocks['eye_object'] = {
    init: function() {
        this.setColour(COLOR_EYE);

        this.appendValueInput('Position')
            .setCheck('MachineEye')
            .appendField('create Eye for');
        this.setOutput(true, 'Eye');

        this.setTooltip(function() {
            return 'Create an eye object which is on the given position.';
        });
    }
}
Blockly.Python['eye_object'] = function(block) {
    Blockly.Python.definitions_['import_eye'] = 'from hackerschool import Eye';

    var argument0 = Blockly.Python.valueToCode(block, 'Position', Blockly.Python.ORDER_ATOMIC) || 'NULL';
    var code = 'Eye(' + argument0 + ')';
    return [code, Blockly.Python.ORDER_ATOMIC];
};

Blockly.Blocks['eye_colour'] = {
    init: function() {
        this.setColour(COLOR_EYE);

        this.appendDummyInput()
            .appendField('Set')
            .appendField(new Blockly.FieldVariable('eye'), 'VAR');
        this.appendDummyInput()
            .appendField('eye color')
            .appendField(new Blockly.FieldColour('#ff0000') , 'Colour');
        this.setInputsInline(true);
        this.setPreviousStatement(true);
        this.setNextStatement(true);

        var thisBlock = this;
        this.setTooltip(function() {
            return 'Define for an element this color ' + thisBlock.getFieldValue('Colour');
        });
    }
}
Blockly.Python['eye_colour'] = function(block) {
    var varName = Blockly.Python.variableDB_.getName(block.getFieldValue('VAR'), Blockly.Variables.NAME_TYPE);
    var colour = block.getFieldValue('Colour');
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(colour);
    var r = parseInt(result[1], 16)
    var g = parseInt(result[2], 16)
    var b = parseInt(result[3], 16)
    var code = varName + '.set_color(' + r + ', ' + g + ', ' + b + ')\n';
    return code;
};

Blockly.Blocks['eye_colour_rgb'] = {
    init: function() {
        this.setColour(COLOR_EYE);

        this.appendDummyInput()
            .appendField('Set')
            .appendField(new Blockly.FieldVariable('eye'), 'VAR');
        this.appendDummyInput()
            .appendField('eye color');
        this.appendValueInput('R')
            .setCheck('Number')
            .appendField('Red');
        this.appendValueInput('G')
            .setCheck('Number')
            .appendField('Green');
        this.appendValueInput('B')
            .setCheck('Number')
            .appendField('Blue');
        this.setInputsInline(true);
        this.setPreviousStatement(true);
        this.setNextStatement(true);

        var thisBlock = this;
        this.setTooltip(function() {
            var r = thisBlock.getFieldValue('R');
            var g = thisBlock.getFieldValue('G');
            var b = thisBlock.getFieldValue('B');
            return 'Define for an element this color (' + r + ', ' + g + ', ' + b + ')';
        });
    }
}
Blockly.Python['eye_colour_rgb'] = function(block) {
    var varName = Blockly.Python.variableDB_.getName(block.getFieldValue('VAR'), Blockly.Variables.NAME_TYPE);
    var r = Blockly.Python.valueToCode(block, 'R', Blockly.Python.ORDER_ATOMIC) || '0';
    var g = Blockly.Python.valueToCode(block, 'G', Blockly.Python.ORDER_ATOMIC) || '0';
    var b = Blockly.Python.valueToCode(block, 'B', Blockly.Python.ORDER_ATOMIC) || '0';
    var code = varName + '.set_color(' + r + ', ' + g + ', ' + b + ')\n';
    return code;
};

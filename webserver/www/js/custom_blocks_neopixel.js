Blockly.Blocks['neopixel_array'] = {
    init: function() {
        this.setColour(208);

        this.appendValueInput('VAR')
            .setCheck('MachinePin')
            .appendField('create NeoPixel list on')
        this.setOutput(true, 'NeoPixelArray');

        this.setTooltip(function() {
            return 'Create a NeoPixel List which is conntected to the given pin.';
        });
    }
}
Blockly.Python['neopixel_array'] = function(block) {
    Blockly.Python.definitions_['import_neopixel'] = 'from neopixel import NeoPixel as NeoPixel';

    var argument0 = Blockly.Python.valueToCode(block, 'VAR', Blockly.Python.ORDER_ATOMIC) || 'NULL';
    var code = 'NeoPixel(' + argument0 + ', 2)';
    return [code, Blockly.Python.ORDER_ATOMIC];
};

Blockly.Blocks['neopixel_colour'] = {
    init: function() {
        this.setColour(208);

        this.appendDummyInput()
            .appendField('NeoPixel color:')
            .appendField(new Blockly.FieldColour('#ff0000') , 'COLOUR');
        this.setOutput(true, 'NeoPixelColor');

        var thisBlock = this;
        this.setTooltip(function() {
            return 'Define for an element this color ' + thisBlock.getFieldValue('COLOUR');
        });
    }
}
Blockly.Python['neopixel_colour'] = function(block) {
    var colour = block.getFieldValue('COLOUR');
    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(colour);
    var r = parseInt(result[1], 16)
    var g = parseInt(result[2], 16)
    var b = parseInt(result[3], 16)
    var code = ' = (' + g + ', ' + r + ', ' + b + ')';
    return [code, Blockly.Python.ORDER_ATOMIC];
};

Blockly.Blocks['neopixel_colour_rgb'] = {
    init: function() {
        this.setColour(208);

        this.appendDummyInput()
            .appendField('NeoPixel color');
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
        this.setOutput(true, 'NeoPixelColor');

        var thisBlock = this;
        this.setTooltip(function() {
            var r = thisBlock.getFieldValue('R');
            var g = thisBlock.getFieldValue('G');
            var b = thisBlock.getFieldValue('B');
            return 'Define for an element this color (' + r + ', ' + g + ', ' + b + ')';
        });
    }
}
Blockly.Python['neopixel_colour_rgb'] = function(block) {
    var r = Blockly.Python.valueToCode(block, 'R', Blockly.Python.ORDER_ATOMIC) || '0';
    var g = Blockly.Python.valueToCode(block, 'G', Blockly.Python.ORDER_ATOMIC) || '0';
    var b = Blockly.Python.valueToCode(block, 'B', Blockly.Python.ORDER_ATOMIC) || '0';
    var code = '(' + g + ', ' + r + ', ' + b + ')';
    return [code, Blockly.Python.ORDER_ATOMIC];
};

Blockly.Blocks['neopixel_write'] = {
    init: function() {
        this.setColour(208);

        this.appendDummyInput()
            .appendField('write')
            .appendField(new Blockly.FieldVariable('np'), 'VAR')
            .appendField('data');
        this.setPreviousStatement(true);
        this.setNextStatement(true);

        var thisBlock = this;
        this.setTooltip(function() {
            return 'Write the NeoPixel data from ' + thisBlock.getFieldValue('VAR');
        });
    }
};
Blockly.Python['neopixel_write'] = function(block) {
    var varName = Blockly.Python.variableDB_.getName(block.getFieldValue('VAR'), Blockly.Variables.NAME_TYPE);
    var code = varName + '.write()\n';
    return code;
};

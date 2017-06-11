var MACHINE_PINS = [
    ['NeoPixel', '14'],
    ['Servo 1', '12'],
    ['Servo 2', '13'],
    ['GPIO 2', '2'],
    ['GPIO 4', '4'],
    ['GPIO 5', '5'],
];

Blockly.Blocks['machine_pin'] = {
    init: function() {
        this.setColour(208);

        this.appendDummyInput()
            .appendField('pin')
            .appendField(new Blockly.FieldDropdown(MACHINE_PINS) , 'MACHINE_PIN_CONSTANT')
        this.setOutput(true, 'MachinePin');

        var thisBlock = this;
        this.setTooltip(function() {
            var pin_number = thisBlock.getFieldValue('MACHINE_PIN_CONSTANT');
            return 'Get a pin object on ' + pin_number;
        });
    }
}
Blockly.Python['machine_pin'] = function(block) {
    Blockly.Python.definitions_['import_machine_pin'] = 'from machine import Pin as Pin';

    var pin = block.getFieldValue('MACHINE_PIN_CONSTANT');
    var code = 'Pin(' + pin + ')';
    return [code, Blockly.Python.ORDER_ATOMIC];
};

Blockly.Blocks['machine_pin_parameter'] = {
    init: function() {
        this.setColour(208);

        this.appendDummyInput()
            .appendField('pin')
            .appendField(new Blockly.FieldDropdown(MACHINE_PINS) , 'MACHINE_PIN_CONSTANT')
        this.appendDummyInput()
            .appendField('direction')
            .appendField(new Blockly.FieldDropdown([
                ['In', 'Pin.IN'],
                ['Out', 'Pin.OUT'],
                ]) , 'MACHINE_PIN_DIRECTION')
        this.setOutput(true, 'MachinePin');

        var thisBlock = this;
        this.setTooltip(function() {
            var pin_number = thisBlock.getFieldValue('MACHINE_PIN_CONSTANT');
            var pin_direction = thisBlock.getFieldValue('MACHINE_PIN_DIRECTION');
            return 'Get a pin object on ' + pin_number + ' with the directio ' + pin_direction;
        });
    }
}
Blockly.Python['machine_pin_parameter'] = function(block) {
    Blockly.Python.definitions_['import_machine_pin'] = 'from machine import Pin as Pin';

    var pin = block.getFieldValue('MACHINE_PIN_CONSTANT');
    var dir = block.getFieldValue('MACHINE_PIN_DIRECTION');
    var code = 'Pin(' + pin + ', ' + dir + ')';
    return [code, Blockly.Python.ORDER_ATOMIC];
};

Blockly.Blocks['machine_pin_get'] = {
    init: function() {
        this.setColour(208);

        this.appendDummyInput()
            .appendField('get value from')
            .appendField(new Blockly.FieldVariable('pin'), 'VAR');
        this.setOutput(true, 'Number');

        var thisBlock = this;
        this.setTooltip(function() {
            return 'Get the value from the machine pin ' + thisBlock.getFieldValue('VAR');
        });
    }
};
Blockly.Python['machine_pin_get'] = function(block) {
    var varName = Blockly.Python.variableDB_.getName(block.getFieldValue('VAR'), Blockly.Variables.NAME_TYPE);
    var code = varName + '.value()';
    return [code, Blockly.Python.ORDER_ATOMIC];
};

Blockly.Blocks['machine_pin_set'] = {
    init: function() {
        this.setColour(208);

        this.appendDummyInput()
            .appendField('Set')
            .appendField(new Blockly.FieldVariable('pin'), 'VAR');
        this.appendDummyInput()
            .appendField('to')
            .appendField(new Blockly.FieldDropdown([
                ['Off', '0'],
                ['On', '1'],
                ]) , 'MACHINE_PIN_VALUE');
        this.setInputsInline(true);
        this.setPreviousStatement(true);
        this.setNextStatement(true);

        var thisBlock = this;
        this.setTooltip(function() {
            return 'Set the value on pin ' + thisBlock.getFieldValue('VAR');
        });
    }
};
Blockly.Python['machine_pin_set'] = function(block) {
    var varName = Blockly.Python.variableDB_.getName(block.getFieldValue('VAR'), Blockly.Variables.NAME_TYPE);
    var pin_value = block.getFieldValue('MACHINE_PIN_VALUE');
    var code = varName + '.value(' + pin_value + ')\n';
    return code;
};

Blockly.Blocks['machine_sleep'] = {
    init: function() {
        this.setColour(208);

        this.appendDummyInput()
            .appendField('Sleep for')
            .appendField(new Blockly.FieldNumber('100') , 'MILLISECONDS')
            .appendField('milliseconds')
        this.setPreviousStatement(true);
        this.setNextStatement(true);

        var thisBlock = this;
        this.setTooltip(function() {
            var time = thisBlock.getFieldValue('MILLISECONDS');
            return 'Sleep for ' + time + 'milliseconds.';
        });
    }
};
Blockly.Python['machine_sleep'] = function(block) {
    Blockly.Python.definitions_['import_time'] = 'import time';

    var time = block.getFieldValue('MILLISECONDS');
    var code = ''
    code += 'time.sleep(' + time/1000 + ')\n';
    return code;
};

var MACHINE_PINS = [
    ['NeoPixel', '14'],
    ['Servo 1', '12'],
    ['Servo 2', '13'],
    ['GPIO 2', '2'],
    ['GPIO 4', '4'],
    ['GPIO 5', '5'],
];

var MACHINE_PIN_VALUES = [
    ['Off', '0'],
    ['On', '1']
];

var MACHINE_PIN_DIRECTIONS = [
    ['In', 'Pin.IN'],
    ['Out', 'Pin.OUT']
];

var MACHINE_SERVO_PINS = [
    ['Channel 1', '0'],
    ['Channel 2', '1'],
    ['Channel 3', '2'],
    ['Channel 4', '3'],
    ['Channel 5', '4'],
    ['Channel 6', '5'],
    ['Channel 7', '6'],
    ['Channel 8', '7'],
    ['Channel 9', '8'],
    ['Channel 10', '9'],
    ['Channel 11', '10'],
    ['Channel 12', '11'],
    ['Channel 13', '12'],
    ['Channel 14', '13'],
];

Blockly.Blocks['machine_servo_channel'] = {
    init: function() {
        this.setColour(208);

        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown(MACHINE_SERVO_PINS) , 'ServoChannel')
        this.setOutput(true, 'MachineServoChannel');

        var thisBlock = this;
        this.setTooltip(function() {
            var channel_number = thisBlock.getFieldValue('ServoChannel');
            return 'Get servo object on channel ' + channel_number;
        });
    }
}
Blockly.Python['machine_servo_channel'] = function(block) {
    var channel = block.getFieldValue('ServoChannel');
    return [channel, Blockly.Python.ORDER_ATOMIC];
};

Blockly.Blocks['machine_pin_parameter'] = {
    init: function() {
        this.setColour(208);

        this.appendDummyInput()
            .appendField('pin')
            .appendField(new Blockly.FieldDropdown(MACHINE_PINS) , 'Pin')
        this.appendDummyInput()
            .appendField('direction')
            .appendField(new Blockly.FieldDropdown(MACHINE_PIN_DIRECTIONS) , 'Direction')
        this.setOutput(true, 'MachinePin');

        var thisBlock = this;
        this.setTooltip(function() {
            var pin_number = thisBlock.getFieldValue('Pin');
            var pin_direction = thisBlock.getFieldValue('Direction');
            return 'Get a pin object on ' + pin_number + ' with the directio ' + pin_direction;
        });
    }
}
Blockly.Python['machine_pin_parameter'] = function(block) {
    Blockly.Python.definitions_['import_machine_pin'] = 'from machine import Pin';

    var pin = block.getFieldValue('Pin');
    var dir = block.getFieldValue('Direction');
    var code = 'Pin(' + pin + ', ' + dir + ')';
    return [code, Blockly.Python.ORDER_ATOMIC];
};

Blockly.Blocks['machine_pin_get'] = {
    init: function() {
        this.setColour(208);

        this.appendDummyInput()
            .appendField('get value from')
            .appendField(new Blockly.FieldVariable('pin'), 'Variable');
        this.setOutput(true, 'MachinePinValue');

        var thisBlock = this;
        this.setTooltip(function() {
            return 'Get the value from the machine pin ' + thisBlock.getFieldValue('Variable');
        });
    }
};
Blockly.Python['machine_pin_get'] = function(block) {
    var varName = Blockly.Python.variableDB_.getName(block.getFieldValue('Variable'), Blockly.Variables.NAME_TYPE);
    var code = varName + '.value()';
    return [code, Blockly.Python.ORDER_ATOMIC];
};

Blockly.Blocks['machine_pin_get_direct'] = {
    init: function() {
        this.setColour(208);

        this.appendDummyInput()
            .appendField('get value from')
            .appendField(new Blockly.FieldDropdown(MACHINE_PINS) , 'Pin')
        this.setOutput(true, 'MachinePinValue');

        var thisBlock = this;
        this.setTooltip(function() {
            return 'Get the value from the machine pin ' + thisBlock.getFieldValue('Pin');
        });
    }
};
Blockly.Python['machine_pin_get_direct'] = function(block) {
    Blockly.Python.definitions_['import_machine_pin'] = 'from machine import Pin';

    var pin = block.getFieldValue('Pin');
    var code = 'Pin(' + pin + ').value()';
    return [code, Blockly.Python.ORDER_ATOMIC];
};

Blockly.Blocks['machine_pin_value'] = {
    init: function() {
        this.setColour(208);

        this.appendDummyInput()
            .appendField('Pin')
            .appendField(new Blockly.FieldDropdown(MACHINE_PIN_VALUES) , 'Value');
        this.setOutput(true, 'MachinePinValue');

        var thisBlock = this;
        this.setTooltip(function() {
            return 'Definition which value are possible.';
        });
    }
};
Blockly.Python['machine_pin_value'] = function(block) {
    var code = block.getFieldValue('Value');
    return [code, Blockly.Python.ORDER_ATOMIC];
};

Blockly.Blocks['machine_pin_set'] = {
    init: function() {
        this.setColour(208);

        this.appendDummyInput()
            .appendField('Set')
            .appendField(new Blockly.FieldVariable('pin'), 'Variable');
        this.appendDummyInput()
            .appendField('to')
            .appendField(new Blockly.FieldDropdown(MACHINE_PIN_VALUES) , 'Value');
        this.setInputsInline(true);
        this.setPreviousStatement(true);
        this.setNextStatement(true);

        var thisBlock = this;
        this.setTooltip(function() {
            return 'Set the value on pin ' + thisBlock.getFieldValue('Variable');
        });
    }
};
Blockly.Python['machine_pin_set'] = function(block) {
    var varName = Blockly.Python.variableDB_.getName(block.getFieldValue('Variable'), Blockly.Variables.NAME_TYPE);
    var value = block.getFieldValue('Value');
    var code = varName + '.value(' + value + ')\n';
    return code;
};

Blockly.Blocks['machine_pin_set_direct'] = {
    init: function() {
        this.setColour(208);

        this.appendDummyInput()
            .appendField('Set')
            .appendField(new Blockly.FieldDropdown(MACHINE_PINS) , 'Pin')
        this.appendDummyInput()
            .appendField('to')
            .appendField(new Blockly.FieldDropdown(MACHINE_PIN_VALUES) , 'Value');
        this.setInputsInline(true);
        this.setPreviousStatement(true);
        this.setNextStatement(true);

        var thisBlock = this;
        this.setTooltip(function() {
            return 'Set the value on pin ' + thisBlock.getFieldValue('Pin');
        });
    }
};
Blockly.Python['machine_pin_set_direct'] = function(block) {
    Blockly.Python.definitions_['import_machine_pin'] = 'from machine import Pin';

    var pin = block.getFieldValue('Pin');
    var value = block.getFieldValue('Value');
    var code = 'Pin(' + pin + ').value(' + value + ')\n';
    return code;
};

Blockly.Blocks['machine_sleep'] = {
    init: function() {
        this.setColour(208);

        this.appendDummyInput()
            .appendField('Sleep for')
            .appendField(new Blockly.FieldNumber('100'), 'Milliseconds')
            .appendField('milliseconds')
        this.setPreviousStatement(true);
        this.setNextStatement(true);

        var thisBlock = this;
        this.setTooltip(function() {
            var time = thisBlock.getFieldValue('Milliseconds');
            return 'Sleep for ' + time + 'milliseconds.';
        });
    }
};
Blockly.Python['machine_sleep'] = function(block) {
    Blockly.Python.definitions_['import_time'] = 'import time';

    var time = block.getFieldValue('Milliseconds');
    var code = ''
    code += 'time.sleep(' + time/1000 + ')\n';
    return code;
};

Blockly.Blocks['machine_sleep_value'] = {
    init: function() {
        this.setColour(208);

        this.appendDummyInput()
            .appendField('Sleep for')
        this.appendValueInput('Milliseconds')
            .setCheck('Number')
        this.appendDummyInput()
            .appendField('milliseconds')
        this.setInputsInline(true);
        this.setPreviousStatement(true);
        this.setNextStatement(true);

        // var thisBlock = this;
        // this.setTooltip(function() {
        //     var time = thisBlock.getFieldValue('Milliseconds');
        //     return 'Sleep for ' + time + 'milliseconds.';
        // });
    }
};
Blockly.Python['machine_sleep_value'] = function(block) {
    Blockly.Python.definitions_['import_time'] = 'import time';

    var time = block.getFieldValue('Milliseconds');
    var code = ''
    code += 'time.sleep(' + time/1000 + ')\n';
    return code;
};

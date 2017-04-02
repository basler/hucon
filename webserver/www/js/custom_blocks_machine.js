Blockly.Blocks['machine_pin'] = {
    init: function() {
        this.setColour(208);

        this.appendDummyInput()
            .appendField('pin')
            .appendField(new Blockly.FieldDropdown([
                ['NeoPixel', 'NEOPIXEL'],
                ['Servo 1', 'SERVO_1'],
                ['Servo 2', 'SERVO_2'],
                ]) , 'MACHINE_PIN_CONSTANT')
        this.setOutput(true, 'MachinePin');

        var thisBlock = this;
        this.setTooltip(function() {
            var pin_number = thisBlock.getFieldValue('MACHINE_PIN_CONSTANT');
            return 'get a pin object on ' + pin_number;
        });
    }
}
Blockly.Python['machine_pin'] = function(block) {
    Blockly.Python.definitions_['import_machine_pin'] = 'from machine import Pin as Pin';

    var pin = block.getFieldValue('MACHINE_PIN_CONSTANT');
    var code = 'Pin(';
    switch(pin) {
        case 'NEOPIXEL':
            code += '14';
            break;
        case 'SERVO_1':
            code += '12';
            break;
        case 'SERVO_2':
            code += '13';
            break;
    }
    code += ')';
    return [code, Blockly.Python.ORDER_ATOMIC];
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

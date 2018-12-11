// 2018-12-11
//
// Blockly blocks to support roboter based things.
//
// Author: Sascha.MuellerzumHagen@baslerweb.com

var COLOR_MACHINE = 180;
var COLOR_EYE = 0;
var COLOR_SERVO = 30;
var COLOR_MOTOR = 60;

Blockly.Blocks['machine_sleep'] = {
    init: function() {
        this.setColour(COLOR_MACHINE);

        this.appendDummyInput()
            .appendField('sleep for')
            .appendField(new Blockly.FieldNumber('100'), 'Milliseconds')
            .appendField('milliseconds')
        this.setPreviousStatement(true);
        this.setNextStatement(true);

        this.setTooltip('Sleep for an amout of time.');
    }
};
Blockly.Python['machine_sleep'] = function(block) {
    Blockly.Python.definitions_['import_time'] = 'import time';

    var time = block.getFieldValue('Milliseconds');
    code = 'time.sleep(' + time/1000 + ')\n';
    return code;
};

Blockly.Blocks['machine_sleep_value'] = {
    init: function() {
        this.setColour(COLOR_MACHINE);

        this.appendDummyInput()
            .appendField('sleep for')
            .appendField(new Blockly.FieldVariable('index'), 'VAR');
        this.appendDummyInput()
            .appendField('milliseconds');
        this.setInputsInline(true);
        this.setPreviousStatement(true);
        this.setNextStatement(true);

        this.setTooltip('Sleep for an amout of time.');
    }
};
Blockly.Python['machine_sleep_value'] = function(block) {
    Blockly.Python.definitions_['import_time'] = 'import time';

    var varName = Blockly.Python.variableDB_.getName(block.getFieldValue('VAR'), Blockly.Variables.NAME_TYPE);
    code = 'time.sleep(' + varName + ' / 1000)\n';
    return code;
};

var MACHINE_EYES = [
    ['position top left',     '1'],
    ['position top right',    '2'],
    ['position bottom left',  '3'],
    ['position bottom right', '4']
];

Blockly.Blocks['machine_eye'] = {
    init: function() {
        this.setColour(COLOR_EYE);

        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown(MACHINE_EYES) , 'Eye')
        this.setOutput(true, 'MachineEye');

        this.setTooltip('Get the right value for the eye position.');
    }
}
Blockly.Python['machine_eye'] = function(block) {
    var channel = block.getFieldValue('Eye');
    return [channel, Blockly.Python.ORDER_ATOMIC];
};

var MACHINE_SERVO_PINS = [
    ['channel 1',  '0'],
    ['channel 2',  '1'],
    ['channel 3',  '2'],
    ['channel 4',  '3'],
    ['channel 5',  '4'],
    ['channel 6',  '5'],
    ['channel 7',  '6'],
    ['channel 8',  '7'],
    ['channel 9',  '8'],
    ['channel 10', '9'],
    ['channel 11', '10'],
    ['channel 12', '11'],
    ['channel 13', '12'],
    ['channel 14', '13'],
];

Blockly.Blocks['machine_servo_channel'] = {
    init: function() {
        this.setColour(COLOR_SERVO);

        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown(MACHINE_SERVO_PINS) , 'ServoChannel')
        this.setOutput(true, 'MachineServoChannel');

        this.setTooltip('Get the right number for the given servo channel.');
    }
}
Blockly.Python['machine_servo_channel'] = function(block) {
    var channel = block.getFieldValue('ServoChannel');
    return [channel, Blockly.Python.ORDER_ATOMIC];
};

Blockly.Blocks['machine_motor_channel'] = {
    init: function() {
        this.setColour(COLOR_MOTOR);

        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown(MACHINE_SERVO_PINS) , 'MotorChannel')
        this.setOutput(true, 'MachineMotorChannel');

        this.setTooltip('Get the right number for the given motor channel.');
    }
}
Blockly.Python['machine_motor_channel'] = function(block) {
    var channel = block.getFieldValue('MotorChannel');
    return [channel, Blockly.Python.ORDER_ATOMIC];
};

var COLOR_MACHINE = 180;
var COLOR_EYE = 0;
var COLOR_SERVO = 30;
var COLOR_MOTOR = 60;

Blockly.Blocks['machine_sleep'] = {
    init: function() {
        this.setColour(COLOR_MACHINE);

        this.appendDummyInput()
            .appendField('Sleep for')
            .appendField(new Blockly.FieldNumber('100'), 'Milliseconds')
            .appendField('milliseconds')
        this.setPreviousStatement(true);
        this.setNextStatement(true);

        var thisBlock = this;
        this.setTooltip(function() {
            var time = thisBlock.getFieldValue('Milliseconds');
            return 'Sleep for ' + time + ' milliseconds.';
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
        this.setColour(COLOR_MACHINE);

        this.appendDummyInput()
            .appendField('Sleep for')
            .appendField(new Blockly.FieldVariable('index'), 'VAR');
        this.appendDummyInput()
            .appendField('milliseconds');
        this.setInputsInline(true);
        this.setPreviousStatement(true);
        this.setNextStatement(true);
    }
};
Blockly.Python['machine_sleep_value'] = function(block) {
    Blockly.Python.definitions_['import_time'] = 'import time';

    var varName = Blockly.Python.variableDB_.getName(block.getFieldValue('VAR'), Blockly.Variables.NAME_TYPE);
    var code = ''
    code += 'time.sleep(' + varName + ' / 1000)\n';
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

        this.setTooltip(function() {
            return 'Get the right value for the eye position.';
        });
    }
}
Blockly.Python['machine_eye'] = function(block) {
    var channel = block.getFieldValue('Eye');
    return [channel, Blockly.Python.ORDER_ATOMIC];
};

var MACHINE_SERVO_PINS = [
    ['Channel 1',  '2'],
    ['Channel 2',  '1'],
    ['Channel 3',  '0'],
    ['Channel 4',  '3'],
    ['Channel 5',  '4'],
    ['Channel 6',  '5'],
    ['Channel 7',  '6'],
    ['Channel 8',  '7'],
    ['Channel 9',  '8'],
    ['Channel 10', '9'],
    ['Channel 11', '10'],
    ['Channel 12', '11'],
    ['Channel 13', '12'],
    ['Channel 14', '13'],
];

Blockly.Blocks['machine_servo_channel'] = {
    init: function() {
        this.setColour(COLOR_SERVO);

        this.appendDummyInput()
            .appendField(new Blockly.FieldDropdown(MACHINE_SERVO_PINS) , 'ServoChannel')
        this.setOutput(true, 'MachineServoChannel');

        this.setTooltip(function() {
            return 'Get the right number for the given servo channel.';
        });
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

        this.setTooltip(function() {
            return 'Get the right number for the given motor channel.';
        });
    }
}
Blockly.Python['machine_motor_channel'] = function(block) {
    var channel = block.getFieldValue('MotorChannel');
    return [channel, Blockly.Python.ORDER_ATOMIC];
};

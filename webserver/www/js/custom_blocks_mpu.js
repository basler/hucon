var COLOR_MOTION_TRACKING = 90;

Blockly.Blocks['mpu_object'] = {
    init: function() {
        this.setColour(COLOR_MOTION_TRACKING);

        this.appendDummyInput()
            .appendField('MPU-6050 Six Axis');
        this.setOutput(true, 'MPU');

        this.setTooltip('Create a motion tracking object.');
    }
}
Blockly.Python['mpu_object'] = function(block) {
    Blockly.Python.definitions_['import_motor'] = 'from hackerschool import Mpu6050';

    var code = 'Mpu6050()';
    return [code, Blockly.Python.ORDER_ATOMIC];
};

Blockly.Blocks['mpu_get_temperature'] = {
    init: function() {
        this.setColour(COLOR_MOTION_TRACKING);

        this.appendDummyInput()
            .appendField('Get temperatur from')
            .appendField(new Blockly.FieldVariable('mpu'), 'VAR');
        this.setOutput(true, 'Number');

        this.setTooltip('Get the temperature from the MPU-6050 device.');
    }
};
Blockly.Python['mpu_get_temperature'] = function(block) {
    var varName = Blockly.Python.variableDB_.getName(block.getFieldValue('VAR'), Blockly.Variables.NAME_TYPE);
    var code = varName + '.get_temp()';
    return [code, Blockly.Python.ORDER_ATOMIC];
};

Blockly.Blocks['mpu_get_accelerometer_data'] = {
    init: function() {
        this.setColour(COLOR_MOTION_TRACKING);

        this.appendDummyInput()
            .appendField('Get accelerometer data from')
            .appendField(new Blockly.FieldVariable('mpu'), 'VAR');
        this.setOutput(true, 'MPU_Data');

        this.setTooltip('Get the accelerometer data from the MPU-6050 device.');
    }
};
Blockly.Python['mpu_get_accelerometer_data'] = function(block) {
    var varName = Blockly.Python.variableDB_.getName(block.getFieldValue('VAR'), Blockly.Variables.NAME_TYPE);
    var code = varName + '.get_accel_data()';
    return [code, Blockly.Python.ORDER_ATOMIC];
};

Blockly.Blocks['mpu_get_gyroscope_data'] = {
    init: function() {
        this.setColour(COLOR_MOTION_TRACKING);

        this.appendDummyInput()
            .appendField('Get gyroscope data from')
            .appendField(new Blockly.FieldVariable('mpu'), 'VAR');
        this.setOutput(true, 'MPU_Data');

        this.setTooltip('Get the gyroscope from the MPU-6050 device.');
    }
};
Blockly.Python['mpu_get_gyroscope_data'] = function(block) {
    var varName = Blockly.Python.variableDB_.getName(block.getFieldValue('VAR'), Blockly.Variables.NAME_TYPE);
    var code = varName + '.get_gyro_data()';
    return [code, Blockly.Python.ORDER_ATOMIC];
};

var MPU_POSITION = [
    ['X', 'x'],
    ['Y', 'y'],
    ['Z', 'z']
];

Blockly.Blocks['mpu_get_mpu_data'] = {
    init: function() {
        this.setColour(COLOR_MOTION_TRACKING);

        this.appendDummyInput()
            .appendField('Get data from')
            .appendField(new Blockly.FieldVariable('mpu'), 'VAR');
        this.appendDummyInput()
            .appendField('position')
            .appendField(new Blockly.FieldDropdown(MPU_POSITION) , 'Position');
        this.setInputsInline(true);
        this.setOutput(true, 'Number');

        this.setTooltip('Get the data from the position for MPU-6050 device.');
    }
};
Blockly.Python['mpu_get_mpu_data'] = function(block) {
    var varName = Blockly.Python.variableDB_.getName(block.getFieldValue('VAR'), Blockly.Variables.NAME_TYPE);
    var position = block.getFieldValue('Position');
    var code = varName + '[\'' + position + '\']';
    return [code, Blockly.Python.ORDER_ATOMIC];
};


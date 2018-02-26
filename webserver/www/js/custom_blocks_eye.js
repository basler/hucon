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

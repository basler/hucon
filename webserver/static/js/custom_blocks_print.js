// custom_blocks_text.js - Blockly blocks to support colored print messages.
//
// Copyright (C) 2021 Basler AG
// All rights reserved.
//
// This software may be modified and distributed under the terms
// of the BSD license.  See the LICENSE file for details.


Blockly.Blocks.text_print_colored = {
    init: function () {
        this.setColour(Blockly.Msg['TEXTS_HUE']);

        var field = new Blockly.FieldColour('#ff4040');
        field.setColours(
            ['#000000',      '#FF0000',      '#008000',      '#0000FF',      '#FFFFFF',
             '#000080',      '#006400',      '#00FFFF',      '#191970',      '#0B0082',
             '#6A5ACD',      '#800080',      '#808080',      '#8B0000',      '#9400D3',
             '#A0522D',      '#ADD8E6',      '#C0C0C0',      '#D3D3D3',      '#EE82EE',
             '#FF4500',      '#FFA500',      '#FFC0CB',      '#FFD700',      '#FFFF00'],
            ['Black',        'Red',          'Green',        'Blue',         'White',
             'Navy',         'DarkGreen',    'Aqua',         'MidnightBlue', 'Indigo',
             'SlateBlue',    'Purple',       'Gray',         'DarkRed',      'DarkViolet',
             'Sienna',       'LightBlue',    'Silver',       'LightGray',    'Violet',
             'OrangeRed',    'Orange',       'Pink',         'Gold',         'Yellow']);
        field.setColumns(5);

        this.appendValueInput('TEXT')
            .appendField(Blockly.Msg['HUCON_TEXT_PRINT_COLORED_SET_1']);
        this.appendDummyInput()
            .appendField(Blockly.Msg['HUCON_TEXT_PRINT_COLORED_SET_2'])
            .appendField(field, 'Colour')
        this.setInputsInline(false);
        this.setPreviousStatement(true);
        this.setNextStatement(true);

        this.setTooltip(Blockly.Msg['HUCON_TEXT_PRINT_COLORED_TOOLTIP']);
    }
};
Blockly.Python.text_print_colored = function (block) {
    var text = Blockly.Python.valueToCode(block, 'TEXT', Blockly.Python.ORDER_ATOMIC) || 'NULL';
    var field = block.getField('Colour');
    var colourValue = block.getFieldValue('Colour');

    var indexOfColour = field.colours_.indexOf(colourValue.toUpperCase());

    console.log(field.colours_);
    console.log(Object.keys(field));
    console.log(indexOfColour);
    console.log(colourValue);

    combined_text = text.slice(0, 1) + '[' + field.titles_[indexOfColour] + '] ' + text.slice(1);

    var code = 'print(' + combined_text + ')\n';
    return code;
};

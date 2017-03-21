
Blockly.Blocks['robo_import'] = {
    init: function() {
        this.jsonInit({
            "message0": "Init",
            "nextStatement": null,
            "colour": 208,
            "tooltip": "Initializie the ESP8266 with the Robo code",
            "helpUrl": ""
        });
    }
};

Blockly.Python['robo_import'] = function(block) {
    var code = '# Import the micro ptython module.\nimport module\n';
    return code;
};
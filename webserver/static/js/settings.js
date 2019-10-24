// On document ready this function will be called and initialize the complete website.
$(document).ready(function () {
    // create web sockets
    var socket = io();
    var was_disconnected = false;
    // add sockets event on connect
    socket.on('connect', function () {
        // show message box, server connected information
        $.uiAlert({
            textHead: 'Server connection', // header
            text: "Server was connected!", // Text
            bgcolor: '#006AB3', // background-color
            textcolor: '#fff', // color
            position: 'top-center',// position . top And bottom ||  left / center / right
            icon: 'info circle', // icon in semantic-UI
            time: 3, // time
        })
    });
    // add sockets event on disconnect
    socket.on('disconnect', function () {
        // show alert message box, server disconnect
        $.uiAlert({
            textHead: 'Server connection', // header
            text: "Server was disconnected! Please check your WiFi connection!", // Text
            bgcolor: '#F99D33', // background-color
            textcolor: '#fff', // color
            position: 'top-center',// position . top And bottom ||  left / center / right
            icon: 'warning  sign', // icon in semantic-UI
            time: 15, // time
        });
        was_disconnected = true;
    });
    // poll for new messages
    HuConApp.poll();
}());

// Check for updates.
function checkUpdate() {
    $('#updateModal').modal('show');
    $('#consoleLog').html('');
    $('#updateButton').addClass('disabled');

    HuConApp.appendConsoleLog('Check for updates ...', 'green');

    var rpcRequest = HuConApp.getRpcRequest();
    rpcRequest['method'] = 'check_update';
    $.ajax('/API', {
        method: 'POST',
        data: JSON.stringify(rpcRequest),
        dataType: 'json',
        success: function (rpcResponse) {
            if (HuConApp.isResponseError(rpcResponse)) {
                alert(rpcResponse[error]);
            }

            if (rpcResponse['result']) {
                $('#updateButton').removeClass('disabled');
            }
        },
        error: HuConApp.appendErrorLog
    });
}

// Call the update script.
function updateSystem() {
    var rpcRequest = HuConApp.getRpcRequest();
    rpcRequest['method'] = 'update';
    $.ajax('/API', {
        method: 'POST',
        data: JSON.stringify(rpcRequest),
        dataType: 'json',
        error: HuConApp.appendErrorLog
    });
}

// Overwrite the default appenConsoleLogMessage function.
// Append the message, which can be a an array, to the console output.
HuConApp.appendConsoleLogMessage = function (message, colour) {
    if (colour === undefined) {
        colour = 'black';
    }

    if (message.includes('Error:')) {
        colour = 'red';
    }

    $('#consoleLog').append($('<span>').css('color', colour).text(message)).append($('<br>'));
    $('#consoleLog').scrollTop($('#consoleLog')[0].scrollHeight);
};

// trigger action: move network up in priority list
function moveWiFiUp(element_id) {
    var rpcRequest = HuConApp.getRpcRequest();
    rpcRequest['method'] = 'move_wifi_up';
    rpcRequest['params'] = [$('#' + element_id).text()];
    // enable loader
    $('#id_wifi_list_loader').removeClass('disabled').addClass('active');
    // trigger action on server
    $.ajax('/API', {
        method: 'POST',
        data: JSON.stringify(rpcRequest),
        dataType: 'json',
        success: function () {
            // disable loader
            $('#id_wifi_list_loader').removeClass('active').addClass('disabled');
            // hide modal dialog with listed networks
            $('#id_wifi_list_modal').modal('hide');
            // and load it again
            listWiFiNetworks();
        },
        error: HuConApp.showAlertBox
    });
}

// trigger action: move network down in priority list
function moveWiFiDown(element_id) {
    var rpcRequest = HuConApp.getRpcRequest();
    rpcRequest['method'] = 'move_wifi_down';
    rpcRequest['params'] = [$('#' + element_id).text()];
    // enable loader
    $('#id_wifi_list_loader').removeClass('disabled').addClass('active');
    // trigger action on server
    $.ajax('/API', {
        method: 'POST',
        data: JSON.stringify(rpcRequest),
        dataType: 'json',
        success: function () {
            // disable loader
            $('#id_wifi_list_loader').removeClass('active').addClass('disabled');
            // hide modal dialog with listed networks
            $('#id_wifi_list_modal').modal('hide');
            // and load it again
            listWiFiNetworks();
        },
        error: HuConApp.showAlertBox
    });
}

// trigger action: remove network from priority list
function removeWiFi(element_id) {
    var rpcRequest = HuConApp.getRpcRequest();
    rpcRequest['method'] = 'remove_wifi';
    rpcRequest['params'] = [$('#' + element_id).text()];
    // enable loader
    $('#id_wifi_list_loader').removeClass('disabled').addClass('active');
    // trigger action on server
    $.ajax('/API', {
        method: 'POST',
        data: JSON.stringify(rpcRequest),
        dataType: 'json',
        success: function () {
            // disable loader
            $('#id_wifi_list_loader').removeClass('active').addClass('disabled');
            // hide modal dialog with listed networks
            $('#id_wifi_list_modal').modal('hide');
            // and load it again
            listWiFiNetworks();
        },
        error: HuConApp.showAlertBox
    });
}

// trigger action: connect to wifi network
function connectWiFi(element_id) {
    var rpcRequest = HuConApp.getRpcRequest();
    rpcRequest['method'] = 'connect_wifi';
    rpcRequest['params'] = [$('#' + element_id).text()];
    // enable loader
    $('#id_wifi_list_loader').removeClass('disabled').addClass('active');
    // trigger action on server
    $.ajax('/API', {
        method: 'POST',
        data: JSON.stringify(rpcRequest),
        dataType: 'json',
        success: function () {
            // disable loader
            $('#id_wifi_list_loader').removeClass('active').addClass('disabled');
            // hide modal dialog with listed networks
            $('#id_wifi_list_modal').modal('hide');
            // and load it again
            listWiFiNetworks();
        },
        error: HuConApp.showAlertBox
    });
}

// gets list with saved network from server and shows it in a list on modal dialog
function listWiFiNetworks() {
    var rpcRequest = HuConApp.getRpcRequest();
    rpcRequest['method'] = 'get_saved_wifi_networks';
    // trigger action on server
    $.ajax('/API', {
        method: 'POST',
        data: JSON.stringify(rpcRequest),
        dataType: 'json',
        success: function (rpcResponse) {
            if (HuConApp.isResponseError(rpcResponse)) {
                // if response gets some errors show it in alert box
                alert(rpcResponse[error]);
            }
            if (rpcResponse['result']) {
                // if response contains valid result build fill modal dialog with content
                if (rpcResponse['result']['wifi_disabled']) {
                    // if network is disabled deactivate search wifi button and set network toggle switch to off
                    $("#id_enable_wifi").checkbox('set unchecked');
                    $("#id_wifi_search_button").addClass('disabled');
                } else {
                    // if network is enabled activate search wifi button and set network toggle switch to on
                    $("#id_enable_wifi").checkbox('set checked');
                    $("#id_wifi_search_button").removeClass('disabled');
                }

                // save current state of modal dialog without content list
                var modal_init_state = $('#id_wifi_list_modal').html();

                var i = 0;
                // create wifi networks list on modal dialog
                for (const x of rpcResponse['result']['wifi_list']) {
                    // crate list item id
                    var item_id = "id_item_" + i;
                    // crate list item
                    var list_item = $("<div class='item'></div>");
                    // crate remove button
                    list_item.append("<div class='right floated content'><button onclick='removeWiFi(\"" + item_id + "\");' class='circular ui icon button' data-content='Delete Network from list'><i class='minus circle icon'></i></button></div>");
                    // crate move down button
                    list_item.append("<div class='right floated content'><button onclick='moveWiFiDown(\"" + item_id + "\");' class='circular ui icon button' data-content='Move Network down in prority list'><i class='arrow circle down icon'></i></button></div>");
                    // crate move up button
                    list_item.append("<div class='right floated content'><button onclick='moveWiFiUp(\"" + item_id + "\");' class='circular ui icon button' data-content='Move Network up in prority list'><i class='arrow circle up icon'></i></button></div>");
                    if (x.enabled) {
                        // if network marked as enabled make icon active
                        list_item.append("<i class='wifi big violet icon'></i><div class='content' id='" + item_id + "'>" + x.ssid + "</div>");
                    } else {
                        // else add connect button and make icon inactive
                        list_item.append("<div class='right floated content'><button onclick='connectWiFi(\"" + item_id + "\");' class='circular ui icon button' data-content='Connect to WiFi Network'><i class='check circle icon'></i></button></div>");
                        list_item.append("<i class='wifi big grey icon'></i><div class='content' id='" + item_id + "'>" + x.ssid + "</div>");
                    }
                    //Append list item to list if its not already available in the current list
                    if ($("#id_wifi_list .item[id=" + item_id + "]").length == 0) {
                        $('#id_wifi_list').append(list_item);
                        i++;
                    }
                }
                // add event listener to wifi enable button
                $("#id_enable_wifi").checkbox({
                    onChecked: function () {
                        // if switch is on, enable wifi
                        var rpcRequest = HuConApp.getRpcRequest();
                        rpcRequest['method'] = 'enable_sta_wifi';
                        // enable loader
                        $('#id_wifi_list_loader').removeClass('disabled').addClass('active');
                        // trigger action on server
                        $.ajax('/API', {
                            method: 'POST',
                            data: JSON.stringify(rpcRequest),
                            dataType: 'json',
                            success: function (rpcResponse) {
                                // disable loader
                                $('#id_wifi_list_loader').removeClass('active').addClass('disabled');
                                // hide modal dialog with listed networks
                                $('#id_wifi_list_modal').modal('hide');
                                // and load it again
                                listWiFiNetworks();
                            },
                            error: HuConApp.showAlertBox
                        });
                    },
                    onUnchecked: function () {
                        // if switch is off, disable wifi
                        var rpcRequest = HuConApp.getRpcRequest();
                        rpcRequest['method'] = 'disable_sta_wifi';
                        // enable loader
                        $('#id_wifi_list_loader').removeClass('disabled').addClass('active');
                        // trigger action on server
                        $.ajax('/API', {
                            method: 'POST',
                            data: JSON.stringify(rpcRequest),
                            dataType: 'json',
                            success: function (rpcResponse) {
                                // disable loader
                                $('#id_wifi_list_loader').removeClass('active').addClass('disabled');
                                // hide modal dialog with listed networks
                                $('#id_wifi_list_modal').modal('hide');
                                // and load it again
                                listWiFiNetworks();
                            },
                            error: HuConApp.showAlertBox
                        });
                    }
                });
                // show modal dialog and bind event handler to it
                $('#id_wifi_list_modal').modal({
                    onHide: function () {
                        // reset content to original on closing modal
                        $('#id_wifi_list_modal').html(modal_init_state);
                    },
                    onShow: function () {
                        // activate tool tips on showing modal
                        $('.button')
                            .popup({
                                inline: true
                            })
                        ;
                    },
                    onApprove: function () {
                        // reset content to original and reload list again on approving modal
                        $('#id_wifi_list_modal').modal('hide');
                        listWiFiNetworks();
                    }
                }).modal('show');
            }
        },
        error: HuConApp.showAlertBox
    });
}

// searches for new wifi networks, will be triggered by Scan Wifi button in Wifi List modal dialog
function wifiSearch() {
    // approves WiFi List modal dialog and close it
    $('#id_wifi_list_modal').modal('approve');
    // save the original state of search wifi modal dialog
    var modal_init_state = $('#id_wifi_search_modal').html();

    // show wifi search modal dialog
    $('#id_wifi_search_modal').modal({
        onHide: function () {
            // reset the state of search modal dialog to original
            $('#id_wifi_search_modal').html(modal_init_state);
            // close wifi search modal dialog
            $('#id_wifi_list_modal').modal('hide');
            // load wifi list modal dialog
            listWiFiNetworks();
        },
        onApprove: function () {
            // reset the state of search modal dialog to original
            $('#id_wifi_search_modal').html(modal_init_state);
            listWiFiNetworks();
        }
    }).modal('show');

    var rpcRequest = HuConApp.getRpcRequest();
    rpcRequest['method'] = 'get_wifi_found';
    // trigger action on server
    $.ajax('/API', {
        method: 'POST',
        data: JSON.stringify(rpcRequest),
        dataType: 'json',
        success: function (rpcResponse) {
            if (HuConApp.isResponseError(rpcResponse)) {
                // show error in alert box if any
                alert(rpcResponse[error]);
            }
            if (rpcResponse['result']) {
                // if result valid, fill search modal dialog
                var i = 0;
                for (const x of rpcResponse['result']) {
                    // filter hidden networks
                    if (x.ssid != "") {
                        $('#id_search_wifi_menu').append("<option id='id_search_menu_item_" + i + "'value='" + x.ssid + "' encr='" + x.encryption + "'>" + x.ssid + "</option>");
                        // first item, ssid empty
                        if ($('#id_ssid').val() == "") {
                            $('#id_encryption option[value="' + x.encryption + '"]').prop('selected', true);
                            $('#id_ssid').val(x.ssid);
                        }
                    }
                    i++;
                }
                // disable loader, active by default in this modal dialog
                $('#id_loader').removeClass('active').addClass('disabled');

                // add event listener to network selector
                $("#id_search_wifi_menu").on('change', function () {
                    // get values
                    var selected_item_id = $('#id_search_wifi_menu option:selected').attr('id');
                    var encryption = $('#' + selected_item_id).attr('encr');
                    var ssid = $('#' + selected_item_id).val();
                    // set right encryption
                    $('#id_encryption option[value="' + encryption + '"]').prop('selected', true);
                    // set right ssid in ssid input box
                    $('#id_ssid').val(ssid);
                });

                // add event to show password checkbox
                $("#id_show_password").checkbox({
                    onChecked: function () {
                        // show password as text if checkbox is checked
                        $('#id_password').attr('type', 'text');
                    },
                    onUnchecked: function () {
                        // hide password if checkbox is unchecked
                        $('#id_password').attr('type', 'password');
                    }
                });
            }
        },
        error: HuConApp.showAlertBox
    });
}

// add new wifi network to priority list, will be triggered by Add Wifi button on search wifi dialog
function addWiFi() {
    var rpcRequest = HuConApp.getRpcRequest();
    rpcRequest['method'] = 'add_wifi';
    rpcRequest['params'] = [$('#id_ssid').val(), $('#id_password').val(), $('#id_encryption').val()];

    // approve search wifi modal dialog
    $('#id_wifi_search_modal').modal('approve');

    // trigger action on server
    $.ajax('/API', {
        method: 'POST',
        data: JSON.stringify(rpcRequest),
        dataType: 'json',
        success: function () {
            // show networ list modal dialog
            listWiFiNetworks();
        },
        error: HuConApp.showAlertBox
    });
}

// show access point settings modal dialog
function showWiFiAPsettings() {
    var rpcRequest = HuConApp.getRpcRequest();
    rpcRequest['method'] = 'get_ap_settings';
    // get data from server
    $.ajax('/API', {
        method: 'POST',
        data: JSON.stringify(rpcRequest),
        dataType: 'json',
        success: function (rpcResponse) {
            // set enable switch to right position
            if (!!+rpcResponse['result']['disabled']) {
                $("#id_enable_ap_mode").checkbox('set unchecked');
            } else {
                $("#id_enable_ap_mode").checkbox('set checked');
            }
            // fill ui wth values get from server
            $('#id_ap_encryption option[value="' + rpcResponse['result']['encryption'] + '"]').prop('selected', true);
            $('#id_ap_ssid').val(rpcResponse['result']['ssid']);
            $('#id_ap_password').val(rpcResponse['result']['key']);
            $('#id_ap_ip').val(rpcResponse['result']['ap_ip_addr']);
            $('#id_ap_wifi_modal').modal('show');

            // add event listener to show password checkbox
            $("#id_show_ap_password").checkbox({
                onChecked: function () {
                    // if checked show password
                    $('#id_ap_password').attr('type', 'text');
                },
                onUnchecked: function () {
                    // if unchecked hide password
                    $('#id_ap_password').attr('type', 'password');
                }
            });

            // add event listener to enable ap network toggle switch
            $("#id_enable_ap_mode").checkbox({
                onChecked: function () {
                    // if toggle switch is on, enable ap network
                    var rpcRequest = HuConApp.getRpcRequest();
                    rpcRequest['method'] = 'enable_ap_wifi';
                    // trigger action on server
                    $.ajax('/API', {
                        method: 'POST',
                        data: JSON.stringify(rpcRequest),
                        dataType: 'json',
                        success: function () {
                            // hide ap settings modal dialog
                            $('#id_ap_wifi_modal').modal('hide');
                            // reload ap settings modal dialog
                            showWiFiAPsettings();
                        },
                        error: HuConApp.showAlertBox
                    });
                },
                onUnchecked: function () {
                    // if toggle switch is off, disable ap network
                    var rpcRequest = HuConApp.getRpcRequest();
                    rpcRequest['method'] = 'disable_ap_wifi';
                    // trigger action on server
                    $.ajax('/API', {
                        method: 'POST',
                        data: JSON.stringify(rpcRequest),
                        dataType: 'json',
                        success: function () {
                            // hide ap settings modal dialog
                            $('#id_ap_wifi_modal').modal('hide');
                            // reload ap settings modal dialog
                            showWiFiAPsettings();
                        },
                        error: HuConApp.showAlertBox
                    });
                }
            });
        },
        error: HuConApp.showAlertBox
    });
}

// set new access point setting, will be triggered by clicking Configure AP button
function setWiFiAPsettings() {
    // get values from ui
    var rpcRequest = HuConApp.getRpcRequest();
    rpcRequest['method'] = 'set_ap_settings';
    rpcRequest['params'] = [$('#id_ap_ssid').val(), $('#id_ap_password').val(), $('#id_ap_encryption').val(), $('#id_ap_ip').val()];
    // trigger action on server
    $.ajax('/API', {
        method: 'POST',
        data: JSON.stringify(rpcRequest),
        dataType: 'json',
        success: function () {
        },
        error: HuConApp.showAlertBox
    });
}
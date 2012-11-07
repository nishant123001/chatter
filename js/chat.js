$('form[name="user_chat_form"]').submit(function(e){
    var selected_cbox = $("input:checkbox[class=usercol]:checked");
    var msg = "Please ";
    var success = true;
    if (selected_cbox.length < 1){
        msg += "\n  - Please select a user to send message to";
        success = false;
    }
    if ($("#message_many").val().length < 1) {
        msg += "\n  - Please type a message.";
        success = false;
    }
    if (success) {
        console.log("submiting");
    }
    else {
        alert(msg);
    }
    return success;
});
$('form[name="message_reply_form"]').submit(function(e){
    var success = true;
    if ($("#replymessage").val().length < 1) {
        msg += "Please type a message befor submiting it.";
        success = false;
    }
    if (success) {
        console.log("submiting");
    }
    else {
        alert(msg);
    }
    return success;
});
function gotothread(threadid){
    $("#selected").val(threadid);
    $('form[name="goto_selected_form"]').submit();
};

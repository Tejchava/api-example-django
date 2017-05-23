$(document).ready(function() {

//    Setting the default values of the form "Subject" and "Body"

    var greeting = $("#id_Greeting");
    greeting.addClass("form-control");
    greeting.removeAttr("cols");
    greeting.text("Wish you a many many happy returns of the day!!");

    var gSubject = $("#id_Subject");
    gSubject.addClass("form-control");
    gSubject.val("Thank You For Choosing Us");

// Function that actived on clicking the "Greet Now" button, this helps in sending the email immediately.

    $(".greetnow").click(function() {
        $(".patients .modal-title").html("<b>This Message will be sent Immediately</b>");
        var value = this.getAttribute('data-greet-now');
        $("#id_Type").val("now");
        $("#id_uId").val(value);
        fillForm(this);
    });

// Function that actived on clicking the "Auto Greet" button, this helps in sheduling the email.

    $(".greetauto").click(function() {
        $(".patients .modal-title").html("<b>This Message will be sent on the Patient BirthDay Automatically</b>");
        var value = this.getAttribute('data-greet-auto');
        $("#id_Type").val("auto");
        $("#id_uId").val(value);
        fillForm(this);
    });

//    This part is to submit the form to the server, before submitting it checks the subject and body.

    $(".send").click(function() {
        var msg = $("#id_Greeting").val();
        var sub = $("#id_Subject").val();
        if (msg == null || msg === '' || sub == null || sub === ''){
            alert("Greeting or Subject cannot be empty");
            return;
        }
        $.ajax({
            url: "/greet/",
            type: "post",
            data: $("#greet-form").serialize(),
            success: function(data) {
                if ($("#id_Type").val() === "auto"){
                    var id = $("#id_uId").val();
                    $("#card"+id).css("background-color", "darkkhaki");
                }
            },
            error: function(data) {
                alert("Error in Processing!");
            },
        });
    });

// This function disables the form for the Patients who doesn't have the Date-of birth or the Email-Id

    function fillForm(child){
        var father = $("#"+child.closest(".contain").getAttribute("id"));
        var dob = father.children(".dob").text();
        var email = father.children(".email").text();
        if (dob == "No Date Of Birth" || email == "No Email Id"){
            $("#showMsg").show();
            $("#greet-form").hide();
        }else{
            $("#showMsg").hide();
            $("#greet-form").show();
            $("#id_DOB").val(dob);
            $("#id_Email").val(email);
        }
    }

//    $(".glyphicon-log-out").click(function(){
//        $.cookie('sessionid', "bddf", {path: '/'});
//        console.log($.cookie("sessionid"));
//        //$.cookie('sessionid', null, {path: '/'});
//        $.removeCookie("sessionid");
//    });

});
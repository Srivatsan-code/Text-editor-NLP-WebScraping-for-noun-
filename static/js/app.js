var data = []
var token = ""
var k2 = 0
$(function() {
    var INDEX = 0;
    $("#chat-submit").click(function(e) {
        e.preventDefault();
        var msg = $("#chat-input").val();
        var reply = '';
        if (msg.trim() == '') {
            return false;
        }

        generate_message(msg, 'self', reply);
        $.ajax({
            url: '/chat-reply',
            type: "post",
            contentType: "application/json",
            dataType: "json",
            data: JSON.stringify({

                "input_text": msg
            }),
        }).done(function(jsondata, textStatus, jqXHR) {

            reply = jsondata['reply'];
            console.log(reply);
            setTimeout(function() {
                generate_message(msg, 'user', reply);
            }, 1000)

        });

    })

    function generate_message(msg, type, reply) {
        INDEX++;

        var str = "";
        str += "<div id='cm-msg-" + INDEX + "' class=\"chat-msg " + type + "\">";


        str += "          <\/span>";
        str += "          <div class=\"cm-msg-text\">";
        // message
        if(reply!=msg){
        if (type == 'user') {
            str +="BOT: CORRECTED SENTENCE--> <p style='font-weight:bold;'>"+ reply+"<p>";
        } else  {
            str +="YOU: "+ msg;
        }
        }
        else{
            if (type == 'user') {
                str +="BOT: Above sentence is correct";
            } else  {
                str +="YOU: "+ msg;
            }
        }
        str += "          <\/div>";
        str += "        <\/div>";
        $(".chat-logs").append(str);
        $("#cm-msg-" + INDEX).hide().fadeIn(300);
        if (type == 'self') {
            $("#chat-input").val('');
        }
        $(".chat-logs").stop().animate({ scrollTop: $(".chat-logs")[0].scrollHeight }, 1000);
    }



    $(document).delegate(".chat-btn", "click", function() {
        var value = $(this).attr("chat-value");
        var name = $(this).html();
        $("#chat-input").attr("disabled", false);
        generate_message(name, 'self');
    })

    $("#chat-circle").click(function() {
        $("#chat-circle").toggle('scale');
        $(".chat-box").toggle('scale');
    })

    $(".chat-box-toggle").click(function() {
        $("#chat-circle").toggle('scale');
        $(".chat-box").toggle('scale');
    })

})

jQuery(document).ready(function() {



    var slider = $('#max_words')
    slider.on('change mousemove', function(evt) {
        $('#label_max_words').text('Top k words: ' + slider.val())
    })

    var slider_mask = $('#max_words_mask')
    slider_mask.on('change mousemove', function(evt) {
        $('#label_max_words').text('Top k words: ' + slider_mask.val())
    })
    $(document).ready(function() {

        // Close modal on button click
        $("#toggle").click(function() {
            $("#notify").hide();
        });
    });
    $(document).ready(function() {

        $('#input_text').on('click', function() {
            $("#notify").text("BOT: You can predict upto 10 words")

            $("#notify").show();
        });
    });

    $('#input_text').on('keyup', function(e) {
        if (e.key == ' ') {
            $("#text_bert").empty();
            $("#scrap").empty();
            $("#spell").empty();
            $.ajax({
                url: '/get_end_predictions',
                type: "post",
                contentType: "application/json",
                dataType: "json",
                data: JSON.stringify({

                    "input_text": $('#input_text').text(),
                    "top_k": slider.val(),
                }),
                beforeSend: function() {
                    $('.overlay').show()
                },
                complete: function() {
                    $('.overlay').hide()
                }
            }).done(function(jsondata, textStatus, jqXHR) {
                var k = 0
                var k1 = 0
                console.log(jsondata)
                $.each(jsondata, function(propName, propVal) {
                    console.log(propName, propVal);
                    $("#notify").text("BOT: Here the next words")
                    if (k == 0 && jsondata[0] != undefined) {

                        $('#text_bert').append("<br><input type=button id=btn style='width:100%;background-color:#FFFF00;' value=" + jsondata[0] + ">");


                        k = 1
                    }
                    if (k1 == 0 && jsondata['k'] != undefined) {
                        full_str = jsondata['k']
                        divi = full_str.split("https:")
                        content = divi[0]
                        link = "https:" + divi[1]
                        $('#scrap').append(content)
                        $('#scrap').append("<br><a target='_blank' style='color:#191970;font-weight: bold;' href=" + link + ">Click here for more</a>")
                        jsondata['k'] = ""
                        k1 = 1
                    }
                    if (propVal != jsondata[0] && propVal != "") {
                        $('#text_bert').append("<br><input type=button id=btn style='width:100%;background-color:white;' value=" + propVal + ">");
                    }

                });


                if (jsondata['st'] != undefined) {
                    var ans = " " + jsondata['st']
                    $('#spell').text("The correct spelling maybe :" + ans)
                }
                // var textval=$('#input_text').text()
                // $("#input_text").empty();
                // var textarr=textval.split(" ")
                // console.log(textarr)
                // $.each(textarr, function(index,Val) {
                //     var val = $.trim(Val);
                //     var val=" "+val
                //   $('#input_text').append("<span>"+val+"</span>")

                //     });
            }).fail(function(jsondata, textStatus, jqXHR) {
                console.log(jsondata)
            });
        }
        var flag = 0

    })


})
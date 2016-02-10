/**
 * Created by DANYAL on 21/09/2015.
 */
$(document).ready(function () {
    $('#user-login').click(function () {
        $("#login-box").fadeIn();
    });

    $('.signup').click(function () {
        $("#signup-box").fadeIn();
    });

    $('#signup-box .submit').click(function (e) {
        $('#signup-name + div').html("");
        $('#signup-email + div').html("");
        $('#signup-pass + div').html("");

        var name = $('#signup-name').val();
        var email = $('#signup-email').val();
        var password = $('#signup-pass').val();
        var emailReg = /^[A-Z0-9._%+-]+@([A-Z0-9-]+\.)+[A-Z]{2,4}$/i;
        var flag = true;
        if (!name || name.search('[a-zA-Z]') > -1) {
            $('#signup-name + div').html("نام باید فارسی باشد.");
            flag = false;
        }
        if (!email || !emailReg.test(email)) {
            $('#signup-email + div').html("ایمیل اشتباه وارد شده است.");
            flag = false;
        }
        if (!password || password.length < 4) {
            $('#signup-pass + div').html("رمز عبور حداقل باید 4 حرف باشد.");
            flag = false;
        }

        if (flag) {
            $.ajax({
                type: 'POST',
                url: checkSignupUrl,
                data: {
                    'username': email
                },
                success: function (msg) {
                    var res = eval(msg);

                    if (res) {
                        $('#signup-box form').submit();
                    } else {
                        $('#signup-email + div').html("ایمیل تکراری است.");

                    }
                }
            });
        }

        e.preventDefault();
        return false;
    });

    $('.go-signup').click(function () {
        $(this).parents('.account-section').fadeOut(function () {
            $("#signup-box").fadeIn();
        });
    });

    $('.forget-pass').click(function () {
        $(this).parents('.account-section').fadeOut(function () {
            $("#forget-box").fadeIn();
        });
    });

    $(".account-section, .close-pop-up").click(function () {
        $('.account-section').fadeOut();
        $("#video-player").find('.content').remove();
    });

    $('.pop-box').click(function (e) {
        e.stopPropagation();
    });


    $('.fire-search').click(function () {
        var url = $('#search-icon').attr("data-url");
        var q = $('#search-text').val().trim();
        var t = $('#search-type').val();
        if (q) {
            window.location = url + "?q=" + q + "&t=" + t;
        }
    });

    $("#search-text, .search-auto-list").click(function (e) {
        e.stopPropagation();
    });

    $("#search-text").keyup(function (e) {
        if (e.keyCode == 13) {
            var url = $('#search-icon').attr("data-url");
            var q = $('#search-text').val().trim();
            var t = $('#search-type').val();
            if (q) {
                window.location = url + "?q=" + q + "&t=" + t;
            }
        } else {
            var term = $('#search-text').val().trim();

            if (term.length > 0) {

                $.ajax({
                    type: 'GET',
                    url: searchUrl,
                    data: {
                        't': term,
                        'h': true
                    },
                    success: function (msg) {
                        var res = msg;

                        $("#search-sug-items").empty();

                        $(res).appendTo('#search-sug-items');
                    }
                });


                $('.search-auto-list').fadeIn(200);

                e.stopPropagation();

            }
            $('.see-all span').html('"' + term + '"');

        }
    });


    var flag2 = false;
    $('.right-arrow').click(function () {
        if (flag2)return;

        flag2 = true;
        var $panel = $(this).parent().find('.slider');

        $panel.animate({scrollLeft: $panel.scrollLeft() + 200}, 500, function () {
            flag2 = false;
        });

    });

    $('.left-arrow').click(function () {
        if (flag2)return;

        flag2 = true;
        var $panel = $(this).parent().find('.slider');

        $panel.animate({scrollLeft: $panel.scrollLeft() - 200}, 500, function () {
            flag2 = false;
        });
    });

    // ROTATABLE
    $('.rotatable .rotate-btn').click(function () {
        if ($(this).parents('.rotatable').hasClass('active'))
            $(this).parents('.rotatable').removeClass("active");
        else
            $(this).parents('.rotatable').addClass("active");
    });


    //SLIDER


    // PERSIAN NUMS
    TraceNodes(document);


    // AUTH CHECK
    $(document).on('click', '.login-need', function (e) {
        if (!is_auth) {
            $("#login-box").fadeIn();
            e.preventDefault();
            e.stopPropagation();
        }
    });

    $(document).on('click', '.signup-need', function (e) {
        if (!is_auth) {
            $("#signup-box").fadeIn();
            e.preventDefault();
            e.stopPropagation();
        }
    });


    $('#login-box .submit').click(function (e) {

        var email = $('#login-email').val();
        var password = $('#login-pass').val();

        $('#login-box .message').html("");

        $.ajax({
            type: 'POST',
            url: checkUrl,
            data: {
                'username': email,
                'password': password
            },
            success: function (msg) {
                var res = eval(msg);

                if (res) {
                    $('#login-box form').submit();
                } else {
                    $('#login-box .message').html("ایمیل یا رمز عبور اشتباه است.");
                }

            }
        });

        e.preventDefault();
        return false;

    });


    // FORGET PASS
    $('#forget-box .submit').click(function (e) {

        var email = $('#forget-email').val();

        $('#forget-box .message').html("");

        $.ajax({
            type: 'POST',
            url: forgetUrl,
            data: {
                'email': email
            },
            success: function (msg) {
                var res = eval(msg);

                var success = res.s;
                var message = res.m;

                $('#forget-box .message').html(message);


                if (success) {
                    $('#forget-box .message').addClass('success').removeClass("red");
                } else {
                    $('#forget-box .message').addClass('red').removeClass("success");
                }

            }
        });

        e.preventDefault();
        return false;

    });

    // RESEND CONFIRM EMAIL
    $('#resend-confirm-email').click(function (e) {

        var $message = $(this).parent().find('.message').first();

        $.ajax({
            type: 'GET',
            url: sendConfirmEmailUrl,
            data: {},
            success: function (msg) {
                var res = eval(msg);

                var success = res.s;
                var message = res.m;

                $message.html(message);

                if (success) {
                    $message.addClass('success').removeClass("red");
                } else {
                    $message.addClass('red').removeClass("success");
                }

            }
        });

        e.preventDefault();
        return false;

    });

    // SUBMIT FORM
    $('.submit-form').click(function () {
        $(this).parents('form').first().submit();
    });

    // SELECTS
    $(document).click(function () {
        $('.select-list').fadeOut(200);
        $('.select-box').removeClass('active');

        $('.search-auto-list').fadeOut(200);

    });

    $('.select-box').click(function (e) {
        $('.select-list').fadeOut(200);
        $('.select-box').removeClass('active');

        var $contact_choices = $(this).find(".select-list");
        if ($contact_choices.is(":visible")) {
            $(this).removeClass("active");
            $contact_choices.fadeOut(200);
        } else {
            $(this).addClass("active");
            $contact_choices.fadeIn(200);
        }

        e.stopPropagation();
    });

    $('.select-item').click(function (e) {
        $(this).parents('.select-list').first().fadeOut(200);

        var $select_box = $(this).parents('.select-box').first();

        $select_box.removeClass("active");
        $select_box.find('.select-input').val($(this).attr('data-value'));
        $select_box.find('.select-text').html($(this).html());

        e.stopPropagation();
    });


    // RADIO BTN
    $('.choices').click(function (e) {
        var isChecked = $(this).find('.choice').is(':checked');

        $(this).parent().find('.choice').removeAttr('checked');

        $(this).find('.choice').attr('checked', !isChecked);
        $(this).find('.choice').prop('checked', !isChecked);

        if (isChecked) {
            $(this).parent().find('.choice').removeAttr('checked');
        }

        e.stopPropagation();
    });

// header
    $(window).scroll(function (event) {
        var scrollheight = $(window).scrollTop();
        if (scrollheight > 10) {
            if (!$("#header").hasClass('header-fix')) {
                $("#header").addClass('header-fix');
            }
        } else {
            $("#header").removeClass('header-fix');
        }

    });


    // FAV

    if (typeof favUrl != "undefined")
        $(document).on('click', '.fav-flag', function () {
            var objId = $(this).attr("data-id");

            var $elem = $(this);

            $.ajax({
                type: 'POST',
                url: favUrl,
                data: {
                    'id': objId
                },
                success: function (msg) {
                    var res = eval(msg);
                    var fav = res.f;


                    if (fav) {
                        $elem.addClass("active");
                    } else {
                        $elem.removeClass("active");
                    }

                }
            });
        });

});


$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});


String.prototype.toPersianDigit = function (a) {
    return this.replace(/\d+/g, function (digit) {
        var enDigitArr = [], peDigitArr = [];
        for (var i = 0; i < digit.length; i++) {
            enDigitArr.push(digit.charCodeAt(i));
        }
        for (var j = 0; j < enDigitArr.length; j++) {
            peDigitArr.push(String.fromCharCode(enDigitArr[j] + ((!!a && a == true) ? 1584 : 1728)));
        }
        return peDigitArr.join('');
    });
};

function TraceNodes(Node) {
    if (Node.nodeType == 3) {  //TextNode
        Node.nodeValue = Node.nodeValue.toPersianDigit();
    } else {
        if (Node.tagName != 'STYLE') {
            for (var i = 0; i < Node.childNodes.length; i++)
                TraceNodes(Node.childNodes[i]);
        }
    }
}

// JQUERY LOAD SCROLL

$(document).ready(function () {
    (function (i, s, o, g, r, a, m) {
        i['GoogleAnalyticsObject'] = r;
        i[r] = i[r] || function () {
                (i[r].q = i[r].q || []).push(arguments)
            }, i[r].l = 1 * new Date();
        a = s.createElement(o),
            m = s.getElementsByTagName(o)[0];
        a.async = 1;
        a.src = g;
        m.parentNode.insertBefore(a, m)
    })(window, document, 'script', '//www.google-analytics.com/analytics.js', 'ga');

    ga('create', 'UA-71770029-1', 'auto');
    ga('send', 'pageview');


    $('img').each(function () {
        if (this.getAttribute("data-src")) {
            this.setAttribute("src", this.getAttribute("data-src"));
            this.removeAttribute("data-src")
        }
    });

});
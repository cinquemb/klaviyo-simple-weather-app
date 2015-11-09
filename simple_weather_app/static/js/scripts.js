      /* csrf for ajax */
(function($) {
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
    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    $.ajaxSetup({
        crossDomain: false, // obviates need for sameOrigin test
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type)) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
})(jQuery);

/*modals*/
(function($) {
    var ajax_modals = [
        {
            selector: '#subscribe-modal'
        }
    ];
    $.each(ajax_modals, function(i, form) {
        //remove old modals
        $(form.selector).on('hidden', function() {
            $(this).removeData('modal');
        });
        $(form.selector).on('submit', 'form', function() {
            $(form.selector).addClass('loading');
            $.ajax({
                type: 'POST',
                url: $(form.selector).find('form').attr('action'),
                data: $(this).serialize(), 
                dataType: 'html',
                success: function(data) {
                    $(form.selector).removeClass('loading');
                    $(form.selector + ' .modal-form-body').html(data);
                }, error: function(a, b, c) {
                    console.log('error', a, b, c);
                }
            });
            return false;
        });
    });

})(jQuery);
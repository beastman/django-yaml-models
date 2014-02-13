$(function() {
    $('#models_list a').click(function() {
        model_class = $(this).attr('href').substr(1);
        $.get('/load-model-data', {model_class:model_class}, function(data) {
            if(data.success) {
                $('h1').text(data.title);
                $('#datatable').html($.tmpl($('#datatable-template').html(), data));
                $('#add-form').html($.tmpl($('#add-form-template').html(), data));
            }
            else {
                alert('Произошла ошибка при загрузке данных.')
            }
        }, 'json');
        $('#models_list a').removeClass('active');
        $(this).addClass('active');
        return false;
    });
    $('#models_list a:first').trigger('click');

    $('#content').on('click', 'input.datepicker', function() {
        $(this).datepicker();
        $(this).datepicker("show");
    });
    $('#content').on('submit', '#add-form form', function() {
        var form_data = $(this).serialize();
        $.post('/add', form_data, function(data){
            if(data.success) {
                $("#models_list .active").trigger('click');
            }
            else {
                if(data.errors) {
                    message = data.errors.join('\n');
                    alert(message);
                }
                else {
                    alert('Произошла ошибка при сохранении');
                }
            }
        }, 'json');
        return false;
    });
});
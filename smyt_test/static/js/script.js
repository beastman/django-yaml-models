function safe_tags(str) {
    return str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;') ;
}

function save_column(column) {
    $form = $('form', column);
    $.post('/edit', $form.serialize(), function(data) {
        if(data.success) {
            value = $('input.value_input', $form).val();
            $form.parents('td:first').html(safe_tags(value)).removeClass('editing');
            csrf_token = data.csrf_token;
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
}

$(function() {
    $('#content').on('click', 'input.datepicker', function() {
        $(this).datepicker({dateFormat: 'yy-mm-dd'});
        $(this).datepicker("show");
    });


    $('#models_list a').click(function() {
        //Выбор таблицы в левой части
        model_class = $(this).attr('href').substr(1);
        $.get('/load-model-data', {model_class:model_class}, function(data) {
            if(data.success) {
                $('h1').text(data.title);
                csrf_token = data.csrf_token;
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


    $('#content').on('submit', '#add-form form', function() {
        //Форма добавления
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

    $('#content').on('click', 'td.editable', function() {
        //Замена значения на форму редактирования
        $this = $(this);
        if(!$this.hasClass('editing')) {
            data = {};
            data.csrf_token = csrf_token;
            data.model_class = $this.parents('table:first').attr('model-class');
            data.row_pk = $this.parents('tr:first').attr('pk');
            data.col_name = $this.attr('column');
            data.type = $this.attr('type');
            data.value = $this.html();
            $this.addClass('editing');
            $this.html($.tmpl($('#edit-form-template').html(), data));
            $('input[name=' + data.col_name + ']', $this).trigger('focus');
            if($('input[name=' + data.col_name + ']', $this).hasClass('datepicker')) {
                $('input[name=' + data.col_name + ']', $this).trigger('click');
            }
        }
    });
    $('#content').on('blur', 'td.editable input.value_input', function() {
        if($(this).hasClass('datepicker')) {
            $(this).datepicker('hide');
        }
        column = $(this).parents('td:first');
        setTimeout(function(){
            save_column(column);
        }, 500);
    });
    $('#content').on('submit', 'td.editable form', function() {
        column = $(this).parents('td:first');
        save_column(column);
        return false;
    });
});
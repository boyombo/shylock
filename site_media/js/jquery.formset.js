(function($) {
    $.fn.formset = function(options)
    {
        options = $.extend({
           prefix: 'form',
           addText: 'add another',
           deleteText: 'remove',
           added: null,
           removed: null
        }, options);

        var updateElementIndex = function(el, prefix, ndx) {
            var id_regex = new RegExp('(' + prefix + '-\\d+)');
            var replacement = prefix + '-' + ndx;
            if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex, replacement));
            if (el.id) el.id = el.id.replace(id_regex, replacement);
            if (el.name) el.name = el.name.replace(id_regex, replacement);
        };

        $(this).each(function() {
            $(this).addClass('dynamic-form');
            if ($(this).attr('tagName') == 'TR') {
                // if the forms are laid out in table rows, insert
                // the remove button into the last table cell:
                $(this).children(':last').append('<a class="delete-row" href="javascript:void(0)">' + options.deleteText + '</a>');
            } else {
                // otherwise, just insert the remove button as the
                // last child element of the form's container:
                $(this).append('<a class="delete-row" href="javascript:void(0)">' + options.deleteText +'</a>');
            }
            $(this).find('a.delete-row').click(function() {
                // remove the parent form containing this button, and
                // update the TOTAL_FORMS hidden field.
                // also, update names and ids for all remaining form controls
                // so they remain in sequence:
                var row = $(this).parents('.dynamic-form');
                row.remove();
                if (options.removed) options.removed(row);
                var forms = $('.dynamic-form');
                $('#id_' + options.prefix + '-TOTAL_FORMS').val(forms.length);
                for (var i=0, formCount=forms.length; i<formCount; i++) {
                    $(forms.get(i)).find('input,select,textarea,label').each(function() {
                        updateElementIndex(this, options.prefix, i);
                    });
                }
                return false;
            });
        });

        if ($(this).length) {
            if ($(this).attr('tagName') == 'TR') {
                // if forms are laid out as table rows, insert the
                // "add" button in a new table row:
                var numCols = this.eq(0).children().length;
                $(this).parent().append('<tr><td colspan="' + numCols + '"><a class="add-row" href="javascript:void(0)">' + options.addText + '</a></tr>');
            } else {
                // otherwise, insert it immediately after the last form:
                $(this).filter(':last').after('<a class="add-row" href="javascript:void(0)">' + options.addText + '</a>');
            }
            $(this).parent().find('a.add-row').click(function() {
                var formCount = parseInt($('#id_' + options.prefix + '-TOTAL_FORMS').val());
                var row = $('.dynamic-form:first').clone(true).get(0);
                $(row).removeAttr('id').insertAfter($('.dynamic-form:last')); //.children('.hidden').removeClass('hidden');
                $(row).find('input,select,textarea,label').each(function() {
                    updateElementIndex(this, options.prefix, formCount);
                    $(this).val('');
                });
                $('#id_' + options.prefix + '-TOTAL_FORMS').val(formCount + 1);
                if (options.added) options.added($(row));
                return false;
            });
        }

        return $(this);
    }
})(jQuery)

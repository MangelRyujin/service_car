

function updateElementIndex(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+-)');
    var replacement = prefix + '-' + ndx + '-';

    
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex,
    replacement));
    if (el.id) el.id = el.id.replace(id_regex, replacement);
    if (el.name) el.name = el.name.replace(id_regex, replacement);
}

function addForm(btn, prefix) {
    var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());

   
    if (formCount < 1000) {
        // Clone a form (without event handlers) from the first form
        var row = $(".item:last").clone(false).get(0);

        // Insert it after the last form
        $(row).removeAttr('id').hide().insertAfter(".item:last").slideDown(300);

        // Remove the bits we don't want in the new row/form
        // e.g. error messages
        $(".errorlist", row).remove();
        
        $(row).children().removeClass("error");
        row.classList.remove('d-none');
        $(row).find('.formset-field').each(function () {
            updateElementIndex(this, prefix, formCount);
            
            $(this).val('');
            $(this).removeAttr('value');
            $(this).prop('checked', false);
        });
        // Relabel or rename all the relevant bits
        $(row).find('.formset-field').each(function () {
            updateElementIndex(this, prefix, formCount);
            
            $(this).val('');
            $(this).removeAttr('value');
            $(this).prop('checked', false);
        });

        // Add an event handler for the delete item/form link
        $(row).find(".delete").click(function () {
            return deleteForm(this, prefix);
        });

        // Update the total form count
        $("#id_" + prefix + "-TOTAL_FORMS").val(formCount + 1);
        const selectOriginal = document.getElementById('select-services');
        const opcionSeleccionada = selectOriginal.options[selectOriginal.selectedIndex];
        
        // Obtener el valor y texto de la opción seleccionada
        const valor = opcionSeleccionada.value;
        const texto = opcionSeleccionada.text;
        
        // Obtener el select donde insertaremos la nueva opción
        const selectNuevo = document.getElementById('id_items-'+formCount+'-service');
        
        // Crear una nueva opción con el mismo texto
        const nuevaOpcion = new Option(texto, valor);
        selectNuevo.replaceChildren();
        // Insertar la nueva opción al final del select
        selectNuevo.add(nuevaOpcion);
        const select = document.getElementsByClassName('item d-none');
        if (select[0]) {
            // select[0].remove();
            const boton = select[0].querySelector('.remove-form-row');
            if (boton) {
                    boton.click();
                }
       
            deleteForm($(this), String($('.add-form-row').attr('id')));
            
    
        }
        // Seleccionar la nueva opción
        selectNuevo.value = valor;
        selectNuevo.selected = true;
        
    } // End if

    return false;
}


function deleteForm(btn, prefix) {
      var formCount = parseInt($('#id_' + prefix + '-TOTAL_FORMS').val());
      if (formCount > 1) {
          // Delete the item/form
          var goto_id = $(btn).find('input').val();
          if( goto_id ){
            $.ajax({
                url: "/" + window.location.pathname.split("/")[1] + "/formset-data-delete/"+ goto_id +"/?next="+ window.location.pathname,
                error: function () {
                  console.log("error");
                },
                success: function (data) {
                  $(btn).parents('.item').remove();                 
                },
                type: 'GET'
            });
          }else{
            $(btn).parents('.item').remove();
          }

          var forms = $('.item'); // Get all the forms
          // Update the total number of forms (1 less than before)
          $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
          var i = 0;
          // Go through the forms and set their indices, names and IDs
          for (formCount = forms.length; i < formCount; i++) {
              $(forms.get(i)).find('.formset-field').each(function () {
                  updateElementIndex(this, prefix, i);
              });
          }
      } // End if

      return false;
  };



// EXTRA


function updateExtraElementIndex(el, prefix, ndx) {
    var id_regex2 = new RegExp('(' + prefix + '-\\d+-)');
    var replacement2 = prefix + '-' + ndx + '-';

    
    if ($(el).attr("for")) $(el).attr("for", $(el).attr("for").replace(id_regex2,
    replacement2));
    if (el.id) el.id = el.id.replace(id_regex2, replacement2);
    if (el.name) el.name = el.name.replace(id_regex2, replacement2);
}

function addExtraForm(btn, prefix2) {
    var formCount2 = parseInt($('#id_' + prefix2 + '-TOTAL_FORMS').val());

   
    if (formCount2 < 1000) {
        // Clone a form (without event handlers) from the first form
        var row2 = $(".extraitem:last").clone(false).get(0);

        // Insert it after the last form
        $(row2).removeAttr('id').hide().insertAfter(".extraitem:last").slideDown(300);

        // Remove the bits we don't want in the new row2/form
        // e.g. error messages
        $(".errorlist", row2).remove();
        
        $(row2).children().removeClass("error");
        row2.classList.remove('d-none');
        $(row2).find('.extraformset-field').each(function () {
            updateExtraElementIndex(this, prefix2, formCount2);
            
            $(this).val('');
            $(this).removeAttr('value');
            $(this).prop('checked', false);
        });
        // Relabel or rename all the relevant bits
        $(row2).find('.extraformset-field').each(function () {
            updateExtraElementIndex(this, prefix2, formCount2);
            
            $(this).val('');
            $(this).removeAttr('value');
            $(this).prop('checked', false);
        });

        // Add an event handler for the delete item/form link
        $(row2).find(".delete").click(function () {
            return deleteExtraForm(this, prefix2);
        });

        // Update the total form count
        $("#id_" + prefix2 + "-TOTAL_FORMS").val(formCount2 + 1);
        const extra_service = document.getElementsByClassName('extraitem d-none');
        if (extra_service[0]) {
            // extra_service[0].remove();
            const btn = extra_service[0].querySelector('.extraitems-remove-form-row');
            if (btn) {
                    btn.click();
                }
       
                deleteExtraForm($(this), String($('.extraitems-add-form-row').attr('id')));
            
    
        }
        
    } // End if

    return false;
}


function deleteExtraForm(btn, prefix2) {
      var formCount2 = parseInt($('#id_' + prefix2 + '-TOTAL_FORMS').val());
      if (formCount2 > 1) {
          // Delete the item/form
          var goto_id2 = $(btn).find('input').val();
          if( goto_id2 ){
            $.ajax({
                url: "/" + window.location.pathname.split("/")[1] + "/extraitems-data-delete/"+ goto_id +"/?next="+ window.location.pathname,
                error: function () {
                  console.log("error");
                },
                success: function (data) {
                  $(btn).parents('.extraitem').remove();                 
                },
                type: 'GET'
            });
          }else{
            $(btn).parents('.extraitem').remove();
          }

          var forms2 = $('.extraitem'); // Get all the forms
          // Update the total number of forms (1 less than before)
          $('#id_' + prefix2 + '-TOTAL_FORMS').val(forms2.length);
          var i = 0;
          // Go through the forms and set their indices, names and IDs
          for (formCount2 = forms2.length; i < formCount2; i++) {
              $(forms2.get(i)).find('.extraformset-field').each(function () {
                  updateExtraElementIndex(this, prefix2, i);
              });
          }
      } // End if

      return false;
  }
// END EXTRA



  $("body").on('click', '.remove-form-row',function () {
    deleteForm($(this), String($('.add-form-row').attr('id')));
  });

  $("body").on('click', '.add-form-row',function () {
    
    
    return addForm($(this), String($(this).attr('id')));
      
      
      
  });

  $("body").on('click', '.extraitems-remove-form-row',function () {
    deleteExtraForm($(this), String($('.extraitems-add-form-row').attr('id')));
  });

  $("body").on('click', '.extraitems-add-form-row',function () {    
      return addExtraForm($(this), String($(this).attr('id')));
      
      
      
  });

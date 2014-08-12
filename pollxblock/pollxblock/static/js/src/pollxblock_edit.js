/* Javascript for PollXBlock, edit view. */
function PollXBlockEdit(runtime, element) {
    
    /* Html element used to alert users, in case of an error */
    $('.xblock-editor-error-message', element).css('display', 'none');
    $('.xblock-editor-error-message', element).css('color', 'red');

    /* Click event for Cancel button, while in the edit mode */
    $(element).find('.cancel-button').bind('click', function() {
        runtime.notify('cancel', {});
    });

    /* Click event for Save button, while in the edit mode */
    /* Gets all the input values and sends them back to model */
    $(element).find('.save-button').bind('click', function() {
        
        /* Get answers */
        answerIds = [];
        answerLabels = [];
        nAnswers = $(element).find('input[id=edit_number_of_answers]').val();
        
        var answerId, answerLabel;
        
        for (var i=1;i<=nAnswers;i++){
            answerId = $(element).find('input[name=answer'+i+'_id]').val();
            answerLabel = $(element).find('input[name=answer'+i+'_label]').val();
            answerIds.push(answerId);
            answerLabels.push(answerLabel);
        }
        
        /* Data for the model */
        var data = {
            'display_name': $('.edit-display-name', element).val(),
            'question': $('.edit-question', element).val(),
            'answerIds': answerIds,
            'answerLabels': answerLabels,
            'reset': $('.edit-reset', element).is(':checked')
        };
        
        /* AJAX call and its handler */
        var handlerUrl = runtime.handlerUrl(element, 'save_edit');
        $.post(handlerUrl, JSON.stringify(data)).done(function(response) {
            if (response.result === 'success') {
                window.location.reload(true);
            } else {
                $('.xblock-editor-error-message', element).html('Error: '+response.message);
                $('.xblock-editor-error-message', element).css('display', 'block');
            }
        });
    });
    
//    /* Validates user input for answer values */
//    $(element).on('keyup', 'input.answer-value', function(){
//        ValidateTextData(this, element, "Answer value", 0);
//    });
//    
//    /* Validates user input for Pie chart width */
//    $(element).on('keyup', 'input#edit_width', function(){
//        ValidateTextData(this, element, "Width", 500);
//    });
//    
//    /* Validates user input for Pie chart height */
//    $(element).on('keyup', 'input#edit_height', function(){
//        ValidateTextData(this, element, "Height", 500);
//    });
//    
//    /* Validates user input for Pie chart start angle */
//    $(element).on('keyup', 'input#edit_start_angle', function(){
//        ValidateNumericData(this, element, "Start angle", 0, 360);
//    });
//    
//    /* Validates user input for Pie chart end angle */
//    $(element).on('keyup', 'input#edit_end_angle', function(){
//        ValidateNumericData(this, element, "End angle", 0, 360);
//    });
//    
//    /* Check the validity of data in text box for editing label threshold 
//       when user chooses to enter the data from keyboard */
//    $(element).on('keyup', 'input#edit_label_threshold', function(){
//        ValidateNumericData(this, element, "Label threshold", 0, 100);
//    });
    
    /* Check the validity of data in text box for editing number of available answers 
       when user chooses to enter the data from keyboard */
    $(element).on('keyup', 'input#edit_answers', function(){
        ValidateNumericData(this, element, "Number of answers", 2, 10);
        GenerateDynamicInputs(element, this);
    });
    
    /* Dynamically recreates html text inputs for answers in case user chooses to interact with the control using up and down buttons */
    $(element).on('change', 'input#edit_answers', function(){
        GenerateDynamicInputs(element, this);
    });
    
    /* 
        Validates data entered within text html input field
        Parameters: -validated html input element
                    -XBlock element sent from server side
                    -description name of the validated element
                    -minimum value
    */
    function ValidateTextData(textElement, element, name, minValue) {
        var txtValue = $(textElement).val();
        if (isNaN( txtValue )){
            $(textElement).val(minValue);
            $('.xblock-editor-error-message', element).html(name + ' must be a number.');
            $('.xblock-editor-error-message', element).css('display', 'block');
        }
        else if (txtValue < 0){
            $(textElement).val(txtValue.substring(1));
            $('.xblock-editor-error-message', element).html(name + ' must be a positive number.');
            $('.xblock-editor-error-message', element).css('display', 'block');
        }
        else {
            $('.xblock-editor-error-message', element).css('display', 'none');    
        }
    }
    
    /* 
        Validates data entered within numeric html input field
        Parameters: -validated html input element
                    -XBlock element sent from server side
                    -description name of the validated element
                    -minimum value
                    -maximum value
    */
    function ValidateNumericData(numericElement, element, name, minValue, maxValue) {
        var nmbValue = $(numericElement).val();
        
        if (nmbValue < minValue) {
            $('.xblock-editor-error-message', element).html(name + ' must be a positive number.');
            $('.xblock-editor-error-message', element).css('display', 'block');
            nmbValue = minValue;
        } else if (nmbValue > maxValue) {
            $('.xblock-editor-error-message', element).html('Maximum ' + name.toLowerCase() + ' is ' + maxValue + '.');
            $('.xblock-editor-error-message', element).css('display', 'block');
            nmbValue = maxValue;
        } else {
            $('.xblock-editor-error-message', element).css('display', 'none');
        }
        
        $(numericElement).val(nmbValue);
    }
    
    /* Generates label and inputs for each group, depending on the entered number of available groups */
    function GenerateDynamicInputs(element, groupElement) {
        var nGroups = $(groupElement).val();

        var html_String = "<label class='label setting-label'>Answer</label><label class='label setting-label' id='name'>ID</label><label class='label setting-label' id='value'>Label</label><span class='tip setting-help'>ID example: yes<br/>Label example: Yes</span>";
        var answerId, answerLabel;
        
        for (var i=1;i<=nGroups;i++){
            
            answerId = $(element).find('input[name=answer'+i+'_id]').val();
            answerLabel = $(element).find('input[name=answer'+i+'_label]').val();
            
            if (answerId == null){
                html_String += "<p><label class='label setting-label'>Group "+i+"</label><input style='margin-left: 4px;' class='input setting-input group-name' name='answer"+i+"_name' id='answer"+i+"_id' value='Answer "+i+"' type='text'>";
            }
            else{
                html_String += "<p><label class='label setting-label'>Group "+i+"</label><input style='margin-left: 4px;' class='input setting-input group-name' name='answer"+i+"_name' id='answer"+i+"_id' value='"+answerId+"' type='text'>";          
            }
            
            if (answerLabel == null){
                html_String += "<input style='margin-left: 4px;' class='input setting-input group-value' name='answer"+i+"_label' id='answer"+i+"_label' value='' type='text'></p>";
            }
            else{
                html_String += "<input style='margin-left: 4px;' class='input setting-input group-value' name='answer"+i+"_label' id='answer"+i+"_label' value='"+answerLabel+"' type='text'></p>";
            }
        }

        $("#panel2", element).html(html_String);
    }
    
    $(function () {
        /* Here's where you'd do things on page load. */
    });
}

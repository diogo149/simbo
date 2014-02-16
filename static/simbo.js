$(document).ready(function()    {
	var uuid = undefined;


    var variables = [];
    var num_distributions = 1;
    var default_var = "";
    var distr_var = "";

    /**********************************************
     ** interactive indepdent variables building **
     **********************************************/

    /****** building the interface ******/
    function build_variable_input_form() {
        // build drop down menu for distributions
        $('#distribution_dd_menu').html('');
        
		$.getJSON('/api/distribution_schema', function (response) {
			var active = "active";
			for (var dist in response) {
				if(active.length)
					$('#distribution_dd .text').html(dist);
				$('#distribution_dd_menu').append('<div class="item '+active+'" data-value="'+ dist +'">'+dist+'</div>'); 
				active = "";
			}
		});

        $('#default_dd').dropdown(); 

        $('#distribution_dd').dropdown();

		$("#feature_form.ui.form").form({
			//item validation
			variable_name: {
			  	identifier: 'variable_name',
			  	rules: [
			  		{
			  		    type   : 'empty',
			  			prompt : 'Please enter variable name'
			  		}
			  	]
			}
		}, {
			// item submission
			onSuccess: function(foo){
				var var_name = $('#feature_form.ui.form').form('get field', "variable_name").val();
				var adistr_var = $("#distribution_dd").dropdown("get text");
				var adefault_var = $("#default_dd").dropdown("get text");
				var item = [var_name, adistr_var, adefault_var];
				console.log(item);
				variables.push(item);
				update_list();

			},
		});		
    }

    /****** interaction functionality ******/
    function make_html_item(item, i)   {
        var html_text = '<tr value="'+i+'"><td>';
        html_text += item[0];
        html_text += '</td><td>';
        html_text += item[1];
        html_text += '</td><td>';
        html_text += item[2];
        html_text += '</td><td><div class="tiny ui icon button edit_item"><i class="edit icon"></i></div></td><td><div class="tiny ui icon button delete_item"><i class="remove icon"></i></div></td></tr>';

        return html_text;
    }

    function update_list()  {
        $('#item_table_body').html("");
        for (var i=0; i<variables.length; i++)  {
            $('#item_table_body').append(make_html_item(variables[i], i));
        }
    }

    ///// user clicked "new experiment" button
    $('#application_nav_btn').click(function()    {
        $('#home_div').hide();
        $('#application_div').show();
    });

    ///// user clicked "home" button
    $('#home_nav_btn').click(function()    {
        $('#application_div').hide();
        $('#home_div').show();
    });

    ///// user clicked "independent variables" tab
    $('#variables_tab').click(function()    {
        // change which tab is active
        $(this).attr('class', 'active item');
        $('#visuals_tab').attr('class', 'item');

        // change which content is displayed
        $('#visuals_sec').hide();
        $('#variables_sec').show();
    });

    ///// user clicked "visualizations" tab
    $('#visuals_tab').click(function()    {
        // change which tab is active
        $(this).attr('class', 'active item');
        $('#variables_tab').attr('class', 'item');

        // change which content is displayed
        $('#variables_sec').hide();
        $('#visuals_sec').show();
    });

    // user wishes to edit an item
    $(document).on('click', '.edit_item', function() {
        var par_elm = $(this).parent().parent();
        var value = $(par_elm).attr('value');
        $("#var_name_input").val(variables[value][0]);

        // emtpy distribution dd menu
        var dist_html = '<input type="hidden" name="distribution"><div class="text">Distribution</div><i class="dropdown icon"></i><div class="menu" id="distribution_dd_menu"></div>';
        var i;
        $('#distribution_dd').html(dist_html);
        $('#distribution_dd_menu').append('<div class="item" data-value="1">1</div>');
        for (i=2; i<=num_distributions; i++) {
            $('#distribution_dd_menu').append('<div class="item" data-value="'+i.toString()+'">'+i.toString()+'</div>');
        }

        $('#distribution_dd').dropdown({
            onChange: function (val) {
                distr_var = val;
            }
        });

        // empty default dd menu
        var default_html = '<input type="hidden" name="default"><div class="text">Default</div><i class="dropdown icon"></i><div class="menu"><div class="item" data-value="off">off</div><div class="item" data-value="on">on</div></div>';
        $('#default_dd').html(default_html);
        
        $('#default_dd').dropdown({
            onChange: function (val) {
                distr_var = val;
            }
        });

        // deletes existing item
        variables.splice(value, 1);
        update_list();
    });

    // user wishes to delete an item
    $(document).on('click', '.delete_item', function() {
        var par_elm = $(this).parent().parent();
        var value = $(par_elm).attr('value');
        variables.splice(value, 1);
        update_list();
    });

	// generate input form
    build_variable_input_form();

	// graph test 
	$("#foo").click(function() {
		$.get( "/foobar", function( data ) {
			// $("#chart").html( data );
                        console.log(data);
                        eval(data);
			alert( "Load was performed." );
		});
	});
});

/*
    <div class="ui horizontal list">
            <div class="item">
              var_name
            </div>
            <div class="item">
              distribution_input
            </div>
            <div class="item">
              default_input
            </div>
            <div class="item">
              <div class="ui icon button" id="add_item_btn">
                <i class="large edit icon"></i>
              </div>
            </div>
            <div class="item">
              <div class="ui icon button" id="add_item_btn">
                <i class="large remove icon"></i>
              </div>
            </div>
          </div>
        </div>
*/
/*

    $("#button").click(function()   {
        var toAdd = $("input[name=checkListItem]").val();
        $('.list').append("<div class='item'>" + toAdd + "</div>");
    });


    <div class="ui form">
      <div class="ui four fields">
        <div class="field">
          <input type="text" placeholder="Variable Name" id="var_name_input">
        </div>
        <div class="field">
          <input type="text" placeholder="Distribution" id="distribution_input">
        </div>
        <div class="field">
          <input type="text" placeholder="Default" id="default_input">
        </div>
        <div class="field">
          <div class="ui blue submit button" id="add_item_btn">+</div>
        </div>
      </div>
    </div>
*/

/*
    to-do (variables):
    { } add labels for input section
    { } make distributions drop-down
    { } if certain dist. are selected, add more options
    {x} edit item
    {x} delete item

*/

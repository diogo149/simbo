$(document).ready(function()    {

    var variables = [];
    var num_distributions = 5;
    var default_var = "";
    var distr_var = "";

    /**********************************************
     ** interactive indepdent variables building **
     **********************************************/

    /****** building the interface ******/
    function build_variable_input_form()    {
        // build drop down menu for distributions
        $('#distribution_dd_menu').html('');
        var i;
        // indexes at 1
        $('#distribution_dd_menu').append('<div class="item" data-value="1">1</div>');
        for (i=2; i<=num_distributions; i++) {
            $('#distribution_dd_menu').append('<div class="item" data-value="'+i.toString()+'">'+i.toString()+'</div>');
        }

        $('#default_dd').dropdown({
            onChange: function (val) {
                default_var = val;
            }
        }); 

        $('#distribution_dd').dropdown({
            onChange: function (val) {
                distr_var = val;
            }
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

    ///// user clicked "new experiment" button
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

    // user added an item
    $("#add_item_btn").click(function()   {
        var var_name = $("#var_name_input").val();
        if (distr_var == "" || distr_var == "" || var_name == "") {
            alert("please do not leave empty fields when inputting an independent variable");
            return;
        }

        var item = [var_name, distr_var, default_var];
        variables.push(item);
        update_list();

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

<<<<<<< HEAD
    build_variable_input_form();
    //$('.ui.dropdown').dropdown();
;
=======
	$("#foo").click(function() {
		$.get( "/foobar", function( data ) {
			// $("#chart").html( data );
                        console.log(data);
                        eval(data);
			alert( "Load was performed." );
		});
	});

>>>>>>> 7eefd1e4a526e42709034aec4a7cca2ffea0946d
/*
    $('#init_round_btn').click(function()   {
        var phrase_to_guess = $('input[name=phrase_to_guess]').val();
        $('input[name=phrase_to_guess]').val('');
        if (phrase_to_guess.length < 3) {
            alert("Your phrase should be at least 3 characters long!");
            return;
        }
        start_round_2(phrase_to_guess.toUpperCase());
    });

    $(document).on('click','.letter', function()  {
        var guess = $(this).val().toUpperCase();
        take_guess(guess);
        $(this).hide();
    });

    $('#play_again_yes').click(function()    {
        console.log('boogers');
        $('#new_round').fadeOut('slow');
        ctx.clearRect(0,0,canvas_w,canvas_h);
        show_buttons();
        round = start_round_1();
    });

    $('#play_again_no').click(function()    {
        $('#new_round').fadeOut('slow');
        $('#mandy_points').html("Mandy got: " + points["Mandy"] + " points");
        $('#deedee_points').html("Deedee got: " + points["Deedee"] + " points");
        $('#game_over').show();
    });

    // to do: implement round_lost()
    function round_lost()    {
        alert(round.host + " won!");
        round.curr_array = round.answer_array;
        points[round.host] += 1;
        draw();
        $('#title').html("You didn't save " + round.friend_name + " :(");
        round_over();
    };

    function round_won()    {
        alert(round.guesser + " won! " + round.friend_name + " has been saved!");
        $('#title').html("You saved " + round.friend_name + "!");
        points[round.guesser] += 1;
        draw();
        round_over();
    };

    function round_over()   {
        $('img').attr("src",round.friend_gif);
        $("#guess_ui").fadeOut('slow');
        $("#new_round").show();
        // you get more points for doing this better, but this will work
        //$('#wrong_guesses').html("");
        round = {};
    };

    // returns true if game is over, false if game is still on!
    function wrong_guess(guess) {
        round.wrong_guesses.push(guess);
        //$('#wrong_guesses').html(array_to_str(round.wrong_guesses));
        round.num_wrong++;
        if (round.num_wrong >= 6)   {
            round_lost();
            return true;
        }
        return false;
    };

    function take_guess(guess)  {
        if (already_guessed(guess)) {
            alert("You already guessed this letter!");
            return;
        }

        round.guesses.push(guess);
        var ans = round.answer_array;
        var correct = false;
        for (var i = 0; i < ans.length; i++)    {
            if (ans[i] === guess)   {
                correct = true;
                round.curr_array[i] = guess;
            }
        }

        if (!correct)   {
            // if game is over
            if (wrong_guess(guess)) {
                return;
            }
            draw();
        }
        else    {
            if (has_won())    {
                round_won();
                return;
            }
        }

        draw();
    };

    /////// gameplay functions ///////

    function start_round_1()  {
        var g = Math.floor(Math.random()*2);
        // 0 for Mandy, 1 for Deedee

        var f = Math.floor(Math.random()*8);

        var r = {
            guesser: g === 0 ? "Mandy" : "Deedee",
            host: g !== 0 ? "Mandy" : "Deedee",
            num_wrong: 0,
            wrong_guesses: [],
            guesses: [],
            friend_img: all_friends[f],
            friend_name: friends_names[f],
            friend_gif: f_gifs[f]
        };

        var dir_text = r.guesser + ", look away while ";
        dir_text += r.host + " enters a phrase.";
        $('#init_round_dir').html(dir_text);
        $('#init_round').show();

        return r;
    }

    function start_round_2(phrase)    {
        $('#init_round').fadeOut('slow');
        $('#guess_ui').fadeIn('slow');
        var dir_text = round.guesser + ', please guess a letter!';
        $('#guess_dir').html(dir_text);
        $('#title').html('You got to save ' + round.friend_name + '!');
        init_phrase_arrays(phrase);
        draw();
    }

    function show_buttons() {
        alpha = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','R','S','T','U','V','W','X','Y','Z']
        for (var i=0; i < 26; i++)  {
            $('#'+alpha[i]).show();
        }
    }

    */
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

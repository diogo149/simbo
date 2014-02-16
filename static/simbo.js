$(document).ready(function()    {


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



	$("#foo").click(function() {
		$.get( "/foobar", function( data ) {
			$("#chart").html( data );
			alert( "Load was performed." );
		});
	});

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

*/




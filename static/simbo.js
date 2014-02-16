/*
0: ginger
1: kuda
2: manda
3: misty
4: pandoo
5: perdy
6: oscar
7: spot
*/

$(document).ready(function()    {

    /**** initializing the game ****/
    function populate_friend_images()    {
        // Add your JavaScript below!
        var ginger_img = [];
        var kuda_img = [];
        var manda_img = [];
        var misty_img = [];
        var oscar_img = [];
        var pandoo_img = [];
        var perdy_img = [];
        var spot_img = [];

        ginger_img[0] = "http://s6.postimg.org/9ujhhp0n5/ginny_1.png";
        ginger_img[1] = "http://s6.postimg.org/o2966cdc1/ginny_2.png";
        ginger_img[2] = "http://s6.postimg.org/6sxalhcw1/ginny_3.png";
        ginger_img[3] = "http://s6.postimg.org/yqcx56nb5/ginny_4.png";
        ginger_img[4] = "http://s6.postimg.org/h1prrb0xt/ginny_5.png";
        ginger_img[5] = "http://s6.postimg.org/a11ryiz5t/ginny_6.png";

        kuda_img[0] = "http://s6.postimg.org/ebgfu448x/kuda_1.png";
        kuda_img[1] = "http://s6.postimg.org/qelrhofb5/kuda_2.png";
        kuda_img[2] = "http://s6.postimg.org/81l6744u9/kuda_3.png";
        kuda_img[3] = "http://s6.postimg.org/s7oo600ht/kuda_4.png";
        kuda_img[4] = "http://s6.postimg.org/ynxmw391d/kuda_5.png";
        kuda_img[5] = "http://s6.postimg.org/47rpxyni9/kuda_6.png";

        manda_img[0] = "http://s6.postimg.org/evvgwsxhd/manda_1.png";
        manda_img[1] = "http://s6.postimg.org/uk1q0pjep/manda_2.png";
        manda_img[2] = "http://s6.postimg.org/7ssneaydd/manda_3.png";
        manda_img[3] = "http://s6.postimg.org/9offpgn7l/manda_4.png";
        manda_img[4] = "http://s6.postimg.org/4zzfu9y0x/manda_5.png";
        manda_img[5] = "http://s6.postimg.org/f14a3lb41/manda_6.png";

        misty_img[0] = "http://s6.postimg.org/epmtqtuo1/misty_1.png";
        misty_img[1] = "http://s6.postimg.org/q5t8ov8u9/misty_2.png";
        misty_img[2] = "http://s6.postimg.org/yya7cjtz5/misty_3.png";
        misty_img[3] = "http://s6.postimg.org/symg8w96p/misty_4.png";
        misty_img[4] = "http://s6.postimg.org/j59u9twg1/misty_5.png";
        misty_img[5] = "http://s6.postimg.org/xn2g42ydd/misty_6.png";

        oscar_img[0] = "http://s6.postimg.org/3xtuph4ld/oscar_1.png";
        oscar_img[1] = "http://s6.postimg.org/7ipq8p94x/oscar_2.png";
        oscar_img[2] = "http://s6.postimg.org/9bsmx0ubl/oscar_3.png";
        oscar_img[3] = "http://s6.postimg.org/dyyoyshoh/oscar_4.png";
        oscar_img[4] = "http://s6.postimg.org/lszak6phd/oscar_5.png";
        oscar_img[5] = "http://s6.postimg.org/giubsw58h/oscar_6.png";

        pandoo_img[0] = "http://s6.postimg.org/cnqxqbm2p/pandoo_1.png";
        pandoo_img[1] = "http://s6.postimg.org/wkwuza4xt/pandoo_2.png";
        pandoo_img[2] = "http://s6.postimg.org/kuixhwc5d/pandoo_3.png";
        pandoo_img[3] = "http://s6.postimg.org/c26k7yge9/pandoo_4.png";
        pandoo_img[4] = "http://s6.postimg.org/gdv5wynb5/pandoo_5.png";
        pandoo_img[5] = "http://s6.postimg.org/nskhpc96p/pandoo_6.png";

        perdy_img[0] = "http://s6.postimg.org/q8qwgxgn5/perdy_1.png";
        perdy_img[1] = "http://s6.postimg.org/maz1ds4g1/perdy_2.png";
        perdy_img[2] = "http://s6.postimg.org/sel7bfk3l/perdy_3.png";
        perdy_img[3] = "http://s6.postimg.org/3zczadl6p/perdy_4.png";
        perdy_img[4] = "http://s6.postimg.org/koef6ahs1/perdy_5.png";
        perdy_img[5] = "http://s6.postimg.org/d9p3dwvwh/perdy_6.png";

        spot_img[0] = "http://s6.postimg.org/3nqxjvfcx/spot_1.png";
        spot_img[1] = "http://s6.postimg.org/t935jq2kh/spot_2.png";
        spot_img[2] = "http://s6.postimg.org/opqwy7kox/spot_3.png";
        spot_img[3] = "http://s6.postimg.org/kcsdfsby9/spot_4.png";
        spot_img[4] = "http://s6.postimg.org/ausmfqq9t/spot_5.png";
        spot_img[5] = "http://s6.postimg.org/axci2ktxd/spot_6.png";

        friends_img = [];
        friends_img[0] = ginger_img;
        friends_img[1] = kuda_img;
        friends_img[2] = manda_img;
        friends_img[3] = misty_img;
        friends_img[4] = oscar_img;
        friends_img[5] = pandoo_img;
        friends_img[6] = perdy_img;
        friends_img[7] = spot_img;

        return friends_img;
    };
    function get_friends_names()    {
        var friends = [];
        friends[0] = "Ginger";
        friends[1] = "Kuda";
        friends[2] = "Manda";
        friends[3] = "Misty";
        friends[4] = "Oscar";
        friends[5] = "Pandoo";
        friends[6] = "Perdy";
        friends[7] = "Spot";
        
        return friends;
    };
    function get_friends_gifs()    {
        var friends = [];
        friends[0] = "http://s6.postimg.org/ddxm253ep/ginny.gif";
        friends[1] = "http://s6.postimg.org/6wjawdif5/kuda.gif";
        friends[2] = "http://s6.postimg.org/yes90swap/manda.gif";
        friends[3] = "http://s6.postimg.org/teq7f41a9/misty.gif";
        friends[4] = "http://s6.postimg.org/v598glitd/oscar.gif";
        friends[5] = "http://s6.postimg.org/uz04r8z29/pandoo.gif";
        friends[6] = "http://s6.postimg.org/qnbj28s5d/perdy.gif";
        friends[7] = "http://s6.postimg.org/z6ux000ht/spot.gif";
        
        return friends;
    };
    
    var ctx = $('canvas')[0].getContext("2d");
    var canvas_h = 500;
    var canvas_w = 1000;
    var all_friends = populate_friend_images();
    var friends_names = get_friends_names();
    var round = {};
    var points = {"Deedee": 0, "Mandy": 0};
    var f_gifs = get_friends_gifs();

    /**** helper functions ****/
    
    // transforms the current array to the string to be displayed on the screen
    function get_display_phrase()   {
        var display_phrase = "";
        var curr_phrase = round.curr_array;
        for (var i = 0; i < curr_phrase.length; i++)    {
            if (curr_phrase[i] === "_") {
                display_phrase += "__ ";
            }
            else if (curr_phrase[i] === " ")    {
                display_phrase += "    ";
            }
            else    {
                display_phrase += curr_phrase[i] + "  ";
            }
        }

        display_phrase.trim();
        return display_phrase;
    };
    
    /* initializes current array (curr_array) in round
       to be an array of the answers characters with all alpha
       characters replaced with underscores */
    function init_phrase_arrays(phrase)    {
        var display_arr = [];
        var answer_arr = [];
        for (var i=0; i < phrase.length; i++)   {
            if (phrase.charAt(i).match(/[A-Z]/))    {
                display_arr[i] = "_";                
            }
            else    {
                display_arr[i] = phrase.charAt(i);
            }
            answer_arr[i] = phrase.charAt(i);
        }
        
        round.curr_array = display_arr;
        round.answer_array = answer_arr;
    };
    
    function array_to_str(arr)    {
        var str = "";
        for (var i=0; i < arr.length; i++)  {
            str += arr[i] + ", ";
        }
    
        return str.trim();
    };

    function has_won()  {
        for (var i = 0; i < round.curr_array.length; i++) {
            if (round.curr_array[i] === "_")    {
                return false;  
            }                          
        }

        return true;
    };

    function already_guessed(guess) {
        var g = round.guesses;
        for (var i = 0; i < g.length; i++)  {
            if (g[i] === guess)
                return true;
        }

        return false;
    };

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

    /**** drawing functions ****/
    function draw() {
        ctx.clearRect(0,0,canvas_w,canvas_h);
        draw_phrase();
        draw_board();
        draw_friend();
    };

    function draw_phrase()     {        
        display_phrase = get_display_phrase();
        if (round.curr_array.length > 10) {
            ctx.font = '20px Consolas';
        }
        else    {
            ctx.font = '30px Consolas';
        }
        ctx.fillStyle = '#354458';        
        ctx.fillText(display_phrase,400,175);
    };

    function draw_board()   {
        var fraction_str = 'you have ' + round.num_wrong + '/6 more tries';
        ctx.font = '30px Consolas';
        ctx.fillStyle = '#354458';
        ctx.fillText(fraction_str,400,300);
    };

    function draw_friend() {
        var num = round.num_wrong;
        if (num === 0)  {
            return;
        }

        var img = new Image();
        img.onload = function(){
        ctx.drawImage(img,10,10);
        };
        img.src = round.friend_img[num-1];
    }
    
    /**** gameplay functions ****/
    
    function start_round_1()  {
        /*** pick player to guess ***/
        var g = Math.floor(Math.random()*2);
        // 0 for Mandy, 1 for Deedee
        
        /*** pick friend to save ***/
        var f = Math.floor(Math.random()*8);
    
        /*** pack round info into an object ***/
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
        
        /*** set up round initialization ***/
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

    $('#init_game_btn').click(function()    {
        $('#init_game').fadeOut('slow');
        round = start_round_1();
    });

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
});


/* all the id's

init_game = the div for starting the game
init_game_dir = the directions for starting the game
init_game_btn = the button to start the game!

init_round = the div for initializing a round
init_round_dir = the directions for starting a round
init_round_btn = the button to start the round with the phrase to guess


to do (more important things first):
    {T} figure out why errors are happening!
    { } draw hanging thingy
    {+} write intro directions
    {+} make game over div
    {+} make new round option
    {+} implement scoring
    {+} either:
        - implement 'buttons' for guessing letter
        - add input checks
            - empty guess input when starting new round
    {+} when lost, display word
    { } figure out placement
    { } general code clean
    {+} implement winning
    {+} use friends names
    {+} implement checking for empty entrys

    
    {+} improve css:
        - buttons
        - colors
        - general info showing
    { } display wrong guesses better (perhaps through buttons)
    { } no flicker
    { } keep track of number of rounds
    
*/




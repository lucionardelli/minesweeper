<?php
    require "minesweeper.php";
    
    $ms = new Minesweeper();
    //$ms->get_all_games();
    $ms->login('minesweeper','TryNotExplode');
    $ms->new_game(9, 9, 10);
    print_r($ms->play(1, 1));
?>

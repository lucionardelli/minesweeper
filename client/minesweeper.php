<?php
class Minesweeper {
    public $host = 'https://ln-minesweeper-api.herokuapp.com/';
    private $base_path = '/api/';
    private $game = -1;
    private $token = "";

    public $response;
    public $error;

    private function curl_call($endpoint,  $method, $args=array())
    {
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $this->host . $this->base_path . $endpoint);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

        if ($this->token != '') {
            curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json',
                                                'Authorization: JWT '.$this->token)
            );
        }
        else {
            curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));
        }

        if ($method == 'POST') {
            curl_setopt($ch, CURLOPT_POST, 1);
        } else {
            curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $method);
        }
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($args));

        $resp = (array) json_decode(curl_exec($ch));
        curl_close ($ch);

        return $resp;
    }

    function login($username, $password)
    {
        $this->token = $this->curl_call("auth/login/", "POST",
                array("username" => $username,
                  "password" => $password))['token'];
        return $this->token;
    }   


    function set_host($host) {
        $this->host = $host;
    }

    function new_game($rows, $cols, $mines) {
        $resp = $this->curl_call("minesweeper/", "POST",
            array("rows" => $rows,
                  "columns" => $cols,
                  "mines" => $mines));
        $this->response = $resp;
        $this->game = $resp["id"];
        return $resp["id"];
    }

    function get_all_games() {
        $resp = $this->curl_call("minesweeper/", "GET");
        $this->response = $resp;
    }

    function get_game($id) {
        $resp = $this->curl_call("minesweeper/", "GET",
            array("id" => $id));
        $this->response = $resp;
        $this->game = $id;
    }

    function play($row, $col, $flag=false) {

        if ($this->game <= 0) {
            throw new Exception("Game not selected. Call `get_game` or `new_game`.");
        }
        $endpoint = "minesweeper/" . $this->game . '/';
        $resp = $this->curl_call($endpoint, "PUT",
            array("column" => $col,
                  "row" => $row));
        $this->response = $resp;
        return $resp;
    }
}
?>

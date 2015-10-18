<?php
# RPEDIRC.php by Tisane, http://www.mediawiki.org/wiki/User:Tisane
#
# This script is free software that is available under the terms of the Creative Commons
# Attribution 3.0 license and the current version of the GNU General Public License.
#
# The purpose of this script is to get the titles of all new, moved, deleted and restored
# pages from #en.wikipedia and add/delete them from the rped_table.

error_reporting( E_ALL | E_STRICT );

include 'wikibot.classes.php'; /* The wikipedia classes. */

$bot = $argv[1];
$wiki = $argv[2];
if ( !isset( $argv[3] ) || $argv[3] != "nodaemon" ){
    $daemonize = true;
}

$wpapi	= new wikipediaapi ( '', '', '', $bot, $wiki, true );
$wpq	= new wikipediaquery ( '', '', '', $bot, $wiki, true );
$wpi	= new wikipediaindex ( '', '', '', $bot, $wiki, true );
$user = getWikibotSetting( 'user', $bot, $wiki );
$pass = getWikibotSetting( 'pass', $bot, $wiki );
$host = getWikibotSetting( 'host', $bot, $wiki );
$port = getWikibotSetting( 'port', $bot, $wiki );
$nick = getWikibotSetting( 'nick', $bot, $wiki );
$ident = getWikibotSetting( 'ident', $bot, $wiki );
$realname = getWikibotSetting( 'realname', $bot, $wiki );
$chan = getWikibotSetting( 'chan', $bot, $wiki );
$deleteLine = getWikibotSetting( 'deleteline', $bot, $wiki );
$moveLine = getWikibotSetting( 'moveline', $bot, $wiki );
$deletedWord = getWikibotSetting( 'deletedword', $bot, $wiki );
$newCharacter = getWikibotSetting( 'thenewcharacter', $bot, $wiki );

if ( $wpapi->login( $user, $pass ) != 'true' ) {
    echo "Login failure\n";
    die();
}

$readbuffer = "";
$startSep = "[[";
$endSep = "]]";

// open a socket connection to the IRC server
$fp = fsockopen( $host, $port, $erno, $errstr, 30 );

// print the error if there is no connection
if ( !$fp ) {
    echo $errstr . " (" . $errno . ")<br />\n";
    die();
}

// write data through the socket to join the channel
fwrite( $fp, "NICK " . $nick . "\r\n" );
fwrite( $fp, "USER " . $ident . " " . $host . " bla :" . $realname . "\r\n" );
fwrite( $fp, "JOIN :" . $chan . "\r\n" );

# Launch daemon!
if ( isset( $daemonize ) ) {

    $pid = pcntl_fork(); // fork
    if ( $pid < 0 ) {
        exit;
    }
    else if ( $pid ){ // parent
        exit;
    }
    // child
    $sid = posix_setsid();
    if ( $sid < 0 ) {
            exit;
    }
}

while ( !feof( $fp ) ) {
    $line =  fgets( $fp, 512 );
    $pingLine = explode( ' ', $line );
    if ( strtolower( $pingLine[0] ) == 'ping' ) {
        $response = "PONG " . $pingLine[1] . "\n";
        fwrite( $fp, "PONG " . $response );
    }
    usleep( 10 );
    $startPos = strpos( $line, $startSep );
    $endPos = strpos( $line, $endSep );
    $subLine = substr( $line, $startPos + 5, $endPos -$startPos -8 );
    if ( $subLine == $deleteLine ) {
        $delstartPos = strpos( $line, $startSep, $endPos );
        $delendPos = strpos( $line, $endSep, $endPos + 1 );
        $delLine = substr( $line, $delstartPos + 5, $delendPos -$delstartPos -8 );
        $action = substr( $line, $delstartPos -9, 7 );
        if ( $action == $deletedWord ) {
            $wpapi->rpedDelete( $delLine );
        } else {
            $wpapi->rpedInsert( $delLine );
        }
    }
    if ( $subLine == $moveLine ) {
        $delstartPos = strpos( $line, $startSep, $endPos );
        $delendPos = strpos( $line, $endSep, $endPos + 1 );
        $delstartPos = strpos( $line, $startSep, $delstartPos + 1 );
        $delendPos = strpos( $line, $endSep, $delendPos + 1 );
        $delLine = substr( $line, $delstartPos + 2, $delendPos -$delstartPos -2 );
        $wpapi->rpedInsert( $delLine );
    }
    if ( substr( $line, $endPos + 5, 1 ) == $newCharacter || substr( $line, $endPos + 6, 1 ) == $newCharacter ) {
        $wpapi->rpedInsert( $subLine );
    }
}

fclose( $fp );
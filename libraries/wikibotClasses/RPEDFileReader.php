<?php
# RPEDFileReader.php by Tisane, http://www.mediawiki.org/wiki/User:Tisane
#
# This script is free software that is available under the terms of the Creative Commons
# Attribution-ShareAlike 3.0 license and the current version of the GNU General Public License.
#
# The purpose of this script is to read a text file (specifically, the list of page titles from
# Wikipedia's data dump) and add each page title to a database table.

error_reporting( E_ALL | E_STRICT );
include 'wikibot.classes.php'; /* The wikipedia classes. */

$bot = $argv[1];
$wiki = $argv[2];
$fileName = $argv[3];
$searching = false;
if ( isset( $argv[4] ) && $argv[4] != '' ) {
    $searching = true;
}
if ( !isset( $argv[5] ) || $argv[5] != "nodaemon" ) {
    $daemonize = true;
}

$user = getWikibotSetting( 'user', $bot, $wiki );
$pass = getWikibotSetting( 'pass', $bot, $wiki );
$maxURLLength = getWikibotSetting( 'maxurllength', $bot, $wiki );

$wpapi	= new wikipediaapi ( '', '', '', $bot, $wiki, true );
$wpq	= new wikipediaquery ( '', '', '', $bot, $wiki, true );
$wpi	= new wikipediaindex ( '', '', '', $bot, $wiki, true );
if ( $wpapi->login( $user, $pass ) != 'true' ) {
    echo "Login failure\n";
    die();
}

$handle = @fopen( $fileName, "r" );
$lineNumber = 0;
$line = "";

if ( isset( $daemonize ) ) {

    $pid = pcntl_fork(); // fork
    if ( $pid < 0 ) {
        exit;
    }
    else if ( $pid ) { // parent
        exit;
    }
    // child
    $sid = posix_setsid();
    if ( $sid < 0 ) {
            exit;
    }
}
     
if ( $handle ) {
    while ( !feof( $handle ) ) {
        $buffer = fgets( $handle, 4096 );
        $buffer = str_replace( "\n", "", $buffer );
        if ( $searching == true ) {
            if ( $buffer == $argv[4] ) {
                $searching = false;
            }
        } else {
            $buffer = urlencode  (  $buffer  );
            if ( $line != "" ) {
                $line .= "|";
            }
            if ( strlen( $line ) + strlen( $buffer ) > $maxURLLength ) {
                $wpapi->rpedInsert( $line );
                $line = "";
            }
            $line .= $buffer;
        }
    }
    $wpapi->rpedInsert( $line );
    fclose( $handle );
} else {
    echo "No handle!\n";
}

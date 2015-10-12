#!/usr/bin/php
<?php

/* EXTERNAL DEPENDENCIES *****************************************************/

set_include_path(get_include_path().PATH_SEPARATOR.realpath('./Console_CommandLine/'));
require_once 'Console/CommandLine.php';


/* BACKWARDS COMPATIBILITY ***************************************************/

if (PHP_VERSION_ID < 50400) {	
	// Define these constants, so that they are not undefined
	define('JSON_PRETTY_PRINT',			0);
	define('JSON_UNESCAPED_SLASHES',	0);
}

define('VERSION', '0.32.5');


/* CONSOLE INTERFACE *********************************************************/

$parser = new Console_CommandLine();
$parser->description =
	"The module reads LaTaLa files for all languages from '101results/101repo/".FindLanguages::ROOT_LANG_DIR_NAME."' "
	."(In this manner, geshi ids and file extensions are looked up for all languages.) "
	."The module writes '".FindLanguages::OUTPUT_FILE."' files for all contributions to '101results/".FindLanguages::ROOT_CONTR_DIR_NAME."/' "
	."The generated json files associate language names as keys with file names and additional metadata as values.";

$parser->version = VERSION;
$parser->addOption('empty', array(
		'short_name'		=> '-e',
		'long_name'			=> '--empty',
		'description'		=> 'determines how to behave with empty output files',
		'action'			=> 'StoreString',
		'choices'			=> array('NO_NEW', 'CREATE', 'DELETE'),
		'add_list_option'	=> true
	));

$parser->addOption('stats', array(
		'short_name'		=> '-s',
		'long_name'			=> '--stats',
		'description'		=> "create a statistics file in actual directory with all languages",
		'action'			=> 'StoreTrue'
	));

$parser->addOption('quiet', array(
		'short_name'		=> '-q',
		'long_name'			=> '--quiet',
		'description'		=> "don't print status messages to stdout",
		'action'			=> 'StoreTrue'
	));


try {
	$result = $parser->parse();
	
	switch ($result->options['empty']) {
		case 'NO_NEW': FindLanguages::$emptyFileBehaviour = FindLanguages::NO_NEW_EMPTY_FILES; break;
		case 'CREATE': FindLanguages::$emptyFileBehaviour = FindLanguages::CREATE_EMPTY_FILES; break;
		case 'DELETE': FindLanguages::$emptyFileBehaviour = FindLanguages::DELETE_EMPTY_FILES; break;
	}
	
	FindLanguages::$beQuiet			= $result->options['quiet'];
	FindLanguages::$createStatFile	= $result->options['stats'];
	
	if (!FindLanguages::$beQuiet) {
		FindLanguages::log(
				"Backwards compatibility is active!"
				."Sorry, there will be '\/' instead of '/'"
				."and no pretty-print in JSON.\n\n"
			);
	}
} catch (Exception $exc) {
	$parser->displayError($exc->getMessage());
	exit(1);
}


/* JOB RUNNING ***************************************************************/

try {
	$job = new FindLanguages('../../../101repo');
	$job->run();
} catch (Exception $e) {
	FindLanguages::log($e->getMessage());
	exit(1);
}


/* JOB DEFINITION ************************************************************/

class FindLanguages {
	
	/* CONSTANTS AND STATIC FIELDS *******************************************/
	
	const ROOT_LANG_DIR_NAME	= 'languages';			// Relative path to languages
	const ROOT_CONTR_DIR_NAME	= 'contributions';		// Relative path to contributions
	const LATALA_FILE			= '.latala';			// File name format of LaTaLa files (placeholders: ":name" for the parent directory)
	const OUTPUT_FILE			= 'languages.json';		// File name of output files
	const OUTPUT_PATH			= '../101results';		// Relative path to 101 results
	
	// Flags for $emptyFileBehaviour
	const FLAG_CREATE = 1;
	const FLAG_DELETE = 2;
	
	// Enumeration for $emptyFileBehaviour = combinations from FLAG_CREATE and FLAG_DELETE
	const NO_NEW_EMPTY_FILES	= 0;					// Create no new empty files
	const CREATE_EMPTY_FILES	= 1;					// Create empty files
	const DELETE_EMPTY_FILES	= 2;					// Delete already existing files and create no new files
	
	// How to behave with empty languages.json files?
	public static $emptyFileBehaviour	= self::NO_NEW_EMPTY_FILES;
	
	// Can be set to true for quiet mode
	public static $beQuiet				= false;
	
	// Can be set to true to create a statistics file
	public static $createStatFile		= false;
	
	// Used to skip version system directories
	public static $skipFiles	= array('.git', '.svn', '.cvs');
	
	// Options for json_encode. These require PHP Version >= 5.4.0.
	public static $jsonEncodeDefaultOptions	= array(JSON_PRETTY_PRINT, JSON_UNESCAPED_SLASHES);
	
	
	/* FIELDS ****************************************************************/
	
	private $rootPath;
	private $outputPath;
	private $rootLanguagesPath;
	private $rootContributionsPath;
	private $jsonEncodeOptions = 0;
	private $languages;
	
	
	/* INSTANCE METHODS ******************************************************/
	
	public function __construct($rootPath) {
		$this->rootPath					= realpath($rootPath);
		$this->rootLanguagesPath		= realpath($this->rootPath.DIRECTORY_SEPARATOR.self::ROOT_LANG_DIR_NAME);
		$this->rootContributionsPath	= realpath($this->rootPath.DIRECTORY_SEPARATOR.self::ROOT_CONTR_DIR_NAME);
		$this->outputPath				= realpath($this->rootPath.DIRECTORY_SEPARATOR.self::OUTPUT_PATH);
		$this->validatePaths();
		
		// This must be done at runtime. PHP doesn't support such things "statically". >:|
		foreach (self::$jsonEncodeDefaultOptions as $option) {
			$this->jsonEncodeOptions |= $option;
		}
	}
	
	/**
	 * Executes prevalidation checks on paths
	 *
	 */
	protected function validatePaths() {	
		if (!is_dir($this->rootPath)) {
			throw new Exception("Invalid path to 101repo! (".$this->rootPath.")\n");
		}
		
		if (!is_dir($this->rootLanguagesPath)) {
			throw new Exception("Invalid path to languages! (".$this->rootLanguagesPath.")\n");
		}
		
		if (!is_dir($this->rootContributionsPath)) {
			throw new Exception("Invalid path to contributions! (".$this->rootContributionsPath.")\\n");
		}
		
		if (empty($this->outputPath) || !is_dir($this->outputPath)) {
			// If path is empty or doesn't exist, try to create it
			$relativePath = $this->rootPath.DIRECTORY_SEPARATOR.self::OUTPUT_PATH;
			mkdir($relativePath);
			$this->outputPath = realpath($relativePath);
			
			if (!is_dir($this->outputPath)) {
				throw new Exception("Can't createa path to 101results! (".$this->outputPath.")\n");
			}
		}
		
		$contrOutputPath = $this->outputPath.DIRECTORY_SEPARATOR.self::ROOT_CONTR_DIR_NAME;
		if (!is_dir($contrOutputPath)) {
			mkdir($contrOutputPath);
			
			if (!is_dir($contrOutputPath)) {
				throw new Exception("Can't create path to 101results/contributions! (".$contrOutputPath.")\n");
			}
		}
	}
	
	
	/**
	 * Runs this job and searches for languages, and creates or replaces
	 * listing files in the contributions.
	 *
	 */
	public function run() {
		self::log("Reading languages from dir ".$this->rootLanguagesPath."\n");
		$this->languages = self::readLanguages($this->rootLanguagesPath);
		
		if (empty($this->languages)) {
			self::log("Found no languages."."\n");
			return;
		}
		
		// Initialize vars to be used in the anonymous function
		$self				= $this;
		$extensions			= array_keys($this->languages);
		$completeJsonArray	= array();
		
		self::log("\nReading contributions from dir ".$this->rootContributionsPath."\n");
		self::discoverDir(
				$this->rootContributionsPath,
				true,
				function($dirName, $path) use ($self, &$extensions, &$completeJsonArray) {
					// Discover all files of the contribution
					$filesByExt = FindLanguages::getFilesByExtensions($path, $path, $extensions);
					
					// Restructure the array and save it as JSON
					$jsonArray	= $self->restructure($filesByExt);
					$self->saveOutput($dirName, $jsonArray);
					
					if (FindLanguages::$createStatFile) {
						$completeJsonArray[$dirName] = $jsonArray;
					}
				});
		
		if (self::$createStatFile) {
			// Save a complete file for statistics and debugging
			$statPath = $this->outputPath.DIRECTORY_SEPARATOR.FindLanguages::OUTPUT_FILE;
			file_put_contents($statPath, json_encode($completeJsonArray, $this->jsonEncodeOptions));
		}
	}
	
	/**
	 * Restructure the data for the output
	 * 
	 * @param filesByExt	an two-dimensional array with files by extension
	 * @return array		in output format
	 */
	public function restructure($filesByExt) {
		$jsonArray = array();
		
		foreach ($filesByExt as $ext => $files) {
			$key = $this->languages[$ext]['name'];
			
			// Merge files and extensions values
			if ($jsonArray[$key] == null) {
				$jsonArray[$key]['extension']	= $this->languages[$ext]['extension'];
				$jsonArray[$key]['files']		= $files;
			} else {
				$jsonArray[$key]['extension']	= array_merge($jsonArray[$key]['extension'],	$this->languages[$ext]['extension']);
				$jsonArray[$key]['files']		= array_merge($jsonArray[$key]['files'],		$files);
			}
			
			// Overwrite geshi value
			$jsonArray[$key]['geshi'] = $this->languages[$ext]['geshi'];
		}
		
		return $jsonArray;
	}
	
	/**
	 * Save an array as JSON to a contributions output path
	 *
	 * @param dirName	- name of the directory in contributions
	 * @param content	- an array which will be encoded as JSON
	 */
	public function saveOutput($dirName, $content) {
		$outputFilePath = implode(
				DIRECTORY_SEPARATOR,
				array(
					$this->outputPath,
					self::ROOT_CONTR_DIR_NAME,
					$dirName, 
					self::OUTPUT_FILE,
				)
			);
		
		// Ensure that the directory exists
		if (!is_dir(dirname($outputFilePath))) {
			mkdir(dirname($outputFilePath));
		}
		
		if (empty($content) && (self::$emptyFileBehaviour & self::FLAG_CREATE) == 0) {
			// Don't create empty files
			if ((self::$emptyFileBehaviour & self::FLAG_DELETE) > 0) {
				// Don't let empty files exist
				if (file_exists($outputFilePath)) {
					// So delete existing files
					@unlink($outputFilePath);
					
					self::log(
							"\t Deleted ".self::OUTPUT_FILE
							." because of no matchings for contribution: "
							.$dirName."\n"
						);
				}
			}
		} else {
			if (empty($content)) {
				// Enforces empty object JSON encoding
				$content = new stdClass();
			}
			
			file_put_contents($outputFilePath, json_encode($content, $this->jsonEncodeOptions));
			
			self::log(
					"\t Created ".self::OUTPUT_FILE." for contribution: "
					.$dirName."\n"
				);
		}
	}
	
	
	/**
	 * Logs a message, which will be echoed if there should be output
	 *
	 */
	public static function log($msg) {
		if (!self::$beQuiet) echo $msg;
	}
	
	
	/**
	 * Read a directory, which contains language sub directories,
	 * which again contains LaTaLa-files
	 * 
	 * @param dirName	directoryName
	 * @return array of languages
	 */
	protected function readLanguages($dirName) {	
		// Initialize empty result array
		$languages = array();
		
		// Discover all sub directories, which matches the naming schema
		self::discoverDir($dirName, true, function($fileName, $filePath) use ($dirName, &$languages) {
				//if (!preg_match('/^[A-Z].*$/', $fileName)) continue;
				
				// Initialize names and paths
				$languageName	= $fileName;
				$latalaName		= str_replace(':name', $languageName, FindLanguages::LATALA_FILE);
				$latalaPath		= $filePath.DIRECTORY_SEPARATOR.$latalaName;
				
				// Check for a LaTaLa-file
				FindLanguages::log("\tFound language '".$languageName."':\t");
				if (!file_exists($latalaPath)) {
					FindLanguages::log("[FAIL] missing ".$latalaName."\n");
					return;
				}
				
				FindLanguages::log("[SUCCESS] found ".$latalaName."\n");
				
				// Load, parse and restructure
				$latalaObject	= json_decode(file_get_contents($latalaPath));
				$latalaArray	= array(
						'name'		=> $languageName,
						'geshi'		=> (String) $latalaObject->geshi,
					);
				
				if (empty($latalaObject->extension)) {
					FindLanguages::log("[FAIL] missing field 'extension'!\n");
					return;
				}
				
				if (is_array($latalaObject->extension)) {
					$latalaArray['extension'] = array();
					foreach ($latalaObject->extension as $ext) {
						$latalaArray['extension'][] = $ext;
						$languages[$ext] = $latalaArray;
					}
				} else {
					$latalaArray['extension'] = (String) $latalaObject->extension;
					$languages[$latalaObject->extension] = $latalaArray;
				}
			});
		
		return $languages;
	}
	
	
	/* HELPER METHODS ********************************************************/
	
	/**
	 * Discover a directory and call a callback for
	 * each file, which would be found.
	 *
	 * @param $dirName	 	a directory name
	 * @param $onlyDirs		boolean flag to ignore files
	 * @param $callback		a function with the arguments $fileName and $filePath,
	 * 						which is called for each file in the directory
	 */
	public static function discoverDir($dirName, $onlyDirs, $callback) {
		$files = array();
		
		// Discover all sub directories
		$rootPath = opendir($dirName);
		while (($fileName = readdir($rootPath)) !== false) {			
			// Skip non relevant files
			if ($fileName == '.' || $fileName == '..') continue;
			if (in_array($fileName, self::$skipFiles)) continue;
			
			// Skip files if argument $onlyDirs is true
			$filePath = $dirName.DIRECTORY_SEPARATOR.$fileName;
			if ($onlyDirs && !is_dir($filePath)) continue;
			
			try {
				$callback($fileName, $filePath);
			} catch (Exception $e) {
				closedir($rootPath);
				throw $e;
			}
		}
		closedir($rootPath);
	}
	
	
	/**
	 * Discover a directory and search all files recursively, which have one
	 * of multiple extensions and list them in arrays by their extension.
	 * 
	 * @param @parent		a path to a directory
	 * @param $path			a  path to a file or a directory
	 * @param $extensions	an array with file extensions to scan for
	 * @param $files		an array, which is filled with files that was found
	 * @return the filled array $files
	 * 			e.g. { '.hs' => ['Cut.hs', 'Company.hs'], '.php' => [...], ... }
	 */
	public static function getFilesByExtensions($parent, $path, $extensions, &$files = array()) {
		if (is_dir($path)) {
			// We got a directory, so let's discover files in there recursively
			self::discoverDir($path, false, function($fileName, $filePath) use (&$parent, &$extensions, &$files) {
					FindLanguages::getFilesByExtensions($parent, $filePath, $extensions, $files);
				});
		} else {
			// We got a file, so get the extension
			$fileExt = '.'.pathinfo($path, PATHINFO_EXTENSION);
			
			// If we are interested in files, with this extension, ...
			if (in_array($fileExt, $extensions)) {
				// Make the $path relative to $parent and only use slashes!
				$relative = str_replace($parent.DIRECTORY_SEPARATOR, '', $path);
				$relative = str_replace('\\', '/', $relative);
				
				// ... put it at adequate place
				if (!is_array($files[$fileExt])) {
					$files[$fileExt] = array($relative);
				} else {
					$files[$fileExt][] = $relative;
				}
			}
		}
		
		return $files;
	}
	
}

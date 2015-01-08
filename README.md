# stringinfo
A modular tool that will provide you as much information about given string(s) as possible

This tool works using plugins, so you can easily add functionality. For now, the following plugins are available:

## BasicInfoPlugin
This plugin returns basic information about the given string(s), such as the length, the number of characters per character group, etc

## HashPlugin
This plugin compares the length of the given string(s) to a table of known CRC, Checksum and hash functions and determines whether the string might be the hex-result of one of those functions.

## XORPlugin
If the input contains all-hex strings, this plugin XOR's all input strings with eachother and prints the result as a hex string.

## DecodeHexPlugin
If the input contains all-hex strings, this plugin will try to decode the bytes using commonly used encodings. Control characters will be filtered from the result, to keep your terminal from breaking. If the resulting string without control characters is empty, or if the decoding failed, the result will be marked as <invalid>

## AlphabetPlugin
This plugin tries to map the input string(s) to the alphabet, bytewise. If the input string is a hex string, it will be converted to decimals first, also bytewise.
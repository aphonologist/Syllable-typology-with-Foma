This repo contains an implementation of finite-state syllabification in OT using Foma ([Hulden 2009](http://hdl.handle.net/10150/196112)).

The Python script iterates through all possible rankings of the constraints below (defined up to ten violations following [Karttunen 1998](https://aclanthology.org/W98-1301/))

* Mᴀx
* Dᴇᴘ
* Oɴsᴇᴛ
* NᴏCᴏᴅᴀ
* *CᴏᴍᴘʟᴇxOɴsᴇᴛ
* *CᴏᴍᴘʟᴇxCᴏᴅᴀ

generates the OT grammar in Foma, runs it (thanks to Jonathan North Washington for his help with the ``subprocess`` module), and collects the SRs for each of the URs

* v
* c
* cv
* vc
* vv
* cc
* cvc
* vcv
* ccvcc
* cvcvcv
* cvccvc

The Gᴇɴ function inserts and deletes consonants and vowels and creates syllables. Syllables contain exactly one vowel and do not contain any deleted segments.

For the script to run, Foma must be installed (run ``apt install foma``).

The output contains each language with its necessary rankings, e.g.,

> ('v', 'c', '[CV]', 'vc', 'vv', 'cc', '[CV]c', 'v[CV]', 'c[CV]cc', '[CV][CV][CV]', '[CV]c[CV]c')

> ComplexOnset>>ParseSeg

> Dep>>ParseSeg

> Max>>ParseSeg

> NoCoda>>ParseSeg

> Onset>>ParseSeg

Key to representations:

* C/c = underlying consonant
* V/v = underlying vowel
* k = deleted consonant
* w = deleted vowel
* Q/q = inserted consonant
* F/f = inserted vowel
* C/V/Q/F = syllabified segments
* c/v/q/f/k/w = unsyllabified segments
* [ = left boundary with simple onset
* < = left boundary without onset
* [{ = left boundary with complex onset
* ] = right boundary without coda
* > = right boundary with coda
* }> = right boundary with complex coda

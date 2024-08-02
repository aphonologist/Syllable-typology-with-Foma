This repo contains an implementation of finite-state syllabification in OT using Foma ([Hulden 2009](https://aclanthology.org/E09-2008/)).

The Python script iterates through all possible rankings of the constraints

* Max
* Dep
* Onset
* NoCoda
* *ComplexOnset
* *ComplexCoda

generates the Foma grammar and collects the SRs for each of the URs

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

For this script to run, Foma must be installed (run ``apt install foma``).

The output contains each language with its necessary rankings, e.g.,

> ('v', 'c', '[CV]', 'vc', 'vv', 'cc', '[CV]c', 'v[CV]', 'c[CV]cc', '[CV][CV][CV]', '[CV]c[CV]c')

> ComplexOnset>>ParseSeg

> Dep>>ParseSeg

> Max>>ParseSeg

> NoCoda>>ParseSeg

> Onset>>ParseSeg

Representations are explained in the Foma code; they are medium transparent.

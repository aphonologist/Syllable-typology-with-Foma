import subprocess
import re

GENCON = r"""#### GEN ####

### URs

# consonant = c
# vowel = v
define Input [c | v]* ;

### deletion

# deleted c = k
define deleteC "c" (->) "k" ;

# deleted v = w
define deleteV "v" (->) "w" ;

define DELETE deleteC .o. deleteV ;

### epenthesis

# inserted c = q
define insertQ [..] (->) "q" ;

# inserted v = f
define insertF [..] (->) "f" ;

define INSERT insertQ .o. insertF ;

### syllabification

## insert left and right syllable boundaries

# insert left syllable boundaries = [
define ParseL [..] (->) "[" ;

# insert right syllable boundaries = ]
define ParseR [..] (->) "]" ;

## clean up representation

# remove unmatched [
define cleanL "[" -> "" || _ [ \"]" ]* [ "[" | .#. ] ;

# remove unmatched ]
define cleanR "]" -> "" || [ "]" | .#. ] [ \"[" ]* _ ;

define CLEAN cleanL .o. cleanR ;

## mark syllabified segments

# syllabified segments are capitalized
define capitalizeC "c" -> "C" || "[" [\"]"]* _ [\"]"]* "]" ;
define capitalizeV "v" -> "V" || "[" [\"]"]* _ [\"]"]* "]" ;
define capitalizeQ "q" -> "Q" || "[" [\"]"]* _ [\"]"]* "]" ;
define capitalizeF "f" -> "F" || "[" [\"]"]* _ [\"]"]* "]" ;

define CAPITALIZE capitalizeC .o. capitalizeV .o. capitalizeQ .o. capitalizeF;

## constraints on syllabification in GEN

# syllables contain no more than one vowel
define oneVowel ~$[ "[" [ \"[" ]* ["V" | "F"] [ \"]" ]* ["V" | "F"] [ \"]" ]* "]" ] ;

# syllables contain at least one vowel
define requireNuc ~$[ "[" ["C" | "Q"]* "]" ] ;

# deleted segments are not syllabified
define noDelInside ~$[ "[" [\"]"*] ["w" | "k"] [\"]"*] "]"] ;

define WELLFORMED oneVowel .o. requireNuc .o. noDelInside ;

## mark up to simplify EVAL

# left edge of onsetless = <
define markOnsetless "[" -> "<" || _ ["V" | "F" ] ;

# right edge of closed = >
define markHasCoda "]" -> ">" || ["C" | "Q"] _ ;

# onset cluster = {
define markOnsetCluster [..] -> "{" || "[" _ ["C" | "Q"] ["C" | "Q"] ;

# coda cluster = }
define markCodaCluster [..] -> "}" || ["C" | "Q"] ["C" | "Q"] _ ">" ;

define MARK markOnsetless .o. markHasCoda .o. markOnsetCluster .o. markCodaCluster ;

define SYLLABIFY ParseL .o. ParseR .o. CLEAN .o. CAPITALIZE .o. WELLFORMED .o. MARK ;

define GEN Input .o. DELETE .o. INSERT .o. SYLLABIFY ;

#### CONSTRAINTS ####

# defined up to nine violations

## faithfulness

define Max1 ~$[ ["w"|"k"] ] ;
define Max2 ~$[ ["w"|"k"] ?* ["w"|"k"] ] ;
define Max3 ~$[ ["w"|"k"] ?* ["w"|"k"] ?* ["w"|"k"] ] ;
define Max4 ~$[ ["w"|"k"] ?* ["w"|"k"] ?* ["w"|"k"] ?* ["w"|"k"] ] ;
define Max5 ~$[ ["w"|"k"] ?* ["w"|"k"] ?* ["w"|"k"] ?* ["w"|"k"] ?* ["w"|"k"] ] ;
define Max6 ~$[ ["w"|"k"] ?* ["w"|"k"] ?* ["w"|"k"] ?* ["w"|"k"] ?* ["w"|"k"] ?* ["w"|"k"] ] ;
define Max7 ~$[ ["w"|"k"] ?* ["w"|"k"] ?* ["w"|"k"] ?* ["w"|"k"] ?* ["w"|"k"] ?* ["w"|"k"] ?* ["w"|"k"] ] ;
define Max8 ~$[ ["w"|"k"] ?* ["w"|"k"] ?* ["w"|"k"] ?* ["w"|"k"] ?* ["w"|"k"] ?* ["w"|"k"] ?* ["w"|"k"] ?* ["w"|"k"] ] ;
define Max9 ~$[ ["w"|"k"] ?* ["w"|"k"] ?* ["w"|"k"] ?* ["w"|"k"] ?* ["w"|"k"] ?* ["w"|"k"] ?* ["w"|"k"] ?* ["w"|"k"] ?* ["w"|"k"] ] ;

define Dep1 ~$[ ["F"|"f"|"Q"|"q"] ] ;
define Dep2 ~$[ ["F"|"f"|"Q"|"q"] ?* ["F"|"f"|"Q"|"q"] ] ;
define Dep3 ~$[ ["F"|"f"|"Q"|"q"] ?* ["F"|"f"|"Q"|"q"] ?* ["F"|"f"|"Q"|"q"] ] ;
define Dep4 ~$[ ["F"|"f"|"Q"|"q"] ?* ["F"|"f"|"Q"|"q"] ?* ["F"|"f"|"Q"|"q"] ?* ["F"|"f"|"Q"|"q"] ] ;
define Dep5 ~$[ ["F"|"f"|"Q"|"q"] ?* ["F"|"f"|"Q"|"q"] ?* ["F"|"f"|"Q"|"q"] ?* ["F"|"f"|"Q"|"q"] ?* ["F"|"f"|"Q"|"q"] ] ;
define Dep6 ~$[ ["F"|"f"|"Q"|"q"] ?* ["F"|"f"|"Q"|"q"] ?* ["F"|"f"|"Q"|"q"] ?* ["F"|"f"|"Q"|"q"] ?* ["F"|"f"|"Q"|"q"] ?* ["F"|"f"|"Q"|"q"] ] ;
define Dep7 ~$[ ["F"|"f"|"Q"|"q"] ?* ["F"|"f"|"Q"|"q"] ?* ["F"|"f"|"Q"|"q"] ?* ["F"|"f"|"Q"|"q"] ?* ["F"|"f"|"Q"|"q"] ?* ["F"|"f"|"Q"|"q"] ?* ["F"|"f"|"Q"|"q"] ] ;
define Dep8 ~$[ ["F"|"f"|"Q"|"q"] ?* ["F"|"f"|"Q"|"q"] ?* ["F"|"f"|"Q"|"q"] ?* ["F"|"f"|"Q"|"q"] ?* ["F"|"f"|"Q"|"q"] ?* ["F"|"f"|"Q"|"q"] ?* ["F"|"f"|"Q"|"q"] ?* ["F"|"f"|"Q"|"q"] ] ;
define Dep9 ~$[ ["F"|"f"|"Q"|"q"] ?* ["F"|"f"|"Q"|"q"] ?* ["F"|"f"|"Q"|"q"] ?* ["F"|"f"|"Q"|"q"] ?* ["F"|"f"|"Q"|"q"] ?* ["F"|"f"|"Q"|"q"] ?* ["F"|"f"|"Q"|"q"] ?* ["F"|"f"|"Q"|"q"] ?* ["F"|"f"|"Q"|"q"] ] ;

## phonotactic

define ParseSeg1 ~$[ ["q"|"f"|"c"|"v"] ];
define ParseSeg2 ~$[ ["q"|"f"|"c"|"v"] ?* ["q"|"f"|"c"|"v"] ];
define ParseSeg3 ~$[ ["q"|"f"|"c"|"v"] ?* ["q"|"f"|"c"|"v"] ?* ["q"|"f"|"c"|"v"] ];
define ParseSeg4 ~$[ ["q"|"f"|"c"|"v"] ?* ["q"|"f"|"c"|"v"] ?* ["q"|"f"|"c"|"v"] ?* ["q"|"f"|"c"|"v"] ];
define ParseSeg5 ~$[ ["q"|"f"|"c"|"v"] ?* ["q"|"f"|"c"|"v"] ?* ["q"|"f"|"c"|"v"] ?* ["q"|"f"|"c"|"v"] ?* ["q"|"f"|"c"|"v"] ];
define ParseSeg6 ~$[ ["q"|"f"|"c"|"v"] ?* ["q"|"f"|"c"|"v"] ?* ["q"|"f"|"c"|"v"] ?* ["q"|"f"|"c"|"v"] ?* ["q"|"f"|"c"|"v"] ?* ["q"|"f"|"c"|"v"] ];
define ParseSeg7 ~$[ ["q"|"f"|"c"|"v"] ?* ["q"|"f"|"c"|"v"] ?* ["q"|"f"|"c"|"v"] ?* ["q"|"f"|"c"|"v"] ?* ["q"|"f"|"c"|"v"] ?* ["q"|"f"|"c"|"v"] ?* ["q"|"f"|"c"|"v"] ];
define ParseSeg8 ~$[ ["q"|"f"|"c"|"v"] ?* ["q"|"f"|"c"|"v"] ?* ["q"|"f"|"c"|"v"] ?* ["q"|"f"|"c"|"v"] ?* ["q"|"f"|"c"|"v"] ?* ["q"|"f"|"c"|"v"] ?* ["q"|"f"|"c"|"v"] ?* ["q"|"f"|"c"|"v"] ];
define ParseSeg9 ~$[ ["q"|"f"|"c"|"v"] ?* ["q"|"f"|"c"|"v"] ?* ["q"|"f"|"c"|"v"] ?* ["q"|"f"|"c"|"v"] ?* ["q"|"f"|"c"|"v"] ?* ["q"|"f"|"c"|"v"] ?* ["q"|"f"|"c"|"v"] ?* ["q"|"f"|"c"|"v"] ?* ["q"|"f"|"c"|"v"] ];

define Onset1 ~$[ "<" ] ;
define Onset2 ~$[ "<" ?* "<" ] ;
define Onset3 ~$[ "<" ?* "<" ?* "<" ] ;
define Onset4 ~$[ "<" ?* "<" ?* "<" ?* "<" ] ;
define Onset5 ~$[ "<" ?* "<" ?* "<" ?* "<" ?* "<" ] ;
define Onset6 ~$[ "<" ?* "<" ?* "<" ?* "<" ?* "<" ?* "<" ] ;
define Onset7 ~$[ "<" ?* "<" ?* "<" ?* "<" ?* "<" ?* "<" ?* "<" ] ;
define Onset8 ~$[ "<" ?* "<" ?* "<" ?* "<" ?* "<" ?* "<" ?* "<" ?* "<" ] ;
define Onset9 ~$[ "<" ?* "<" ?* "<" ?* "<" ?* "<" ?* "<" ?* "<" ?* "<" ?* "<" ] ;

define NoCoda1 ~$[ ">" ] ;
define NoCoda2 ~$[ ">" ?* ">" ] ;
define NoCoda3 ~$[ ">" ?* ">" ?* ">" ] ;
define NoCoda4 ~$[ ">" ?* ">" ?* ">" ?* ">" ] ;
define NoCoda5 ~$[ ">" ?* ">" ?* ">" ?* ">" ?* ">" ] ;
define NoCoda6 ~$[ ">" ?* ">" ?* ">" ?* ">" ?* ">" ?* ">" ] ;
define NoCoda7 ~$[ ">" ?* ">" ?* ">" ?* ">" ?* ">" ?* ">" ?* ">" ] ;
define NoCoda8 ~$[ ">" ?* ">" ?* ">" ?* ">" ?* ">" ?* ">" ?* ">" ?* ">" ] ;
define NoCoda9 ~$[ ">" ?* ">" ?* ">" ?* ">" ?* ">" ?* ">" ?* ">" ?* ">" ?* ">" ] ;

define ComplexOnset1 ~$[ "{" ] ;
define ComplexOnset2 ~$[ "{" ?* "{" ] ;
define ComplexOnset3 ~$[ "{" ?* "{" ?* "{" ] ;
define ComplexOnset4 ~$[ "{" ?* "{" ?* "{" ?* "{" ] ;
define ComplexOnset5 ~$[ "{" ?* "{" ?* "{" ?* "{" ?* "{" ] ;
define ComplexOnset6 ~$[ "{" ?* "{" ?* "{" ?* "{" ?* "{" ?* "{" ] ;
define ComplexOnset7 ~$[ "{" ?* "{" ?* "{" ?* "{" ?* "{" ?* "{" ?* "{" ] ;
define ComplexOnset8 ~$[ "{" ?* "{" ?* "{" ?* "{" ?* "{" ?* "{" ?* "{" ?* "{" ] ;
define ComplexOnset9 ~$[ "{" ?* "{" ?* "{" ?* "{" ?* "{" ?* "{" ?* "{" ?* "{" ?* "{" ] ;

define ComplexCoda1 ~$[ "}" ] ;
define ComplexCoda2 ~$[ "}" ?* "}" ] ;
define ComplexCoda3 ~$[ "}" ?* "}" ?* "}" ] ;
define ComplexCoda4 ~$[ "}" ?* "}" ?* "}" ?* "}" ] ;
define ComplexCoda5 ~$[ "}" ?* "}" ?* "}" ?* "}" ?* "}" ] ;
define ComplexCoda6 ~$[ "}" ?* "}" ?* "}" ?* "}" ?* "}" ?* "}" ] ;
define ComplexCoda7 ~$[ "}" ?* "}" ?* "}" ?* "}" ?* "}" ?* "}" ?* "}" ] ;
define ComplexCoda8 ~$[ "}" ?* "}" ?* "}" ?* "}" ?* "}" ?* "}" ?* "}" ?* "}" ] ;
define ComplexCoda9 ~$[ "}" ?* "}" ?* "}" ?* "}" ?* "}" ?* "}" ?* "}" ?* "}" ?* "}" ] ;

"""

from subprocess import Popen, PIPE, STDOUT

import itertools
constraints = ["Max", "Dep", "ParseSeg", "Onset", "NoCoda", "ComplexCoda", "ComplexOnset"]

typology = {}

n = 0

for ranking in itertools.permutations(constraints):

  model = GENCON + r"define G" + r" GEN "
  for constraint in ranking:
    for i in range(10):
      model += ".O. " + constraint + str(i) + " "
  model += """ ;
push G
down v
down c
down cv
down vc
down vv
down cc
down cvc
down vcv
down ccvcc
down cvcvcv
down cvccvc
clear"""

  foma = Popen(['foma', '-p'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
  foma_stdout = foma.communicate(input=model.encode())[0]
  output = foma_stdout.decode()
  #print(output)
  SRs = tuple([x for x in re.findall('down [^\n]*\n([^\n]*)\n', output)])

  if SRs not in typology:
    typology[SRs] = []
    #print(SRs)
    if '[CF][CF][QV][CF][CF]' in SRs:
      print(ranking)
  typology[SRs].append(ranking)

  n += 1
  if n % 200 == 0:
    print(n)

constraints = ["Max", "Dep", "ParseSeg", "Onset", "NoCoda", "ComplexCoda", "ComplexOnset"]

for x in typology:
  print(x)
  shared = set()
  for y in typology[x]:
    thisone = set()
    for i in range(len(y)):
      for j in range(i+1, len(y)):
        r = (y[i], y[j])
        thisone.add(r)
    if shared:
      shared &= thisone
    else:
      shared |= thisone
  # remove transitive edges
  for a in constraints:
    for b in constraints:
      for c in constraints:
        if (a,b) in shared and (b,c) in shared:
          if (a,c) in shared:
            shared.remove((a,c))
  for s in sorted(shared):
    print('>>'.join(s))

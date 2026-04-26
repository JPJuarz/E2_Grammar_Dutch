import nltk
from nltk import CFG

nltk.download('punkt')
nltk.download('punkt_tab')

#  Gramática Libre de Contexto — Holandés (Dutch)
#  Sin ambigüedad y sin recursión izquierda

grammar = CFG.fromstring("""
  S        -> MC Punct | MC Conj MC Punct
  MC       -> NP VP
  NP       -> SimpleNP | SimpleNP PP
  SimpleNP -> Det N | Pron | Det Adj N
  VP       -> V | V NP | V Neg | V NP Neg | V PP | V NP PP
  PP       -> P NP

  Det   -> 'de' | 'het' | 'een'
  Pron  -> 'ik' | 'jij' | 'hij' | 'zij' | 'wij'
  N     -> 'man' | 'vrouw' | 'kind' | 'huis' | 'hond'
  V     -> 'ben' | 'heb' | 'eet' | 'ga' | 'zie'
  Adj   -> 'groot' | 'klein'
  P     -> 'met' | 'in' | 'op' | 'naar'
  Neg   -> 'niet'
  Conj  -> 'en' | 'maar'
  Punct -> '.'
""")

parser = nltk.ChartParser(grammar)

# Pruebas

oraciones = [
    # Aceptadas 
    ("ACEPTADA", "Ik ben een man."),
    ("ACEPTADA", "Zij zie de hond."),
    ("ACEPTADA", "De groot man eet."),
    ("ACEPTADA", "Wij heb het huis."),
    ("ACEPTADA", "Hij ga niet."),
    ("ACEPTADA", "Jij zie de vrouw niet."),
    ("ACEPTADA", "De hond eet met een kind."),
    ("ACEPTADA", "Ik ben een man en zij zie de hond."),
    ("ACEPTADA", "Wij eet maar hij ga niet."),
    ("ACEPTADA", "De klein kind eet."),
    ("ACEPTADA", "Hij zie een vrouw in het huis."),
    ("ACEPTADA", "Ik ga naar het huis."),
    # Rechazadas 
    ("RECHAZADA", "Ik ben een man"),
    ("RECHAZADA", "Ben ik een man."),
    ("RECHAZADA", "De man."),
    ("RECHAZADA", "Ik zie niet de hond."),
    ("RECHAZADA", "Zij en hij eet."),
    ("RECHAZADA", "Ik eet de groot."),
    ("RECHAZADA", "."),
    ("RECHAZADA", "Ik eet maar."),
    ("RECHAZADA", "De vrouw de hond zie."),
    ("RECHAZADA", "Wij ga ga niet."),
    ("RECHAZADA", "Het groot."),
    ("RECHAZADA", "Ik zie een groot."),
    ("RECHAZADA", "Naar het huis ik ga."),
    ("RECHAZADA", "Ik eet de hond niet niet."),
    ("RECHAZADA", "Een man een vrouw zie."),
    ("RECHAZADA", "Ik"),
    ("RECHAZADA", "De hond de vrouw."),
    ("RECHAZADA", "Groot man eet."),
]


#  Parseo y resultados
print(" \nParser LL(1) — Holandés (Dutch)")

for esperado, oracion in oraciones:
    tokens = nltk.word_tokenize(oracion.lower())
    arboles = list(parser.parse(tokens))

    print()
    print(f"Oración  : {oracion}")
    print(f"Esperado : {esperado}")

    if arboles:
        print(f"Resultado: ACEPTADA ✓" if esperado == "ACEPTADA" else f"Resultado: ACEPTADA ✗ (debería ser rechazada)")
        for arbol in arboles:
            arbol.pretty_print()
    else:
        print("Unable to parse")
        print(f"Resultado: RECHAZADA ✓" if esperado == "RECHAZADA" else f"Resultado: RECHAZADA ✗ (debería ser aceptada)")
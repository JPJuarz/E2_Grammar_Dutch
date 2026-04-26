# E2_Grammar_Dutch
#### Juan Pablo Juárez Ortiz - A01708685

## Evidencia 2: Generación y Limpieza de Gramática | Dutch (Holandés)

---

## Descripción

Las gramáticas constituyen lo que es el fundamento  sobre el que se construyen los métodos computacionales para el procesamiento del lenguaje natural. Basicamente, una gramática describe la estructura de un idioma mediante un conjunto de reglas que dictan como es que se  se pueden combinar palabras y símbolos para formar oraciones o cadenas válidas. En este proyecto se desarrollara un parser capaz de determinar si una oración dada pertenece o no al lenguaje definido por la gramática.

El idioma seleccionado es el **holandés (Dutch)**, una lengua la cuál es germánica occidental y hablada principalmente en los Países Bajos y Bélgica. El holandés comparte raíces con el alemán y el inglés y su sintaxis sigue un orden relativamente estricto de "Sujeto + Verbo + Complemento", con el verbo siempre ocupando la segunda posición en una oración principal sin importar que. Algo importante de saber es que, el holandés utiliza dos tipos de artículos definidos utilizadno "de" para la mayoría de los sustantivos y "het" para los neutros, lo cual influye directamente en la estructura de la frase nominal.

La gramática construida acepta las siguientes estructuras:

- Oraciones simples: Frase Nominal + Frase Verbal (con o sin objeto directo)
- Frases Nominales: vsustantivos simples, con determinante, con pronombre, o con adjetivo
- Frases Verbales: verbo solo, verbo con objeto, verbo con negación (*niet*)
- Frases Preposicionales: preposición seguida de frase nominal
- Oraciones compuestas: dos oraciones principales unidas por una conjunción

**Todas las oraciones deben terminar con un punto (`.`).**

Para la implementación se utiliza un **parser LL(1)**, una técnica de análisis sintáctico descendente empleada en lingüística computacional. "LL significa *left-to-right, leftmost derivation*: el parser lee la entrada de izquierda a derecha construyendo siempre el símbolo no-terminal más a la izquierda. El "(1)" indica que se utiliza un único token de anticipación (*lookahead*) para tomar decisiones, eliminando la necesidad de hacer backtracking" (GeeksforGeeks, 2023).

---

## Vocabulario

Antes de definir la gramática, se este es el vocabulario del subconjunto del holandés que se va a analizar.

### Pronombres (sujeto)

| Holandés | Español |
|----------|---------|
| ik       | yo      |
| jij      | tú      |
| hij      | él      |
| zij      | ella    |
| wij      | nosotros|

### Verbos

| Holandés | Español      | Conjugación singular | Conjugación plural |
|----------|--------------|----------------------|--------------------|
| zijn     | ser / estar  | ben / bent / is      | zijn               |
| hebben   | tener        | heb / hebt / heeft   | hebben             |
| eten     | comer        | eet                  | eten               |
| gaan     | ir           | ga / gaat            | gaan               |
| zien     | ver          | zie / ziet           | zien               |

**Regla de conjugación holandesa:** en singular se usa la raíz del verbo mientras que en plural se usa el verbo completo.

### Sustantivos

| Holandés | Español | Artículo |
|----------|---------|----------|
| man      | hombre  | de       |
| vrouw    | mujer   | de       |
| kind     | niño    | het      |
| huis     | casa    | het      |
| hond     | perro   | de       |

### Adjetivos

| Holandés | Español  |
|----------|----------|
| groot    | grande   |
| klein    | pequeño  |

### Otras palabras

| Holandés | Función     | Español       |
|----------|-------------|---------------|
| de       | artículo    | el / la       |
| het      | artículo    | el / la (neutro) |
| een      | artículo    | un / una      |
| niet     | negación    | no            |
| en       | conjunción  | y             |
| maar     | conjunción  | pero          |
| met      | preposición | con           |
| in       | preposición | en            |
| op       | preposición | sobre         |
| naar     | preposición | hacia         |

---

## Modelos

La construcción de la gramática sigue tres pasos fundamentales: primero se genera la gramática base que captura la esencia del idioma, luego se elimina la ambigüedad y finalmente se elimina la recursión izquierda, obteniendo una gramática compatible con el parser LL(1).

---

### Modelo 1 — Gramática Base (con ambigüedad y recursión izquierda)

El primer paso consiste en generar una gramática que capture correctamente la estructura sintactica del holandés, sin preocuparnos todavía por los defectos como ambigüedad y recursión izquierda. En esta fase se identifican las unidades sintacticas basicas y las reglas que influyen en la formación de oraciones.

```
S   →  NP VP Punct
S   →  S Conj S Punct

NP  →  Det N
NP  →  Pron
NP  →  Det Adj N
NP  →  NP PP

VP  →  V
VP  →  V NP
VP  →  V niet
VP  →  V NP niet

PP  →  P NP

Det  → 'de' | 'het' | 'een'
Pron → 'ik' | 'jij' | 'hij' | 'zij' | 'wij'
N    → 'man' | 'vrouw' | 'kind' | 'huis' | 'hond'
V    → 'ben' | 'heb' | 'eet' | 'ga' | 'zie'
Adj  → 'groot' | 'klein'
P    → 'met' | 'in' | 'op' | 'naar'
Conj → 'en' | 'maar'
Punct → '.'
```

**Ejemplo Arbol Modelo 1**

<img width="1260" height="682" alt="image" src="https://github.com/user-attachments/assets/23e3b657-e9ad-455f-990d-c9d88653e15b" />


Esta gramática es una Gramática Libre de Contexto, clasificada en el **Nivel 2 de la Jerarquía de Chomsky**, dado que todas las producciones tienen exactamente un símbolo no-terminal en el lado izquierdo. Sin embargo, presenta dos problemas que impiden implementarla directamente como parser LL(1):

**Problema 1 — Ambigüedad:** La regla `S → S Conj S` puede generar la misma cadena de dos maneras distintas. Por ejemplo, la oración *"ik eet en zij ziet en hij ga"* puede agruparse como `(ik eet en zij ziet) en hij ga` o como `ik eet en (zij ziet en hij ga)`, produciendo dos árboles de sintaxis diferentes para la misma entrada.

**Problema 2 — Recursión izquierda:** Las reglas `S → S Conj S` y `NP → NP PP` tienen el símbolo no-terminal como primer elemento de su propia producción. Un parser LL(1) que intente derivar `S` con la regla `S → S Conj S` intentara derivar `S` nuevamente inmediatamente, entrando en un bucle infinito.

---

### Modelo 2 — Eliminación de Ambigüedad
 
"Una gramática es ambigua cuando la misma cadena puede derivarse de más de una forma, generando árboles de sintaxis diferentes para la misma entrada. Esto es un problema directo para el parser LL(1) ya que este necesita tomar decisiones únicas con un solo token de anticipación, y si hay dos caminos posibles para la misma entrada simplemente no sabe cual tomar" (GeeksforGeeks, 2026).
 
La solución es restructurar las reglas para que cada cadena tenga un único camino de derivación posible.
 
**Paso 1 — Eliminar la ambigüedad en `S`:**
 
La regla `S → S Conj S` es el problema principal ya que no define asociatividad, o sea el parser no sabe cómo agrupar cuando hay varias conjunciones seguidas. Se introduce la **cláusula principal (MC)** y se fuerza a que la conjunción siempre continue hacia la derecha:
 
```
Antes:
  S  →  S Conj S Punct
 
Después:
  S   →  MC Punct
  S   →  MC Conj MC Punct
  MC  →  NP VP
```
 
Con esto, una oración como *"A en B en C"* solo puede leerse como *A en (B en C)*, una única interpretación posible.
 
**Paso 2 — Eliminar la ambigüedad en `NP`:**
 
La regla `NP → NP PP` junto con las demás producciones de `NP` permitía llegar a la misma frase nominal por rutas distintas. Se introduce `SimpleNP` para separar claramente el núcleo nominal de sus complementos preposicionales:
 
```
Antes:
  NP  →  Det N | Pron | Det Adj N | NP PP
 
Después:
  NP       →  SimpleNP
  NP       →  SimpleNP PP
  SimpleNP →  Det N
  SimpleNP →  Pron
  SimpleNP →  Det Adj N
```
 
La gramática completa sin ambigüedad queda así:
 
```
S        →  MC Punct
S        →  MC Conj MC Punct
 
MC       →  NP VP
 
NP       →  SimpleNP
NP       →  SimpleNP PP
 
SimpleNP →  Det N
SimpleNP →  Pron
SimpleNP →  Det Adj N
 
VP       →  V
VP       →  V NP
VP       →  V niet
VP       →  V NP niet
 
PP       →  P NP
```
 
---
 
### Modelo 3 — Eliminación de Recursión Izquierda
 
Aunque ya no hay ambigüedad, la regla `NP → NP PP` sigue teniendo recursión izquierda. Cuando el parser LL(1) encuentra `NP` e intenta aplicar `NP → NP PP`, necesita expandir `NP` nuevamente antes de leer cualquier token, lo que genera un ciclo infinito.
 
El algoritmo estándar para eliminar recursión izquierda directa toma una producción de la forma: 
 
```
A  →  A β | α
```
 
y la transforma en:
 
```
A   →  α A'
A'  →  β A' | ε
```
 
donde `A'` es un nuevo símbolo auxiliar y `ε` representa la producción vacía.
 
**Entonces aplicandolo a `NP` queda de la siguiente manera:**
 
```
Antes:
  NP  →  SimpleNP
  NP  →  SimpleNP PP
 
Después:
  NP    →  SimpleNP NP'
  NP'   →  PP NP' | ε
```
 
La gramática final sin ambigüedad y sin recursión izquierda, lista para el parser LL(1):
 
```
S        →  MC Punct | MC Conj MC Punct

MC       →  NP VP

NP       →  SimpleNP | SimpleNP PP

SimpleNP →  Det N
SimpleNP →  Pron
SimpleNP →  Det Adj N

VP  →  V
VP  →  V NP
VP  →  V Neg
VP  →  V NP Neg
VP  →  V PP
VP  →  V NP PP

PP  →  P NP

Det   → 'de' | 'het' | 'een'
Pron  → 'ik' | 'jij' | 'hij' | 'zij' | 'wij'
N     → 'man' | 'vrouw' | 'kind' | 'huis' | 'hond'
V     → 'ben' | 'heb' | 'eet' | 'ga' | 'zie'
Adj   → 'groot' | 'klein'
P     → 'met' | 'in' | 'op' | 'naar'
Neg   → 'niet'
Conj  → 'en' | 'maar'
Punct → '.'
```
---
 
## Implementación
 
La gramática se implementó en Python usando **NLTK** (*Natural Language Toolkit*), una biblioteca que ofrece herramientas para tokenización, definición de gramáticas y análisis sintáctico (Bird et al., 2009).
 
### Requisitos
 
- Python
- NLTK
  
### Instalación
 
pip install nltk (en consola)
 
### Ejecución
 
Correr dutch_grammar.py (Ctrl + alt + n (en windows))
 
Al correr el programa se muestra el árbol de análisis de cada oración de prueba. Las oraciones válidas muestran su árbol y las que no pertenecen a la gramática imprimen `"Unable to parse"`.
 
---
 
## Pruebas
 
### Oraciones aceptadas 
 
| # | Oración | Traducción |
|---|---------|------------|
| 1 | `ik ben een man .` | Yo soy un hombre. |
| 2 | `zij zie de hond .` | Ella ve al perro. |
| 3 | `de groot man eet .` | El hombre grande come. |
| 4 | `wij heb het huis .` | Nosotros tenemos la casa. |
| 5 | `hij ga niet .` | Él no va. |
| 6 | `jij zie de vrouw niet .` | Tú no ves a la mujer. |
| 7 | `de hond eet met een kind .` | El perro come con un niño. |
| 8 | `ik ben een man en zij zie de hond .` | Yo soy un hombre y ella ve al perro. |
| 9 | `de klein kind eet .` | El niño pequeño come. |
| 10 | `hij zie een vrouw in het huis .` | Él ve a una mujer en la casa. |
| 11 | `ik ga naar het huis .` | Yo voy hacia la casa. |
 
### Oraciones rechazadas 
 
| # | Oración | Razón del rechazo |
|---|---------|-------------------|
| 1 | `ik ben een man` | Falta el punto final |
| 2 | `ben ik een man .` | El verbo no puede ser el primer token |
| 3 | `de man .` | No hay verbo en la oración |
| 4 | `ik zie niet de hond .` | *niet* debe ir después del objeto, no antes |
| 5 | `zij en hij eet .` | La gramática no acepta conjunción entre dos sujetos |
| 6 | `ik eet de groot .` | *groot* es adjetivo, no puede usarse como objeto solo |
| 7 | `.` | Solo un punto, sin ninguna oración |
| 8 | `ik eet maar .` | Conjunción sin segunda cláusula |
| 9 | `de vrouw de hond zie .` | Objeto antes del verbo, orden incorrecto |
| 10 | `wij ga ga niet .` | El verbo aparece dos veces seguido |
| 11 | `het groot .` | Artículo con adjetivo pero sin sustantivo ni verbo |
| 12 | `ik zie een groot .` | Adjetivo después de artículo pero sin sustantivo |
| 13 | `naar het huis ik ga .` | La frase preposicional no puede ir al inicio |
| 14 | `ik eet de hond niet niet .` | La negación aparece dos veces |
| 15 | `een man een vrouw zie .` | Dos frases nominales seguidas sin verbo en posición correcta |
| 16 | `ik` | Una sola palabra, no forma ninguna oración |
| 17 | `de hond de vrouw .` | Dos frases nominales seguidas, falta el verbo |
| 18 | `groot man eet .` | Adjetivo sin artículo antes del sustantivo |
 
---
### Árboles de sintaxis de oraciones correctas (output del programa)
<img width="512" height="492" alt="image" src="https://github.com/user-attachments/assets/d99279ab-9b55-472f-bcfd-19f62ea3323a" />

<img width="510" height="483" alt="image" src="https://github.com/user-attachments/assets/8d01bf8a-5c83-49a5-b537-9b13b19fbc77" />

<img width="445" height="423" alt="image" src="https://github.com/user-attachments/assets/1871e8f5-c1ef-4f14-98b3-e6c2075cd891" />

<img width="549" height="499" alt="image" src="https://github.com/user-attachments/assets/046f6eb8-d8d9-4087-b615-8c21bc2f14b2" />

<img width="747" height="562" alt="image" src="https://github.com/user-attachments/assets/438abc7a-8b8c-40e9-982c-2e7584fb8bbb" />

<img width="694" height="549" alt="image" src="https://github.com/user-attachments/assets/34599005-fc10-4445-beb8-9fddebfc69eb" />


---
 
## Análisis — Jerarquía de Chomsky
 
La **Jerarquía de Chomsky** clasifica los lenguajes formales en cuatro niveles según las restricciones de sus reglas y el tipo de autómata que puede reconocerlos:
 
| Tipo | Nombre                | Autómata reconocedor         |
|------|-----------------------|------------------------------|
| 0    | Sin restricciones     | Turing Machine            |
| 1    | Sensible al contexto  | Linear bounded Automaton |
| **2**| **Libre de contexto** | **Push down Automaton**         |
| 3    | Regular               | Finite Automaton             |
 
### Antes de limpiar la gramática
 
La gramática base es **Tipo 2 (CFG)** ya que todas sus producciones tienen un solo no-terminal en el lado izquierdo, y el lado derecho puede ser cualquier combinación de terminales y no-terminales. No puede ser Tipo 3 (regular) porque tiene reglas como `MC → NP VP` con más de un símbolo en el lado derecho, algo que las gramáticas regulares no permiten.
 
### Después de limpiar la gramática
 
La gramática limpia sigue siendo **Tipo 2**. Aun eliminando ambigüedad y recursión izquierda, esto no cambia el nivel en la jerarquía de Chomsky. Lo que sí cambia es la eficiencia del análisis: al ser compatible con un parser LL(1), la complejidad baja a **O(n)** osea una complejidad lineal, lo cual es una mejora importante especialmente cuando se procesan grandes cantidades de oraciones.
 
---
 
## Referencias
 
GeeksforGeeks. (2023). Construction of LL(1) Parsing Table.
https://www.geeksforgeeks.org/construction-of-ll1-parsing-table/

GeeksforGeeks. (2026). Ambiguous Grammar.
https://www.geeksforgeeks.org/ambiguous-grammar/

GeeksforGeeks. (2026). Chomsky Hierarchy in Theory of Computation.
https://www.geeksforgeeks.org/chomsky-hierarchy-in-theory-of-computation/

NLTK Project. (2025). Natural Language Toolkit Documentation.
https://www.nltk.org/

Linz, P. (2017). An introduction to formal languages and automata (6th ed.). Jones & Bartlett Learning.

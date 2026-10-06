 ▐▛███▛█   Claude Code v2.1.289
▝▜██████▀  Fable 5.1 · Claude Team
 ▝▝   ▝▝   ~/Desktop/personal-hq/projects/unr-tesina-new


❯ /clear                                                                        

❯ /model fable                                                                  
  ⎿  Set model to Fable 5.1 and saved as your default for new sessions

❯ para [1] hemos hecho un resumen usando IA y luego yo he ido leyendo y         
  entendiendo y escribí un resumen con mis palabras (muchas veces ampliado o    
  borrando cosas repetidas y re-ordenando)                                      
  La idea es hacer eso con [2], como ya tenemos mi version final del resumen de 
  [1] estaria  bueno que el output final se adapte a mis formas y objetivos,    
  yo lo escribí generalmente en item, con cada item un concepto o idea facil de 
  entender (como un bocado de informacion), no necesariamente auto contenida    
  (estan relacionados con los items previos y siguientes). Aunque tambien       
  inclui parrafos. Y algo en particular que creo que he hecho es ir a los       
  detalles, a como estaba implementado (muchas veces chequeando en el           
  repositorio para constatar como realmente operó [1]. Y por ultimo me fijé que 
  todo [1] esté cubierto: que no haya analisis o experimento que hayan hecho o  
  idea propia del papper que haya quedado excluida en mi resumen (mas que un    
  resumen es una digestion, ya que casi que la longitud es la del papper)       
                                                                                
  Creo que lo mejor para hacerlo sería primero tratar de crear un resumen con   
  tus palabras y luego pasarlo a la forma de mi resumen final de [1] y siempre  
  chequeando esto que no hayas dejado informaicon relevante afuera de esta      
  digestion                                                                     
                                                                                
  [1]: /Users/marianocrosetti/Desktop/personal-hq/projects/unr-tesina-new/refer 
  encias/zhang2024_transcendence.pdf                                            
  [2]: /Users/marianocrosetti/Desktop/personal-hq/projects/unr-tesina-new/refer 
  encias/abreu2025_taxonomy_of_transcendence.pdf                                
  primer resumen de 1:                                                          
  /Users/marianocrosetti/Desktop/personal-hq/projects/unr-tesina-new/referencia 
  s/mi-review-de-literatura/summary-papper1-ai-generated.md                     
  segundo resumen "con mis palabras" de                                         
  1:/Users/marianocrosetti/Desktop/personal-hq/projects/unr-tesina-new/referenc 
  ias/mi-review-de-literatura/summary-papper1-v1.md                             
                                                                                
  ultrathink                                                                    

⏺ Voy a leer los dos resúmenes de [1] (para calibrar el estilo) y el paper [2]
  completo, y después armo la digestión en dos pasadas como propusiste.

  Read 1 file, listed 1 directory, ran 2 shell commands (ctrl+o to expand)

⏺ Ya revisé el PDF completo de [2] y los resúmenes de [1]. Ahora extraeré el
  texto para verificar cifras, buscaré si [2] tiene repositorio público y
  prepararé las figuras para img/. · summary

  Ran 1 shell command (ctrl+o to expand)

⏺ Web Search(""A Taxonomy of Transcendence" Abreu Zhang Malach Saphra github
            code")
  ⎿  Did 1 search in 5s

  Ran 3 shell commands (ctrl+o to expand)

⏺ Voy a confirmar si existe un repo público de [2] (arXiv y GitHub de los
  autores) y luego recortaré las figuras del PDF renderizado usando las
  coordenadas de los captions. · summary

⏺ Fetch(https://arxiv.org/abs/2508.17669)
  ⎿  Received 38.6KB (200 OK)

⏺ Web Search("github natalieabreu transcendence knowledge graph experts")
  ⎿  Did 1 search in 5s

  Ran 1 shell command (ctrl+o to expand)

⏺ No encuentro repositorio público para [2], a diferencia de [1], lo cual limita
  las verificaciones de implementación que se hicieron con ese; lo anotaré en
  la digestión. Ahora recorto las 7 figuras. · summary

⏺ Bash(cd /private/tmp/claude-501/-Users-marianocrosetti-Desktop-personal-hq-pro
      jects-unr-tesina-new/9f3b2a6d-8f75-4a78-94a0-4438bcc4ff7e/scratchpad &&
      mkdir -p hi &&…)
  ⎿  p-04.png
     p-05.png
     p-06.png
     … +10 lines (ctrl+o to expand)
  ⎿  Shell cwd was reset to 
     /Users/marianocrosetti/Desktop/personal-hq/projects/unr-tesina-new
  ⎿  7 files changed (binary, mode only or too large to show)

⏺ Figuras recortadas. Verifico rápido que los recortes quedaron bien (las 7 de
  una) y después paso a escribir.

  Read 1 file, ran 1 shell command (ctrl+o to expand)

⏺ Corrijo el recorte de la Fig. 4 que corta la etiqueta del eje x. Luego reviso
  tu propuesta y los diseños de experimentos para que la sección de
  "posicionamiento" de [2] refleje tus experimentos reales en lugar de
  generalidades. · summary

  Read 2 files, ran 3 shell commands (ctrl+o to expand)

⏺ Ahora que tengo todo el contexto, escribo la pasada 1 (resumen propio
  siguiendo la estructura del paper) y luego la pasada 2 (adaptada a tu estilo),
  guardándolas en referencias/mi-review-de-literatura/ junto a los archivos de
  [1]. · summary

⏺ Write(referencias/mi-review-de-literatura/summary-papper2-ai-generated.md)
  ⎿  Wrote 171 lines to
     referencias/mi-review-de-literatura/summary-papper2-ai-generated.md
      1 # Resumen de [2] (pasada 1: con mis palabras, siguiendo la estruc
      2 
        ce*. COLM 2025. https://arxiv.org/abs/2508.17669 (v1, 25 ago 2025
      4 - Código: **no hay repositorio público** (ni en arXiv, ni en GitH
        erimentos se basaron en código provisto por Annabelle Michael Car
        rell". A diferencia de [1], no se puede contrastar paper vs imple
      5 - Dos de los autores son de [1] (Edwin Zhang, Eran Malach). Mismo
      6 
      8 
         un *grupo*. Un grupo
     … +456 lines (ctrl+o to expand)

⏺ Primera pasada lista. Ahora redacto la pasada 2 con el formato solicitado y
  luego verifico la cobertura y compilo con el Makefile. · summary

⏺ Write(referencias/mi-review-de-literatura/summary-papper2-v0.md)
  ⎿  Wrote 290 lines to
     referencias/mi-review-de-literatura/summary-papper2-v0.md
       1 # Resumen de [2]
       3 - Papper: https://arxiv.org/abs/2508.17669 (COLM 2025, v1 25-ago
       4 - Código de los experimentos: **no hay repositorio público**. No
         ntos: "some experiments were based on code provided by Annabelle
         exto, no pude constatar implementación como con [1].
       5 - Mismo grupo que [1] (Kempner, Harvard). Zhang y Malach son aut
       6 
       8 
         ita a un *grupo*. El grupo puede superar a cada integrante de tr
      10 - El papper formaliza esas tres formas como 
     … +710 lines (ctrl+o to expand)

⏺ Bash(cd /Users/marianocrosetti/Desktop/personal-hq/projects/unr-tesina-new/ref
      erencias/mi-review-de-literatura && python3 - <<'EOF'
      import re…)
  ⎿  ok
     /opt/homebrew/bin/pandoc
     /opt/homebrew/bin/tectonic
     … +71 lines (ctrl+o to expand)
  ⎿  Updated
     referencias/mi-review-de-literatura/summary-papper2-ai-generated.md
     (+2 -0)
       8  
       9  Un modelo entrenado por imitación no imita a *una* persona sino
           a un *grupo*. Un grupo puede superar a cada uno de sus miembro
          s de tres maneras distintas, y el paper las formaliza como tres
           **modos de trascendencia**: (i) **skill denoising** (voto: los
           errores independientes se cancelan, lo que estudió [1]), (ii) 
          **skill selection** (ruteo: cada entrada la responde el experto
           que la conoce, porque es el que más habla de ella), (iii) **sk
          ill generalization** (composición: se combina conocimiento de d
          istintos expertos en un espacio latente compartido para respond
          er lo que ningún experto sabe). Para cada modo dan una condició
          n sobre los *datos de entrenamiento* y la verifican en un domin
          io sintético de grafos de conocimiento con expertos simulados. 
          La tesis transversal: el modelo sólo trasciende si el conjunto 
          de expertos es suficientemente **heterogéneo** (diversidad de e
          rrores, de expertise, de fraseo, de composiciones).
      10  
      11 +Matiz de la intro: mezclar muchas personas también puede amplif
         +icar sesgos compartidos (Bender et al. 2021, *stochastic parrot
         +s*); el paper estudia el lado positivo. Ejemplo motivador: un c
         +hatbot igual de competente en criptografía, derecho internacion
         +al y Dostoievski.                                              
      12 +                                                               
      13  Contribuciones declaradas:
      14  1. Formalizar los tres modos partiendo de las definiciones de [
          1].
      15  2. Proponer condiciones sobre los datos para cada modo, con int
          uición en settings teóricos simples.
  ⎿  Updated referencias/mi-review-de-literatura/summary-papper2-v0.md (+2 
     -0)
      12      - **Skill selection** (selección / ruteo): cada experto sab
          e de una región; la clave es que **habla más de la región que s
          abe**. El modelo aprende a dar la respuesta del experto que más
           aparece en ese contexto. Acá los errores de los no-expertos pu
          eden estar correlacionados y el voto fallar igual.
      13      - **Skill generalization** (composición): la pregunta no la
           sabe nadie; el modelo combina conocimiento de dos expertos dis
          tintos en un espacio latente compartido.
      14  - La analogía humana que usan: votar; derivar la pregunta al cr
          iptógrafo o al abogado; que criptógrafo y abogado razonen junto
          s sobre la legalidad de un embargo algorítmico.
      15 +- Aclaran que la combinación de muchas personas también puede *
         +*amplificar los sesgos compartidos** (citan *stochastic parrots
         +*, Bender et al. 2021). El papper estudia el otro lado: cuándo 
         +la diversidad del grupo le gana al individuo. El ejemplo motiva
         +dor es un chatbot que habla con igual competencia de criptograf
         +ía, derecho internacional y Dostoievski.                       
      16 +- Cuándo aplica cada modo, según la intro: denoising cuando tod
         +os los expertos producen datos relevantes para la entrada pero 
         +con errores independientes; selection cuando la entrada le es f
         +amiliar a *al menos un* experto (y ese experto la encuentra más
         + seguido); generalization cuando la entrada no le es familiar a
         + *ninguno* pero se entiende por generalización.                
      17  - La tesis transversal: el modelo trasciende sólo si el conjunt
          o de expertos es suficientemente **heterogéneo**. "Diversidad" 
          quiere decir cosas distintas en cada modo: errores no correlaci
          onados, expertises variadas, fraseos y composiciones variadas.
      18  - Contribución adicional que reivindican: el *testbed* de grafo
           de conocimiento con expertos simulados, como banco controlado 
          para trabajo futuro.
      19  - Diferencia de dominio con [1]: no hay juego ni secuencia de d
          ecisiones. Cada consulta es un hecho aislado (head, relation, t
          ail). La verdad se conoce por construcción (no hace falta Stock
          fish).
  ⎿  … 4 more files changed
  ⎿  (timeout 10m)

⏺ Los dos PDFs compilaron. Hago una verificación visual rápida del PDF de la v0
  (tabla de supuestos y una figura) y un chequeo de cobertura mecánico con los
  números clave del paper.

  Searched for 1 pattern, read 1 file, ran 2 shell commands, wrote 1 memory (ctrl+o to expand)

⏺ Listo. Hice la digestión de [2] en las dos pasadas que propusiste y dejé todo
  en referencias/mi-review-de-literatura/, al lado de los de [1].

  Archivos nuevos

  - summary-papper2-ai-generated.md: pasada 1, con mis palabras, siguiendo la
    estructura del paper (equivalente al ai-generated de [1]).
  - summary-papper2-v0.md: pasada 2, adaptada a tu forma. Le puse v0 y no v1
    porque la v1 de [1] es la tuya; cuando la revises y reescribas, esa sería tu
    v1.
  - img/abreu2025/: las 7 figuras del paper recortadas del PDF (son vectoriales,
    no se podían extraer directo).
  - Los dos PDFs compilados con tu Makefile (la v0 queda en 12 páginas).

  Qué tiene la v0, en tu formato

  - Idea principal en ítems, formalización completa con lo que cambia respecto
    de [1] ($p_i$ por experto, $g(i \mid x)$, clase de hipótesis $\mathcal{H}$),
    tabla de qué supuesto se elimina en cada modo.
  - Teorema 2.1 con la prueba del apéndice y tres notas mías: es condición
    necesaria y no suficiente, es trascendencia a temperatura 1 (la "ponderación
    bayesiana" que vos ya habías anotado en [1]), y los experimentos de
    selection usan greedy, así que mezclan selección con denoising.
  - Setup del grafo, generación de datos, evaluación y régimen de entrenamiento
    con todos los números del paper y los apéndices.
  - Los tres experimentos con resultados leídos del texto y de los gráficos, más
    cuentas mías marcadas como tales. Dos que te pueden servir para el
    experimento 2: el techo sin generalización $1-(1-c)^{n_e}$ coincide con la
    Figura 5 en $\alpha = 1$, y la transición abrupta con $c = 0.01$ sale de
    contar votos correctos vs erróneos, que es el mismo argumento de tu
    $\alpha^*$.
  - Apéndice A.2 (sesgo de simplicidad) desarrollado, trabajo relacionado
    agrupado para tu marco teórico, limitaciones declaradas.
  - Sección "Posicionamiento" y "DUDAS" escritas por mí como borrador a partir
    de la propuesta aprobada. Están marcadas como borrador: son decisiones
    tuyas.

  Chequeo de cobertura: recorrí sección por sección (intro, definiciones,
  setting, los tres experimentos, related work, discusión, agradecimientos,
  apéndices A.1, A.2, B.1 a B.3.4 y la Tabla 1) y verifiqué que cada ítem esté
  en la v0. Al cierre me faltaban dos detalles de la intro (Bender et al. sobre
  sesgos compartidos y el ejemplo del chatbot) y los agregué.

  Dos cosas a tener en cuenta

  - [2] no tiene repositorio público (verifiqué arXiv y GitHub). Así que no pude
    hacer el contraste paper vs código que hiciste con [1]. En la v0 dejé una
    lista de lo que el paper no especifica: tamaño de GPT-2, cómo se arma el
    vector de cobertura $s_i$, cantidad de expertos en generalization, formato
    de CoT, y que no hay semillas ni barras de error.
  - Varios números de resultados los leí de los gráficos (Figuras 3, 4 y 5), no
    del texto. Están marcados como "leído del gráfico".

✻ Baked for 14m 8s · done 1:38 am
❯ /model opus                                                                   
  ⎿  Set model to Opus 5.5 and saved as your default for new sessions

❯ podrías hacer una busqueda exhaustiva de internet a ver si no encontrás repo  
  publico?                                                                      

⏺ Busco en paralelo en GitHub, Papers with Code, OpenReview, Hugging Face y los
  perfiles de los autores.

⏺ Web Search(""Taxonomy of Transcendence" code repository")
  ⎿  Did 1 search in 5s

⏺ Web Search("Natalie Abreu Harvard Kempner github")
  ⎿  Did 1 search in 5s

⏺ Web Search(""2508.17669"")
  ⎿  Did 1 search in 4s

⏺ Web Search("openreview "A Taxonomy of Transcendence" COLM 2025")
  ⎿  Did 1 search in 5s

  Ran 1 shell command (ctrl+o to expand)

⏺ Fetch(https://openreview.net/forum?id=tfTn8616Gf)
  ⎿  Received 4.7KB (200 OK)

⏺ Fetch(https://natalieabreu.github.io/website/)
  ⎿  Received 5.2KB (200 OK)

⏺ Fetch(https://paperswithcode.co/paper/2508.17669)
  ⎿  Received 1.7KB (200 OK)

⏺ Encontré candidatos en el GitHub de Natalie Abreu: transcendence y
  kg_multihop. Los reviso.

  Ran 1 shell command (ctrl+o to expand)

⏺ Encontré dos repositorios candidatos: natalieabreu/transcendence, de octubre
  de 2025 con un único commit "src code" cuyos archivos coinciden con el paper,
  y kg_multihop, un fork de bellecarrell/twohop (Annabelle Carrell, mencionada
  en los agradecimientos). Ahora reviso el código para confirmar cuál
  corresponde al paper.

  Ran 3 shell commands (ctrl+o to expand)

⏺ Leo las partes que responden lo que el paper no especifica: cómo se arman los
  vectores de expertise, la corrupción y la generación por modo.

  Ran 3 shell commands (ctrl+o to expand)

⏺ Esto ya responde varias de las dudas que había dejado abiertas. Reviso además
  cómo se puntúa cada arista, el denoising, y si kg_multihop tiene el código de
  entrenamiento.

  Ran 3 shell commands (ctrl+o to expand)

⏺ El fork kg_multihop sí tiene el código de entrenamiento y evaluación. Miro
  cómo decide si una respuesta es correcta y qué hace el driver de
  entrenamiento.

  Ran 2 shell commands (ctrl+o to expand)

⏺ Tengo suficiente para actualizar las dos digestiones y la memoria. Busco las
  afirmaciones de "no hay código" para corregirlas.

  Ran 1 shell command (ctrl+o to expand)

⏺ Bash(python3 - <<'EOF'
      p='summary-papper2-v0.md'; s=open(p).read()…)
  ⎿  ok
     -rw-r--r--@ 1 marianocrosetti  staff   63955  5 Oct 01:43 summary-papp
     er2-ai-generated.pdf
     … +2 lines (ctrl+o to expand)
  ⎿  Updated
     referencias/mi-review-de-literatura/summary-papper2-ai-generated.md
     (+2 -2)
      1  # Resumen de [2] (pasada 1: con mis palabras, siguiendo la estru
         ctura del paper)
      2  
      3  - Paper: Abreu, Zhang, Malach, Saphra. *A Taxonomy of Transcende
         nce*. COLM 2025. https://arxiv.org/abs/2508.17669 (v1, 25 ago 20
         25).
      4 -- Código: **no hay repositorio público** (ni en arXiv, ni en Git
        -Hub de los autores). En los agradecimientos dicen que "algunos e
        -xperimentos se basaron en código provisto por Annabelle Michael 
        -Carrell". A diferencia de [1], no se puede contrastar paper vs i
        -mplementación.                                                  
      4 +- Código: no está linkeado desde el paper. Hay dos repos público
        +s de la primera autora: https://github.com/natalieabreu/transcen
        +dence (generación de expertos y datos, oct-2025) y https://githu
        +b.com/natalieabreu/kg_multihop (fork del repo de Annabelle Carre
        +ll con entrenamiento y evaluación, versión anterior que sólo cub
        +re denoising). Detalles constatados en `summary-papper2-v0.md`, 
        +sección "Constatación en el código".                            
      5  - Dos de los autores son de [1] (Edwin Zhang, Eran Malach). Mism
         o grupo (Kempner, Harvard).
      6  
      7  ## 1. Idea en una frase
     ...
      163  - El setup controlado aísla fenómenos pero es limitado; piden 
           trabajo en settings reales.
      164  - El marco **no captura *skill discovery*** (descubrir algo qu
           e ningún experto ni su composición sabe).
      165  
      166 -## 10. Lo que el paper no especifica (y no se puede chequear p
          -orque no hay código)                                          
      166 +## 10. Lo que el paper no especifica (ver la v0 para lo que se
          + pudo constatar en el código)                                 
      167  
      168  - Tamaño de GPT-2 usado.
      169  - Cómo se construye el vector de cobertura $s_i$ (qué clusters
            recibe cada experto, si los valores son 0/1).
  ⎿  Updated referencias/mi-review-de-literatura/summary-papper2-v0.md (+31
     -6)
       1  # Resumen de [2]
       2  
       3  - Papper: https://arxiv.org/abs/2508.17669 (COLM 2025, v1 25-ag
          o-2025)
       4 -- Código de los experimentos: **no hay repositorio público**. N
         -o figura en arXiv ni en los GitHub de los autores. En agradecim
         -ientos: "some experiments were based on code provided by Annabe
         -lle Michael Carrell". Consecuencia: todo lo que digo acá sale d
         -el texto, no pude constatar implementación como con [1].       
       4 +- Código de los experimentos: **no está linkeado** desde el pap
         +per, arXiv, OpenReview ni la web de la autora. Pero hay dos rep
         +os públicos en el GitHub de Natalie Abreu (encontrados el 2026-
         +10-05):                                                        
       5 +    - https://github.com/natalieabreu/transcendence: **generaci
         +ón de expertos y datasets** (los tres modos, refraseo con GPT-4
         +o-mini). Un único commit "src code" del 14-oct-2025, sin README
         + ni licencia. No tiene entrenamiento ni evaluación.            
       6 +    - https://github.com/natalieabreu/kg_multihop: fork de `bel
         +lecarrell/twohop` (Annabelle Carrell, la de los agradecimientos
         +), que a su vez parte del código de RippleEdits de Cohen et al.
         + 2023. Tiene **entrenamiento y evaluación** (`train/`), con com
         +mits de oct-2024. Es una versión **anterior** al papper: sus co
         +nfigs sólo cubren denoising.                                   
       7 +    - Ninguno de los dos trae los scripts que lanzan las corrid
         +as del papper (los parámetros concretos de cada figura), ni el 
         +grafo de entidades ficticias. Lo que constaté está abajo en "Co
         +nstatación en el código".                                      
       8  - Mismo grupo que [1] (Kempner, Harvard). Zhang y Malach son au
          tores de ambos.
       9  
      10  ## Idea principal
     ...
      113  
      114  ### Régimen de entrenamiento
      115  
      113 -- **Modelo (denoising y selection)**: *finetuning* de **GPT-2 
          -preentrenado**. No dicen qué tamaño (el chico es 124M). Como l
          -as entidades son ficticias, el preentrenamiento no aporta hech
          -os del grafo, sólo lenguaje.                                  
      116 +- **Modelo (denoising y selection)**: *finetuning* de **GPT-2 
          +preentrenado**. No dicen qué tamaño. **En el código** (`kg_mul
          +tihop/train/train_2.py`) es `"gpt2"`, o sea el chico de **124M
          +**. Como las entidades son ficticias, el preentrenamiento no a
          +porta hechos del grafo, sólo lenguaje.                        
      117  - **Modelo (generalization)**: **LLaMA 3.2 de 1B** porque la t
           area es más difícil. Experimentos preliminares: agrandar el mo
           delo mejora poco el two-hop (consistente con Yang et al. 2024 
           y Allen-Zhu & Li 2024b).
      118  - **Objetivo**: next-token prediction sobre los párrafos.
      119  - **Optimización**: AdamW, lr $10^{-3}$, weight decay 0.1, 100
           0 pasos de warmup, cosine decay, batch size 24. Nota: lr $10^{
           -3}$ es alto para finetuning; no lo justifican.
     ...
      148      - Cada experto $i$ tiene un **vector de cobertura** $s_i =
            (s_i^{(1)}, \dots, s_i^{(5000)})$ con $s_i^{(j)} \in [0, 1]$ 
           = accuracy del experto en las aristas del cluster $j$, sujeto 
           a
      149  $$\sum_{j=1}^{5000} s_i^{(j)}\, |C_j| = c \cdot |E|$$
      150      - Para cada arista $e \in C_j$: con probabilidad $s_i^{(j)
           }$ se incluye correcta, con $1 - s_i^{(j)}$ corrupta.
      148 -    - **No especifican** cómo se eligen los $s_i^{(j)}$ (qué c
          -lusters le tocan a cada experto, si los valores son 0/1 o inte
          -rmedios). Tampoco si las corrupciones son independientes entre
          - expertos. Por la descripción de la Sección 3 (corrupción al a
          -zar por experto), parece que sí. O sea: la motivación habla de
          - misconceptions **compartidas**, pero lo implementado parece s
          -er "la mayoría se equivoca, cada uno a su manera". Lo que hace
          - fallar al voto no es que coincidan en el error sino que son m
          -uchos más los que se equivocan.                               
      151 +    - El papper **no especifica** cómo se eligen los $s_i^{(j)
          +}$. **En el código** (`transcendence/src/dataset_generator.py`
          +, `skill_selection`, `select_clusters` y `get_confidence_score
          +s_lp`):                                                       
      152 +        - Cada experto elige clusters **al azar** (shuffle) ha
          +sta juntar `edges_per_expert` aristas.                        
      153 +        - Los $s_i^{(j)}$ de esos clusters salen de un **progr
          +ama lineal**: maximizar $\sum_j s_i^{(j)}$ sujeto a $\sum_j |C
          +_j|\, s_i^{(j)} = c\,|E|$ y $0 \le s \le 1$. La solución de un
          + LP así cae en un vértice: casi todos los $s$ quedan en **0 o 
          +1** y a lo sumo uno fraccionario. O sea, en la práctica la exp
          +ertise es binaria por cluster.                                
      154 +        - Los clusters no elegidos quedan con $s = 0$: el expe
          +rto los sabe **siempre mal**.                                 
      155 +    - Corrupción (`get_modified_graph_over_edges`): con probab
          +ilidad $1 - s$ se reemplaza, con 50/50, el tail o el head por 
          +una entidad sorteada **uniformemente** entre las que aparecen 
          +como tail (o head) de esa misma relación. Eso es lo que el pap
          +per llama "entidad del mismo tipo". El sorteo es **independien
          +te por experto**.                                             
      156 +    - Conclusión: la sospecha era correcta. La motivación habl
          +a de misconceptions **compartidas**, pero lo implementado es "
          +la mayoría se equivoca, cada uno a su manera". Lo que hace fal
          +lar al voto no es que coincidan en el error sino que son mucho
          +s más los que se equivocan.                                   
      157  - **Generación con la perilla $\alpha$**: se samplea un nodo u
           niforme del grafo personal como antes, pero ahora cada hecho c
           onectado se escribe con probabilidad
      158  $$p = \alpha\, s_i^{(j)} + (1 - \alpha), \qquad \alpha \in [0,
            1]$$
      159  donde $j$ es el cluster de la arista.
     ...
      179  ### Experimento 3: skill generalization
      180  
      181  - **Idea**: en selection al menos un experto sabe la respuesta
           ; acá **ninguno**. El modelo tiene que componer conocimiento d
           e dos expertos usando representaciones compartidas.
      174 -- **Construcción de los expertos**: versión simplificada de se
          -lection. **Cada experto conoce un único cluster** y **sin erro
          -res** (Figura 1). No dicen cuántos expertos hay (¿uno por clus
          -ter, 5.000?). Cada experto genera muestras **en proporción al 
          -tamaño de su cluster** (acá sí se aparta del $N / n_e$ uniform
          -e).                                                           
      182 +- **Construcción de los expertos**: versión simplificada de se
          +lection. **Cada experto conoce un único cluster** y **sin erro
          +res** (Figura 1). El papper no dice cuántos expertos hay. **En
          + el código** (`per_cluster_strategy`): el experto $i$ es exact
          +amente el cluster $i$, con expertise one-hot y su grafo person
          +al formado sólo por las aristas de ese cluster (no hay aristas
          + corruptas). Con `num_experts = n` se usan los clusters $0, \d
          +ots, n-1$; no hay forma de saber qué $n$ usaron en el papper. 
          +Hay un caso especial de un solo experto que usa el cluster 499
          +9, comentado como "baseline con el cluster más grande". Cada e
          +xperto genera muestras **en proporción al tamaño de su cluster
          +** (acá sí se aparta del $N / n_e$ uniforme).                 
      183  - **Marco de evaluación**: el de Yang et al. 2024 (*Do LLMs la
           tently perform multi-hop reasoning?*). Capacidad composicional
            **latente** = responder el hecho de dos saltos **sin generar 
           la entidad intermedia**, sabiendo los hechos de un salto.
      184  - **Dos tipos de hechos de dos saltos**:
      185      - **Within-expertise**: las dos aristas están en el mismo 
           cluster. Algún experto sabe ambos saltos.
     … 36 more lines (ctrl+o to expand)
  ⎿  … 2 more files changed
  ⎿  (timeout 5m)

  Ran 1 shell command (ctrl+o to expand)

⏺ Sí, hay código público. No está linkeado desde el paper, arXiv, OpenReview,
  Papers with Code ni la web de la autora, y por eso las búsquedas web no lo
  encontraban. Lo encontré listando los repos de cada autor en GitHub.

  Los dos repos de Natalie Abreu, la primera autora

  - natalieabreu/transcendence: genera los expertos y los datasets de los tres
    modos, e incluye el refraseo con GPT-4o-mini. Tiene un solo commit "src
    code" de octubre de 2025, sin README ni licencia. No incluye entrenamiento
    ni evaluación.
  - natalieabreu/kg_multihop: es un fork del repo de Annabelle Carrell, la
    persona que nombran en los agradecimientos, que parte del código de Cohen et
    al. 2023. Tiene el entrenamiento y la evaluación. Es una versión anterior
    al paper y sus configs solo cubren denoising.

  Faltantes: no están los scripts que lanzan cada figura, el grafo de entidades
  ficticias, el código de LLaMA 1B ni el de Chain-of-Thought.

  Lo que se pudo constatar en el código

  - GPT-2 es el chico, de 124M parámetros.
  - Batch 24 sale de 8 por GPU por 3 pasos de acumulación de gradiente.
  - Expertise en selection: cada experto elige clusters al azar. Un programa
    lineal fija la expertise de cada cluster, y en la práctica queda casi
    siempre en 0 o 1. Los clusters no elegidos los sabe siempre mal.
  - Corrupción: es independiente por experto, como sospechaba. La motivación del
    paper habla de errores compartidos, pero lo implementado es que la mayoría
    se equivoca, cada uno a su manera.
  - Generalization: cada experto es exactamente un cluster, sin errores. No se
    puede saber cuántos expertos usaron.
  - Evaluación: greedy con hasta 20 tokens, cortando en el primer punto, con
    match exacto. En cada evaluación también se reporta la accuracy a
    temperatura 1.
  - Ablaciones no reportadas: hay configs con los nombres reales de Wikidata y
    con otros templates. El paper no las menciona.

  Cambios en los archivos

  - La v0: agregué una sección "Constatación en el código" y corregí las partes
    que decían que no había código o que el paper no especificaba algo.
  - El resumen de la primera pasada: actualicé el ítem del código.
  - PDFs y memoria: recompilé los dos PDFs y corregí la memoria del proyecto.

✻ Crunched for 3m 8s · done 1:43 am

※ recap: Estamos digiriendo el paper de Abreu 2025 para tu review de literatura. Encontré su código en el GitHub de la primera autora y ya actualicé la digestión v0 con lo que constaté ahí. Lo que sigue es que revises la v0 y escribas tu versión final con tus palabras. (disable recaps in /config)
# unr-tesina-new

## Contexto general

El objetivo del proyecto es escribir una tesina de grado para Mariano Crosetti recibirse de Licenciado en Ciencias de la Computación de UNR.

### Personajes relevantes
El usuario y autor es Mariano Crosetti.

El director es Dante Zanarini (referido como Dante). Dante es director de LCC, coordina proyectos y es profesor. No es investigador ; ni sabe de machine learning. La idea es que me ayude con la redacción / formato / parte introductoria del marco teórico ("que cualquier lcc lo pueda entender") / presentaciones.

El co-director es Pablo Granitto (referido como Pablo). Es investigador de machine learning y deep learning. La idea es que me ayude con el contenido, diseño e implementación de experimentos, metodología, formulación téorica de ML / DL.

También Pablo Racca (referido como Racca) es un profesor que dirige un taller de escritura de tesina que me está ayudando con la redacción (Dante está un poco ocupado con mil proyectos).

### Objetivo principal + Principio de pragmatismo
Mi objetivo personal es entregar la tesina lo antes posible y recibirme por lo que el pragmatismo es clave. Ejemplo: luego de presentar la propuesta v1, Pablo me dijo que el título deberíamos cambiarlo, me sugierió uno o que piense otro parecido pero directamente adopté el título que sugiere Pablo. Este criterio debe imperar para todo el desarrollo.

### Principio Risk-first
El principio que dirige mi operarar es avanzar siempre sobre lo más riesgoso primero.
Por ejemplo escribí la primera versión de la propuesta. Pablo validó que los experimentos fueran suficientemente originales para una tesina. Y aunque me dijo que en cuanto al formato / redacción está lejos de ser una propuesta, hemos decidido avanzar con los experimentos, ya que el formato lo podemos ver luego, la idea fue validada y entonces lo más riesgoso es el diseño / factibilidad de implementación de los experimentos.
Cuando arranque con los experimentos, arranqué con el experimento 1. Lo más riesgoso sería que haya algo en los detalles (diseño planteado, modelo elegido, modo de entrenar, evaluar, etc) que haya que corregir y cuando los corrija los nuevos resultados cambien totalmente el rumbo del trabajo. Una vez mitigado ese riesgo avanzaré con los otros experimentos, pero ante me aseguro que "ya tengo algo"/"estoy por buen camino"
Menciono esto porque si ves un riesgo que se mesté pasando testear: mencionarlo

## Propuesta

La propuesta es hacer experimentos que amplien y complementen el fenómeno denominado como "trascendencia" estudiado en los siguiente trabajos:
  - /Users/marianocrosetti/Desktop/personal-hq/projects/unr-tesina-new/referencias/abreu2025_taxonomy_of_transcendence.pdf
  - /Users/marianocrosetti/Desktop/personal-hq/projects/unr-tesina-new/referencias/zhang2024_transcendence.pdf

## Estructura de directorio

- `./` (raiz): infra va acá ya que tiene que estar en la raiz del directorio de trabajo (uv, pyproject.toml, CLAUDE.md)

- `generated/`: es el greenfield para todo lo *nuevo* (greenfield) que produce el agente.
Si se le requiere por ejemplo hacer un experimento del cual no hay nada hecho en el directorio principal, el agente trabajará en en este subdirectorio. 
Luego el usuario revisará, refactorizará y extraerá el resultado.
Si por el contrario se está trabajando ampliando algo que ya existe en el directorio principal, no se utilizará el subdirectorio `generated/` incluso si se crean nuevos archivos.

- `referencias/`: las referencias bibliográficas

- `propuesta/`: la propuesta de tesina presentada el comité de tesina que aprueba si el trabajo tiene sentido de hacerse

## Reglas generales de los archivos
- Algunos directorios tienen un `CURRENT_STATUS.md` con el estado actual de dicha sección por ejemplo `propuesta/CURRENT_STATUS.md`
- Las cosas que fueron marcadas como pendientes a ser cerradas antes de la versión final incluyen la string "TODO"
- Hemos incluid en el directorio raiz pedazos de contenido generado no revisado en profundidad / curado usando los tags: <AI-CONTENT-NOT-CURATED>. El mismo puede no ser correcto o no ser válido para el trabajo que actualmente estamos haciendo.

Lo primero que hice (antes incluso del mail inicial, ni la propuesta v1) fue pensar que experimentos podía ser interesantes diseñar, e implementarlos y ejecutarlos totalmente IA-generated y sin revisarlos para confirmar si los resultados arrojaban algo que tuviera sentido.
- Los hallazgos y conclusiones se condensan en: `./trascendencia_slides.html`
- Todo el código, run, logs, resultados e incluso el papper que se desprendería de estos experimentos se encuenta en `./generated`. No fue revisado para analizar la correctitud. La idea es luego ir extrayendo los experimentos de a uno, comenzando con `experimento1`. 

```
c4/                 paquete Python del experimento (game, solver, experts, generate, model, train, evaluate, plots, report) — ver generated/README.md para el rol de cada módulo
c4_transcendence.egg-info/   artefacto de build (editable install), regenerable con uv sync
configs/            colas/listas usadas por los scripts overnight
data/               datasets generados (.npz + .meta.json) — gitignored, pesado
overnight/          logs y checkpoints de las corridas overnight — trackeado en git (son resultados citados en la tesina, no basura de log)
paper/              El "papper"
results/            resultados de evaluación por corrida (states.json, figuras) — trackeado
runs/               checkpoints/logs de entrenamiento — gitignored, pesado
scripts/            shell scripts de setup y orquestación de corridas
third_party/        solver de Connect-4 de Pons (AGPL), vendored — gitignored
README.md, NARRATIVE.md, RESULTS.md, RESUMEN.md documentación
```
- El "paper" es una referencia sintética de lo hecho, no es la idea publicar eso ; probablemente en el desarrollo y pulido de la tesina vayamos a hacer cambios / pivotear, etc
- Todos los .md de la carpeta son documentación y borradores del avance de esta fase del exploracion que el agente fue escribiendo a mendida que avanzaba con el diseño / implementación / escritura de resultados de esta fase. Es útil explorarlos para tener idea precisa de lo que se hizo.
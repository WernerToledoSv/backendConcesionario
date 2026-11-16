---
name: uso-eficiente-de-tokens
description: Reduce el contexto y las lecturas innecesarias al trabajar en este repositorio, sin sacrificar exactitud, seguridad ni validación.
---

# Uso eficiente de tokens

## Exploración

- Empieza por los archivos nombrados en la solicitud y localiza dependencias con búsquedas acotadas por símbolo o carpeta.
- Lee rangos pequeños y archivos directamente relacionados; amplía la lectura solo cuando aparezca una dependencia concreta.
- Para cambios existentes, prioriza `git status` y el diff antes de volver a leer archivos sin cambios.
- Agrupa lecturas independientes en una sola ronda y evita repetir búsquedas que ya dieron el dato necesario.

## Implementación y validación

- Haz el cambio más pequeño que resuelva la solicitud; no replantees arquitectura ni arregles problemas ajenos.
- Ejecuta la prueba o comprobación más pequeña que cubra el comportamiento modificado. Amplía la suite si afecta varias capas o si falla.
- Conserva las validaciones requeridas: no ahorres contexto omitiendo comprobaciones importantes, manejo de errores o revisión de cambios.
- En la respuesta, resume resultado, archivos relevantes, validación y limitaciones en pocas líneas.

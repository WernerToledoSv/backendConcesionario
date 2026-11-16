---
name: documentar-cambios
description: Documenta cambios implementados en AutoMarket a partir del diff, el código y las pruebas verificables. Úsala para actualizar la documentación del backend o redactar notas de cambios.
---

# Documentar cambios

## Proceso

1. Revisa el diff y los archivos relacionados con el cambio; consulta la documentación existente antes de editarla.
2. Describe el comportamiento que confirma el código, incluidos los endpoints, estados, validaciones y requisitos de base de datos que hayan cambiado.
3. Actualiza la documentación existente más pertinente. No crees un changelog ni otro documento nuevo si no lo solicitan.
4. Comprueba que ejemplos, nombres de rutas y códigos HTTP coincidan con el código actual.
5. Informa qué documentación cambió y qué pruebas se ejecutaron, sin afirmar resultados que no se hayan verificado.

## Convenciones

- Redacta en español y conserva el formato y vocabulario del proyecto.
- Distingue claramente entre comportamiento implementado y trabajo pendiente, como despliegues o cambios de esquema aún no aplicados.
- No inventes requisitos, endpoints, resultados de pruebas ni instrucciones de despliegue.
- No incluyas secretos, valores de `.env` ni datos personales.
- No modifiques código fuente cuando la tarea sea únicamente documentar.

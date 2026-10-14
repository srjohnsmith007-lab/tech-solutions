# Como contribuir a LuxuryCo

Gracias por aportar a LuxuryCo. Sigue estas reglas para mantener un trabajo ordenado en el equipo.

## Flujo de trabajo

1. Toma un Issue de la lista y asignatelo.
2. Crea una rama solo para esa tarea:

   ```bash
   git switch -c feat/issue-N-descripcion
   ```

3. Haz tus cambios y tus commits.
4. Sube la rama a GitHub:

   ```bash
   git push -u origin nombre-de-la-rama
   ```

5. Abre un Pull Request y agrega `Closes #N` en la descripcion.
6. Espera la revision y aprobacion de un companero.
7. Fusiona el Pull Request.

## Reglas de la rama main

- Nadie sube codigo directo a `main`. Todo cambio entra por Pull Request.
- `main` esta protegida: requiere al menos **1 aprobacion** antes de fusionar.

## Estilo de commits

- `feat:` nueva funcionalidad o contenido
- `fix:` correccion
- `docs:` documentacion
- `chore:` tareas menores

## Revision de codigo

Cada integrante debe revisar al menos un Pull Request de un companero y dejar un comentario.

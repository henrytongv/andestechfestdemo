# Fly.io GPU Machine

Información tomada de: https://fly.io/docs/python/do-more/add-ollama/

- Crea un usuario en Fly.io
- Instala la línea de comando de Fly.io

## Ejecución

```
fly launch -c myMachine.toml 

fly m run -e OLLAMA_HOST=http://mi-nombre-bonito-de-maquina.dev --shell --command "ollama pull phi3:mini" ollama/ollama

fly deploy -c myMachine.toml
```

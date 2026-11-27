// Guarda las respuestas de los cuestionarios de https://mflowsuite.github.io/guzel-ia/
// Publicar: `cf deploy` desde esta carpeta. La base D1 «guzel-datos» se crea sola la primera vez.
import { bindings, defineConfig } from "cf/config";
import * as entrypoint from "./src/index.js" with { type: "cf-worker" };

export default defineConfig({
  worker: {
    name: "guzel-datos",
    entrypoint,
    compatibilityDate: "2026-09-01",
    env: { DB: bindings.d1({ name: "guzel-datos" }) },
  },
});

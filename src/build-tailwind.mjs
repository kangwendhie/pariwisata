// Local build helper based on the official Tailwind v4 compiler API.
// In a normal development machine run `npm run build` using @tailwindcss/cli.
import {compile} from '/opt/nvm/versions/node/v22.16.0/lib/node_modules/tailwindcss/dist/lib.mjs';
import fs from 'node:fs';
import path from 'node:path';
const base='/opt/nvm/versions/node/v22.16.0/lib/node_modules/tailwindcss';
const root=path.resolve(import.meta.dirname,'..');
const source=fs.readFileSync(path.join(root,'src/input.css'),'utf8');
const html=fs.readFileSync(path.join(root,'index.html'),'utf8');
const candidates=new Set();
for(const match of html.matchAll(/\bclass\s*=\s*(["'])(.*?)\1/gs)){
 for(const cls of match[2].split(/\s+/)) if(cls) candidates.add(cls);
}
const compiler=await compile(source,{loadStylesheet:async (id,from)=>{
 const file=id==='tailwindcss'?path.join(base,'index.css'):path.resolve(from,id);
 return {content:fs.readFileSync(file,'utf8'),base:path.dirname(file)};
}});
const output=compiler.build(Array.from(candidates));
fs.writeFileSync(path.join(root,'style.css'),output);
console.log('Tailwind v4.1.10, scanned',candidates.size,'classes, generated',output.length,'bytes');

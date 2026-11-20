import http from 'node:http';
import fs from 'node:fs/promises';
const file=new URL('../outputs/Dual_Reality_Maze_Story_Edition.html',import.meta.url);
const server=http.createServer(async(req,res)=>{
 if(req.url==='/favicon.ico'){res.writeHead(204);res.end();return}
 if(!['/','/Dual_Reality_Maze_Story_Edition.html'].includes(req.url)){res.writeHead(404);res.end();return}
 try{const html=await fs.readFile(file);res.writeHead(200,{'Content-Type':'text/html; charset=utf-8','Cache-Control':'no-store'});res.end(html)}catch{res.writeHead(500);res.end('Build the story edition first.')}
});
server.listen(4317,'127.0.0.1',()=>console.log('Maze preview: http://127.0.0.1:4317'));

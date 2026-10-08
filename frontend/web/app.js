'use strict';
const $ = s => document.querySelector(s);
const state = {token: sessionStorage.getItem('visagio-token'), tab:'analyses', register:false, editing:null};
const labels = {id:'Código',name:'Nome',email:'E-mail',phone:'Telefone',birth_date:'Nascimento',notes:'Observações',avatar_url:'Foto de perfil (URL)',hair_type:'Tipo de cabelo',hair_length:'Comprimento',face_shape:'Formato declarado do rosto',hair_texture:'Textura',hair_density:'Densidade',current_length:'Comprimento atual',image_url:'Imagem (URL)',score:'Pontuação informada',observations:'Observações',procedure_type:'Procedimento',description:'Descrição',procedure_date:'Data do procedimento',next_maintenance_date:'Próxima manutenção',professional_id:'Profissional',appointment_date:'Data e hora',service_name:'Serviço',status:'Situação',analysis_id:'Análise',recommendation_id:'Recomendação',before_image_url:'Imagem anterior (URL)',after_image_url:'Imagem posterior (URL)',category:'Categoria',title:'Título',technical_reason:'Motivo da sugestão',compatibility:'Compatibilidade',created_at:'Criação',studio_name:'Estúdio',specialty:'Especialidade',rating:'Avaliação de demonstração',duration_minutes:'Duração em minutos',professional_name:'Profissional',role:'Tipo de conta',client_id:'Perfil',user_id:'Usuário'};
const words={straight:'Liso',wavy:'Ondulado',curly:'Cacheado',coily:'Crespo',short:'Curto',medium:'Médio',long:'Longo',oval:'Oval',round:'Redondo',square:'Quadrado',heart:'Coração',diamond:'Diamante',scheduled:'Marcado',completed:'Concluído',cancelled:'Cancelado',haircut:'Corte',beard:'Barba',coloring:'Coloração',care:'Cuidados',client:'Cliente'};
const options = {hair_type:['straight','wavy','curly','coily'],hair_length:['short','medium','long'],current_length:['short','medium','long'],face_shape:['oval','round','square','heart','long','diamond'],status:['scheduled','completed','cancelled']};
const specs={
 analyses:{name:'Minhas análises',single:'análise',help:'Registre suas características. Os dados são autodeclarados; nenhuma foto é analisada automaticamente.',fields:['face_shape','hair_type','hair_texture','hair_density','current_length','image_url','observations'],title:x=>`${words[x.face_shape]} · ${words[x.hair_type]}`,summary:x=>x.observations||'Características do visual registradas.'},
 recommendations:{name:'Sugestões de estilo',help:'Sugestões de um catálogo local baseadas nas características registradas. Não são resultados de IA.',title:x=>x.title,summary:x=>x.description},
 simulations:{name:'Comparações de visual',single:'comparação',help:'Guarde imagens de antes e depois por URL e vincule uma sugestão. O sistema não gera nem modifica imagens.',fields:['analysis_id','recommendation_id','before_image_url','after_image_url'],title:x=>`Comparação #${x.id}`,summary:x=>`Referência da análise #${x.analysis_id}`},
 appointments:{name:'Minha agenda',single:'agendamento',help:'Escolha um profissional de demonstração e um horário. As reservas ficam salvas apenas neste projeto.',fields:['professional_id','appointment_date','service_name','status','notes'],title:x=>x.service_name,summary:x=>`${x.professional_name} · ${format('appointment_date',x.appointment_date)} · ${words[x.status]}`},
 history:{name:'Histórico de cuidados',single:'procedimento',help:'Acompanhe os cuidados já realizados e planeje a próxima manutenção.',fields:['procedure_type','procedure_date','next_maintenance_date','description','image_url'],title:x=>x.procedure_type,summary:x=>`${format('procedure_date',x.procedure_date)} · ${x.description||'Sem observações'}`},
 professionals:{name:'Profissionais',help:'Catálogo de profissionais fictícios para a demonstração acadêmica.',title:x=>x.name,summary:x=>`${x.studio_name} · ${x.specialty} · ${x.duration_minutes} min`},
 profile:{name:'Meu perfil',help:'Mantenha seus dados pessoais atualizados.',fields:['name','phone','birth_date','notes','avatar_url']},
 preferences:{name:'Preferências',help:'Salve o tipo e o comprimento do seu cabelo para consultar depois.',fields:['hair_type','hair_length']}
};
function node(tag, text, cls){const n=document.createElement(tag); if(text!==undefined)n.textContent=text;if(cls)n.className=cls;return n;}
function button(text,handler,cls='secondary'){const b=node('button',text,cls);b.type='button';b.onclick=()=>safe(handler);return b;}
let toastTimer;
function toast(text,error=false){$('#toast').textContent=text;$('#toast').className=error?'error':'';$('#toast').hidden=false;clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('#toast').hidden=true,6500);}
async function safe(fn){try{await fn();}catch(e){toast(e.message,true);}}
async function api(path,method='GET',body){
 const response=await fetch('/api/'+path,{method,headers:{'Content-Type':'application/json',...(state.token?{Authorization:'Bearer '+state.token}:{})},...(body===undefined?{}:{body:JSON.stringify(body)})});
 if(response.status===204)return null;
 const data=await response.json();
 if(!response.ok){if(response.status===401 && !path.startsWith('auth/'))logout();throw Error(data.message||'Não foi possível concluir.');}return data;
}
function endpoint(tab){return tab==='professionals'?'appointments/professionals':tab;}
function format(key,value){
 if(value===null||value===undefined||value==='')return '—';
 if(key==='appointment_date'||key==='created_at')return new Date(value+(value.endsWith('Z')?'':'Z')).toLocaleString('pt-BR');
 if(key.includes('date'))return value.split('-').reverse().join('/');
 return words[value]||String(value);
}
function detailList(data){const dl=node('dl',undefined,'detail-grid');for(const [k,v] of Object.entries(data)){dl.append(node('dt',labels[k]||k),node('dd',format(k,v)));}return dl;}
function logout(){sessionStorage.removeItem('visagio-token');state.token=null;$('#app').hidden=true;$('#auth').hidden=false;document.querySelectorAll('dialog[open]').forEach(d=>d.close());}
async function enter(){const user=await api('profile');$('#user-name').textContent=user.name;$('#auth').hidden=true;$('#app').hidden=false;await render();}
$('#toggle-auth').onclick=()=>{state.register=!state.register;$('#name-label').hidden=!state.register;$('#name-label input').required=state.register;$('#auth-title').textContent=state.register?'Crie seu espaço':'Entre no seu espaço';$('#auth-help').textContent=state.register?'Preencha seus dados para começar.':'Use seu e-mail e sua senha para continuar.';$('#auth-form button').textContent=state.register?'Criar conta':'Entrar';$('#toggle-auth').textContent=state.register?'Já tenho conta':'Ainda não tenho conta';};
$('#auth-form').onsubmit=async event=>{event.preventDefault();const b=event.submitter;b.disabled=true;try{const data=Object.fromEntries(new FormData(event.target));const result=await api('auth/'+(state.register?'register':'login'),'POST',data);state.token=result.token;sessionStorage.setItem('visagio-token',state.token);await enter();event.target.reset();toast('Acesso realizado.');}catch(e){toast(e.message,true);}finally{b.disabled=false;}};
$('#logout').onclick=logout;
for(const [key,spec] of Object.entries(specs)){$('#nav').append(button(spec.name,async()=>{state.tab=key;await render();},''));}
for(const b of document.querySelectorAll('[data-close]'))b.onclick=()=>$('#'+b.dataset.close).close();
async function render(){
 const tab=state.tab,spec=specs[tab];$('#title').textContent=spec.name;$('#subtitle').textContent=spec.help;[...$('#nav').children].forEach((b,i)=>b.classList.toggle('active',Object.keys(specs)[i]===tab));
 const content=$('#content');content.replaceChildren(node('p','Carregando registros…','small'));
 try{
 let path=endpoint(tab);if(tab==='recommendations'){const q=new URLSearchParams();if(state.category)q.set('category',state.category);if(state.analysisFilter)q.set('analysis_id',state.analysisFilter);path+='?'+q;}
 const data=await api(path);if(tab!==state.tab)return;
 content.replaceChildren();
 if(tab==='profile'||tab==='preferences'){
 const panel=node('div',undefined,'profile-panel');panel.append(detailList(data),button(tab==='profile'?'Editar perfil':'Salvar preferências',()=>openEditor(tab,data), 'primary'));content.append(panel);return;
 }
 const toolbar=node('div',undefined,'toolbar');toolbar.append(node('span',`${data.length} registro(s)`,'small'));const actions=node('div');
 if(spec.fields)actions.append(button('Adicionar '+spec.single,()=>openEditor(tab), 'primary'));
 actions.append(button('Atualizar lista',render));toolbar.append(actions);content.append(toolbar);
 if(tab==='recommendations'){
 const filter=node('select');filter.setAttribute('aria-label','Filtrar por categoria');filter.append(new Option('Todas as categorias',''));for(const v of ['haircut','beard','coloring','care'])filter.append(new Option(words[v],v));filter.value=state.category||'';filter.onchange=()=>safe(async()=>{state.category=filter.value;await render();});
 const analyses=await api('analyses');if(tab!==state.tab)return;const a=node('select');a.setAttribute('aria-label','Filtrar por análise');a.append(new Option('Todas as análises',''));for(const item of analyses)a.append(new Option('Análise #'+item.id,item.id));a.value=state.analysisFilter||'';a.onchange=()=>safe(async()=>{state.analysisFilter=a.value;await render();});toolbar.append(filter,a);
 }
 if(!data.length){content.append(node('div',tab==='recommendations'?'Nenhuma sugestão encontrada. Gere sugestões em Minhas análises.':'Nenhum registro ainda. Comece adicionando o primeiro.','empty'));return;}
 const cards=node('div',undefined,'cards');
 for(const item of data){const card=node('article',undefined,'card');card.dataset.id=item.id;card.append(node('span',`REGISTRO ${String(item.id).padStart(3,'0')}`,'eyebrow'),node('h2',spec.title(item)),node('p',spec.summary(item)));const buttons=node('div',undefined,'actions');
 if(tab!=='professionals')buttons.append(button('Detalhes',()=>showDetails(tab,item.id)));
 if(spec.fields){buttons.append(button('Editar',async()=>openEditor(tab,await api(`${tab}/${item.id}`))));buttons.append(button('Excluir',async()=>{if(confirm('Excluir este registro? Análises também excluem suas sugestões e comparações.')){await api(`${tab}/${item.id}`,'DELETE');toast('Registro excluído.');await render();}},'danger'));}
 if(tab==='analyses')buttons.append(button('Gerar sugestões',async()=>{await api(`recommendations/analysis/${item.id}/generate`,'POST',{});state.analysisFilter=String(item.id);state.tab='recommendations';await render();toast('Sugestões do catálogo salvas.');},'primary'));
 if(tab==='professionals')buttons.append(button('Agendar',()=>openEditor('appointments',{professional_id:item.id}), 'primary'));
 card.append(buttons);cards.append(card);
 }content.append(cards);
 }catch(e){content.replaceChildren(node('p',e.message),button('Tentar novamente',render));throw e;}
}
async function showDetails(tab,id){const data=await api(`${tab}/${id}`);const body=$('#detail-body');body.replaceChildren(detailList(data));if(tab==='simulations'){const grid=node('div',undefined,'compare');for(const [field,title] of [['before_image_url','Antes'],['after_image_url','Depois']]){const figure=node('figure');figure.append(node('figcaption',title));if(data[field]){const img=node('img');img.src=data[field];img.alt=title;img.referrerPolicy='no-referrer';figure.append(img);}else figure.append(node('p','Imagem não informada.'));grid.append(figure);}body.append(grid);}$('#details').showModal();}
async function openEditor(tab,data={}){
 state.editing={tab,id:data.id};$('#fields').replaceChildren();$('#form-error').textContent='';$('#editor-title').textContent=tab==='profile'?'Editar perfil':tab==='preferences'?'Preferências':`${data.id?'Editar':'Adicionar'} ${specs[tab].single}`;
 let analyses=[],recommendations=[],professionals=[];
 if(tab==='simulations'){[analyses,recommendations]=await Promise.all([api('analyses'),api('recommendations')]);}
 if(tab==='appointments')professionals=await api('appointments/professionals');
 for(const key of specs[tab].fields){
 if(key==='status'&&!data.id)continue;
 const label=node('label',labels[key]);let input;
 if(options[key]||['analysis_id','recommendation_id','professional_id'].includes(key)){
 input=node('select');
 if(key==='recommendation_id')input.append(new Option('Sem recomendação',''));
 const opts=options[key]?.map(v=>[v,words[v]])||(key==='analysis_id'?analyses.map(x=>[x.id,`Análise #${x.id} · ${words[x.face_shape]}`]):key==='recommendation_id'?recommendations.map(x=>[x.id,`#${x.analysis_id} · ${x.title}`]):professionals.map(x=>[x.id,`${x.name} · ${x.specialty}`]));
 for(const [value,title] of opts)input.append(new Option(title,value));
 }else if(['notes','description','observations'].includes(key))input=node('textarea');
 else{input=node('input');input.type=key==='appointment_date'?'datetime-local':key.includes('date')?'date':key.includes('url')?'url':'text';input.maxLength=key.includes('url')?500:key==='phone'?25:key==='name'?120:key==='procedure_type'?100:key==='service_name'?150:50;}
 input.name=key;
 if(['name','face_shape','hair_type','hair_length','current_length','procedure_type','procedure_date','professional_id','appointment_date','service_name','analysis_id'].includes(key))input.required=true;
 if(data[key]!==undefined&&data[key]!==null){let value=data[key];if(key==='appointment_date'){const date=new Date(value+'Z');value=new Date(date.getTime()-date.getTimezoneOffset()*60000).toISOString().slice(0,16);}input.value=value;}
 label.append(input);$('#fields').append(label);
 }
 if(tab==='simulations'){
 const a=$('#fields [name=analysis_id]'),r=$('#fields [name=recommendation_id]');const filter=()=>{const prev=r.value;r.replaceChildren(new Option('Sem recomendação',''));for(const rec of recommendations.filter(x=>String(x.analysis_id)===a.value))r.append(new Option(rec.title,rec.id));r.value=[...r.options].some(x=>x.value===prev)?prev:'';};a.onchange=filter;filter();
 }
 $('#editor').showModal();
}
$('#edit-form').onsubmit=async event=>{
 event.preventDefault();const submit=event.submitter;submit.disabled=true;$('#form-error').textContent='';
 try{const {tab,id}=state.editing;const data=Object.fromEntries(new FormData(event.target));if(data.appointment_date)data.appointment_date=new Date(data.appointment_date).toISOString();for(const k of ['analysis_id','recommendation_id','professional_id'])if(k in data)data[k]=data[k]?Number(data[k]):null;
 const singleton=tab==='profile'||tab==='preferences';await api(tab+(!singleton&&id?'/'+id:''),singleton||id?'PUT':'POST',data);$('#editor').close();state.tab=tab;await render();if(tab==='profile')$('#user-name').textContent=data.name;toast('Dados salvos com sucesso.');
 }catch(e){$('#form-error').textContent=e.message;}finally{submit.disabled=false;}
};
if(state.token)safe(enter);

(()=>{
  const key='glaze-ui-site-theme';
  const root=document.documentElement;
  const buttons=[...document.querySelectorAll('[data-theme-choice]')];
  const navLinks=[...document.querySelectorAll('.nav-wrap nav a[href^="#"]')];
  const sections=navLinks.map(link=>document.querySelector(link.getAttribute('href'))).filter(Boolean);
  const apply=choice=>{
    if(choice==='system'){
      root.removeAttribute('data-theme');
      root.removeAttribute('data-glaze-appearance');
    }else{
      root.dataset.theme=choice;
      root.dataset.glazeAppearance=choice;
    }
    buttons.forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.themeChoice===choice)));
  };
  const setCurrent=id=>{
    navLinks.forEach(link=>{
      const current=link.getAttribute('href')===`#${id}`;
      if(current)link.setAttribute('aria-current','true');
      else link.removeAttribute('aria-current');
    });
  };
  let saved='system';
  try{saved=localStorage.getItem(key)||'system';}catch(_){}
  if(!['system','light','dark'].includes(saved))saved='system';
  apply(saved);
  buttons.forEach(button=>button.addEventListener('click',()=>{
    const choice=button.dataset.themeChoice;
    apply(choice);
    try{localStorage.setItem(key,choice);}catch(_){}
  }));
  if(sections.length&&'IntersectionObserver'in window){
    const observer=new IntersectionObserver(entries=>{
      const visible=entries.filter(entry=>entry.isIntersecting).sort((a,b)=>b.intersectionRatio-a.intersectionRatio);
      if(visible[0])setCurrent(visible[0].target.id);
    },{rootMargin:'-22% 0px -62% 0px',threshold:[0,.1,.25,.5]});
    sections.forEach(section=>observer.observe(section));
  }
  navLinks.forEach(link=>link.addEventListener('click',()=>setCurrent(link.getAttribute('href').slice(1))));

  const governance=document.querySelector('.consumer-governance');
  if(governance){
    const search=governance.querySelector('[data-governance-search]');
    const statusButtons=[...governance.querySelectorAll('[data-governance-status]')];
    const cards=[...governance.querySelectorAll('.consumer-card[data-consumer-name][data-consumer-repository][data-consumer-status]')];
    const result=governance.querySelector('[data-governance-result]');
    let status='all';
    const normalize=value=>String(value||'').trim().toLocaleLowerCase();
    const applyGovernanceFilters=()=>{
      const query=normalize(search?.value);
      let visible=0;
      cards.forEach(card=>{
        const matchesStatus=status==='all'||card.dataset.consumerStatus===status;
        const searchText=normalize(`${card.dataset.consumerName} ${card.dataset.consumerRepository}`);
        const matchesQuery=!query||searchText.includes(query);
        const show=matchesStatus&&matchesQuery;
        card.hidden=!show;
        if(show)visible+=1;
      });
      statusButtons.forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.governanceStatus===status)));
      if(result)result.textContent=`${visible} of ${cards.length} consumers shown.`;
    };
    if(search)search.addEventListener('input',applyGovernanceFilters);
    statusButtons.forEach(button=>button.addEventListener('click',()=>{
      status=button.dataset.governanceStatus||'all';
      applyGovernanceFilters();
    }));
    applyGovernanceFilters();
  }
})();
